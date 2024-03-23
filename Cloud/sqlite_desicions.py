import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from DMI import dmi_vejr
from datetime import datetime
from time import sleep
import sqlite3
import threading

latitude = 55.69167045976886
longitude = 12.554718594176451
api_key = 'fafd94e1-e6ce-44d3-b5c9-13fd9f92ab6a'

dmi = dmi_vejr(latitude, longitude, api_key)

basement_hum = None
basement_gas = None
basement_temp = None
console_hum = None
console_temp = None

##############################################################
#Defines the function to create and get data from the basement database
def get_basement_data(number_of_rows):
    create_query = """CREATE TABLE IF NOT EXISTS basement (datetime TEXT NOT NULL, humidity REAL NOT NULL, temperature REAL NOT NULL, gas REAL NOT NULL);"""
    select_query = """SELECT * FROM basement ORDER BY datetime DESC;"""
    datetimes = []
    humidities = []
    temperatures = []
    gas = []
    try:
        conn = sqlite3.connect("C:\GitHub\IOT2_SmartHumidity\Cloud\database/basement_data.db")
        cur = conn.cursor()
        cur.execute(create_query)
        cur.execute(select_query)
        rows = cur.fetchmany(number_of_rows)
        for row in reversed(rows):
            datetimes.append(row[0])
            humidities.append(row[1])
            temperatures.append(row[2])
            gas.append(row[3])
        return datetimes, humidities, temperatures, gas
    except sqlite3.Error as sql_e:
        print(f"sqlite error occured: {sql_e}")
        conn.rollback()
    except Exception as e:
        print(f"Error occured: {e}")
    finally:
        conn.close()

##############################################################
#Defines the function to create and get data from the console database
def get_console_data(number_of_rows):
        create_query = """CREATE TABLE IF NOT EXISTS console (datetime TEXT NOT NULL, humidity REAL NOT NULL, temperature REAL NOT NULL);"""
        select_query = """SELECT * FROM console ORDER BY datetime DESC;"""
        datetimes = []
        temperatures = []
        humidities = []
        try:
            conn = sqlite3.connect("C:\GitHub\IOT2_SmartHumidity\Cloud\database/sensor_data.db")
            cur = conn.cursor()
            cur.execute(create_query)
            cur.execute(select_query)
            rows = cur.fetchmany(number_of_rows)
            for row in reversed(rows):
                 datetimes.append(row[0])
                 temperatures.append(row[2])
                 humidities.append(row[1])
            return datetimes, temperatures, humidities
        except sqlite3.Error as sql_e:
            print(f"sqlite error occured: {sql_e}")
            conn.rollback()
        except Exception as e:
            print(f"Error occured: {e}")
        finally:
            conn.close()
##############################################################
#Makes sure the tabels in the database is created
get_basement_data(0)
get_console_data(0)

##############################################################
#Callback functions for mqtt
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("basement_hum")
    client.subscribe("basement_temp")
    client.subscribe("basement_gas")
    client.subscribe("console_hum")
    client.subscribe("console_temp")

def on_message(client, userdata, msg):
    global basement_hum, basement_gas, basement_temp, console_hum, console_temp
    #print(msg.topic+" "+str(msg.payload))
    if msg.topic == "basement_hum":
        basement_hum = str(msg.payload.decode())

    if msg.topic == "basement_temp":
        basement_temp = str(msg.payload.decode())

    if msg.topic == "basement_gas":
        basement_gas = str(msg.payload.decode())
    
    if msg.topic == "console_hum":
        console_hum = str(msg.payload.decode())
        desicions()

    if msg.topic == "console_temp":
        console_temp = str(msg.payload.decode())

    
##############################################################
#Takes the data recieved from mqtt and enters it into the databases
def log_data():
    global basement_hum, basement_gas, basement_temp, console_hum, console_temp
    while True:
        now = datetime.now()
        now = now.strftime("%d/%m/%y %H:%M:%S")
        try:
            conn = sqlite3.connect("C:\GitHub\IOT2_SmartHumidity\Cloud\database/sensor_data.db")
            cur = conn.cursor()
            console_query = """INSERT INTO console(datetime, humidity, temperature) VALUES(?, ?, ?)"""
            if console_temp and console_hum is not None:
                console_data = (now, console_hum, console_temp,)
                cur.execute(console_query, console_data)
                conn.commit()
        except sqlite3.Error as sql_e:
            print(f"sqlite error occured: {sql_e}")
            conn.rollback()
        except Exception as e:
            print(f"Error occured: {e}")
        finally:
            conn.close()

        try:
            conn = sqlite3.connect("C:\GitHub\IOT2_SmartHumidity\Cloud\database/basement_data.db")
            cur = conn.cursor()
            basement_query = """INSERT INTO basement(datetime, humidity, temperature, gas) VALUES(?, ?, ?, ?)"""
            if basement_gas is not None and basement_hum is not None and basement_temp is not None:
                basement_data = (now, basement_hum, basement_temp, basement_gas)
                cur.execute(basement_query, basement_data)
                conn.commit()
        except sqlite3.Error as sql_e:
            print(f"sqlite error occured: {sql_e}")
            conn.rollback()
        except Exception as e:
            print(f"Error occured: {e}")
        finally:
            conn.close()
        sleep(1)
    
##############################################################
#Decideds if the window should open and if the furnace should turn off
def desicions():
    global console_hum
    wind_speed, total_precipitation, forecast_datetime = dmi.get_rain_wind()
    if total_precipitation <= 0.5:
        if console_hum is not None:
            console_hum = float(console_hum)
            print(console_hum)
            if console_hum > 60.0:
                print("Open")
                publish.single("window_command", "open" , hostname="4.231.174.166")
                publish.single("furnace_command", "on" , hostname="4.231.174.166")
            elif console_hum < 50.0:
                print("Close")
                publish.single("window_command", "close" , hostname="4.231.174.166")
                publish.single("furnace_command", "off" , hostname="4.231.174.166")
    else:
        publish.single("window_command", "close" , hostname="4.231.174.166")
        publish.single("furnace_command", "off" , hostname="4.231.174.166")

##############################################################
#Starts a non-blocking loop for mqtt and starts a thread for logging the data
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("4.231.174.166", 1883, 60)

mqttc.loop_start()

log_thread = threading.Thread(target=log_data, daemon=True)

log_thread.start()



