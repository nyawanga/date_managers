

## Date Managers
A utility function(s) that help generate date ranges based on a set of rules that determine what time interval is applied.
The time interval needs to be a string format in either day, week, month, year interval options.
The rules guiding what interval gets applied are as follows:

### Interval date string rules
- yearly: always start from the first day in the year of start_date provided
- monthly: always start from the first day in the month of start_date provided
- weekly: always start from the first day in the week (Sunday) of start_date provided
- day: starts from the start_date provided
- 1_year/2_year/n_year: start from the  start_date provided
- 1_month/2_month/n_month: start from the first day in the month of the start_date provided
- 1_week/2_week/n_week: start from the start_date provided


### Date value string rules (start_date, end_date)
- `day`: `today, yesterday, 1_days_ago, 2_days_ago, n_days_ago`
- `last_week`: translates to previous week on Sunday
- `1_weeks_ago`: `7 days` from `current_date`
- `last_month`/`1_months_ago`/`n_months_ago`: translates to start of `n_months` from `current date`
- `last_year`: translates to start of the previous year
- `1_years_ago`/`n_years_ago`: translates to n_years from current date
For each interval, it should return start date  that should be inclusive and final range `MUST` include the provided end_date.  For example:
```
Given input `start_date 2022-01-01` and `end_date 2022-01-03` with daily interval we get back these pairs:

2022-01-01 2022-01-02
2022-01-02 2022-01-03
2022-01-03 2022-01-04
```
Also allows for specifying what date format you want back though it has to conform to python standard date formats.

### How to use:
most direct use will be to import `date_range_iterator` from date_range_handlers i.e
```python
    from date_managers import date_range_iterator


    date_iterator = date_range_iterator(
        start_date=datetime_string, 
        end_date=datetime_string, 
        interval="1_day", 
        end_inclusive=False
        time_format="%Y-%m-%d"
        )

    for start, end in date_iterator:
        ## do something  
```
### Parameters
- `start_date`  date_string as described on the date string rules
- `end_date`  date string as described on the date string rules
- `interval` string as described on the interval date string rules
- `end_inclusive` boolean if `True` withing each interval start and end, the end date value will be inclusive otherwise exclusive
- `time_format` the time format that you want back from the function.

You can also build your own entry point by importing `DateHandlerFactory` from `date_managers`
