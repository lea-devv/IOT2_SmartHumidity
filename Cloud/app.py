from flask import Flask, render_template
import base64
from io import BytesIO
from matplotlib.figure import Figure
from get_dht11_data import get_stue_data

app = Flask(__name__) 
def stue_temp():
    timestamps, temp, hum = get_stue_data(10)
      # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor("#fff")
    ax.plot(timestamps, temp, c="#f11", marker="o")
    ax.set_xlabel("timestamp")
    ax.set_ylabel("temperature")
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def stue_hum():
    timestamps, temp, hum = get_stue_data(10)
      # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor("#fff")
    ax.plot(timestamps, hum, c="#f11", marker="o")
    ax.set_xlabel("timestamp")
    ax.set_ylabel("humidity")
    ax.plot(timestamps, hum)
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

@app.route('/') 
def home():
    return render_template('index.html')

@app.route('/stue') 
def stue():
    stue_temperature = stue_temp()
    stue_humidity = stue_hum()
    return render_template('stue.html', stue_temperature = stue_temperature, stue_humidity = stue_humidity)
app.run(debug=True)
