"""
Driver for module Bluetooth HC-5
"""









"""" COMAND LIST
*******************************************************************␍␊
    Command             Description⇥	⇥	⇥	           *␍␊
    ---------------------------------------------------------------- *␍␊
    AT                  Check if the command terminal work normally  *␍␊
    AT+RESET            Software reboot⇥	⇥	⇥	⇥	   *␍␊
    AT+VERSION          Get firmware, bluetooth, HCI and LMP version *␍␊
    AT+HELP             List all the commands⇥	⇥	           *␍␊
    AT+NAME             Get/Set local device name                    *␍␊
    AT+PIN              Get/Set pin code for pairing                 *␍␊
    AT+BAUD             Get/Set baud rate⇥	⇥	                   *␍␊
    AT+LADDR            Get local bluetooth address⇥	⇥	   *␍␊
    AT+ADDR             Get local bluetooth address⇥	⇥	   *␍␊
    AT+DEFAULT          Restore factory default⇥	⇥	⇥	   *␍␊
    AT+RENEW            Restore factory default⇥	⇥	⇥	   *␍␊
    AT+STATE            Get current state⇥	⇥	⇥	⇥	   *␍␊
    AT+PWRM             Get/Set power on mode(low power) ⇥	⇥	   *␍␊
    AT+POWE             Get/Set RF transmit power ⇥	⇥	   *␍␊
    AT+SLEEP            Sleep mode ⇥	⇥	                   *␍␊
    AT+ROLE             Get/Set current role.⇥	                   *␍␊
    AT+PARI             Get/Set UART parity bit.                     *␍␊
    AT+STOP             Get/Set UART stop bit.                       *␍␊
    AT+INQ              Search slave model                           *␍␊
    AT+SHOW             Show the searched slave model.               *␍␊
    AT+CONN             Connect the index slave model.               *␍␊
    AT+IMME             System wait for command when power on.⇥	   *␍␊
    AT+START            System start working.⇥	⇥	⇥	   *␍␊
    AT+UUID             Get/Set system SERVER_UUID .            ⇥	   *␍␊
    AT+CHAR             Get/Set system CHAR_UUID .            ⇥	   *␍␊
    -----------------------------------------------------------------*␍␊
    Note: (M) = The command support master mode only. ⇥	           *␍␊

"""

#READY

HC5_READY = "AT"


#GET BACK TO USER MODE
HC5_USER_MODE ="AT+RESET"

#VERSION

HC5_GET_VERSION="AT+VERSION"

#RESTORE ALL


HC5_RESTORE_ALL = "AT+DEFAULT"

#MAC ADDRES 

HC5_GET_ADDRESS = "AT+LADDR"


#DEVICE NAME

HC5_NAME = "AT+NAME"

HC5_SET_NAME = HC5_NAME + "{}"


#ROLE DEVICE

HC5_ROLE = "AT+ROLE"

HC5_SET_ROLE = HC5_ROLE + "{}"   # 0 SLAVE, 1 MASTER








# Baudrate
"""
GET:
AT+BAUD
SET:
AT+BAUD1          1200bps
AT+BAUD2          2400bps
AT+BAUD3          4800bps
AT+BAUD4          9600bps (Default)
AT+BAUD5          19200bps
AT+BAUD6          38400bps
AT+BAUD7          57600bps
AT+BAUD8          115200bps
"""

HC5_BAUD="AT+BAUD"

HC5_SET_BAUD= HC5_BAUD + "{}"


#PIN
"""
GET:
AT+PIN

SET:
AT+PIN{PIN[LEN= 4]}
"""

HC5_PIN = "AT+PIN"

HC5_SET_PIN = HC5_PIN+"{}"



#PASSWORD

HC5_PASSWORD= "AT+PSWD"

HC_GET_PASSWROD = HC5_PASSWORD+"?"
HC_SET_PASSWROD = HC5_PASSWORD = "{}"


