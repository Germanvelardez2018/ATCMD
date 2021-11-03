"""
Author: German Velardez
Interface for SIM devices

"""

import time
from Serial_AT import Serial_AT
from SIM7000_CMDS import *

from credentials import credentials as DATA    #CLASS WITH DATA NOT PUBLIC
import json


MIN_SIGNAL = 20

MAX_SIGNAL = 33 # WHEN THE DEVICE NOT SIGNAL,RETURN 99.99

DATA_FIELD_NMEA = [         "status"
                          , "fix status"
                          , "date and time"
                          , "Latitude"
                          , "Longitud"
                          , "Altitude"
                          , "Speed over ground"
                          , "Course over Ground"
                          , "Fix mode"
                          , "Reserverd1"
                          , "HDOP"
                          , "PDOP"
                          , "Reserved2"
                          , "GNSS satellites in View"
                          , "GNSS Satellites used"
                          , "Reserved3"
                          , "c/no max"
                          , "HPA"
                          , "VPA"
                          , "x"
                         
                          ]



class SIM_AT(Serial_AT):
    def __init__(self,device_name="SIM",pre_cmd="",pos_cmd= "\r\n") :
        super().__init__(pre_cmd,pos_cmd)


    #COMMADS

    def is_SIM_ready(self):
        """
        check if the device is ready to receive commands        
        """
        state,buff =  self._send_cmd_and_check(CMD_READY,IS_OK)
        return state


    def set_echo(self,value):
        """
        Turn echo on or off
        """
        echo = bool(value)
        if echo == True:
            cmd = CMD_ECHO_ON
        else:
            cmd = CMD_ECHO_OFF
        s,buff = self._send_cmd_and_check(cmd,IS_OK)
        while s == False:
            time.sleep(1)
            s,buff = self._send_cmd_and_check(cmd,IS_OK)

        



    def set_error_coding(self,value):
        """
        Turn error code on or off
        """
        cmd = bool(value)
        if cmd == True:
            cmd = CMD_SET_ERROR_CODE.format(1)
        else:
            cmd = CMD_SET_ERROR_CODE.format(0)
        s,buff = self._send_cmd_and_check(cmd,IS_OK)
        while s == False:
            time.sleep(1)
            s,buff = self._send_cmd_and_check(cmd,IS_OK)





    def get_signal(self):
        """
        get signal level
        """
        #-------------------------inner function start----------------------
        def get_signal_in_number(buffer):
            """
            return signal in float
            """

            # step 1: search +CSQ
            finded = False
            index = 0
            i = 0
            for element in buffer:
                if str(element).count("+CSQ: ") >0 :
                    index = i
                    finded = True
                    break   
                i = i + 1
            number = 0
            if finded == True:

                pos = str(buffer[index]).find("+CSQ: ")

                if pos >= 0:   # pos == -1 when find failed
                    if pos != -1:
                        substring = str(buffer[index][(pos+5):(pos+10)]).replace(",",".")
                        try:
                            number = float(substring)
                            print( "substring is {}".format(substring))
                        except Exception:
                            pass
            return number
        #----------------inner function end-------------------------------------
        state,buffer = self._send_cmd_and_check(CMD_GET_SIGNAL,IS_OK)

        if state == True:

            n = get_signal_in_number(buffer)
            #print("signal level: {}".format(n))

        return n






    def get_phone_operator(self):
        """
        Get the cellphone operator.     
        """
        state,buffer = self._send_cmd_and_check(CMD_SET_OPERATOR.format(0),IS_OK,timeout=5)
        time.sleep(1)
        state,buffer = self._send_cmd_and_check(CMD_GET_OPERATOR,"OK")
    
        return state

        



    def send_sms(self,number,message="test message"):
        """"
        Send a sms to the cellpohne number. Remember that this could have a cost
        """
        #Active the message function
        self._send_cmd(CMD_SMS_SET_FUNCTION)
        time.sleep(1)
        #set the number into the command
        cmd = CMD_SEND_MSM.format(str(number))
        self._send_cmd(cmd,5)
        self._send_cmd(message,2)
        buff_hex = [26,] # you need to send this character to end the message and send
        self._send_buffer_raw(buff_hex,2)


    def _open_APN_services(self):
        """
        SET APN and get data services
        """
        #set APN of your cellpone operator. In my case is Personal Argentina
        self._send_cmd(CMD_OPEN_CONN.format(APN_PERSONAL))
        self._send_cmd(CMD_GET_CONN,"OK")

    def mqtt_close(self):
        self._send_cmd(CMD_DISCONECT_MQTT)
        self._send_cmd(CMD_CLOSE_MQTT_CONN)


    

    #mqtt things
    def mqtt_init(self,url,user,password,try_again = True):
        """
        Configure mqtt services
        """
        
        #DEFAULT CONFIG
        self._send_cmd(CMD_DEFAULT_CONFIG)
        time.sleep(1)
        #init
        self._open_APN_services()
        #close

        URL  = CMD_MQTT_SET_URL.format(url)
        USER = CMD_MQTT_SET_USERNAME.format(user)
        PASSWORD = CMD_MQTT_SET_PASSWORD.format(password)
        self._send_cmd(URL)
        self._send_cmd(USER)
        self._send_cmd(PASSWORD)
        self._send_cmd(CMD_MQTT_CHECKS_PARAMS)
 



    def mqtt_publish(self,topic,message):
        """
        Pubish a message in the topic
        """
        PUB = CMD_MQTT_PUBLISH.format(topic,len(message))
        self._send_cmd(PUB)
        self._send_cmd(message)


    def mqtt_subscribe(self,topic):
        """
        Subscribe to the topic
        """
        TOPIC = CMD_MQTT_SUBSCRIBE.format(topic)
        self._send_cmd(TOPIC)


    def mqtt_unsubscribe(self,topic):
        """
        Unsubscribe to the topic
        """
        TOPIC = CMD_MQTT_UNSUBSCRIBE.format(topic)
        self._send_cmd(TOPIC)


    def set_gnss(self,value):

        if value == True:
            cmd = CMD_PWR_GPS.format(1)
        else:
            cmd = CMD_PWR_GPS.format(0)
        
        self._send_cmd(cmd)







    def get_position(self):
        """
        return json with data from gnss. 
        Before call this function you have to call set_gnss(1) to init the gnss
         """
        #---------inner function start------------------------------------
        def nmea_format(nmea,size = 8):  
                """
                NMEA has 21 field but i use size = 8 because. Return json with data
                """
                frame = dict()
                
                for i in range(size): # len(nmea) - 1 because the last element is \r\n
                    #print("{}) {}: {}".format(i,DATA_FIELD_NMEA[i],nmea[i]))
                    frame[DATA_FIELD_NMEA[i]]=nmea[i]

                    data = json.dumps(frame)

                return data
        #-------------------inner function end-------------------      
        #GNSS GET
        state,buffer = self._send_cmd_and_check(CMD_GET_INFO_GPS,"OK")
            
        if state == True:
            for line in buffer:
                if str(line).count("+CGNSINF:") == 1: #filter the data buffer
                    data = str(line).split(",")
                    #print("send {} to nmea_format()".format(data))
                    data_json = nmea_format(data)
            
        return  data_json


       


   

