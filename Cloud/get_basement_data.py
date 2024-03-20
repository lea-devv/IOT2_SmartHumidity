import sqlite3
from datetime import datetime
from time import sleep

def get_basement_data(number_of_rows):
   
        query = """SELECT * FROM basement ORDER BY datetime DESC;"""
        datetimes = []
        gas = []
        temperatures = []
        humidities = []
        try:
            conn = sqlite3.connect("database/basement_data.db")
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchmany(number_of_rows)
            for row in reversed(rows):
                 datetimes.append(row[0])
                 gas.append(row[1])
                 temperatures.append(row[3])
                 humidities.append(row[2])
            return datetimes, gas, humidities, temperatures
        except sqlite3.Error as sql_e:
            print(f"sqlite error occured: {sql_e}")
            conn.rollback()
        except Exception as e:
            print(f"Error occured: {e}")
        finally:
            conn.close()