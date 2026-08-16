from PySide6.QtWidgets import (
    QMainWindow, #provides a main application window.
    QWidget,    #Returns the menu bar for the main window
    QTabWidget, #Adds a tab with the given page, icon, and label to the tab widget, and returns the index of the tab in the tab bar.
    QVBoxLayout #lines up widgets vertically.
)

from PySide6.QtGui import QIcon

#importacion de las clases (entornos) para cada ventana
from ui.config_tab import ConfigTab # ui pestaña config
from ui.pid_tab import PIDTab       # ui pestaña PID
from ui.state_tab import StateTab   # ui pestaña controlador de estados
from comunicacion.connection_manager import ( #gestionador de metodo de conexion 
    ConnectionManager
)
from models.state_model import StateModel

class MainWindow(QMainWindow): #genera una ventana principal

    def __init__(self): #definition for the constructor method in a Python class. It acts as an initializer that is automatically called as soon 
                        #as you create (instantiate) a new object. It is used to set initial values and prepare the object for use.


        super().__init__() #cada vez que se cree una instancia de la clase se ejecutar este codigo

         # =========================================================================================================================
        #                                                 Coordinacion de actividades
        # ========================================================================================================================

        # gestor de conexion 
        self.connection_manager = ConnectionManager()

        #gestores de informacion
        self.state_model = StateModel()

        self.connection_manager.data_received.connect( 
            self.process_received_data
        )


        # =========================================================================================================================
        #                                                     Ventana
        # ========================================================================================================================

        # titulo de la app
        self.setWindowTitle( 
            "Control de Péndulo Invertido"
        )

        self.setWindowIcon(
            QIcon("resources/icon.png")
        )

        # dimensionamiento de ventana inicial
        self.resize(900, 400) 

        #contenedor central: contiene los botones/tabs/graficos
        self.central_widget = QWidget() #nota: los objetos no los contiene la ventana, sino el contenedor
        self.setCentralWidget( #Se establece que todo lo que se va a generar, será parte de este widget
            self.central_widget
        )


        #disposicion grafica vertical. layout: distribución espacial de elementos 
        self.layout = QVBoxLayout() 

        self.central_widget.setLayout( #se asigna el layout (organizador) al widget
            self.layout 
        )


        #permite crear las pestañas/ventanas
        self.tabs = QTabWidget() 

        self.layout.addWidget( #se agregan las pestañas al layout
            self.tabs
        )

        # pestañas/ventanas 

        self.config_tab = ConfigTab(
            self.connection_manager
        ) # importa clase pestaña de configuracion

        self.pid_tab = PIDTab(
            self.connection_manager
        )       # importa clase pestaña de controlador PID

        self.state_tab = StateTab(
            self.connection_manager,
            self.state_model
        )   # importa clase  pestaña de controlador por variables de estado.

        #crea las pestañas y las muestra arriba de la main window
        self.tabs.addTab(
            self.config_tab,
            "Configuración"
        )
        

        self.tabs.addTab(
            self.pid_tab,
            "Control PID"
        )

        self.tabs.addTab(
            self.state_tab,
            "Control por Retroalimentación de Estado"
        )

    # recibe, gestiona y actualiza la informacion 
    def process_received_data(self, data):

        print(data)

        self.state_model.angle = data["d1"]
        
        self.state_model.angular_velocity = data["d2"]

        self.state_model.position = data["d3"]

        self.state_model.linear_velocity = data["d4"]

        self.state_tab.refresh()

       