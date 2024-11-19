from purpleair import PurpleAir
from datetime import datetime, time, date
from zoneinfo import ZoneInfo  # Python 3.9+
from time import sleep

# See https://api.purpleair.com/
# api throttling kicks in unless we  between requests
DELAY = 1
with open('API_KEY.txt') as f:
    MATZ_KEY = f.read()
    print("MATZ_KEY:", MATZ_KEY)

#OUR_SENSOR_ID = '106786' #CC indoor sensor
#LATITUDE = 51.3061  # CC
#LONGITUDE = -116.97414 #CC

OUR_SENSOR_ID = '100155'
LATITUDE = 51.29780  # golden 7th and 7th ish
LONGITUDE = -116.97246  
DELTA = 0.2  # degrees.. delta of .005 finds just our house. .009 finds a few more
LOCATION_TYPE=0 #outside
DATA_FIELDS = ('temperature','pm2.5_atm') #for outdoor sensor
#LOCATION_TYPE=1 #inside maybe need to adjust the DATA_FIELDS for an inside sensor. pm2.5_cf_1
#DATA_FIELDS = ('temperature','pm2.5_cf_1') #this for indoor sensor

p = PurpleAir(MATZ_KEY.strip())
# Add these lines after creating PurpleAir instance

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
print("data fields:", DATA_FIELDS)

if False:
    #debug code that got history_csv working
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




# query the sensors in the area +- delta degrees from the point
sensors = p.get_sensors_data(    
    max_age=0,
    fields=('name','temperature','pm2.5_atm'),
    location_type=LOCATION_TYPE,
    nwlat=LATITUDE+DELTA,
    nwlng=LONGITUDE-DELTA,
    selat=LATITUDE-DELTA,
    selng=LONGITUDE+DELTA
)
local_sensors_name = {}

# save a map from sensor id to name
for x in sensors["data"]:
    local_sensors_name[x[0]] = (x[1])

# print the map from sensor id to name
for sid in local_sensors_name.keys():
    print(sid,local_sensors_name[sid])

# get the history for each sensor and build a map from timestamp to pmi25 directly
timestamp_to_pmi_map_for_sensor = {}
for sid in local_sensors_name.keys():
    print("sleep " + str(DELAY) + " before getting history for sensor:", sid)
    sleep(DELAY)
    s_history = p.get_sensor_history(sensor_index=sid,fields=DATA_FIELDS,start_timestamp=start_time,end_timestamp=end_time)
    # Create map of timestamp -> pmi2.5 for this sensor
    pmi_map_for_sensor = {}
    if not s_history["data"]:
        print("no data for sensor" + str(sid))
        continue
    for time_data in s_history["data"]:
        timestamp, temp, pmi25 = time_data
        pmi_map_for_sensor[timestamp] = pmi25
    print("sensor" + str(sid), "timestamp_to_pmi_map_for_sensor", pmi_map_for_sensor)
    timestamp_to_pmi_map_for_sensor[sid] = pmi_map_for_sensor

# print the timestamp/pmi25 data for each sensor
# Get all unique timestamps across all sensors, sorted chronologically
merged_timestamps = sorted(
    set(  # using set() to ensure uniqueness
        timestamp 
        for sensor_data in timestamp_to_pmi_map_for_sensor.values() 
        for timestamp in sensor_data.keys()
    )
)
#print("merged_timestamps:", merged_timestamps)
import sys

map_sid_to_time_data = {} # for each sensor maintain a map from time to pmi25 data
for sid in timestamp_to_pmi_map_for_sensor.keys():
    pmi25_data_for_time = {}
    print("timestamp/pmi25 data for sensor" + str(sid), "{")
    for timestamp in merged_timestamps:
        if timestamp not in timestamp_to_pmi_map_for_sensor[sid]:
            print("NO", timestamp, "in timestamp_to_pmi_map_for_sensor["+str(sid)+"]")
            print("timestamp_to_pmi_map_for_sensor[sid]:",timestamp_to_pmi_map_for_sensor[sid])
            sys.exit()
            continue
        else:
            print(timestamp,timestamp_to_pmi_map_for_sensor[sid][timestamp])
    print("} end time data for sensor" + str(sid))

#no print out rows by timestamp column of pmi25 data for each sensor
print("start data for all sensors {}")
line = "timestamp"
for sid in timestamp_to_pmi_map_for_sensor.keys():
    line = line + ", " + str(sid)
print(line)

for timestamp in merged_timestamps:
    line=str(timestamp)
    for sid in timestamp_to_pmi_map_for_sensor.keys():
        line = line + ", " + str(timestamp_to_pmi_map_for_sensor[sid][timestamp])
    print(line)
print("} end data for all sensors")

sys.exit()



# Print sensor information
for sensor in sensors:
    print(f"Sensor ID: {sensor['sensor_index']}")
    print(f"Name: {sensor['name']}")
    print(f"Distance: {sensor['distance']:0.2f} km")
    print("---")

################# junk here on down #########################

history = p.get_sensor_history(
    sensor_index=OUR_SENSOR_ID,
    fields=DATA_FIELDS,
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
