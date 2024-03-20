from flask import Flask, render_template, request
import base64
from io import BytesIO
from matplotlib.figure import Figure
from get_console_data import get_bathroom_data
from get_basement_data import get_basement_data
import paho.mqtt.publish as publish
import json
app = Flask(__name__) 
def bathroom_temp():
    timestamps, temperature, humidity = get_bathroom_data(10)
      # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor("#fff")
    ax.plot(timestamps, temperature, c="#f11", marker="o")
    ax.set_xlabel("timestamp")
    ax.set_ylabel("temperature")
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def bathroom_hum():
    timestamps, temperature, humidity = get_bathroom_data(10)
      # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor("#fff")
    ax.plot(timestamps, humidity, c="#f11", marker="o")
    ax.set_xlabel("timestamp")
    ax.set_ylabel("humidity")
    ax.plot(timestamps, humidity)
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data
def basement_temp():
    timestamps, gas, humidity, temperature = get_basement_data(10)
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor("#fff")
    ax.plot(timestamps, temperature, c="#f11", marker="o")
    ax.set_xlabel("timestamp")
    ax.set_ylabel("temperature")
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def basement_gas():
    timestamps, gas, humidity, temperature = get_basement_data(10)
      # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor("#fff")
    ax.plot(timestamps, gas, c="#f11", marker="o")
    ax.set_xlabel("timestamp")
    ax.set_ylabel("gas")
    ax.plot(timestamps, gas)
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def basement_hum():
    timestamps, gas, humidity, temperature = get_basement_data(10)
      # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
    ax.tick_params(axis='x', which='both', rotation=30)
    ax.set_facecolor("#fff")
    ax.plot(timestamps, humidity, c="#f11", marker="o")
    ax.set_xlabel("timestamp")
    ax.set_ylabel("humidity")
    ax.plot(timestamps, humidity)
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

timer = "Initial Value"
@app.route('/window_timer', methods=['GET', 'POST'])
def change_timer():
    global timer
    if request.method == 'POST':
        # Update the timer value if the request method is POST
        timer = request.form['timer']
        payload = timer
        print(payload)
        publish.single("autoclose_variable", payload, hostname="4.231.174.166")
    return render_template('window_timer.html', timer=timer)
  


@app.route('/') 
def home():
    return render_template('index.html')

@app.route('/bathroom') 
def bathroom():
    bathroom_temperature = bathroom_temp()
    bathroom_humidity = bathroom_hum()
    return render_template('bathroom.html', bathroom_temperature = bathroom_temperature, bathroom_humidity = bathroom_humidity)
app.run(debug=True)

@app.route('/basement') 
def basement():
    basement_temperature = basement_temp()
    basement_humidity = basement_hum()
    basement_gass = basement_gas()
    return render_template('basement.html', basement_temperature = basement_temperature, basement_humidity = basement_humidity, basement_gas = basement_gass)
app.run(debug=True)

def timer_value():
  while True:
    global timer
    timer_value = timer
    payload = timer_value
    publish.single("autoclose_variable", json.dumps(payload) , hostname="4.231.174.166")
    print(payload)

