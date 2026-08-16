from PySide6.QtCore import (
    QObject,
    Signal #emite señales cuando un evento ocurre> junto con los "slots" es el reemplazo de los callback
)

import json

import serial.tools.list_ports #obtiene la lista de puertos del sistema: https://pyserial.readthedocs.io/en/latest/tools.html
import serial #libreria de comunicacion serial


class SerialManager(QObject):
    
    connection_changed = Signal(bool) #variable bool de senal> true or false a un evento
    connection_error = Signal(str) #variable de signal tipo str, contiene el msj de error

    data_received = Signal(dict)


    def __init__(self):
        super().__init__()

        self.connected = False

        self.serial = None


    def get_available_ports(self): #obtener los nombres de los puertos

        ports = []

        for port in serial.tools.list_ports.comports():

            ports.append(port.device) #device> Obtain Full device name

        return ports


    def connect_port(self, port): #conexion

    #     print(
    #     f"Conectando a {port}" #imprime en la terminal el port al cual se ha conectado
    # )
        
        try:

            self.serial = serial.Serial(
                port,
                115200,
                timeout=1
            )

            self.connected = True

            self.connection_changed.emit(
                True
            )

        except Exception as e:

            self.connected = False

            self.connection_changed.emit(
                False
            )

            self.connection_error.emit(
                str(e)
            )


    def disconnect_port(self): #desconexion

        if self.serial:
            
            self.serial.close()

        self.connected = False

        self.connection_changed.emit(
            False        #actualiza el signal> no hay puerto conectado
        )


    def send(self, data):

        if not self.connected:

            return
        
        self.serial.write(
            (data + "\n").encode("utf-8")
        )


    def read_once(self):

        if not self.connected:

            return
        
        line = (
            self.serial.readline().decode("utf-8").strip()
        )

        if not line:

            return
        
        try:

            data = json.loads(
                line
            )

            self.data_received.emit(
                data
            )

        except json.JSONDecodeError:

            print(
                "JSON inválido"
            )