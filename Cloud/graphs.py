from matplotlib.figure import Figure
from sqlite_desicions import get_basement_data, get_console_data
from datetime import datetime
from io import BytesIO
import matplotlib.ticker as ticker
import base64


###############################################################
#Bathroom temperature graph
def bathroom_temp():
    timestamps, temperature, humidity = get_console_data(10)
    formatted_timestamps = [datetime.strptime(ts, "%d/%m/%y %H:%M:%S").strftime("%H:%M:%S") for ts in timestamps]
    fig = Figure()
    fig.subplots_adjust(bottom=0.3)
    ax = fig.subplots()
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor("#fff")
    ax.plot(formatted_timestamps, humidity)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10, prune='both'))
    ax.set_title('Humidity')
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Percent")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

###############################################################
#Bathroom temperature graph
def bathroom_hum():
    timestamps, temperature, humidity = get_console_data(10)
    formatted_timestamps = [datetime.strptime(ts, "%d/%m/%y %H:%M:%S").strftime("%H:%M:%S") for ts in timestamps]
    fig = Figure()
    fig.subplots_adjust(bottom=0.3)
    ax = fig.subplots()
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor("#fff")
    ax.plot(formatted_timestamps, temperature)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10, prune='both'))
    ax.set_title('Temperature')
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Celcius")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

###############################################################
#Basement temperature graph
def basement_temp():
    timestamps, humidity, temperature, gas = get_basement_data(5000)
    formatted_timestamps = [datetime.strptime(ts, "%d/%m/%y %H:%M:%S").strftime("%H:%M:%S") for ts in timestamps]
    fig = Figure()
    fig.subplots_adjust(bottom=0.3)
    ax = fig.subplots()
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor("#fff")
    ax.plot(formatted_timestamps, temperature)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10, prune='both'))
    ax.set_title('Temperature')
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Celcius")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

###############################################################
#Basement gas graph
def basement_gas():
    timestamps, humidity, temperature, gas = get_basement_data(5000)
    formatted_timestamps = [datetime.strptime(ts, "%d/%m/%y %H:%M:%S").strftime("%H:%M:%S") for ts in timestamps]
    fig = Figure()
    fig.subplots_adjust(bottom=0.3)
    ax = fig.subplots()
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor("#fff")
    ax.plot(formatted_timestamps, gas)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10, prune='both'))
    ax.set_title('Gas')
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Units")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

###############################################################
#Basement humidity graph
def basement_hum():
    timestamps, humidity, temperature, gas = get_basement_data(5000)
    formatted_timestamps = [datetime.strptime(ts, "%d/%m/%y %H:%M:%S").strftime("%H:%M:%S") for ts in timestamps]
    fig = Figure()
    fig.subplots_adjust(bottom=0.3)
    ax = fig.subplots()
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor("#fff")
    ax.plot(formatted_timestamps, humidity)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=10, prune='both'))
    ax.set_title('Humidity')
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Percent")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data