from PySide6.QtCore import (
    QObject,
    Signal
)

import json

class TCPManager(QObject):

    connection_changed = Signal(bool) #signal
    connection_error = Signal(str)

    data_received = Signal(dict)

    def __init__(self): #metodo constructor 
        super().__init__()

        self.connected = False # bandera estado de conexion


    def connect_network(self, ip): 

        print(
            f"Conectando a {ip}" #mensaje de conexion
        )

        self.connected = True #actualiza el estado de conexion
         
        print(
        "TCP conectado"
    )

        self.connection_changed.emit(   # actualiza el "signal" 
            True    
        )

    def disconnect_network(self):

        print(
            "Desconectando red"
        )

        self.connected = False

        self.connection_changed.emit(
            False
        )
    
    def send(self, data):

        print(
            f"TCP TX: {data}"
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