import serial.tools.list_ports
import time

portModule = None

#########################
# ECO off configuration #
#########################
def initModule():

    _dataOK = b"\r\nOK\r\n"
    _dataERROR = b"\r\nERROR\r\n"

    if portModule is not None :
        i = 0
        _dataSerial_RX = b''      
        portModule.write("AT\r".encode())
        
        while True :
            
            if portModule.in_waiting > 0:
                _dataSerial_RX += portModule.read()

                if _dataOK in _dataSerial_RX :

                    if i == 0 :
                        _dataSerial_RX = b''
                        portModule.write("ATE0\r".encode()); i += 1

                    elif i == 1 :
                        print("InitModule OK...")
                        break

            elif _dataERROR in _dataSerial_RX :
                print("Error InitModule...")
                break

        if i == 1 :
            return 1
        else :
            return 0

###################################################################################################
# Serial port's configuration of the raspberry to 9600 for communication with the GSM/GPRS module #
###################################################################################################
def configSerialMoule():
    
    global portModule
    
    #List serial port
    portSerialModule = list(serial.tools.list_ports.comports())
    print(len(portSerialModule))

    
    for port in portSerialModule:
        if "COM3" in port.device:
            portModule = serial.Serial(port.device, baudrate=9600)
            return 1
        else:
            return 0 

#############################################
# Configuration of the module GPS to 115200 #
#############################################
def configGPS():
    
    global portModule
    _dataOK = b"\r\nOK\r\n"
    _dataERROR = b"\r\nERROR\r\n"
    _gpsOFF = b'\r\n+CGNSPWR: 0\r\n'
    _gpsON = b'\r\n+CGNSPWR: 1\r\n'

    if portModule is not None :
        i = 0
        _dataSerial_RX = b''      
        portModule.write("AT\r".encode())
        
        while True :
            
            if portModule.in_waiting > 0:
                _dataSerial_RX += portModule.read()
                #print(_dataSerial_RX)

                if _dataOK in _dataSerial_RX :

                    if i == 0 :
                        _dataSerial_RX = b''
                        portModule.write("AT+CGNSPWR?\r".encode()); i += 1

                    elif i == 2 :
                        _dataSerial_RX = b''
                        portModule.write("AT+CGNSIPR=115200\r".encode()); i += 1

                    elif i == 3 :
                        _dataSerial_RX = b''
                        portModule.write("AT+CGNSSEQ=RMC\r".encode()); i += 1

                    elif i == 4 :
                        _dataSerial_RX = b''
                        portModule.write("AT+CGNSTST=0\r".encode()); i += 1

                    elif i == 5 :
                        _dataSerial_RX = b''
                        print("Configuration GPS OK"); i += 1
                        break
                
                elif _gpsOFF in _dataSerial_RX :
                    _dataSerial_RX = b''
                    portModule.write("AT+CGNSPWR=1\r".encode()); i += 1

                elif _gpsON in _dataSerial_RX :
                    _dataSerial_RX = b''
                    portModule.write("AT\r".encode()); i += 1

                elif _dataERROR in _dataSerial_RX :
                    _dataSerial_RX = b''
                    print("Error GPS Configuration")
                    break
        
        if i == 6 :
             return 1
        else :
             return 0

###################################################
# Configuration GPRS module with the RED operator #
###################################################
def configREDGPRS():
    global portModule

    _dataSerial_RX = b''
    _dataOK = b"\r\nOK\r\n"
    _dataERROR = b"\r\nERROR\r\n"
    i = 0

    if portModule is not None:
        gprsDisconnect()
        portModule.write("AT\r".encode())
        while True:
            
            if portModule.in_waiting > 0:
                _dataSerial_RX += portModule.read()

                if _dataOK in _dataSerial_RX :

                    if i == 0 :
                        #print("R AT", _dataSerial_RX)
                        _dataSerial_RX = b''
                        portModule.write('AT+SAPBR=3,1,"CONTYPE","GPRS"\r'.encode()); i += 1

                    elif i == 1 :
                        #print("R AT+SAPBR", _dataSerial_RX)
                        _dataSerial_RX = b''
                        portModule.write('AT+SAPBR=3,1,"APN","web.vmc.net.co"\r'.encode()); i += 1

                    elif i == 2 :
                        #print("R AT+SAPBR", _dataSerial_RX)
                        _dataSerial_RX = b''
                        portModule.write('AT+SAPBR=1,1\r'.encode()); i += 1

                    elif i == 3 :
                        #print("R AT+SAPBR", _dataSerial_RX)
                        _dataSerial_RX = b''
                        portModule.write('AT+SAPBR=2,1\r'.encode()); i += 1

                    elif i == 4 :
                        #print("R AT+SAPBR", _dataSerial_RX)
                        _dataSerial_RX = b''
                        print("GPRS Connection On"); i += 1
                        break

                elif _dataERROR in _dataSerial_RX :
                    break

        if i == 5 :
            return 1
        else :
            print("Configuration GPRS ERROR...")
            return 0
    else:
        print("port ERROR")

##########################################
# Disconnect the GPRS connection exiting #
##########################################
def gprsDisconnect():
    global portModule

    _dataOK = b"\r\nOK\r\n"
    _dataERROR = b"\r\nERROR\r\n"
    _dataSerial_RX = b''
    _shutOK = b"\r\nSHUT OK\r\n"
    i = 0

    if portModule is not None:

        portModule.write("AT\r".encode())
        while True:
            
            if portModule.in_waiting > 0:
                _dataSerial_RX += portModule.read()
                
                if _dataOK in _dataSerial_RX:
                    
                    if i == 0 :
                        #print("R AT", _dataSerial_RX)
                        _dataSerial_RX = b''
                        portModule.write('AT+CIPSHUT\r'.encode()); i += 1

                    elif i == 2 :
                        #print("R AT+CGATT: ", _dataSerial_RX)
                        _dataSerial_RX = b''
                        portModule.write('AT+SAPBR=0,1\r'.encode()); i += 1

                    elif i == 3 :
                        #print("R AT+SAPBR: ", _dataSerial_RX)
                        _dataSerial_RX = b''
                        print("GPRS Connection Off"); i += 1
                        time.sleep(10)
                        break

                elif _shutOK in _dataSerial_RX :
                    #print("R AT+CIPSHUT: ", _dataSerial_RX)
                    _dataSerial_RX = b''
                    portModule.write('AT+CGATT=0\r'.encode()); i += 1

                elif _dataERROR in _dataSerial_RX:
                    print("Error to disconnect")
                    break

        if i == 4 :
            return 1
        else :
            return 0

######################################
# Read the position given by the GPS #
######################################
def readGPS():
    global portModule

    _dataERROR = b"\r\nERROR\r\n"
    _dataOK = b"\r\nOK\r\n"
    #_dataGNSINF = b"\r\nOK\r\n"
    _dataSerial_RX = b''
    _dataOut = None
    i = 0

    if portModule is not None:
        time.sleep(3)
        portModule.write("AT\r".encode())
        
        while True:

            if portModule.in_waiting > 0:
                _dataSerial_RX += portModule.read()

                if _dataERROR in _dataSerial_RX :
                    print("Error reading GPS")
                    break

                if _dataOK in _dataSerial_RX:

                    if i == 0 :
                        _dataSerial_RX = b''
                        portModule.write("AT+CGNSINF\r".encode()); i += 1

                    elif i == 1 and (_dataOK in _dataSerial_RX):
                        _dataSerial_RX = b''
                        i += 1

                    elif i == 2 :
                        #print("Datos de GPS: ", _dataSerial_RX)
                        _data = _dataSerial_RX.decode()
                        _dataOut = _data.split(',')
                        #print(_dataOut)
                        _dataSerial_RX = b''
                        _data = ""
                        if len(_dataOut) >= 5 :
                            _fecha = _dataOut[2]
                            _año = '"Fecha":' + '"' + _fecha[0:3] + '-' + _fecha[4:5] + '-' + _fecha[6:7] + '"'
                            _hora = '"Hora":' + '"' + _fecha[8:9] + '-' + _fecha[10:11] + '-' + _fecha[12:13] + '"'
                            _data = '"Latitud":' + _dataOut[3] + '\r' + '"Longitud":' + _dataOut[4] + '\r' + _año + '\r' + _hora + '\r'
                            break
                        else:
                            print("No Data")
                            break
                    
        if _data is not None :
            return _data
        else :
            return 0

######################################################
# Configuration of the Internet connection to the IP #
######################################################
def gprsConnect():
    global portModule
    
    _dataOK = b"\r\nOK\r\n"
    _dataERROR = b"\r\nERROR\r\n"
    _simCardOK = b"\r\n+CPIN: READY\r\n\r\nOK\r\n"
    _simCardERROR = b"\r\n+CPIN: PH_SIM PIN\r\n"
    _closeConnection = b"\r\nCLOSE OK\r\n"
    _modeIP0 = b"\r\n+CIPMODE: 0\r\n\r\nOK\r\n"
    _modeIP1 = b"\r\n+CIPMODE: 1\r\n\r\nOK\r\n"
    _ipConnection1 = b"\r\n+CIPMUX: 1\r\n\r\nOK\r\n"
    _ipConnection0 = b"\r\n+CIPMUX: 0\r\n\r\nOK\r\n"
    _apnVirgin = b'\r\n+CSTT: "web.vmc.net.co","",""\r\n\r\nOK\r\n'
    _CGREG01 = b"\r\n+CGREG: 0,1\r\n"
    _CGREG00 = b"\r\n+CGREG: 0,0\r\n"
    _CGATT1 = b"\r\n+CGATT: 1\r\n\r\nOK\r\n"
    _CGATT0 = b"\r\n+CGATT: 0\r\n\r\nOK\r\n"
    _CONNECT = b"\r\nCONNECT OK\r\n"

    if portModule is not None :
        i = 0
        _dataSerial_RX = b''
        portModule.write("AT\r".encode())
        while True:
            if portModule.in_waiting > 0:
                _dataSerial_RX += portModule.read()

                if _dataOK in _dataSerial_RX: 

                    if i == 0:
                        print("R AT", _dataSerial_RX)
                        _dataSerial_RX = b''
                        portModule.write("ATE0\r".encode()); i += 1
                        
                    elif i == 1 and ( _dataOK in _dataSerial_RX ) :
                        print("R AT+CFUN=1", _dataSerial_RX)
                        _dataSerial_RX = b''
                        portModule.write("AT+CNMI=2,2,0,0,0\r".encode()); i += 1

                    elif i == 2 :
                        print("R AT+CNMI=2,2,0,0,0", _dataSerial_RX)
                        _dataSerial_RX = b''
                        portModule.write("AT+CMGF=1\r".encode()); i += 1

                    elif i == 3 :
                        print("R AT+CMGF=1", _dataSerial_RX)
                        _dataSerial_RX = b''
                        portModule.write("AT+CPIN?\r".encode()); i += 1

                    elif i == 4 :
                        if _simCardERROR in _dataSerial_RX:
                            break
                                        
                        elif _simCardOK in _dataSerial_RX:
                            print("R AT+CPIN?", _dataSerial_RX)
                            _dataSerial_RX = b''
                            portModule.write("AT+CSQ\r".encode()); i += 1
                        
                    elif i == 5 :
                        print("R AT+CSQ: ", _dataSerial_RX)
                        _dataSerial_RX = b''
                        portModule.write("AT+CGATT?\r".encode()); i += 1
                        
                    elif i == 6 :
                        if _CGATT0 in _dataSerial_RX:
                            print("R AT+CGATT?", _dataSerial_RX)
                            _dataSerial_RX = b''
                            portModule.write("AT+CGATT=1\r".encode()); i = 0
                        
                        elif _CGATT1 in _dataSerial_RX:
                            print("R AT+CGATT?", _dataSerial_RX)
                            _dataSerial_RX = b''
                            portModule.write("AT+CGREG?\r".encode()); i += 1

                    elif i == 7 :
                        if _CGREG00 in _dataSerial_RX:
                            break

                        elif _CGREG01 in _dataSerial_RX:
                            print("R AT+CGREG?", _dataSerial_RX)
                            _dataSerial_RX = b''
                            portModule.write("AT+CIPMODE?\r".encode()); i += 1
                        
                    elif i == 8 :
                        if _modeIP0 in _dataSerial_RX:
                            print("R AT+CIPMODE?", _dataSerial_RX)
                            _dataSerial_RX = b''
                            portModule.write("AT+CIPMODE=1\r".encode()); i = 0
                            
                        elif _modeIP1 in _dataSerial_RX:
                            print("R AT+CIPMODE?", _dataSerial_RX)
                            _dataSerial_RX = b''
                            portModule.write('AT+CIPMUX?\r'.encode()); i += 1

                    elif i == 9 :
                        if _ipConnection1 in _dataSerial_RX :
                            print("R AT+CIPMUX?", _dataSerial_RX)
                            _dataSerial_RX = b''
                            portModule.write('AT+CIPMUX=0\r'.encode()); i = 0

                        elif _ipConnection0 in _dataSerial_RX :
                            print("R AT+CIPMUX?", _dataSerial_RX)
                            _dataSerial_RX = b''
                            portModule.write('AT+CSTT?\r'.encode()); i += 1

                    elif i == 10 :
                        if _apnVirgin in _dataSerial_RX :
                            print("R AT+CSTT?", _dataSerial_RX)
                            _dataSerial_RX = b''
                            portModule.write("AT\r".encode()); i += 1

                        else:
                            print("R AT+CSTT?", _dataSerial_RX)
                            _dataSerial_RX = b''
                            portModule.write('AT+CSTT="web.vmc.net.co"\r'.encode()); i = 0
                        
                    elif i == 11 :
                        print("R AT+CIICR", _dataSerial_RX)
                        _dataSerial_RX = b''
                        portModule.write('AT+CIPSTART="TCP","192.168.242.8",2000\r'.encode()); i += 1

                    elif i == 12 :
                        if _CONNECT in _dataSerial_RX :
                            print('Envio de datos al servidor')
                            _dataSerial_RX = b''
                            portModule.write("Hola Mundo CONEXION EXITOSA".encode()); i += 1

                    elif i == 13 :
                        portModule.write("ATO\r".encode()); i += 1

                    elif i == 14 :
                        print("R ATO", _dataSerial_RX)
                        _dataSerial_RX = b''
                        portModule.write("AT+CIPCLOSE\r".encode()); i += 1

                    elif i == 15 and (_closeConnection in _dataSerial_RX):
                        break

                elif _dataERROR in _dataSerial_RX:
                    _dataSerial_RX = b''
                    print(i)
                    print("ERROR")
                    break

        if i == 4 :
            print("No SIMCard - Error")
        elif i == 6 :
            print("No Attach GPRS")
        elif i == 7 :
            print("No red register") 
        elif i == 15 :
            print("Conexión exitosa")

###############################################################
# Configuration of the Internet connection to the HTTP Server #
###############################################################
def connectHTTP():

    _dataOK = b"\r\nOK\r\n"
    _dataERROR = b"\r\nERROR\r\n"
    _dataACT = b"200"

    if portModule is not None :
        i = 0
        _dataSerial_RX = b''
        portModule.write("AT\r".encode())
        while True:
            if portModule.in_waiting > 0:
                _dataSerial_RX += portModule.read()

                if _dataOK in _dataSerial_RX: 

                    if i == 0:
                        print("R AT", _dataSerial_RX)
                        _dataSerial_RX = b''
                        portModule.write("AT+HTTPINIT\r".encode()); i += 1
                        
                    elif i == 1 :
                        print("R AT+HTTPINIT", _dataSerial_RX)
                        _dataSerial_RX = b''
                        portModule.write('AT+HTTPPARA="CID",1\r'.encode()); i += 1

                    elif i == 2 :
                        print('R AT+HTTPPARA="CID",1', _dataSerial_RX)
                        _dataSerial_RX = b''
                        portModule.write('AT+HTTPPARA="URL","http://everpizza.necatp.com"\r'.encode()); i += 1

                    elif i == 3 :
                        print('R AT+HTTPPARA="URL","http://everpizza.necatp.com"', _dataSerial_RX)
                        _dataSerial_RX = b''
                        portModule.write('AT+HTTPACTION=0\r'.encode()); i += 1

                    elif i == 4 :
                        if ( _dataACT in _dataSerial_RX ):
                            print('R AT+HTTPACTION=0', _dataSerial_RX)
                            _dataSerial_RX = b''
                            portModule.write('AT+HTTPREAD\r'.encode()); i += 1

                    elif i == 5 :
                        print('R AT+HTTPREAD', _dataSerial_RX)
                        _dataSerial_RX = b''
                        portModule.write('AT+HTTPTERM\r'.encode()); i += 1

                    elif i == 6 :
                        print('R AT+HTTPTERM', _dataSerial_RX)
                        _dataSerial_RX = b''
                        print("Service OK...")
                        break

                elif _dataERROR in _dataSerial_RX :
                    if i == 1:
                        _dataSerial_RX = b''
                        portModule.write('AT+HTTPTERM\r'.encode()); i = 0
                    else :
                        print("Error to connected HTTPS")
                

'''if configSerialMoule():

    if initModule():
        if configREDGPRS():
            if configGPS():
                dataGPS = readGPS()
                if dataGPS is not None:
                    connectHTTP()'''
