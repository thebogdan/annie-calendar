# KCMT BAND Calendar Maintenance

This repository publishes iCalendar (`.ics`) feeds for KCMT calendars. BAND subscribes to these feeds through **Subscribe by URL**, so calendar updates are made by editing the appropriate `.ics` file and publishing it to GitHub Pages.

## Source of truth

Only the six subscribed feed files are active sources of truth:

| Calendar | File | Public URL |
| --- | --- | --- |
| Group Calendar | `group.ics` | `https://thebogdan.github.io/annie-calendar/group.ics` |
| Rehearsal Calendar | `rehearsal.ics` | `https://thebogdan.github.io/annie-calendar/rehearsal.ics` |
| Harmony Singers | `harmony-singers.ics` | `https://thebogdan.github.io/annie-calendar/harmony-singers.ics` |
| Dancer Schedule | `dancers.ics` | `https://thebogdan.github.io/annie-calendar/dancers.ics` |
| Sets | `sets.ics` | `https://thebogdan.github.io/annie-calendar/sets.ics` |
| Marketing Calendar | `marketing.ics` | `https://thebogdan.github.io/annie-calendar/marketing.ics` |

Do not update `calendar.ics` or `annie-september-2026.ics` as part of normal maintenance. They are older aggregate/local artifacts and are not the feeds currently subscribed in BAND.

## Event classification

- **Group Calendar:** Parent meetings, volunteer meetings, and general KCMT events that do not belong to another calendar.
- **Rehearsal Calendar:** Scene rehearsals, cast rehearsals, callbacks, character choreography, and vocal rehearsals.
- **Harmony Singers:** Harmony Singers events only.
- **Dancer Schedule:** Dancer rehearsals and dancer-specific calls.
- **Sets:** Set construction, painting, load-in, strike, and other set-related work.
- **Marketing Calendar:** Publicity, promotions, photography, social media, and other marketing deadlines or events.

If an event clearly belongs to a specialist calendar, do not also add it to Group Calendar unless the source schedule explicitly requires both.

## Naming conventions

Use readable titles while preserving production-specific cast labels:

- `Sn 4a` becomes `Scene 4a Rehearsal`.
- `AB` becomes `Cast AB`.
- `CD` becomes `Cast CD`.
- `ABCD` becomes `Cast ABCD`.
- `A` in a character list means `Annie`.
- `WB` means `Warbucks`, not `Daddy Warbucks`.
- `G` means `Grace`; do not include her last name, `Farrell`, in event titles.
- `H, R, L` means `Hannigan, Rooster, and Lily`; do not put `Miss` before `Hannigan`.
- `Dancers` may be titled `Dance Rehearsal`.
- A generic source entry named `Meeting` remains `Meeting` unless more context is provided.

Examples:

- `AB A & WB Choreo` becomes `Cast AB - Annie and Warbucks Choreography`.
- `CD A, WB, G Choreo` becomes `Cast CD - Annie, Warbucks, and Grace Choreography`.
- `ABCD H, R, L Choreo & Vocals` becomes `Cast ABCD - Hannigan, Rooster, and Lily Choreography & Vocals`.

Avoid titles such as `All Casts` when the source says `ABCD`; “all casts” can sound like every company member is called.

## Locations

Use this default location unless the source schedule names another venue:

```text
The Creative Consortium
1015 NE Hostmark St #101
Poulsbo, WA 98370
```

The **KCMT Room** is a specific room inside The Creative Consortium, not a separate venue. When the source says a rehearsal takes place in the KCMT Room only, use:

```text
KCMT Room, The Creative Consortium
1015 NE Hostmark St #101
Poulsbo, WA 98370
```

Pearson Elementary School is:

```text
Pearson Elementary School
15650 Central Valley Rd NW
Poulsbo, WA 98370
```

Prefix event titles held at Pearson with `Pearson -` so the venue is immediately visible in BAND. For example: `Pearson - Scene 10b Rehearsal`.

Escape commas in iCalendar text fields:

```text
LOCATION:The Creative Consortium\, 1015 NE Hostmark St #101\, Poulsbo\,
  WA 98370
```

The second physical line begins with two spaces: the first is the iCalendar fold marker and is removed during unfolding; the second is the actual space required between the comma and `WA`.

## Date and time rules

- The operating time zone is `America/Los_Angeles`.
- Current feeds store event times in UTC with a trailing `Z`.
- During Pacific Daylight Time, add seven hours to convert local time to UTC.
- During Pacific Standard Time, add eight hours.
- UTC conversion can move an evening event's end time to the following UTC date. For example, September 19 from 3:00–6:00 PM PDT is:

```text
DTSTART:20260919T220000Z
DTEND:20260920T010000Z
```

This is valid and still displays as September 19 from 3:00–6:00 PM in Pacific time.

- When a source gives a start time but no end time, use a one-hour duration only when the user has approved that default.
- Preserve simultaneous or overlapping events as separate `VEVENT` blocks.
- Do not invent recurrences. A pattern such as Friday dancer rehearsals should be added only for the dates covered by the supplied schedule unless the user explicitly requests a recurring event.
- When a pasted calendar table has shifted weekday columns, prefer the printed date number, but flag the discrepancy before publishing if it changes the interpretation.

## iCalendar requirements

Each feed must be a valid VCALENDAR document:

```text
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//KCMT//Calendar Name//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:Calendar Name
X-WR-TIMEZONE:America/Los_Angeles
...
END:VCALENDAR
```

Each event must include at least:

```text
BEGIN:VEVENT
UID:a-stable-unique-id@band-us.local
DTSTAMP:20260919T190000Z
DTSTART:20260919T220000Z
DTEND:20260920T010000Z
SUMMARY:Cast AB Rehearsal
LOCATION:The Creative Consortium\, 1015 NE Hostmark St #101\, Poulsbo\,
  WA 98370
END:VEVENT
```

Formatting rules:

- Use a globally unique, stable `UID` for each event.
- Keep the same `UID` when correcting an existing event so subscribers can update it rather than create a duplicate.
- Never reuse one event's UID for a different event.
- Escape commas as `\,`, semicolons as `\;`, backslashes as `\\`, and embedded newlines as `\n` in text values.
- Fold content lines longer than 75 octets. A continuation line must begin with a space or tab, and that first whitespace character is removed when a reader unfolds the value.
- When a fold occurs between words, preserve the logical separator. Either leave the real space at the end of the preceding physical line or begin the continuation with two spaces: one fold marker plus one content space. Using only one leading space joins the words (for example, `FarrellChoreography` or `&Vocals`).
- Prefer CRLF line endings for standards-compliant `.ics` files. Be aware that some files in this repository may contain mixed historical line endings; avoid committing line-ending-only rewrites unless intentional.
- Empty feeds are valid and should retain their VCALENDAR wrapper so their subscription URLs remain stable.

## Editing workflow

1. Read the new schedule and list every event with its date, local start/end time, title, calendar, and location.
2. Resolve ambiguous abbreviations, missing end times, and venue exceptions before publishing.
3. Edit only the applicable subscribed feed files.
4. Validate event-block balance and inspect summaries:

```sh
awk 'BEGIN{b=0;e=0} /^BEGIN:VEVENT\r?$/{b++} /^END:VEVENT\r?$/{e++} END{printf "%d begin, %d end\n",b,e; exit(b==e ? 0 : 1)}' rehearsal.ics
rg '^SUMMARY:' rehearsal.ics
```

5. Check for overlong unfolded lines:

```sh
awk 'length($0)>76 {print FILENAME ":" FNR ":" length($0)}' *.ics
```

6. Review the diff, commit, and push:

```sh
git diff --check
git add group.ics rehearsal.ics harmony-singers.ics dancers.ics sets.ics marketing.ics
git commit -m "Update KCMT calendars"
git push origin main
```

7. Wait for GitHub Pages to finish building, then verify each changed URL returns HTTP 200 with `text/calendar` and inspect the live content rather than relying only on the local file:

```sh
curl -I https://thebogdan.github.io/annie-calendar/rehearsal.ics
curl -L -sS https://thebogdan.github.io/annie-calendar/rehearsal.ics | tr -d '\r' | rg '^SUMMARY:'
```

## BAND synchronization behavior

- BAND subscribes to the public GitHub Pages URLs; it does not read this working directory directly.
- GitHub Pages must finish rebuilding before changes are available to BAND.
- BAND refreshes external calendars periodically and may take about 30 minutes to show a change.
- To request an immediate refresh in BAND, go to **Settings → Manage Events**, select/change the external calendar, and use the sync icon.
- A title visible in BAND may temporarily be an older cached title even when the live feed has already changed.
- Before republishing or changing a UID because an event appears missing, inspect the live GitHub Pages feed and allow or trigger a BAND sync. Changing a UID unnecessarily can create duplicate events.

## September 2026 decisions

- The initial published range begins September 19, 2026; earlier September events were intentionally omitted from the six subscribed feeds.
- The September 25 dancer event is `Dance Rehearsal`, 4:30–7:30 PM.
- The September 19 `Cast AB Rehearsal`, 3:00–6:00 PM, is present in the live rehearsal feed. A repeated user message briefly made it appear missing, but no forced republish was needed.
- General rehearsal-note text about memorization, vocals, and choreography was intentionally not added to event descriptions.
