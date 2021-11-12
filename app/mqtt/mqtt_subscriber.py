import paho.mqtt.client as mqtt
import time
from Credentials import credentials as  DATA








_API_NAME_ = "mqtt client"

def on_connect(client,userdata,flags,rc):
    if rc == 0:

        print("[{}]connected to the broker".format(_API_NAME_))
        print("[{}] subcribe to the topic {}".format(_API_NAME_,DATA.TOPIC))
        client.subscribe(DATA.TOPIC)
    else:
        print("[{}]Connection Error".format(_API_NAME_))

def on_disconnected(client,userdata,rc):

    if rc !=0:
        print("[{}]disconnected to the broker".format(_API_NAME_))

def on_message(client,userdata,msg):
    print("[{}]you have a new message. {}".format(_API_NAME_,str(msg.payload)))



print("init subscriber")

client = mqtt.Client(client_id= "simo-sub", clean_session=False)


print("conencted: {} port: {}".format(DATA.URL,DATA.PORT))
client.on_connect = on_connect
client.on_message = on_message
#client.on_disconnect = on_disconnected


client.username_pw_set(DATA.ID,DATA.PASS)
client.connect(host=DATA.URL,port=DATA.PORT,keepalive=60)
client.loop_forever()