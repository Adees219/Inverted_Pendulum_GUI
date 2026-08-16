#UNIVERSIDAD DEL VALLE DE GUATEMALA
#Anderson Daniel Eduardo Escobar Sandoval - 21712
#Interfaz gráfica - Proyecto de graduación: Acondicionamiento de un sistema de péndulo invertido 

#documentacion Qt Widgets: https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/index.html
#funciones: https://doc.qt.io/qt-6/functions.html
from PySide6.QtWidgets import QApplication #importa el motor de la interfaz para crear una ventana
from ui.main_window import MainWindow  #de la carpeta "ui" > archivo "main_window" importa la ventana personalizada [MainWindow > clase]

import sys #carga el modulo "sys", permite interactuar directamente con el entorno de ejecución de Python y el sistema operativo

app = QApplication(sys.argv) #clase que adminsitra el flujo de la app y main settings

window = MainWindow()
window.show() #muestra la ventana principal

sys.exit(app.exec()) # app.exec() inicia el bucle de eventos de Qt y devuelve un código de salida (un entero 1 o 0) cuando el bucle termina.
                     #Pasar ese código a sys.exit() garantiza que Python termine con el estado correcto
                     