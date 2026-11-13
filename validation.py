"""Validates the web form (replaces the input() loops in user_input.py)."""
from datetime import datetime

CHART_TYPES = {"line": "Line", "bar": "Bar"}
TIME_SERIES = {
    "TIME_SERIES_DAILY": "Daily",
    "TIME_SERIES_WEEKLY": "Weekly",
    "TIME_SERIES_MONTHLY": "Monthly",
}


def _parse_date(text):
    try:
        return datetime.strptime((text or "").strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


def validate(form, valid_symbols):
    """Return (clean_values, list_of_error_messages)."""
    errors = []
    clean = {}

    symbol = (form.get("symbol") or "").strip().upper()
    if symbol in valid_symbols:
        clean["symbol"] = symbol
    else:
        errors.append("Please select a stock symbol from the list.")

    chart_type = form.get("chart_type")
    if chart_type in CHART_TYPES:
        clean["chart_type"] = chart_type
    else:
        errors.append("Please select a chart type.")

    function = form.get("time_series")
    if function in TIME_SERIES:
        clean["function"] = function
    else:
        errors.append("Please select a time series.")

    start = _parse_date(form.get("start_date"))
    if start:
        clean["start"] = start
    else:
        errors.append("Please enter a valid start date (YYYY-MM-DD).")

    end = _parse_date(form.get("end_date"))
    if end:
        clean["end"] = end
    else:
        errors.append("Please enter a valid end date (YYYY-MM-DD).")

    if start and end and end <= start:
        errors.append("The end date must be after the start date.")

    return clean, errors
