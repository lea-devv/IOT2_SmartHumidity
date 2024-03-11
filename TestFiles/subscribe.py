import paho.mqtt.subscribe as subscribe
print("subscribe MQTT script running")
def on_message_print(client, userdata, message):  #brug disse argumenter
    print("%s %s" % (message.topic, message.payload)) #her printes dataen
    userdata["message_count"] += 1
    if userdata["message_count"] >= 5: #dette definere hvor lange data beskeder der bliver modtaget, husk at ændre hvis du modtager lange beskeder
        # it's possible to stop the program by disconnecting
        client.disconnect()

subscribe.callback(on_message_print, "paho/test/topic", hostname="4.231.174.166", userdata={"message_count": 0})  #brug paho til at subscribe til bestemt topic, hostname er sensorens ip adresse. Userdata er beskedlængden