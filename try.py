from purpleair import PurpleAir
from datetime import datetime, time, date
from zoneinfo import ZoneInfo  # Python 3.9+

MATZ_KEY = '9EC43FD3-93E0-11EF-A261-42010A80000F'
OUR_SENSOR_ID = '100155'

p = PurpleAir(MATZ_KEY)

# the day we want the data for..
start_date = date(2024,10,24)
#last day we want data for..
end_date = date(2024,10,25)
print("start date:", start_date)
print("end date:", end_date)
# just get all the data for that day, from 0:00 to 23:59 Mountain time
time_zone = ZoneInfo('Canada/Mountain')
start_time = datetime.combine(start_date, time(0, 0).replace(tzinfo=time_zone))
end_time = datetime.combine(end_date, time(23, 59, 59).replace(tzinfo=time_zone))
data_fields = ('temperature','pm2.5_atm')

print("Mountain Time start,end datetimes:",  start_time, end_time)
print("data fields:", data_fields)

history_csv = p.get_sensor_history_csv(
    sensor_index=OUR_SENSOR_ID,
    fields=data_fields,
    start_timestamp=start_time,
    end_timestamp=end_time
)
#retuns a string containing the csv format data
print("history_csv:", history_csv)
with open('sensor_data.csv', 'w') as file:
    file.write(history_csv)
import sys
sys.exit()

################# junk here on down #########################

history = p.get_sensor_history(
    sensor_index=OUR_SENSOR_ID,
    fields=data_fields,
    start_timestamp=start_time,
    end_timestamp=end_time
)
sorted_data = sorted(history["data"], key=lambda x: x[0])
print("sorted_data:", sorted_data)

#print("today:", history)
print("result.time_stamp:", history["time_stamp"])
print("result.sensor_index:", history["sensor_index"])
print("result.start_timestamp:", history["start_timestamp"])
print("result.end_timestamp:", history["end_timestamp"])
print("result.average:", history["average"])
print("result.fields:", history["fields"])
#print("result.data:", history["data"])
print("date","time",history["fields"][1])
for timestamp, datum in sorted_data:
    #print(datetime.fromtimestamp(timestamp), datum)
    print(date.fromtimestamp(timestamp), datetime.fromtimestamp(timestamp).time(), datum)
