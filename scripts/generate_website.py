#!/usr/bin/env python3
"""Generate HTML website from stadtbibliothek.yaml"""

from datetime import datetime, timedelta
from pathlib import Path
import shutil

import markdown
import yaml


def load_events():
    """Load events from stadtbibliothek.yaml"""
    events_file = Path(__file__).parent.parent / "calendars" / "stadtbibliothek.yaml"
    with open(events_file) as f:
        data = yaml.safe_load(f)
    return data


def parse_begin(value):
    """Normalize YAML date values to datetime."""
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value)


def render_markdown(text):
    """Render Markdown descriptions to HTML."""
    return markdown.markdown(text, extensions=["nl2br"])


def format_event(event):
    """Format a single event for display"""
    begin = parse_begin(event["begin"])
    duration_minutes = event.get("duration", {}).get("minutes", 60)
    end = begin + timedelta(minutes=duration_minutes)

    date_str = begin.strftime("%d.%m.%Y")
    time_str = begin.strftime("%H:%M") + " – " + end.strftime("%H:%M")

    return {
        "summary": event["summary"],
        "location": event.get("location", ""),
        "date": date_str,
        "time": time_str,
        "url": event.get("url", ""),
        "description_html": render_markdown(event.get("description", "")),
    }


def build_events_html(upcoming_events):
    """Build HTML for event list"""
    events_html = ""
    for event in upcoming_events:
        events_html += f"""        <article class="event">
            <div class="event-header">
                <h3>{event["summary"]}</h3>
                <div class="event-meta">
                    <span class="date">📅 {event["date"]}</span>
                    <span class="time">🕐 {event["time"]}</span>
                    {f'<span class="location">📍 {event["location"]}</span>' if event["location"] else ""}
                    {f'<span class="url">🔗 <a href="{event["url"]}" target="_blank" rel="noopener noreferrer">Zur Veranstaltung</a></span>' if event["url"] else ""}
                </div>
            </div>
            <div class="event-content">
                <div class="description markdown-content">{event["description_html"]}</div>
            </div>
        </article>
"""
    return events_html


def main():
    """Main entry point"""
    # Load and filter data
    data = load_events()
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    upcoming_events = [
        e for e in data.get("events", []) if parse_begin(e["begin"]) >= today
    ]

    formatted_events = [format_event(e) for e in upcoming_events]

    # Build content
    description_html = render_markdown(data.get("description", ""))
    events_html = build_events_html(formatted_events)

    # Load template
    template_file = Path(__file__).parent / "template.html"
    template = template_file.read_text()

    # Render
    html = template.format(
        description_html=description_html,
        events_html=events_html,
    )

    # Write output
    output_dir = Path(__file__).parent.parent / "_site" / "calendars"
    output_dir.mkdir(exist_ok=True)

    index_file = output_dir / "index.html"
    index_file.write_text(html)
    print(f"✓ Generated {index_file}")

    # Copy CSS
    css_src = Path(__file__).parent / "style.css"
    css_dst = output_dir / "style.css"
    shutil.copy(css_src, css_dst)
    print(f"✓ Copied {css_dst}")

    # Copy JavaScript
    js_src = Path(__file__).parent / "copy_calendar.js"
    js_dst = output_dir / "copy_calendar.js"
    shutil.copy(js_src, js_dst)
    print(f"✓ Copied {js_dst}")


if __name__ == "__main__":
    main()
