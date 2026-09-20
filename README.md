# Annie Calendar

This repository hosts KCMT calendars in two formats:

- `.ics` files for BAND's **Subscribe by URL** feature and other calendar apps.
- `.csv` files for BAND's **Import by File** feature. CSV-imported events can be
  edited directly in BAND.

Subscribed iCalendar URLs:

- Group Calendar: `https://thebogdan.github.io/annie-calendar/group.ics`
- Rehearsal Calendar: `https://thebogdan.github.io/annie-calendar/rehearsal.ics`
- Harmony Singers: `https://thebogdan.github.io/annie-calendar/harmony-singers.ics`
- Dancer Schedule: `https://thebogdan.github.io/annie-calendar/dancers.ics`
- Sets: `https://thebogdan.github.io/annie-calendar/sets.ics`
- Marketing Calendar: `https://thebogdan.github.io/annie-calendar/marketing.ics`

These URLs remain unchanged as events are added or corrected.

CSV download URLs:

- Group Calendar: `https://thebogdan.github.io/annie-calendar/group.csv`
- Rehearsal Calendar: `https://thebogdan.github.io/annie-calendar/rehearsal.csv`
- Harmony Singers: `https://thebogdan.github.io/annie-calendar/harmony-singers.csv`
- Dancer Schedule: `https://thebogdan.github.io/annie-calendar/dancers.csv`
- Sets: `https://thebogdan.github.io/annie-calendar/sets.csv`
- Marketing Calendar: `https://thebogdan.github.io/annie-calendar/marketing.csv`

The `.ics` files are the maintained event source. After changing them, regenerate
all six CSV files with:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/ics_to_csv.py
```

CSV imports are snapshots rather than subscriptions. Reimporting a calendar may
create duplicates, and edits made directly in BAND do not flow back into this
repository.
