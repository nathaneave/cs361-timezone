import re
from fastapi import FastAPI, HTTPException
from datetime import datetime, timezone, timedelta

app = FastAPI()

@app.get("/timezone_converter")
def root(event_time: str, from_timezone: str, to_timezone: str):

    #event_time should be in the format YYYY-MM-DDThh:mm:ss
    #try to convert the provided values a date object, if not return 400 error code
    try:
        target_date = datetime.fromisoformat(event_time)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date/time format. Please use YYYY-MM-DDThh:mm:ss.")
    

    #DEBUG print("target date:", target_date)

    #both from and to timezones should be in the format of UTC[+/-]hh:mm
    from_timezone_match = re.match(r"^UTC([+-])(0\d|1\d|2[0-3]):([0-5]\d)$", from_timezone)
    to_timezone_match = re.match(r"^UTC([+-])(0\d|1\d|2[0-3]):([0-5]\d)$", to_timezone)
    if (from_timezone_match is None) or (to_timezone_match is None):
        raise HTTPException(status_code=400, detail="Invalid timezone format. Please use UTC[+/-]hh:mm.")

    #convert from_timezone string into disparate parts 
    if from_timezone_match.group(1) == "-":
        from_sign = -1
    else:
        from_sign = 1
    from_hours = int(from_timezone_match.group(2))
    from_minutes = int(from_timezone_match.group(3))
    from_tzinfo = timezone(from_sign * timedelta(hours=from_hours, minutes=from_minutes))
    #DEBUG print("from tzinfo:", from_tzinfo)

    #convert to_timezone string into disparate parts
    if to_timezone_match.group(1) == "-":
        to_sign = -1
    else:
        to_sign = 1
    to_hours = int(to_timezone_match.group(2))
    to_minutes = int(to_timezone_match.group(3))
    to_tzinfo = timezone(to_sign * timedelta(hours=to_hours, minutes=to_minutes))
    #DEBUG print("to tzinfo:", to_tzinfo)

    #create from_target_date - a date object with the same info as the target_date, but with a timezone of from_timezone
    from_target_date = target_date.replace(tzinfo=from_tzinfo)
    #DEBUG print("target date w/ FROM tzinfo:", from_target_date)

    #create to_target_date - a date object with the same info as the target_date, but with a timezone of to_timezone
    to_target_date = target_date.replace(tzinfo=to_tzinfo)
    #DEBUG print("target date w/ TO tzinfo:", to_target_date)

    #uses max to avoid going "backwards" in time and having the hours be too large
    time_difference = max((from_target_date - to_target_date), (to_target_date - from_target_date))
    #DEBUG print("diff:", time_difference)

    #shift the to_target_date forward by the difference in the timezones
    converted_time = to_target_date + (from_target_date - to_target_date)
    #DEBUG print("converted time:", converted_time)

    #convert seconds to hours by dividing by 60 (hours -> minutes) and dividng by 60 (minutes -> seconds)
    hours_difference = time_difference.seconds / 60 / 60
    #DEBUG print("hrs diff:", hours_difference)

    return {"converted_time": converted_time.isoformat(), "hours_difference": hours_difference}

#convert March 2, 2026 at 8:00am from PT to ET
#DEBUG print(root("2025-07-21T08:00:00", "UTC-08:00", "UTC-05:00"))