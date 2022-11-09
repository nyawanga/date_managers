"""TEST READERS"""
# pylint: disable=protected-access, wrong-import-position, import-error, unused-argument

import os
import sys
from datetime import datetime

import pytest


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# from base_test import BaseTest
from date_range_handlers import (
    DayInterval,
    MonthInterval,
    YearInterval,
    WeekInterval,
    DateIntervalHandler,
)


# @pytest.mark.usefixtures("environ_fixture")
class TestReaders:
    """Class for Date Handler Classes and Methods"""

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

    def test_date_interval_factory(self):
        """Test the init method"""

        handler = DateIntervalHandler(interval="day", time_format="%Y-%m-%d")
        interval_handler = handler.range_iterator_factory()
        assert handler.time_bucket == "day"
        assert handler.cadence == 1
        assert handler.root_bucket == "day"
        assert handler.time_format == "%Y-%m-%d"
        assert isinstance(interval_handler, DayInterval)

        handler = DateIntervalHandler(interval="2_day", time_format="%Y-%m-%d")
        interval_handler = handler.range_iterator_factory()
        assert handler.time_bucket == "day"
        assert handler.cadence == 2
        assert handler.root_bucket == "day"
        assert handler.time_format == "%Y-%m-%d"
        assert isinstance(interval_handler, DayInterval)

    def test_monthly_interval_processor_method(self):
        """Test the init method"""

        handler = DateIntervalHandler(interval="Monthly", time_format="%Y-%m-%d")
        interval_handler = handler.range_iterator_factory()
        assert handler.time_bucket == "monthly"
        assert handler.cadence == 1
        assert handler.root_bucket == "month"
        assert isinstance(interval_handler, MonthInterval)

        handler = DateIntervalHandler(interval="2_month", time_format="%Y-%m-%d")
        interval_handler = handler.range_iterator_factory()

        assert handler.time_bucket == "month"
        assert handler.cadence == 2
        assert handler.root_bucket == "month"
        assert isinstance(interval_handler, MonthInterval)

    def test_year_interval_processor_method(self):
        """Test the init method"""

        handler = DateIntervalHandler(interval="yearly", time_format="%Y-%m-%d")
        interval_handler = handler.range_iterator_factory()

        assert handler.time_bucket == "yearly"
        assert handler.cadence == 1
        assert handler.root_bucket == "year"
        assert isinstance(interval_handler, YearInterval)

        handler = DateIntervalHandler(interval="3_year", time_format="%Y-%m-%d")
        interval_handler = handler.range_iterator_factory()

        assert handler.time_bucket == "year"
        assert handler.cadence == 3
        assert handler.root_bucket == "year"
        assert isinstance(interval_handler, YearInterval)

    def test_week_interval_processor_method(self):
        """Test the init method"""

        handler = DateIntervalHandler(interval="2_weekly", time_format="%Y-%m-%d")
        interval_handler = handler.range_iterator_factory()

        assert handler.time_bucket == "weekly"
        assert handler.cadence == 2
        assert handler.root_bucket == "week"
        assert isinstance(interval_handler, WeekInterval)

        handler = DateIntervalHandler(interval="1_week", time_format="%Y-%m-%d")
        interval_handler = handler.range_iterator_factory()

        assert handler.time_bucket == "week"
        assert handler.cadence == 1
        assert handler.root_bucket == "week"
        assert isinstance(interval_handler, WeekInterval)

    def test_interval_processor_wrong_interval_type(self):
        """Test the stemmer method"""

        with pytest.raises(TypeError):
            DateIntervalHandler(
                interval="50", time_format="%Y-%m-%d"
            ).range_iterator_factory()

        with pytest.raises(TypeError):
            DateIntervalHandler(
                interval=None, time_format="%Y-%m-%d"
            ).range_iterator_factory()

        with pytest.raises(TypeError):
            DateIntervalHandler(
                interval="", time_format="%Y-%m-%d"
            ).range_iterator_factory()

        with pytest.raises(TypeError):
            DateIntervalHandler(
                interval=1234, time_format="%Y-%m-%d"
            ).range_iterator_factory()

    def test_interval_processor_wrong_value(self):
        """Test the stemmer method"""

        with pytest.raises(ValueError):
            DateIntervalHandler(
                interval="2_weekly_another", time_format="%Y-%m-%d"
            ).range_iterator_factory()

        with pytest.raises(ValueError):
            DateIntervalHandler(
                interval="weeks", time_format="%Y-%m-%d"
            ).interval_processor()

    def test_get_interval_bucket(self):
        """Test interval_bucket_mapping"""
        handler = DateIntervalHandler(interval="2_", time_format="%Y-%m-%d")
        assert isinstance(handler.interval_bucket_mapping, dict)

    def test_exist_conditions(self):
        """test range_iterator exit conditions"""
        handler = DateIntervalHandler(interval="2_day", time_format="%Y-%m-%d")
        interval_handler = handler.range_iterator_factory()

        iterator = interval_handler.range_iterator(
            datetime(2022, 11, 9), datetime(2022, 11, 11)
        )
        assert next(iterator) == ("2022-11-09", "2022-11-11")
        with pytest.raises(StopIteration):
            next(iterator)

    def test_get_start_date_conditions(self):
        """test range_iterator exit conditions"""
        handler = DateIntervalHandler(interval="weekly", time_format="%Y-%m-%d")
        interval_handler = handler.range_iterator_factory()

        iterator = interval_handler.range_iterator(
            datetime(2022, 11, 9), datetime(2022, 11, 15)
        )
        assert next(iterator) == ("2022-11-06", "2022-11-13")
        assert next(iterator) == ("2022-11-13", "2022-11-20")

        handler = DateIntervalHandler(interval="monthly", time_format="%Y-%m-%d")
        interval_handler = handler.range_iterator_factory()

        iterator = interval_handler.range_iterator(
            datetime(2022, 11, 9), datetime(2022, 11, 15)
        )
        assert next(iterator) == ("2022-11-01", "2022-12-01")
        with pytest.raises(StopIteration):
            next(iterator)

        handler = DateIntervalHandler(interval="yearly", time_format="%Y-%m-%d")
        interval_handler = handler.range_iterator_factory()
        iterator = interval_handler.range_iterator(
            datetime(2022, 11, 9), datetime(2022, 11, 15)
        )
        assert next(iterator) == ("2022-01-01", "2023-01-01")
        with pytest.raises(StopIteration):
            next(iterator)

        handler = DateIntervalHandler(interval="2_year", time_format="%Y-%m-%d")
        interval_handler = handler.range_iterator_factory()

        iterator = interval_handler.range_iterator(
            datetime(2022, 11, 9), datetime(2022, 11, 15)
        )
        assert next(iterator) == ("2022-11-09", "2024-11-09")
        with pytest.raises(StopIteration):
            next(iterator)
