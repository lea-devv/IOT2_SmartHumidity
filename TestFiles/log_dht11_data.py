import sqlite3
from random import randint
from datetime import datetime
from time import sleep

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

def log_stue_dht11():
    while True:
        query = """INSERT INTO stue(datetime, temperature, humidity) VALUES(?, ?, ?)"""
        now = datetime.now()
        now = now.strftime("%d/%m/%y %H:%M:%S")
        data = (now, randint(0, 30), randint(0, 100))
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
        sleep(1)


create_table()        
log_stue_dht11()