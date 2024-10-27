# purpleair-api
fool around with various APIs used to retrieve purpleair historical data
https://github.com/csm10495/purpleair
https://api.purpleair.com/#api-welcome

currently code hardcodes a date and fetches the data for that whole day, 0:00 to 23:59 Mountain time. The returned CSV string is written into the file sensor_data.csv.

FYI, the timestamps in the returned CSV data are in unix epoch time format and refer to UTC.
purpleair-log.xls shows how to convert the timestamps to excel time and chart.  

works in google sheets too: https://docs.google.com/spreadsheets/d/1_daZIKzCiptYk0-mmFv5jgxVFiODE0h312t-qh_Ipgk/edit?usp=sharing