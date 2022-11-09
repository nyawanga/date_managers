
A utility function(s) that help generate date ranges based on a set of rules that determine what time interval is applied.
The time interval needs to be a string format in either day, week, month, year interval options.
The rules guiding what interval gets applied are as follows:


- yearly: always start from the first day in the year of start_date provided
- monthly: always start from the first day in the month of start_date provided
- weekly: always start from the first day in the week (Sunday) of start_date provided
- day: starts from the start_date provided
- 1_year/2_year/n_year: start from the  start_date provided
- 1_month/2_month/n_month: start from the first day in the month of the start_date provided
- 1_week/2_week/n_week: start from the start_date provided


For each interval, it should return start date  that should be inclusive and end date that is exclusive but the final range `MUST` include the provided end_date.  For example:
```
Given input start_date 2022-01-01 and end_date 2022-01-03 with daily interval we get back these pairs:

2022-01-01 2022-01-02
2022-01-02 2022-01-03
2022-01-03 2022-01-04
```
Also allows for specifying what date format you want back though it has to conform to python standard date formats.

### How to use:
most direct use will be to import `date_range_iterator` from date_range_handlers i.e
```python
    from date_range_handlers import date_range_iterator


    date_iterator = date_range_iterator(
        start_date=datetime, 
        end_date=datetime, 
        interval="1_week", 
        time_format="%Y-%m-%d"
        )

    for start, end in date_iterator:
        ## do something  
```

You can also build your own entry point by importing `DateIntervalHandler` from `date_range_managers`
