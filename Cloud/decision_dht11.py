import paho.mqtt.publish as publish
import json
from time import sleep
import sqlite3
from datetime import datetime


def check_humidity(number_of_rows):
        query = """SELECT humidity FROM stue ORDER BY datetime DESC;"""
        humidities = []
        try:
            conn = sqlite3.connect("database/sensor_data.db")
            cur = conn.cursor()
            cur.execute(query)
            humidities = cur.fetchone()
            humidity = humidities[0]
            return humidity
        except sqlite3.Error as sql_e:
            print(f"sqlite error occured: {sql_e}")
            conn.rollback()
        except Exception as e:
            print(f"Error occured: {e}")
        finally:
            conn.close()
        


while True:
    humidity = check_humidity(1)
    print(humidity)
    if humidity is not None and humidity < 32.0:
        payload = "open"
        publish.single("window_command", json.dumps(payload) , hostname="4.231.174.166")
    print("scritp is running")
    sleep(1)