# file_parser.py
import io
import re
from datetime import datetime
import pandas as pd
from icalendar import Calendar
import PyPDF2

def parse_pdf(file_bytes):
    """
    Naively extracts events from a PDF.
    Assumes each relevant line contains a date in YYYY-MM-DD format followed by an event name,
    e.g., "2025-07-04: Independence Day".
    """
    events = []
    reader = PyPDF2.PdfReader(file_bytes)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    pattern = re.compile(r'(\d{4}-\d{2}-\d{2})\s*[:\-]\s*(.+)')
    for line in text.splitlines():
        match = pattern.search(line)
        if match:
            date_str = match.group(1)
            event_name = match.group(2).strip()
            try:
                event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                events.append({"date": event_date, "name": event_name})
            except Exception:
                continue
    return events

def parse_ics(file_bytes):
    """
    Extracts events from an ICS file.
    """
    events = []
    try:
        cal = Calendar.from_ical(file_bytes.read())
        for component in cal.walk():
            if component.name == "VEVENT":
                dt = component.get('dtstart').dt
                # Normalize dt to date if it’s a datetime
                if hasattr(dt, 'date'):
                    dt = dt.date()
                event_name = str(component.get('summary'))
                events.append({"date": dt, "name": event_name})
    except Exception as e:
        print("Error parsing ICS:", e)
    return events

def parse_csv(file_bytes):
    """
    Extracts events from a CSV file.
    Expects columns: "date" (YYYY-MM-DD) and "event_name".
    """
    events = []
    try:
        df = pd.read_csv(file_bytes)
        # Normalize column names to lower-case
        df.columns = [col.lower() for col in df.columns]
        if 'date' in df.columns and 'event_name' in df.columns:
            for index, row in df.iterrows():
                try:
                    event_date = datetime.strptime(row['date'], "%Y-%m-%d").date()
                    events.append({"date": event_date, "name": row['event_name']})
                except Exception:
                    continue
    except Exception as e:
        print("Error parsing CSV:", e)
    return events

def parse_calendar(file, file_type):
    """
    Routes the file to the correct parser based on file_type.
    """
    if file_type == "pdf":
        return parse_pdf(file)
    elif file_type == "ics":
        return parse_ics(file)
    elif file_type == "csv":
        return parse_csv(file)
    else:
        return []

def is_weekend(date_obj):
    """
    Returns True if the given date (datetime.date) is a Saturday or Sunday.
    """
    return date_obj.weekday() in (5, 6)
