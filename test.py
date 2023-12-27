from datetime import datetime, timezone, timedelta

print(datetime.now(tz=timezone(timedelta(hours=5, minutes=30))))


from datetime import datetime

# Provided date and time string
date_string = "2023-12-27T19:00:00+05:30"

# Convert the string to a datetime object
datetime_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")

# Print the datetime object
print(datetime_object)
