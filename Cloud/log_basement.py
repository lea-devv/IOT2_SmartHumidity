import sqlite3
from datetime import datetime
import paho.mqtt.subscribe as subscribe
import json
from time import sleep




def create_table():
    query = """CREATE TABLE IF NOT EXISTS basement (humidity REAL NOT NULL, datetime TEXT NOT NULL, temperature REAL NOT NULL);"""
    try:
        conn = sqlite3.connect("database/basement_data.db")
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except sqlite3.Error as sql_e:
        print(f"sqlite error occured: {sql_e}")
    except Exception as e:
        print(f"Error occured: {e}")
    finally:
        conn.close()

create_table()     
def basement_data():
    humidity = subscribe.simple("basement_hum", hostname="4.231.174.166")
    temperature = subscribe.simple("basement_temp", hostname="4.231.174.166")
    gas = subscribe.simple("basement_gas", hostname="4.231.174.166")
    basement_hum = humidity.payload.decode()
    basement_temp = temperature.payload.decode()
    basement_gas = gas.payload.decode()
    print(basement_temp, basement_hum, basement_gas)
    now = datetime.now()
    now = now.strftime("%d/%m/%y %H:%M:%S")  
    data = (now, basement_temp, basement_hum, basement_gas)
    query = """INSERT INTO basement(datetime, gas, humidity, temperature) VALUES(?, ?, ?)"""

   
   
    try:
        conn = sqlite3.connect("database/basement_data.db")
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
    

