#!/usr/bin/env python3
"""Generate BAND-importable CSV files from the six published KCMT calendars."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parent.parent
LOCAL_ZONE = ZoneInfo("America/Los_Angeles")
CALENDARS = (
    "group",
    "rehearsal",
    "harmony-singers",
    "dancers",
    "sets",
    "marketing",
)
CSV_HEADERS = (
    "Subject",
    "Start Date",
    "Start Time",
    "End Date",
    "End Time",
    "All Day Event",
    "Description",
    "Location",
    "Private",
)


@dataclass(frozen=True)
class CalendarValue:
    value: date | datetime
    all_day: bool


def unfold_ical(text: str) -> list[str]:
    """Return logical iCalendar lines with RFC 5545 continuations joined."""
    physical_lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    logical_lines: list[str] = []
    for line in physical_lines:
        if line.startswith((" ", "\t")) and logical_lines:
            logical_lines[-1] += line[1:]
        else:
            logical_lines.append(line)
    return logical_lines


def unescape_text(value: str) -> str:
    """Decode the iCalendar TEXT escapes used by the source feeds."""
    return re.sub(
        r"\\([nN,;\\])",
        lambda match: {
            "n": "\n",
            "N": "\n",
            ",": ",",
            ";": ";",
            "\\": "\\",
        }[match.group(1)],
        value,
    )


def read_events(path: Path) -> list[dict[str, tuple[dict[str, str], str]]]:
    events: list[dict[str, tuple[dict[str, str], str]]] = []
    event: dict[str, tuple[dict[str, str], str]] | None = None

    for line in unfold_ical(path.read_text(encoding="utf-8")):
        if line == "BEGIN:VEVENT":
            event = {}
            continue
        if line == "END:VEVENT":
            if event is not None:
                events.append(event)
            event = None
            continue
        if event is None or ":" not in line:
            continue

        raw_name, value = line.split(":", 1)
        parts = raw_name.split(";")
        name = parts[0].upper()
        parameters: dict[str, str] = {}
        for parameter in parts[1:]:
            if "=" in parameter:
                key, parameter_value = parameter.split("=", 1)
                parameters[key.upper()] = parameter_value
        event[name] = (parameters, value)

    return events


def parse_calendar_value(
    property_value: tuple[dict[str, str], str],
) -> CalendarValue:
    parameters, raw_value = property_value
    if parameters.get("VALUE") == "DATE" or re.fullmatch(r"\d{8}", raw_value):
        return CalendarValue(datetime.strptime(raw_value, "%Y%m%d").date(), True)

    if raw_value.endswith("Z"):
        parsed = datetime.strptime(raw_value, "%Y%m%dT%H%M%SZ").replace(
            tzinfo=timezone.utc
        )
    else:
        zone = ZoneInfo(parameters.get("TZID", "America/Los_Angeles"))
        parsed = datetime.strptime(raw_value, "%Y%m%dT%H%M%S").replace(tzinfo=zone)
    return CalendarValue(parsed.astimezone(LOCAL_ZONE), False)


def format_date(value: date | datetime) -> str:
    return value.strftime("%m/%d/%Y")


def format_time(value: datetime) -> str:
    hour = value.hour % 12 or 12
    return f"{hour}:{value.minute:02d} {'AM' if value.hour < 12 else 'PM'}"


def event_to_row(
    event: dict[str, tuple[dict[str, str], str]],
) -> dict[str, str]:
    start = parse_calendar_value(event["DTSTART"])
    end = parse_calendar_value(event["DTEND"]) if "DTEND" in event else None
    subject = unescape_text(event["SUMMARY"][1])
    location = unescape_text(event.get("LOCATION", ({}, ""))[1]).strip()
    source_description = unescape_text(event.get("DESCRIPTION", ({}, ""))[1]).strip()

    description_parts = [part for part in (source_description,) if part]
    if location:
        description_parts.append(f"Location: {location}")

    if start.all_day:
        start_date = start.value
        if end is not None:
            # iCalendar's all-day DTEND is exclusive; CSV end dates are inclusive.
            end_date = end.value - timedelta(days=1)
        else:
            end_date = start_date
        start_time = ""
        end_time = ""
    else:
        assert isinstance(start.value, datetime)
        start_date = start.value
        start_time = format_time(start.value)
        if end is not None:
            assert isinstance(end.value, datetime)
            end_date = end.value
            end_time = format_time(end.value)
        else:
            end_date = ""
            end_time = ""

    return {
        "Subject": subject,
        "Start Date": format_date(start_date),
        "Start Time": start_time,
        "End Date": format_date(end_date) if end_date else "",
        "End Time": end_time,
        "All Day Event": "True" if start.all_day else "False",
        "Description": "\n\n".join(description_parts),
        "Location": location,
        "Private": "False",
    }


def row_sort_key(row: dict[str, str]) -> tuple[datetime, str]:
    start_date = datetime.strptime(row["Start Date"], "%m/%d/%Y")
    if row["Start Time"]:
        start_time = datetime.strptime(row["Start Time"], "%I:%M %p").time()
        start_date = datetime.combine(start_date.date(), start_time)
    return start_date, row["Subject"]


def convert_calendar(name: str) -> int:
    source = ROOT / f"{name}.ics"
    destination = ROOT / f"{name}.csv"
    rows = sorted((event_to_row(event) for event in read_events(source)), key=row_sort_key)

    with destination.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"{source.name}: {len(rows)} events -> {destination.name}")
    return len(rows)


def main() -> None:
    total = sum(convert_calendar(name) for name in CALENDARS)
    print(f"Generated {len(CALENDARS)} CSV files with {total} total events")


if __name__ == "__main__":
    main()
