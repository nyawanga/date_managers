"""TEST READERS"""
# pylint: disable=protected-access, wrong-import-position, import-error, unused-argument

import os
import sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import pytest


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# from base_test import BaseTest
from exceptions import (
    TimeIntervalError,
    TimeBucketError,
    CadenceTimeBucketError,
    DateValueError,
)

from date_managers import (
    DayInterval,
    MonthInterval,
    YearInterval,
    WeekInterval,
    PastDatePhraseHandler,
    IntervalDatePhraseHandler,
    DateHandlerFactory,
    date_string_handler,
    date_range_iterator,
)


# @pytest.mark.usefixtures("environ_fixture")
class TestDateManagers:
    """Class for Date Handler Classes and Methods"""

    def time_bucket_mapping(self) -> dict:
        """map interval with base bucket

        Args:
            interval (str): interval provided to be used

        Returns:
            dict:
        """
        time_bucket_mapping = {
            "day": ["day", "yesterday", "today"],
            "week": ["week", "weekly", "last_week", "this_week"],
            "month": ["month", "monthly", "last_month", "this_month"],
            "year": ["year", "yearly", "last_year", "this_year"],
        }

        return time_bucket_mapping

    def date_handler_classes(self):
        """Fixture for date handlers"""
        return {
            "day": DayInterval,
            "week": WeekInterval,
            "month": MonthInterval,
            "year": YearInterval,
        }

    def test_past_date_phrase_handler(self):
        """Test the class PastDatePhraseHandler"""

        handler = PastDatePhraseHandler("1_week_ago")
        assert handler.date_value == "1_week_ago"
        assert handler.cadence is None
        assert handler.time_bucket is None

        handler.phrase_to_date()
        assert handler.cadence == 1
        assert handler.time_bucket == "week"

        handler = PastDatePhraseHandler("1")
        with pytest.raises(TypeError):
            handler.phrase_to_date()

        handler = PastDatePhraseHandler("2_years_before")
        with pytest.raises(DateValueError):
            handler.phrase_to_date()

        handler = PastDatePhraseHandler("daily")
        with pytest.raises(CadenceTimeBucketError):
            handler.phrase_to_date()

    def test_interval_date_phrase_handler(self):
        """Test the class PastDatePhraseHandler"""

        handler = IntervalDatePhraseHandler("monthly")
        assert handler.date_value == "monthly"
        assert handler.cadence is None
        assert handler.time_bucket is None

        handler.phrase_to_date()
        assert handler.cadence == 1
        assert handler.time_bucket == "monthly"

        handler = IntervalDatePhraseHandler("1")
        with pytest.raises(TypeError):
            handler.phrase_to_date()

        handler = IntervalDatePhraseHandler("2_month_before")
        with pytest.raises(TimeIntervalError):
            handler.phrase_to_date()

        handler = IntervalDatePhraseHandler("quarterly")
        with pytest.raises(CadenceTimeBucketError):
            handler.phrase_to_date()

    def test_data_handler_factory(self):
        """Test dat_handler_factory"""
        time_bucket_mapping = self.time_bucket_mapping()
        for key, val in time_bucket_mapping.items():
            for time_bucket in val:
                handler = DateHandlerFactory()
                date_handler = handler.get_date_handler(
                    time_bucket=time_bucket, cadence=1
                )
                if key == "day":
                    assert isinstance(date_handler, DayInterval)
                if key == "week":
                    assert isinstance(date_handler, WeekInterval)
                if key == "month":
                    assert isinstance(date_handler, MonthInterval)
                if key == "year":
                    assert isinstance(date_handler, YearInterval)

        wrong_time_buckets = ["annually", "quarterly", "daily", "termly", "biannually"]
        for time_bucket in wrong_time_buckets:
            with pytest.raises(TimeBucketError):
                handler = DateHandlerFactory()
                date_handler = handler.get_date_handler(
                    time_bucket="annually", cadence=1
                )

    def test_date_string_handler(self):
        """Test sate_string_handler method"""

        assert date_string_handler("2022-11-14") == datetime.strptime(
            "2022-11-14", "%Y-%m-%d"
        )

        assert datetime.strftime(
            date_string_handler("today"), "%Y-%m-%d"
        ) == datetime.strftime(datetime.now(), "%Y-%m-%d")

        yesterday_date = datetime.now() - timedelta(days=1)
        assert datetime.strftime(
            date_string_handler("yesterday"), "%Y-%m-%d"
        ) == datetime.strftime(yesterday_date, "%Y-%m-%d")

        with pytest.raises(TypeError):
            date_string_handler("2022/11/14")
        with pytest.raises(DateValueError):
            date_string_handler("1_Week")

    def test_date_range_iterator_end_inclusive_true(self):
        """Test date_range_iterator"""
        start_date, end_date = "2022-11-14", "2022-11-15"
        date_iterator = date_range_iterator(
            start_date, end_date, "1_day", end_inclusive=True
        )
        assert next(date_iterator) == ("2022-11-14", "2022-11-14")
        assert next(date_iterator) == ("2022-11-15", "2022-11-15")
        with pytest.raises(StopIteration):
            next(date_iterator)

    def test_date_range_iterator_end_inclusive_false(self):
        """Test date_range_iterator"""
        start_date, end_date = "2022-11-14", "2022-11-15"
        date_iterator = date_range_iterator(
            start_date, end_date, "1_day", end_inclusive=False
        )
        assert next(date_iterator) == ("2022-11-14", "2022-11-15")
        assert next(date_iterator) == ("2022-11-15", "2022-11-16")
        with pytest.raises(StopIteration):
            next(date_iterator)

    def test_date_range_iterator_time_format(self):
        """Test date_range_iterator"""
        start_date, end_date = "2022-11-14", "2022-11-15"
        date_iterator = date_range_iterator(
            start_date, end_date, "1_day", end_inclusive=False, time_format="%d/%m/%Y"
        )
        assert next(date_iterator) == ("14/11/2022", "15/11/2022")
        assert next(date_iterator) == ("15/11/2022", "16/11/2022")
        with pytest.raises(StopIteration):
            next(date_iterator)

    def test_date_string_handler_this_prefix(self):
        """Test this date phrases"""
        current_date = datetime.now()
        week_start = (current_date - timedelta(days=current_date.weekday())).date()
        month_start = current_date.replace(day=1).date()
        year_start = current_date.replace(month=1, day=1).date()
        if datetime.strftime(current_date, "%A") == "Sunday":
            week_start = current_date.date()

        assert date_string_handler("this_week").date() == week_start
        assert date_string_handler("this_month").date() == month_start
        assert date_string_handler("this_year").date() == year_start

    def test_date_string_handler_last_prefix(self):
        """Test last date phrases"""
        current_date = datetime.now()
        last_week_start = (current_date - timedelta(days=current_date.weekday())).date()
        last_month_start = current_date.replace(day=1).date() - relativedelta(months=1)
        last_year_start = current_date.replace(month=1, day=1).date() - relativedelta(
            years=1
        )
        if datetime.strftime(current_date, "%A") == "Sunday":
            last_week_start = current_date.date()
        last_week_start = last_week_start - relativedelta(weeks=1)
        assert date_string_handler("last_week").date() == last_week_start
        assert date_string_handler("last_month").date() == last_month_start
        assert date_string_handler("last_year").date() == last_year_start
