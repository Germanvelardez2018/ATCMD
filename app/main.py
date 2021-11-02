"""
Author: German Velardez
email: germanvelardez16@gmail.com
date: 29/10/2021

"""
import time
from SIM_AT import SIM_AT
from credentials import credentials as DATA

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


    number = 1234

    while number <= 1250:
        time.sleep(8)
        device.mqtt_publish(DATA.TOPIC,"count: {}".format(number))
        print("count: {}".format(number))
        number +=1
    
    device.mqtt_close()




if __name__ =="__main__":
    print("init program")
    main()