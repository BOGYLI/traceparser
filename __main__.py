import requests
import xml.etree.ElementTree as ET
import yaml
import time
from influxdb_client import InfluxDBClient, Point, WriteOptions

# load config
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

feed_url = config['feed_url']
feed_password = config['feed_password']
influxdb_token = config['influxdb_token']
influxdb_org = config['influxdb_org']
influxdb_bucket = config['influxdb_bucket']
influxdb_url = config['influxdb_url']

# request data from feed
response = requests.get(f"{feed_url}?feedPassword={feed_password}")
response.raise_for_status()  # Fehlermeldung bei Anfragenfehler

# parse XML data
root = ET.fromstring(response.content)

#  create InfluxDB client
client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
write_api = client.write_api(write_options=WriteOptions(batch_size=1))

while True:
    # parse XML data and write to InfluxDB
    for message in root.findall('.//message'):
        measuretime = message.find('dateTime').text
        latitude = message.find('latitude').text
        longitude = message.find('longitude').text
        altitude = message.find('altitude').text

        point = Point("spot_gps") \
            .field("latitude", float(latitude)) \
            .field("longitude", float(longitude)) \
            .field("altitude", float(altitude)) \
            .time(measuretime)

        try:
            write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=point)
        except Exception as e:
            print("Error writing data to InfluxDB: ", e)
            continue

    print("Written data to InfluxDB successfully.")
    
    time.sleep(60)
