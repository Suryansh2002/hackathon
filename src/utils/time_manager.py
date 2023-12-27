from datetime import datetime, timezone, timedelta

get_current_time = lambda: datetime.now(tz=timezone(timedelta(hours=5, minutes=30)))


def get_datetime(date_string: str) -> datetime:
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")


def get_datetime_string(date: datetime) -> str:
    return date.strftime("%Y-%m-%dT%H:%M:%S%z")
