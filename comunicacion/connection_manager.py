from PySide6.QtCore import (
    QObject,
    Signal
)

from comunicacion.serial_manager import ( # metodo conexion serial: clase
    SerialManager
)

from comunicacion.tcp_manager import (  # metodo conexion tcp: clase
    TCPManager
)

from comunicacion.Serial_reader_thread import (
    SerialReaderThread
)


class ConnectionManager(QObject): 

    connection_changed = Signal(bool) # signal 
    data_received = Signal(dict)


    #constantes
    SERIAL = "serial"
    NETWORK = "network"

    
    def __init__(self): # metodo constructor


        super().__init__()


        self.serial_manager = ( # llama a la clase de comunicacion serial
            SerialManager()
        )

        self.serial_thread = SerialReaderThread(
            self.serial_manager
        )

        self.tcp_manager = (    # llama a la clase de comunicacion TCP
            TCPManager()
        )

        self.serial_manager.connection_changed.connect(
            self.connection_changed.emit
        )

        self.tcp_manager.connection_changed.connect(
            self.connection_changed.emit
        )

        self.current_mode = self.SERIAL # metodo predeterminado

        self.serial_manager.data_received.connect(
            self.data_received.emit
        )

        self.tcp_manager.data_received.connect(
            self.data_received.emit
        )
    

    def set_mode(self, mode: str):   # determina el metodo de conexion


        self.current_mode = mode


    def connect(self, target):  # realiza la conexion en base a la seleccion del radio button.


        if self.current_mode == self.SERIAL:

            self.serial_manager.connect_port(
                target
            )

            if self.serial_manager.connected:

                self.serial_thread.start()


        else:

            self.tcp_manager.connect_network(
                target
            )

            
    def disconnect(self):    # realiza la desconexion.


        if self.current_mode == self.SERIAL:

            self.serial_manager.disconnect_port()

            if self.serial_thread.isRunning():

                self.serial_thread.stop()

        else:

            self.tcp_manager.disconnect_network()

    
    def get_available_ports(self): #obtiene puertos COM del equipo


        return (
            self.serial_manager
            .get_available_ports()
        )
    

    @property #convierte la funcion en atributo
    def connected(self):


        if self.current_mode == self.SERIAL:

            return (
                self.serial_manager.connected
            )

        return (
            self.tcp_manager.connected
        )


    def send(self, data): #gestiona el envio de datos del JSON en base al metodo de conexion empleado


        if self.current_mode == self.SERIAL:

            self.serial_manager.send(
                data
            )

        else:

            self.tcp_manager.send(
                data
            )
    
    def send_model(self, model):

        self.send(
             model.to_json()
        )
        
        
    def read_once(self):

        if self.current_mode == self.SERIAL:

            self.serial_manager.read_once()

        else:

            self.tcp_manager.read_once()
