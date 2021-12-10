
"""" Client MQTT: Subscriber """

import paho.mqtt.client as mqtt
import time


#Credentials
TOPIC = "X1111"
BROKER2="xxxx.cloud.shiftr.io"
PORT = 1883
ID = "xxxx"
PASS ="fdZxxxxxxVsAns" 
_API_NAME_ = "mqtt client publisher"

#----------------------Callback functions--------------------------
def on_connect(client,userdata,flags,rc):
    if rc == 0:
        print("[{}]connected to the broker".format(_API_NAME_))
        print("[{}] subcribe to the topic {}".format(_API_NAME_,TOPIC))
        client.subscribe("X1111")
    else:
        print("[{}]Connection Error".format(_API_NAME_))

def on_disconnected(client,userdata,rc):
    if rc !=0:
        print("[{}]disconnected to the broker".format(_API_NAME_))

def on_message(client,userdata,msg):
    print("[{}]you have a new message. {}".format(_API_NAME_,str(msg.payload)))
#-----------------------------------------------------------------

def Main():
    print(_API_NAME_)
    client = mqtt.Client(client_id= "simo-sub", clean_session=False)
    print("conencted: {} port: {}".format(BROKER2,PORT))
    client.on_connect = on_connect
    client.on_message = on_message
    #client.on_disconnect = on_disconnected
    client.username_pw_set(ID,PASS)
    client.connect(host=BROKER2,port=PORT,keepalive=60)
    client.loop_forever()


if __name__ == "__main__":
    Main()
