""""


"""
from ESP01S import *
from Serial_interface.Serial_AT import Serial_AT


class ESP01_AT(Serial_AT):

    def __init__(self, pre_cmd="", pos_cmd=""):
        super().__init__(pre_cmd=pre_cmd, pos_cmd=pos_cmd)



    def is_ready(self,timeout=1):
        """
        send AT to the ESP01 ad check response
        """ 


        state,buff = self._send_cmd_and_check(ESP01_IS_READY,"OK")

        return state


def test():
    
    device = ESP01_AT()

    device.is_ready()


if __name__ == "__main__":
    print("init test")
    test()
