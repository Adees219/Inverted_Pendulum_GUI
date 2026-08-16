from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFormLayout,
    QGroupBox,
    QLineEdit, 
    QHBoxLayout,
    QGridLayout,
    QPushButton
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

from plots.state_plots import(
    StatePlots
)

#TEMPORAL> simulacion datos
from PySide6.QtCore import(
    QTimer
)
import math

class StateTab(QWidget):

    def __init__(self, connection_manager, state_model):


        super().__init__()


        self.state_plots = StatePlots()

        self.connection_manager = connection_manager

        self.state = state_model

        self.setup_ui()

        #timer
        self.timer = QTimer()

    #     self.timer.timeout.connect(
    #         self.simulate_data
    #     )

    #    # self.timer.start(100)
    #     self.counter = 0

        


    def setup_ui(self): #distribucion visual
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
        #                                                      Variables de estado
        # ========================================================================================================================

        state_group = QGroupBox(
            "Variables de Estado"
        )

        state_layout = QFormLayout()

        self.angle_label = QLabel(
            "0.00 °"
        )

        self.angular_velocity_label = QLabel(
            "0.00 °/s"
        )

        self.position_label = QLabel(
            "0.00 mm"
        )

        self.linear_velocity_label = QLabel(
            "0.00 mm/s"
        )

        state_layout.addRow(
            "Ángulo:",
            self.angle_label
        )

        state_layout.addRow(
            "Vel. Angular:",
            self.angular_velocity_label
        )

        state_layout.addRow(
            "Posición:",
            self.position_label
        )

        state_layout.addRow(
            "Vel. Lineal:",
            self.linear_velocity_label
        )

        state_group.setLayout(
            state_layout
        )

        # =========================================================================================================================
        #                                                      Ganancias
        # ========================================================================================================================

        gains_group = QGroupBox(
            "Ganancias del Controlador"
        )

        gains_layout = QGridLayout()

        #inputs
        self.k1 = QLineEdit()
        self.k2 = QLineEdit()
        self.k3 = QLineEdit()
        self.k4 = QLineEdit()

        # valores predeterminados/iniciales
        self.k1.setText("0.0")
        self.k2.setText("0.0")
        self.k3.setText("0.0")
        self.k4.setText("0.0")

        #layout
        gains_layout.addWidget(
            QLabel("K1"),
            0,0
        )
        gains_layout.addWidget(
            self.k1,
            0,1
        )

        gains_layout.addWidget(
            QLabel("K2"),
            0,2
        )
        gains_layout.addWidget(
            self.k2,
            0,3
        )

        gains_layout.addWidget(
            QLabel("K3"),
            1,0
        )
        
        gains_layout.addWidget(
            self.k3,
            1,1
        )
        
        gains_layout.addWidget(
            QLabel("K4"),
            1,2
        )
        
        gains_layout.addWidget(
            self.k4,
            1,3
        )

        gains_group.setLayout(
            gains_layout
        )

        # =========================================================================================================================
        #                                                      Ganancias
        # ========================================================================================================================

        reference_group = QGroupBox(
            "Referencia del Carro"
        )        

        reference_layout = QFormLayout()

        self.reference = QLineEdit()

        reference_layout.addRow(
            "Posición Objetivo (mm)",
            self.reference
        )

        reference_group.setLayout(
            reference_layout
        )

         # =========================================================================================================================
        #                                                      status
        # ========================================================================================================================

        status_group = QGroupBox(
            "Sistema de Control"
        )

        status_layout = QFormLayout()

        self.control_mode = QLabel(
            "Estado"
        )

        status_layout.addRow(
            "Modo:",
            self.control_mode
        )

        self.control_status = QLabel(
            "● Inactivo"
        )

        set_status(self.control_status,STATUS_INACTIVE, STATUS_RED)

        self.last_update = QLabel(
            "---"
        )

        status_layout.addRow(
            "Estado:",
            self.control_status
        )

        status_layout.addRow(
            "Última actualización",
            self.last_update
        )

        status_group.setLayout(
            status_layout
        )

        # =========================================================================================================================
        #                                                      Controlador
        # ========================================================================================================================
        
        controller_group = QGroupBox(
            "Controlador"
        )

        controller_layout = QVBoxLayout()

        self.update_button = QPushButton(
            "Guardar Configuración"
        )

        buttons_layout = QHBoxLayout() #layout secundario

        self.control_button = QPushButton(
            "Activar Control"
        )

        self.reset_button = QPushButton(
            "Reset"
        )

        buttons_layout.addWidget(
            self.control_button
        )

        buttons_layout.addWidget(
            self.reset_button
        )

        controller_layout.addWidget(
            self.update_button
        )

        controller_layout.addLayout(
            buttons_layout
        )

        controller_group.setLayout(
            controller_layout
        )

        # =========================================================================================================================
        #                                                      widget style
        # ========================================================================================================================

        set_control_height(
            self.k1,
            self.k2,
            self.k3,
            self.k4,
            self.reference
        )

        set_primary_button(
            self.update_button
        )

        set_secondary_button(
            
            self.control_button,
            self.reset_button
        )

        configure_layout(
            main_layout
        )

        

         # =========================================================================================================================
        #                                                      aplicar layout
        # ========================================================================================================================
         

        left_layout.addWidget(
            state_group
        )

        left_layout.addWidget(
            gains_group
        )

        left_layout.addWidget(
            reference_group
        )

        left_layout.addStretch()

        right_layout.addWidget(
            self.state_plots
        )

        

        bottom_layout.addWidget(
            status_group,
            1
        )

        bottom_layout.addWidget(
            controller_group,
            2
        )

        self.setLayout(
            main_layout
        )

         # =========================================================================================================================
        #                                               actualizacion de valores
        # ========================================================================================================================

        self.update_ui()
         

    def update_ui(self): #actualiza los valores de los labels acorde a las variables de estado obtenidas

        self.angle_label.setText(
            f"{self.state.angle:.2f} °"
        )

        self.angular_velocity_label.setText(
            f"{self.state.angular_velocity:.2f} °/s"
        )

        self.position_label.setText(
            f"{self.state.position:.2f} mm"
        )

        self.linear_velocity_label.setText(
            f"{self.state.linear_velocity:.2f} mm/s"
        )

    # def simulate_data(self):

    #     self.counter+=1
    #     t = self.counter/10
        
    #     self.state.angle = ( 
    #         20* math.sin(t)
    #     )

    #     self.state.angular_velocity = (
    #         20 * math.cos(t)
    #     )

    #     self.state.position = (
    #         200 * math.sin(t/2)
    #     )

    #     self.state.linear_velocity = (
    #         100 * math.cos(t/2)
    #     )

    #     self.refresh()


    def refresh(self):

        self.update_ui()
        
        self.state_plots.update_plots(
            self.state
        )