"""Demo of how to compute the delta (uptime) between two dates."""

from datetime import datetime, timedelta


def get_uptime(start: datetime, end: datetime) -> timedelta:
    """Calculate the time difference between two datetime objects.

    Args:
        start: The earlier datetime.
        end: The later datetime.

    Returns:
        A timedelta representing the difference.
    """
    return end - start


if __name__ == "__main__":
    date_init = datetime.strptime("5-8-2000 13:45:10.345", "%d-%m-%Y %H:%M:%S.%f")
    date_final = datetime(year=2018, month=1, day=30)

    uptime = get_uptime(date_init, date_final)
    print(f"Uptime: {uptime}")
