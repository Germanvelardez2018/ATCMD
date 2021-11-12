"""
Author: German Velardez
email: germanvelardez16@gmail.com
date: 29/10/2021

"""
import time
from SIM_AT import SIM_AT
from credentials import Credentials as DATA  # REMENBER CREATE your own credential.py

def main():

    print ("Class SIM_AT (sim7000g")
    device = SIM_AT("SIM 7000")
    device.set_echo(False)


    s = device.is_SIM_ready()

    while s ==False:
        s = device.is_SIM_ready()
        print("waiting...")

   
  
    print("PHONE OPERATOR READY")
    signal_level = device.get_signal()
   
    if signal_level == 0 or signal_level >=40.0:  #when deade phone signal return 99.99
        print("WITHOUT SIGNAL CELLPHONE")
    else:
        print("CELLPONE OPERATOR READY")
        print("Send a message")
       # device.send_sms(xxxxxxx,"this a message  from SIM7000G")

    

  
    print("MQTT TEST")
    device.set_error_coding(1)
    device.mqtt_init(DATA.URL,DATA.ID,DATA.PASS)
    device.mqtt_subscribe(DATA.TOPIC)


    number = 0
    device.set_gnss(1)
    time.sleep(30)
    while number <= 10:
       time.sleep(30)
       data =device.get_position()
       print("send data: {}".format(data))
       device.mqtt_publish(DATA.TOPIC,"GNSS:{}".format(data))
       number += 1
       
    print("fin")
    device.set_gnss(0)
    device.mqtt_close()



if __name__ =="__main__":
    print("init program")
    main()