"""
Gestor de comunicación por red (TCP/IP).

Define la clase TCPManager, encargada de manejar la conexión, envío y
recepción de datos con el microcontrolador a través de la red (modo
alternativo al puerto serial). Actualmente es una implementación parcial/
de prueba (ver notas en connect_network y read_once).
"""

from PySide6.QtCore import (
    QObject,
    Signal
)

import json


class TCPManager(QObject):
    """
    Gestiona la conexión y comunicación por red (TCP/IP) con el
    microcontrolador.

    Sigue la misma interfaz que SerialManager (connect/disconnect/send/
    read_once y las mismas señales) para que ConnectionManager pueda
    intercambiar ambos gestores sin cambiar su lógica.

    NOTA: esta clase aún no implementa una conexión TCP real (no abre un
    socket); por ahora solo simula el cambio de estado. Ver detalles en
    cada método.
    """

    connection_changed = Signal(bool)  # Señal emitida cuando cambia el estado de conexión (True = conectado)
    connection_error = Signal(str)     # Señal emitida cuando ocurre un error de conexión, con el mensaje de error

    data_received = Signal(dict)  # Señal emitida cada vez que se recibe y parsea correctamente un paquete de datos

    def __init__(self):
        """Inicializa el gestor sin ninguna conexión activa."""
        super().__init__()

        self.connected = False  # Bandera que indica si actualmente hay una conexión de red activa

    def connect_network(self, ip):
        """
        Establece (simula) la conexión de red con la dirección indicada.

        NOTA: actualmente no abre un socket TCP real; solo marca el estado
        como conectado y emite la señal correspondiente. Es un placeholder
        para la futura implementación de la conexión por red.

        Args:
            ip (str): Dirección IP del equipo al que se desea conectar.
        """
        print(
            f"Conectando a {ip}"  # Depuración: muestra en consola la IP a la que se intenta conectar
        )

        self.connected = True  # Se marca como conectado (sin validar la conexión real todavía)

        print(
            "TCP conectado"
        )

        self.connection_changed.emit(  # Notifica a la interfaz que la conexión está activa
            True
        )

    def disconnect_network(self):
        """Cierra (simula) la conexión de red y notifica el nuevo estado."""
        print(
            "Desconectando red"
        )

        self.connected = False

        self.connection_changed.emit(
            False
        )

    def send(self, data):
        """
        Envía datos al microcontrolador por red.

        NOTA: actualmente solo imprime el dato en consola; no realiza un
        envío real por socket. Pendiente de implementación.

        Args:
            data (str): Datos (normalmente JSON) a enviar.
        """
        print(
            f"TCP TX: {data}"
        )

    def read_once(self):
        """
        Intenta leer una línea de datos entrante y, si es un JSON válido,
        la convierte a diccionario y emite data_received.

        NOTA: este método usa "self.serial", que no existe en esta clase
        (es un atributo de SerialManager, no de TCPManager). Actualmente
        provocaría un AttributeError si se llega a ejecutar en modo Red.
        Pendiente de implementar la lectura real por socket TCP.
        """
        if not self.connected:

            return

        line = (
            self.serial.readline().decode("utf-8").strip()  # ⚠️ "self.serial" no está definido en TCPManager
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