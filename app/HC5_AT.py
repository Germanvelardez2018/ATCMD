""""
Author: German Velardez
email: germanvelardez16@gmail.com
date: 10/11/2021


"""



from Serial_interface.Serial_AT import Serial_AT
import time
from HC5 import *


class HC5_AT(Serial_AT):
    def __init__(self, pre_cmd="", pos_cmd="\r\n"):
        super().__init__(pre_cmd,pos_cmd)



    #commands


    def get_version(self,timeout=1):

        """
        get firmware version
        """

        state,buff = self._send_cmd_and_check(HC5_GET_VERSION,"OK",timeout)

        return state


    def get_role_device(self,timeout=1):
        """
        get rol of the device. 
        """
        state, buff = self._send_cmd_and_check(HC5_ROLE,"OK",timeout)

        return state

    def set_role_master(self,role,timeout=1):

        """
        set role . set o for slave, 1 for master
        """
        role = bool(role)
        master = 0
        if role:
            master = 1

        state,buff = self._send_cmd_and_check(HC5_SET_ROLE.format(master),"OK",timeout)
        return state

    def get_pin(self,timeout):
        
        """
         get pin of the device
        """
        state, buff = self._send_cmd_and_check(HC5_PIN,"OK",timeout)

        return state


    def is_ready(self,timeout=1):
        """
        Check if the device is ready to receive commands
        """

        state,buff = self._send_cmd_and_check(HC5_READY,"OK",timeout) 
        return state


    def set_device_name(self,name,timeout=1):
        """
        set device name
        """

        state,buff = self._send_cmd_and_check(HC5_SET_NAME.format(name),"OK",timeout)
        
        return buff


    def get_device_name(self,timeout=1):
        """
        Get device name
        """

        state,buff = self._send_cmd_and_check(HC5_NAME,"OK",timeout)

        return state


    def user_mode(self,timeout=1):
        state,buffer = self._send_cmd_and_check(HC5_USER_MODE,"OK",timeout)

        return state



if __name__ == "__main__":
    print("runnig test: HC5 BLUETOOTH MODULE")

    device = HC5_AT()

    if device.is_ready():
        print("device ready ")
        print("ask its name")

        device.get_version()
        device.get_device_name()
        print("set device name")
        #device.set_device_name("simo inti")
        #time.sleep(5)
        print("ask its name")
        device.get_device_name()

        device.get_role_device()

        time.sleep(4)
        device.set_role_master(0)

        #finish 
        print("into user mode")
        device.user_mode()
    else:
        print("we got a problem")



      
