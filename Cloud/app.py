from flask import Flask, render_template, request
import paho.mqtt.publish as publish
import graphs
import json

app = Flask(__name__) 

@app.route('/') 
def home():
    return render_template('index.html')

@app.route('/bathroom') 
def bathroom():
    bathroom_temperature = graphs.bathroom_temp()
    bathroom_humidity = graphs.bathroom_hum()
    return render_template('bathroom.html', bathroom_temperature = bathroom_temperature, bathroom_humidity = bathroom_humidity)

@app.route('/basement') 
def basement():
    basement_temperature = graphs.basement_temp()
    basement_humidity = graphs.basement_hum()
    basement_gas = graphs.basement_gas()
    return render_template('basement.html', basement_temperature = basement_temperature, basement_humidity = basement_humidity, basement_gas = basement_gas)

@app.route('/window_timer', methods=['GET', 'POST'])
def change_timer():
    timer = None
    if request.method == 'POST':
        timer = request.form['timer']
        payload = timer
        print(payload)
        publish.single("autoclose_variable", payload, hostname="4.231.174.166")
    return render_template('window_timer.html', timer=timer)
  
app.run(debug=True)

