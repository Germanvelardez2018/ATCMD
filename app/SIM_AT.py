"""
Author: German Velardez
Interface for SIM devices

"""

import time
from Serial_AT import Serial_AT
from SIM7000_CMDS import *






MIN_SIGNAL = 20

MAX_SIGNAL = 33 # WHEN THE DEVICE NOT SIGNAL,RETURN 99.99





class SIM_AT(Serial_AT):
    def __init__(self,device_name="SIM",pre_cmd="",pos_cmd= "\r\n") :
        super().__init__(pre_cmd,pos_cmd)






    #COMMADS


    def is_SIM_ready(self):
        """
        check if the device is ready to receive commands
        
        """
        state,buff =  self._send_cmd_and_check(CMD_READY,IS_OK)
       
        if state == True:
            print("its ready")

        else:
            print("it isn't responding")



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
            s = self._send_cmd_and_check(cmd,IS_OK)

        



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


        def get_signal_in_number(buffer):
            """
            return signal in float
            """

            # step 1: search +CSQ
            finded = False
            index = 0
            i = 0
            #print( "buffer {}".format(buffer))
            for element in buffer:
             #   print("element{} {}".format(i,element))
                if str(element).count("+CSQ: ") >0 :
                    index = i
                    finded = True
                    break   
                i = i + 1
            #ste 2 : transfor that element in a number
            #print("index is {}".format(index))
            number = 0
            if finded == True:

                pos = str(buffer[index]).find("+CSQ: ")

                if pos >= 0:   # pos == -1 when find failed
                   substring = str(buffer[index][(pos+5):(pos+10)]).replace(",",".")
                   try:
                       number = float(substring)
                       print( "substring is {}".format(substring))

                   except Exception:
                       pass
            return number

            
                


        state,buffer = self._send_cmd_and_check(CMD_GET_SIGNAL,IS_OK)

        if state == True:

            n = get_signal_in_number(buffer)
            print("la señal del dispostivo es: {}".format(n))


            









# test 


if __name__ == "__main__":

    print ("Class SIM_AT (sim7000g")
    device = SIM_AT("SIM 7000")

    device.get_signal()
   # device.set_error_coding(1)

   # device.is_SIM_ready()

   # device.is_SIM_ready()

   # device.set_echo(False)
   # device.is_SIM_ready()

   # device.set_echo(True)
   # device.is_SIM_ready()

   

