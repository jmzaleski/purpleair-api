# fetch indoor data from CC sensor
from purpleair import PurpleAir
from datetime import datetime, time, date
from zoneinfo import ZoneInfo  # Python 3.9+
from time import sleep
import sys

# See https://api.purpleair.com/
# api throttling kicks in unless we  between requests
DELAY = 1
with open('API_KEY.txt') as f:
    MATZ_KEY = f.read()
    print("MATZ_KEY:", MATZ_KEY)

OUR_SENSOR_ID = '106786' #CC indoor sensor

# confluence climbing at 51.30610, -116.97414
LATITUDE = 51.3061  # CC
LONGITUDE = -116.97414 #CC

LOCATION_TYPE=1 #inside maybe need to adjust the DATA_FIELDS for an inside sensor. pm2.5_cf_1
DATA_FIELDS = ('temperature','pm2.5_cf_1') #this for indoor sensor
#DATA_FIELDS = ('temperature','pm2.5_atm') #for outdoor sensor

p = PurpleAir(MATZ_KEY.strip())

# the days we want the data for..
start_date = date(2024,11,17)
end_date = start_date # samedate(2024,11,17)

print("start date:", start_date)
print("end date:", end_date)
# just get all the data for that day, from 0:00 to 23:59 Mountain time
time_zone = ZoneInfo('Canada/Mountain')
start_time = datetime.combine(start_date, time(0, 0).replace(tzinfo=time_zone))
end_time = datetime.combine(end_date, time(23, 59, 59).replace(tzinfo=time_zone))

print("Mountain Time start,end datetimes:",  start_time, end_time)
print("data fields:", DATA_FIELDS)

history_csv = p.get_sensor_history_csv(
        sensor_index=OUR_SENSOR_ID,
        fields=DATA_FIELDS,
        start_timestamp=start_time,
        end_timestamp=end_time
    )
#retuns a string containing the csv format data
print("history_csv:", history_csv)
with open('sensor_data.csv', 'w') as file:
        file.write(history_csv)

