"""For two given calendars with the schedule of a date, return another calendar
 with all the available time periods where a meeting can be scheduled in both
calendars. A meeting can only be scheduled if it has at least a given duration
in minutes.
e.g.:
calendar0 = [['09:00', '10:30'], ['12:00', '13:00'], ['16:00', '18:00']]
daily_bounds0 = ['09:00', '20:00']
calendar1 = [['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'],
['16:00', '17:00']]
daily_bounds1 = ['10:00', '18:30']
meeting_duration = 30

output = [['11:30', '12:00'], ['15:00', '16:00'], ['18:00', '18:30']]

The calendar consists of tuples or arrays of size 2 of str, which represents
the start and end time of a meeting already scheduled in the calendar.
e.g.:
 - meeting = ['09:00', '10:30']
 - calendar0 = [meeting, ['12:00', '13:00'], ['16:00', '18:00']]

assume that a meeting can begin at the same time as another ends in the calendar.
e.g.: calendar = [['...', '10:30'], ['10:30', '...']]

assume that input is always a valid one for the calculations you need to do.
i.e.:
- No empty strings.
- time in 'hh:mm' format.
- time in 24 hour format. e.g.: '15:00' not '03:00'

Question from https://www.youtube.com/watch?v=kbwk1Tw3OhE
"""
# Standard Library
from typing import List

CALENDAR0 = [["09:00", "10:30"], ["12:00", "13:00"], ["16:00", "18:00"]]
DAILY_BOUNDS0 = ["09:00", "20:00"]
CALENDAR1 = [
    ["10:00", "11:30"],
    ["12:30", "14:30"],
    ["14:30", "15:00"],
    ["16:00", "17:00"],
]
DAILY_BOUNDS1 = ["10:00", "18:30"]
MIN_MEET_TIME = 30


def get_daily_bounds(bounds: List[List[str]]) -> List[str]:
    """Get the more restrict times for the daily bounds."""
    actual_bounds = [max(bounds[0][0], bounds[1][0]), min(bounds[0][1], bounds[1][1])]
    return actual_bounds


def remove_out_of_bounds(
    calendar: List[List[str]], bounds: List[str]
) -> List[List[str]]:
    """Goes through the calendar of closed timestamps and change it to comply
    with the bounds.
    """
    new_calendar = []
    for _ in range(len(calendar)):
        if bounds[0] < calendar[0][0]:
            new_calendar.append(["", bounds[0]])
            break
        elif bounds[0] < calendar[0][1]:
            new_calendar.append([bounds[0], calendar[0][1]])
            del calendar[0]
            break
        elif calendar[0][1] <= bounds[0]:
            del calendar[0]
    new_calendar.extend(calendar)
    for _ in range(len(new_calendar)):
        if new_calendar[-1][1] < bounds[1]:
            new_calendar.append([bounds[1], ""])
            break
        elif new_calendar[-1][0] < bounds[1]:
            saved_timestamp = new_calendar[-1]
            del new_calendar[-1]
            new_calendar.append([saved_timestamp[-1][0], bounds[1]])
            break
        elif bounds[1] <= new_calendar[-1][0]:
            del new_calendar[-1]
    return new_calendar


def get_open_calendar(calendar: List[List[str]], bounds: List[str]) -> List[List[str]]:
    """returns another calendar with the open timespans for a given calendar
    and given daily bounds.
    """
    new_calendar = remove_out_of_bounds(calendar=calendar, bounds=bounds)
    open_calendar = []
    for ss, ee in zip(new_calendar[:-1], new_calendar[1:]):
        open_calendar += [[ss[1], ee[0]]]
    return open_calendar


# if __name__ == "__main__":
#     cal = get_open_calendar(calendar=CALENDAR0, bounds=["00:00", "21:00"])
#     print(cal)


def intersect_timespan(span_0: List[str], span_1: List[str]) -> List[str]:
    """checks whether  two timespans intersect and return a new timestamp.
    returns none if no intersection was found.
    """
    if max(span_0[0], span_1[0]) < min(span_0[1], span_1[1]):
        return [max(span_0[0], span_1[0]), min(span_0[1], span_1[1])]
    return


# if __name__ == "__main__":
#     span0 = ["10:30", "12:00"]
#     span1 = ["11:30", "12:30"]
#     timespan = intersect_timespan(span_0=span0, span_1=span1)
#     print(timespan)


def intersect_calendars(
    cal_0: List[List[str]], cal_1: List[List[str]]
) -> List[List[str]]:
    """checks whether any of the available timespans intersect and return them
    as a new calendar.
    """
    new_calendar = []
    for time_0 in cal_0:
        for time_1 in cal_1:
            if time_0[1] < time_1[0]:
                break
            if time_1[1] < time_0[0]:
                continue
            timespan = intersect_timespan(span_0=time_0, span_1=time_1)
            if timespan:
                new_calendar.append(timespan)
    return new_calendar


def get_hour_delta(timestamp: List[str]) -> int:
    """return the hour delta between two timestamps."""
    return int(timestamp[1][:2]) - int(timestamp[0][:2])


def get_minute_delta(timestamp: List[str]) -> int:
    """return the minute delta between two timestamps."""
    return int(timestamp[1][-2:]) - int(timestamp[0][-2:])


def filter_calendar(calendar: List[List[str]], min_time: int) -> List[List[str]]:
    """Checks if the timestamps are greater or equal than the minimum time in minutes for
    a meeting to be available.
    """
    timestamps_to_remove = []
    for timestamp in calendar:
        hour_delta = get_hour_delta(timestamp=timestamp)
        minute_delta = get_minute_delta(timestamp=timestamp)
        delta = hour_delta * 60 + minute_delta
        if delta < min_time:
            timestamps_to_remove.append(timestamp)
    filtered_calendar = [ts for ts in calendar if ts not in timestamps_to_remove]
    return filtered_calendar


def get_available_time_in_calendars(
    calendar_0: List[List[str]],
    calendar_1: List[List[str]],
    daily_bounds_0: List[str],
    daily_bounds_1: List[str],
    min_meet_time: int,
) -> List[List[str]]:
    """
    goes through both calendars and returns a new calendar with the available times in them.

    :param calendar_0:
    :param calendar_1:
    :param daily_bounds_0:
    :param daily_bounds_1:
    :param min_meet_time:
    :return:
    """
    bounds = get_daily_bounds([daily_bounds_0, daily_bounds_1])
    new_calendar_0 = get_open_calendar(calendar=calendar_0, bounds=bounds)
    new_calendar_1 = get_open_calendar(calendar=calendar_1, bounds=bounds)
    intersection = intersect_calendars(cal_0=new_calendar_0, cal_1=new_calendar_1)
    new_calendar = filter_calendar(calendar=intersection, min_time=min_meet_time)
    return new_calendar


if __name__ == "__main__":
    cal = get_available_time_in_calendars(
        calendar_0=CALENDAR0,
        calendar_1=CALENDAR1,
        daily_bounds_0=DAILY_BOUNDS0,
        daily_bounds_1=DAILY_BOUNDS1,
        min_meet_time=MIN_MEET_TIME,
    )
    print(cal)
