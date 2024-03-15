import sqlite3
from random import randint
from datetime import datetime
import paho.mqtt.subscribe as subscribe
import json



def create_table():
    query = """CREATE TABLE IF NOT EXISTS stue (humidity REAL NOT NULL, datetime TEXT NOT NULL, temperature REAL NOT NULL);"""
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

create_table()   
     
def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))
    query = """INSERT INTO stue(datetime, temperature, humidity) VALUES(?, ?, ?)"""
    now = datetime.now()
    now = now.strftime("%d/%m/%y %H:%M:%S")
    print(type(json.loads(message.payload.decode())))
    dht11_data = json.loads(message.payload.decode())
    data = (now, dht11_data['temperature'], dht11_data['humidity'])
   
   
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
subscribe.callback(on_message_print, "test", hostname="4.231.174.166", userdata={"message_count": 0})
