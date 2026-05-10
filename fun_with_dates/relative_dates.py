"""Demo of computing relative dates using dateutil's relativedelta."""

from datetime import datetime

from dateutil.relativedelta import relativedelta


def add_months(base_date: datetime, months: int) -> datetime:
    """Add (or subtract) a number of months from a date.

    Args:
        base_date: The starting datetime.
        months: Number of months to add (negative to subtract).

    Returns:
        A new datetime offset by the given months.
    """
    return base_date + relativedelta(months=months)


if __name__ == "__main__":
    base_date = datetime(2018, 1, 31, 10, 11, 12)
    new_date = add_months(base_date, 1)

    print(f"Base date:     {base_date}")
    print(f"Plus 1 month:  {new_date}")
