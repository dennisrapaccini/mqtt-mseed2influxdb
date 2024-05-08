import configparser
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import csv
import numpy as np
from datetime import timedelta
from scipy import signal

# AT THE MOMENT THIS CODE WORKS ONLY WITH 2 SENSORS

# Calculate the cross-correlation between the two sensor signals to find the delay between them
def delay_finder(y1, y2, sr):
    y1 = [item for sublist in query_api.query(y1).to_values(columns=['_value']) for item in sublist]
    y2 = [item for sublist in query_api.query(y2).to_values(columns=['_value']) for item in sublist]
    n = len(y1)
    corr = signal.correlate(y2, y1, mode='same') / np.sqrt(signal.correlate(y1, y1, mode='same')[int(n/2)] * signal.correlate(y2, y2, mode='same')[int(n/2)])
    delay_arr = np.linspace(-0.5*n/sr, 0.5*n/sr, n)
    delay = delay_arr[np.argmax(corr)]
    print('The delay between s2 and s1 is:', delay, 's')
    return delay  

# Connect to InfluxDB 
config_path = "config.ini"
config = configparser.ConfigParser()
config.read(config_path)
influx_client = InfluxDBClient.from_config_file(config_path)
query_api = influx_client.query_api()

# Data are stored in timezone UTC+0 (Greenwich Mean Time) so choose start and stop time accordingly
start_time = "2024-05-08T08:05:00.00Z"
stop_time = "2024-05-08T08:09:00.000Z"

# Define the sensors to query
sensors = ["IU.ANMO.08.BHZ", "IU.ANMO.25.BHZ"]


# Write and execute Flux queries
queries = [
    f'''from(bucket:"{config['influx2']['bucket']}")
      |> range(start: 2024-05-08T08:05:00.00Z, stop: 2024-05-08T08:09:00.000Z)
      |> filter(fn: (r) => r["_measurement"] == "acceleration")
      |> filter(fn: (r) => r["sensor_id"] == "{sensor_id}")'''  
    for sensor_id in sensors]

csv_result_1 = np.array(query_api.query(queries[0]).to_values(columns=['_measurement', '_field', '_time', '_value']))
csv_result_2 = np.array(query_api.query(queries[1]).to_values(columns=['_measurement', '_field', '_time', '_value']))

min_length = min(len(csv_result_1), len(csv_result_2))

csv_result_1 = csv_result_1[:min_length]
csv_result_2 = csv_result_2[:min_length]

#delay_finder(csv_result_1, csv_result_1, 250)

# Delay the second sensor (25) signal by 2 milliseconds (or the time calculated by delay_finder()) to align the signals
delay = timedelta(milliseconds = 2)

csv_result_2[:,2] = [dt + delay for dt in csv_result_2[:,2]]

# Merge the two sensor data into a single CSV file
csv_merged = np.concatenate((csv_result_1, csv_result_2[:, [3]]), axis=1)


# with open('query1.csv', 'w', newline='') as file:
#      writer = csv.writer(file)
#      writer.writerow(['_measurement', '_field', '_time', '_value'])
#      writer.writerows(csv_result_1)
# with open('query2.csv', 'w', newline='') as file:
#      writer = csv.writer(file)
#      writer.writerow(['_measurement', '_field', '_time', '_value'])
#      writer.writerows(csv_result_2)

# Save the merged data to a CSV file
with open('src/query.csv', 'w', newline='') as file:
     writer = csv.writer(file)
     writer.writerow(['_measurement', '_field', '_time', '_value_IU.ANMO.08.BHZ','_value_IU.ANMO.25.BHZ'])
     writer.writerows(csv_merged)
     print("query.csv created successfully")


