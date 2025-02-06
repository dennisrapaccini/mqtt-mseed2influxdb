import configparser
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import csv
import os
import numpy as np
from datetime import timedelta
from scipy import signal
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# AT THE MOMENT THIS CODE WORKS ONLY WITH 2 SENSORS

# Calculate the cross-correlation between the two sensor signals to find the samples delay between them
def delay_finder(s1,s2,sr): # s1 is the vector of values
    cross_corr = np.correlate(s1, s2, mode='full')
    fig = plt.figure()
    plt.stem(cross_corr)
    plt.show()
    fig.savefig("cross_corr.png")
    delay = (np.argmax(cross_corr) - (len(s1) - 1))/sr
    return delay

# Calculate the delay using the peaks of the signals
def delay_finder_pk (s1,s2,sr):
    peak1 = np.argmax(s1)
    peak2 = np.argmax(s2)
    delay = (peak2 - peak1)/sr
    return delay

# Connect to InfluxDB 
config_path = "config.ini"
config = configparser.ConfigParser()
config.read(config_path)
load_dotenv()
influx_client = InfluxDBClient(url = os.getenv("URL"), token=os.getenv("TOKEN"), org=os.getenv("ORG"))
query_api = influx_client.query_api()

# Data are stored in timezone UTC+0 (Greenwich Mean Time) so choose start and stop time accordingly
start_time = "2024-05-10T15:25:54.000+02:00"
stop_time = "2024-05-10T15:25:56.000+02:00"

# Define the sensors to query
sensors = ["IU.ANMO.08.BHZ", "IU.ANMO.25.BHZ"]
axis = "z"

# Write and execute Flux queries
queries = [
    f'''from(bucket:"test")
      |> range(start: {start_time}, stop: {stop_time})
      |> filter(fn: (r) => r["_measurement"] == "acceleration")
      |> filter(fn: (r) => r["_field"] == "{axis}")
      |> filter(fn: (r) => r["sensor_id"] == "{sensor_id}")'''  
    for sensor_id in sensors]

csv_result_1 = np.array(query_api.query(queries[0]).to_values(columns=['_measurement', '_field', '_time', '_value']))
csv_result_2 = np.array(query_api.query(queries[1]).to_values(columns=['_measurement', '_field', '_time', '_value']))

min_length = min(len(csv_result_1), len(csv_result_2))

csv_result_1 = csv_result_1[:min_length]
csv_result_2 = csv_result_2[:min_length]

#y1 = [item for sublist in query_api.query(queries[0]).to_values(columns=['_value']) for item in sublist]
#print(y1)

# It could be useful to convert the data to absolute values for evaluating the delay
s1 = ([item for sublist in query_api.query(queries[0]).to_values(columns=['_value']) for item in sublist])
s2 = ([item for sublist in query_api.query(queries[1]).to_values(columns=['_value']) for item in sublist])

# Calculate the delay between the two sensors using the two methods only during a very stong peak
# r = delay_finder(s1,s2, 250)
# r_pk = delay_finder_pk(s1,s2 ,250)
# print("Delay_xcorr: ", r, " s")
# print("Delay_peaks: ", r_pk, " s")


# Delay the second sensor (25) signal by time founded with delay_finder during peaks to align the signals
delay = timedelta(milliseconds = 8)

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


