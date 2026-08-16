from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGroupBox,
    QRadioButton,
    QButtonGroup,
    QMessageBox
)

from ui.utils.widget_style import *

from ui.constants.ui_constants import(
    STATUS_GREEN,
    STATUS_RED,
    STATUS_YELLOW,
    STATUS_ACTIVE,
    STATUS_INACTIVE,
    STATUS_WAITING
)

from PySide6.QtGui import ( # valida entradas de los inputs
    QDoubleValidator 
)

from models.pid_model import PIDModel # valores que recibe el modelo

from plots.pid_plots import PIDPlots

from PySide6.QtCore import QTimer
import math

class PIDTab(QWidget):


    def __init__(self, connection_manager):
        
        
        super().__init__()


        self.pid = PIDModel()

        self.pid_plots = PIDPlots()

        self.connection_manager = (
            connection_manager
        )

        self.setup_ui()

        self.counter = 0

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.simulate_pid
        )

        self.timer.start(50)

    def setup_ui(self):
      # =========================================================================================================================
        #                                                      Distribucion/layout
        # ========================================================================================================================
        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()

        left_layout = QVBoxLayout()

        right_layout = QVBoxLayout()

        bottom_layout = QHBoxLayout()

        top_layout.addLayout(
            left_layout,
            1
        )

        top_layout.addLayout(
            right_layout,
            2
        )

        main_layout.addLayout(
            top_layout
        )

        main_layout.addLayout(
            bottom_layout
        )


        # =========================================================================================================================
        #                                                      equilibrio
        # ========================================================================================================================

        equilibrium_group = QGroupBox(
            "Punto de Equilibrio"
        )

        equilibrium_layout = QVBoxLayout()

        self.down_radio = QRadioButton(
            "Abajo"
        )

        self.up_radio = QRadioButton(
            "Arriba"
        )

        self.down_radio.setChecked(True) #valor predefinido: abajo

        self.mode_group = QButtonGroup() #grupo de botones

        self.mode_group.addButton(
            self.down_radio
        )

        self.mode_group.addButton(
            self.up_radio
        )


        #formulario
        equilibrium_layout.addWidget(
            self.down_radio
        )

        equilibrium_layout.addWidget(
            self.up_radio
        )

        equilibrium_group.setLayout(
            equilibrium_layout
        )
        # =========================================================================================================================
        #                                                      parametros PID
        # ========================================================================================================================
        pid_group = QGroupBox(
            "Parámetros del Controlador PID"
        )

        pid_layout = QFormLayout()

        self.kp = QLineEdit()

        self.ki = QLineEdit()

        self.kd = QLineEdit()

        #valores por defecto

        self.kp.setText("900")

        self.ki.setText("0.1")

        self.kd.setText("0.001")

        #validadores

        validator = QDoubleValidator(
            -100000.0,  #lower limit
            100000.0,   #upper limit
            6           #decimales
        )

        self.kp.setValidator(
            validator
        )

        self.ki.setValidator(
            validator
        )

        self.kd.setValidator(
            validator
        )

        #formulario
        pid_layout.addRow(
            "Kp",
            self.kp
        )

        pid_layout.addRow(
            "Ki",
            self.ki
        )

        pid_layout.addRow(
            "Kd",
            self.kd
        )

        pid_group.setLayout(
            pid_layout
        )
        

        # =========================================================================================================================
        #                                                      Estado
        # ========================================================================================================================
        status_group = QGroupBox(
            "Sistema de Control"
        )

        status_layout = QFormLayout()

        self.control_mode = QLabel(
            "PID"
        )

        self.control_status = QLabel(
            
        )

        set_status(self.control_status,STATUS_INACTIVE, STATUS_RED)

        self.freq_status = QLabel(
            "---- Hz"
        )

        status_layout.addRow(
            "Modo:",
            self.control_mode
        )

        status_layout.addRow(
            "Estado:",
            self.control_status
        )

        status_layout.addRow(
            "Frecuencia:",
            self.freq_status
        )

        status_group.setLayout(
            status_layout
        )

        # =========================================================================================================================
        #                                                      Acciones
        # ========================================================================================================================
        actions_group = QGroupBox("Acciones")

        actions_layout = QHBoxLayout()


        self.apply_button = QPushButton(
            "Guardar Configuración PID"
        )
        
        self.control_button = QPushButton(
            "Activar"
        )

        self.reset_button = QPushButton(
            "Reset"
        )

        self.apply_button.clicked.connect(
            self.save_pid
        )

        actions_layout.addWidget(
            self.apply_button
        )

        actions_layout.addWidget(
            self.control_button
        )

        actions_layout.addWidget(
            self.reset_button
        )

        actions_group.setLayout(
            actions_layout
        )

        # =========================================================================================================================
        #                                                      widget style
        # ========================================================================================================================

        set_control_height(
            self.kp,
            self.ki,
            self.kd
        )

        set_primary_button(
            self.apply_button,
        )

        set_secondary_button(
            
            self.control_button,
            self.reset_button
        )

        configure_layout(
            main_layout
        )

        configure_group_width(
            equilibrium_group
        )

        configure_group_width(
            pid_group
        )

        

        # =========================================================================================================================
        #                                                      aplicar layout
        # ========================================================================================================================
           
        left_layout.addWidget(
            equilibrium_group
        )

        left_layout.addWidget(
            pid_group
        )  

        right_layout.addWidget(
            self.pid_plots
        )

        bottom_layout.addWidget(
            status_group,
            1
        )

        bottom_layout.addWidget(
            actions_group,
            2
        )

        bottom_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        bottom_layout.setSpacing(8)

        self.setLayout(
            main_layout
        )



    def save_pid(self):

        # Ganancias controlador

        if not self.kp.hasAcceptableInput():
            QMessageBox.warning(
                self,
                "Error",
                "Kp inválido"
            )
            return  
        self.pid.kp = float(
            self.kp.text()
        )

        if not self.ki.hasAcceptableInput():
            QMessageBox.warning(
                self,
                "Error",
                "Ki inválido"
            )
            return  
        self.pid.ki = float(
            self.ki.text()
        )

        if not self.kd.hasAcceptableInput():
            QMessageBox.warning(
                self,
                "Error",
                "Kd inválido"
            )
            return  
        self.pid.kd = float(
            self.kd.text()
        )

        # modo/posicion pendulo

        if self.down_radio.isChecked():
            self.pid.mode = (
                PIDModel.DOWN
            )

        else:
            self.pid.mode = (
                PIDModel.UP
            )

        # enviar json

        print(self.pid.to_json())

        self.connection_manager.send_model(
            self.pid
        )


    def simulate_pid(self):

        self.counter += 1

        t = self.counter / 15

        angle = 15 * math.sin(t)

        control = (
            1000 * math.sin(t)
            +
            150 * math.sin(4*t)
        )

        self.pid_plots.update_plots(
            angle,
            control
        )
        