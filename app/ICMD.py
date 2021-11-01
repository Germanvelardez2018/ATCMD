"""
Author: German Velardez
email: germanvelardez16@gmail.com
date: 29/10/2021

"""


from abc import ABC, abstractclassmethod


class ICMD(ABC):

    _PRE_CMD = ""
    _POS_CMD = ""

    _inferface = None


    def set_pre_cmd(self,pre):
        """
        Set pre commands 
        """
        if type(pre) == str:
            self._PRE_CMD = pre

    def set_pos_cmd(self,pos):
        if type(pos) == str:
            self._POS_CMD = pos


    def get_pre_cmd(self):
        return self._PRE_CMD

    def get_pos_cmd(self):
        return self._POS_CMD

    def set_debug(self,debug):
        self.debug = bool(debug) 

    @abstractclassmethod
    def init_interface(self,*arg):
        pass


    @abstractclassmethod
    def _send_cmd(self,cmd,timeout):
        pass


    @abstractclassmethod
    def _send_cmd_list(*arg):
        pass
    

    @abstractclassmethod
    def _debug_print(self,message):
        pass

    @abstractclassmethod
    def _debug_print(self,message,output=True,device_name=""):
        pass