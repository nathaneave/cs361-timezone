# CS361 (Group 17) - Small Pool Microservice: Timezone Converter

**What does this microservice do?**

This microservice allows the user to provide a date and time, a timezone to convert from, and a timezone to convert to, and returns the provided date/time in the requested timezone.

**How do I request data from this microservice?**

To request data from this microservice, you will need to make an `HTTP GET request` to the `/timezone_converter` endpoint. You must pass the `event_time` as a string in the form of `YYYY-MM-DDThh:mm:ss`, the `from_timezone` as a string in the form of `UTC[+/-]hh:mm`, and the `to_timezone` as a string in the form of `UTC[+/-]hh:mm` as query parameters.

_Example call:_ `GET http://127.0.0.1:8000/timezone_converter?event_time=2026-03-02T08:00:00&from_timezone=UTC-08:00&to_timezone=UTC-05:00`

**How will I receive data from this microservice?**

The microservice will return a `JSON object`. The object will have two name/value pairs. The name/value pairs will be `converted_time` which is an string that is the time converted to the requested timezone in ISO8601 format and `hours_difference` which is an integer that represents the hours between the two timezones.

_Example response (valid input)_:

Status code: `200`
```yaml
{
“converted_time”: “2026-02-14T10:00:00”,
“hours_difference”: 3
}
```

_Example response (invalid date/time)_:

Status code: `400`
```yaml
{
"detail": "Invalid date/time format. Please use YYYY-MM-DDThh:mm:ss."
}
```

_Example response (invalid timezone)_:

Status code: `400`
```yaml
{
"detail": "Invalid timezone format. Please use UTC[+/-]hh:mm."
}
```

**UML Sequence Diagram**

<img width="585" height="395" alt="image" src="https://github.com/user-attachments/assets/745bb4c4-ac01-45b0-8ef9-daadebaeaeb2" />
