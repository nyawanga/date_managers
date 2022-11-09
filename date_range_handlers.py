"""Date Range Handler"""

from abc import ABC, abstractmethod
import re
from datetime import datetime, timedelta, date
from typing import Tuple, Generator
from dateutil.relativedelta import relativedelta


class BaseDateInterval(ABC):
    """Get Start of the Date Range"""

    def __init__(self, time_bucket: str, cadence: int, time_format: str = "%Y-%m-%d"):
        self.time_format = time_format
        self.time_bucket = time_bucket
        self.cadence = cadence

    @abstractmethod
    def get_start_date(self, start_date: datetime) -> datetime:
        """Gets the start date of the range provided the input startdate

        Args:
            start_date (datetime): should be a datetime value

        Raises:
            NotImplementedError: _description_

        Returns:
            datetime: the processed start date
        """
        raise NotImplementedError

    @abstractmethod
    def add_interval(self, date_value: datetime, cadence: int) -> datetime:
        """Add the time interval to the current start date to get the end date

        Args:
            date_value (datetime): datetime value that is the start of the period
            cadence (int): time interval to add to the start date tp the end date

        Raises:
            NotImplementedError: raise error of NotImplementedError

        Returns:
            datetime: the end date value not inclusive
        """
        raise NotImplementedError

    def range_iterator(
        self, start_date: datetime, end_date: datetime
    ) -> Generator[Tuple[str, str], None, None]:
        """Iterator method that yields the start and end date exclusive

        Args:
            start_date (datetime): start date inclusive
            end_date (datetime): the end date inclusive

        Yields:
            Generator[Tuple[str, str], None, None]: yields the start and end date (exclusive)
        """

        start_date = self.get_start_date(start_date=start_date)
        next_end = self.add_interval(date_value=start_date, cadence=self.cadence)
        while start_date <= end_date:
            yield datetime.strftime(start_date, self.time_format), datetime.strftime(
                next_end, self.time_format
            )
            start_date = next_end
            next_end = self.add_interval(date_value=start_date, cadence=self.cadence)


class YearInterval(BaseDateInterval):
    """Class ti Get Yearly Cadence Start Date"""

    def __init__(self, time_bucket: str, cadence: int, time_format: str = "%Y-%m-%d"):
        super().__init__(
            time_bucket=time_bucket, cadence=cadence, time_format=time_format
        )

    def get_start_date(self, start_date: datetime) -> datetime:
        """Handles Yearly Buckets"""
        if self.time_bucket in ["yearly"]:
            start_date = start_date.replace(month=1, day=1)
        return start_date

    def add_interval(self, date_value: datetime, cadence: int):
        """Return a date that's `years` years after the date (or datetime)
        object `date_value`. Return the same calendar date (month and day) in the
        destination year, if it exists, otherwise use the following day
        (thus changing February 29 to March 1).

        """
        try:
            next_date = date_value.replace(year=date_value.year + cadence)
        except ValueError:
            next_date = date_value + (
                date(date_value.year + cadence, 1, 1) - date(date_value.year, 1, 1)
            )
        return next_date


class MonthInterval(BaseDateInterval):
    """Gets the Monthly Cadence Start Date"""

    def __init__(self, time_bucket: str, cadence: int, time_format: str = "%Y-%m-%d"):
        super().__init__(
            time_bucket=time_bucket, cadence=cadence, time_format=time_format
        )

    def get_start_date(self, start_date: datetime) -> datetime:
        """Handles Monthly Buckets"""
        if self.time_bucket in ["monthly", "month"]:
            start_date = start_date.replace(day=1)
        return start_date

    def add_interval(self, date_value: datetime, cadence: int):
        next_date = date_value + relativedelta(months=cadence)
        return next_date


class WeekInterval(BaseDateInterval):
    """Get the Weekly Cadence Start Date"""

    def __init__(self, time_bucket: str, cadence: int, time_format: str = "%Y-%m-%d"):
        super().__init__(
            time_bucket=time_bucket, cadence=cadence, time_format=time_format
        )

    def get_start_date(self, start_date: datetime) -> datetime:
        """Handles Weekly Buckets"""
        if self.time_bucket in ["weekly"]:
            start_date = start_date - timedelta(days=start_date.weekday() + 1)
        return start_date

    def add_interval(self, date_value: datetime, cadence: int):
        next_date = date_value + relativedelta(weeks=cadence)
        return next_date


class DayInterval(BaseDateInterval):
    """Get the Daily Cadence Start Date"""

    def __init__(self, time_bucket: str, cadence: int, time_format: str = "%Y-%m-%d"):
        super().__init__(
            time_bucket=time_bucket, cadence=cadence, time_format=time_format
        )

    def get_start_date(self, start_date: datetime) -> datetime:
        """Handles Daily Buckets"""
        return start_date

    def add_interval(self, date_value: datetime, cadence: int):
        next_date = date_value + relativedelta(days=cadence)
        return next_date


class DateIntervalHandler:
    """Date Handler Class"""

    def __init__(self, interval: str, time_format: str = "%Y-%m-%d"):
        self.interval = interval
        self.time_format = time_format
        self.cadence = None
        self.time_bucket = None
        self.root_bucket = None
        self.interval_bucket_mapping: dict = self.map_interval_bucket()

    def map_interval_bucket(self) -> dict:
        """map interval with base bucket

        Args:
            interval (str): interval provided to be used

        Returns:
            dict:
        """
        interval_bucket = {
            "day": ["day"],
            "week": ["week", "weekly"],
            "month": ["month", "monthly"],
            "year": ["year", "yearly"],
        }

        return interval_bucket

    def interval_processor(self) -> Tuple[int, str]:
        """Processes the interval variable to get the cadence and the time_bucket

        Raises:
            TypeError: is the interval value p[rovided is not a string]
            ValueError: if the interval can be split more than 2 times
            ValueError: if time_bucket and cadence end up to be None

        Returns:
            Tuple[int, str]: cadence that is an int and time_bucket
        """

        if not isinstance(self.interval, str) or not re.search(
            r"[a-z]+", str(self.interval).lower()
        ):
            raise TypeError("WARNING: Wrong interval provided, expecting a string")

        self.interval = self.interval.lower().strip()
        if len(self.interval.split("_")) > 2:
            raise ValueError("Invalid value for interval provided")

        if self.interval in ["day", "yearly", "weekly", "monthly"]:
            self.cadence, self.time_bucket = 1, self.interval
            # return self.cadence, self.time_bucket

        if len(self.interval.replace(" ", "_").split("_")) == 2:
            self.cadence, self.time_bucket = self.interval.split("_")

        if self.cadence is None or self.time_bucket is None:
            raise ValueError("INFO: wrong interval provided")
        print(self.cadence, self.time_bucket)

        return int(self.cadence), self.time_bucket.strip()

    def range_iterator_factory(self) -> BaseDateInterval:
        """A function that decides what interval handler to work with based on the interval passed

        Raises:
            ValueError: if one passes an interval that is not implemented yet

        Returns:
            BaseDateInterval: date interval handler to give us time intervals
        """

        self.cadence, self.time_bucket = self.interval_processor()
        for key, value in self.interval_bucket_mapping.items():
            if self.time_bucket in value:
                self.root_bucket = key

        if self.root_bucket is None:
            raise ValueError(f"WARNING: Wrong interval provided {self.interval}")

        interval_processors = {
            "year": YearInterval,
            "month": MonthInterval,
            "week": WeekInterval,
            "day": DayInterval,
        }

        return interval_processors[self.root_bucket](
            self.time_bucket, self.cadence, self.time_format
        )

def date_range_iterator(start_date: datetime, end_date: datetime, interval: str, time_format="%Y-%m-%d") -> Generator[Tuple[str, str], None, None]:
    """
    The range is inclusive, so both start_date and end_date will be returned.
    :start_date: The datetime object representing the first day in the range.
    :end_date: The datetime object representing the last day in the range.
    :delta: A datetime.timedelta instance, specifying the step interval. 
    Yields:
        Each datetime object in the range.
    """

    date_range = DateIntervalHandler(interval=interval, time_format=time_format
        ).range_iterator_factory()
    date_iter = date_range.range_iterator(start_date, end_date)
    for start, end in date_iter:
        yield start, end
