""""Client MQTT: Publisher """

import paho.mqtt.client as mqtt
import time

# Credentials
TOPIC = "Xxxxx"
BROKER2="xxxxx.cloud.shiftr.io"
PASS= "fdZxxxxxxxAns"
ID ="xxxx"
PORT = 1883
_API_NAME_ = "mqtt client subscriber"

#----------------------Callback functions--------------------------
def on_connect(client,userdata,flags,rc):
    if rc == 0:

        print("[{}]connected to the broker".format(_API_NAME_))
        print("[{}] subcribe to the topic {}".format(_API_NAME_,TOPIC))
        client.subscribe(TOPIC)
    else:
        print("[{}]Connect Error".format(_API_NAME_))

def on_disconnected(cleint,userdata,rc):

    if rc !=0:
        print("[{}]disconnected to the broker".format(_API_NAME_))

def on_message(client,userdata,msg):
    print("[{}]you have a new message. {}".format_API_NAME_,str(msg.payload.decode("utf-8")))

#--------------------------------------------------------------

def Main():
    print(_API_NAME_)
    client = mqtt.Client(client_id= "simo-pub", clean_session=False)
    print("conented: {} port: {}".format(BROKER2,PORT))
    client.on_connect = on_connect
    #client.on_message = on_message
    client.on_disconnect = on_disconnected
    client.username_pw_set(ID,PASS)
    client.connect(host=BROKER2,port=PORT,keepalive= 60)

    counter = 0
    while True:
        print("TOPIC :{}=>{}".format(TOPIC,counter))
        client.publish(TOPIC,"TOPIC: {} =>  {}".format(TOPIC,counter))
        counter += 1
        time.sleep(10)


if __name__ == "__main__":
    Main()
