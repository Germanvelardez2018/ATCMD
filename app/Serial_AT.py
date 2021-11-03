"""
Author: German Velardez
email: germanvelardez16@gmail.com
date: 29/10/2021

"""


from ICMD import ICMD



from os import write
import time
import sys
import glob
import time    
import serial
from serial.serialutil import SerialException, SerialTimeoutException, Timeout
from datetime import date, datetime


class Serial_AT(ICMD):


    #PRIVATE PARAMETES
    _BAUDRATE_LIST = [9600,19200,38400,57600,115200] #Valid Baudrate
    _port = None
    _baudrate = 9600
    _device_name= "Device"
    _debug = True

    def __init__(self,pre_cmd="",pos_cmd= ""):
      super().set_pre_cmd(pre_cmd)
      super().set_pos_cmd(pos_cmd)
      self.init_interface()   


    


    def _set_baudrate(self,baudrate):

        self._baudrate = baudrate

    def get_baudrate(self):
        return self._baudrate



    def _set_serial_baudrate(self,baudrate):
        print("set baudrate {}".format(baudrate))
        self._baudrate = baudrate    

    def get_serial_baudrate(self):
        return self._baudrate

    def _set_serial_port(self,port):
        print("set port: {}".format(port))
        self._port = port
        
    def get_serial_port(self):
        return self._port
    
        

    
    def init_interface(self,*arg):
        """"
        Config and init  hardware interface. It uses a menu with the opctions
        """
        print("init interface")
        
        
        print("read ports")
        port_list = self._read_ports() #reading the serial ports

        port_selected = self._select_option(port_list,"List of serial ports","Select a serial port")
        if port_selected == 0:
             raise Exception
        
        try:
            self._set_serial_port(port_list[port_selected-1])


            baudrate_selected = self._select_option(self._BAUDRATE_LIST,"List of Baudrates valide","Select a baudrate")

            self._set_serial_baudrate(self._BAUDRATE_LIST[baudrate_selected-1])
        
        except Exception:
            print("Port Config Error")
            print("close the program")
            exit()

        


    
    def _send_cmd_and_check(self,cmd,expected_response,timeout=1):

        buffer_rx = self._send_cmd(cmd,timeout=timeout)

        ok = False
        for line in buffer_rx:
            if str(line).count(expected_response) >0:    ## the response contain the excepted response
                ok = True
                break
        return ok,buffer_rx    # if state is True then buffer is valid



    def _send_buffer_raw(self,buffer,timeout=1):
        """
        Send a buffer  command by the interface and return buffer_rx
        """
        commands =  buffer 
        

        try:
            with serial.Serial(self._port,self._baudrate,timeout=1) as s:
                s.flushOutput()
                s.flushOutput()
                w = s.write(bytes(commands))
                self._debug_print(commands,device_name=self._device_name)

                rx_buffer = []
                lines = s.readlines()
                for line in lines :
                    line_formated = (str(line).replace("b",""))
                    self._debug_print(line_formated,output=False,device_name=self._device_name)
                    rx_buffer.append(line_formated) 

        except SerialException:
            self._debug_print("Serial Interface Error",device_name=self._device_name)
        except SerialTimeoutException:
            self._debug_print("device not respond",device_name=self._device_name)

       

        





    def _send_cmd(self,cmd,timeout=1):
        """
        Send a commnad by the interface and return buffer_rx
        """
        commands = self._PRE_CMD + cmd + self._POS_CMD

        rx_buffer=[]
        try:
            with serial.Serial(self._port,self._baudrate,timeout=1) as s:
                s.flushOutput()
                s.flushOutput()
                w = s.write(bytes(commands,"utf-8"))
                self._debug_print(commands,device_name=self._device_name)

                
                lines = s.readlines()
                for line in lines :
                    line_formated = (str(line).replace("b",""))
                    self._debug_print(line_formated,output=False,device_name=self._device_name)
                    rx_buffer.append(line_formated) 

           

        except SerialException:
            self._debug_print("Serial Interface Error",device_name=self._device_name)
        except SerialTimeoutException:
            self._debug_print("device not respond",device_name=self._device_name)
        
        return rx_buffer # return all buffer rx




    
    def _send_cmd_list(self,*arg,timeout=1):
        

        for cmd in arg:
            self._send_cmd(cmd,timeout=timeout)



      
   
        








# PRIVATE FUNCTIONS


 
    def _debug_print(self,message,output=True,device_name=""):

        """
        Output for debug. Maybe it can save information in a file
        """
        if self._debug == True:
            if output == True:
            
                o = "==>"
            else:
                o = "<=="

            print("[{}] {} {}".format(device_name,o,message))
            




    def _select_option(self,option_list,wellcome_msg="List options: ",select_msg="select one option"):
        """
        list the option and select one. Return the opcion seleted
        """
        #list the options

        self._debug_print(wellcome_msg,device_name="PyInterface")
        self._debug_print("-"*50,device_name="PyInterface")
        #list the options

        counter = 0
        for option in option_list:
            counter +=1
            self._debug_print("[{}] {} ".format(counter,option),device_name="PyInterface")

        self._debug_print("[0] to exit",device_name="PyInterface")
        self._debug_print("-"*50,device_name="PyInterface")
        self._debug_print(select_msg,device_name="PyInterface")
        option_select = 0
        end_loop= False
        while end_loop == False:
            try:
                option_select = int(input())
                # filter 
                self._debug_print("you select option {}".format(option_select),device_name="PyInterface")
                if option_select >=0 or option_select <= len(option_list):
                    end_loop = True

                self._debug_print("invalid option. Try again",device_name="PyInterface")
            except Exception:
                self._debug_print("Input error.Try again",device_name="PyInterface")
        self._debug_print("-"*50,device_name="PyInterface")
        return option_select
 




    def _read_ports(self):
            """
            Return serial ports
            """
            if sys.platform.startswith('win'):
                ports = ['COM%s' % (i + 1) for i in range(256)]
            elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
                # this excludes your current terminal "/dev/tty"
                ports = glob.glob('/dev/tty[A-Za-z]*')
            elif sys.platform.startswith('darwin'):
                ports = glob.glob('/dev/tty.*')
            else:
                raise EnvironmentError('Unsupported platform')
            list = []
            for port in ports:
                try:
                   
                    s = serial.Serial(port)
                    s.close()
                    list.append(port)
                except (OSError, serial.SerialException):
                    pass
                   
        
            return list

       
       
            

        
      





if __name__ == "__main__":

    print("init program")
    s = Serial_AT()
    res = s._send_cmd_and_check("","OK",1)

    if res == True:
        print("expected response")

    else:
        print("without unexpected response")
    

