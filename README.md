# Grips im Spiel Kalender

This repository builds a small GitHub Pages site and an ICS calendar feed for the "Grips im Spiel" events.

## Local preview

Install dependencies with `uv`:

```bash
uv sync
```

Build and serve the site locally:

```bash
./scripts/build_site.sh --serve
```

Then open `http://127.0.0.1:8000/calendars/` in your browser.

## Adding new events

Open any of the `.yaml` files in the `calendars/` directory and add new events to the `events:` list. The website and
calendar will be updated automatically on the next push to GitHub.
