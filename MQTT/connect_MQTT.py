import paho.mqtt.client as mqtt
broker = "158.180.44.197"
port = 1883
topic = "at/house/bulb1"
payload = "on"

# create function for callback
def on_publish(client, userdata, flags, reasonCode, properties):
    print("data published \n")

# create client object
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.username_pw_set("bobm", "letmein")              

# assign function to callback
mqttc.on_publish = on_publish                          

# establish connection
mqttc.connect(broker,port)                                 

# publish
return_code = mqttc.publish(topic, payload)

mqttc.disconnect()