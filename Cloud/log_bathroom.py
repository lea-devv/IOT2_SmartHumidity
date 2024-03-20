import sqlite3
from datetime import datetime
import paho.mqtt.subscribe as subscribe
import json
from time import sleep




def create_table():
    query = """CREATE TABLE IF NOT EXISTS bathroom (humidity REAL NOT NULL, datetime TEXT NOT NULL, temperature REAL NOT NULL);"""
    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except sqlite3.Error as sql_e:
        print(f"sqlite error occured: {sql_e}")
    except Exception as e:
        print(f"Error occured: {e}")
    finally:
        conn.close()

#create_table()     
def console_data():
    humidity = subscribe.simple("console_hum", hostname="4.231.174.166")
    temperature = subscribe.simple("console_temp", hostname="4.231.174.166")
    bathroom_hum = humidity.payload.decode()
    bathroom_temp = temperature.payload.decode()
    print(bathroom_temp, bathroom_hum)
    now = datetime.now()
    now = now.strftime("%d/%m/%y %H:%M:%S")  
    data = (now, bathroom_temp, bathroom_hum)
    query = """INSERT INTO bathroom(datetime, temperature, humidity) VALUES(?, ?, ?)"""

   
   
    try:
        conn = sqlite3.connect("database/sensor_data.db")
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
    except sqlite3.Error as sql_e:
        print(f"sqlite error occured: {sql_e}")
        conn.rollback()
    except Exception as e:
        print(f"Error occured: {e}")
    finally:
        conn.close()
print("script is running")
while True: 
    console_data()
    sleep(1)
    

