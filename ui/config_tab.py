from PySide6.QtWidgets import ( #importando librerias de Qt
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGroupBox,
    QRadioButton,
    QButtonGroup,
    QMessageBox
)

from ui.utils.widget_style import * # funciones para definir dimensiones/colores/font de los widgets

from ui.constants.ui_constants import(
    STATUS_GREEN,
    STATUS_RED,
    STATUS_YELLOW
)

from PySide6.QtGui import ( #validadores de texto
    QIntValidator,
    QDoubleValidator
)

from models.config_model import ConfigModel

class ConfigTab(QWidget):


    def __init__(self, connection_manager):


        super().__init__()


        self.connection_manager = (
            connection_manager
        ) #llama a la clase que hace la comunicacion.
        

        self.connection_manager.connection_changed.connect( #cuando cambia el estado de conexion en "serial_manager"
            self.update_connection_status   #actualiza el estado el estado por el actual.
        )

        self.connection_manager.serial_manager.connection_error.connect(
            self.show_connection_error
        )

        self.config = ConfigModel() #referencia a la clase de config_model

        self.setup_ui() #llama a la funcion que hace el apartado grafico.


    def setup_ui(self):


        # Layout principal
        main_layout = QVBoxLayout() #layout vertical → "V"

        # =========================================================================================================================
        #                                                      metodo de conexion
        # ========================================================================================================================
        conec_group = QGroupBox("Método de Conexión")
        

        conec_form = QFormLayout()
        radio_layout = QHBoxLayout()

        #radio botton para seleccionar el metodo de conexion
        self.serial_radio = QRadioButton("Serial")
        self.network_radio = QRadioButton("Red")

        #agregando al layout del grupo
        radio_layout.addWidget(
            self.serial_radio
        )

        radio_layout.addWidget(
            self.network_radio
        )

        radio_widget = QWidget()
        radio_widget.setLayout(
            radio_layout
        )

        self.connection_status = QLabel( #etiqueta que avisa el estado de conexion
            
        )

        set_status(self.connection_status,"● Desconectado", STATUS_RED)
      
        conec_form.addRow(
           "Estado",
            self.connection_status
        )

        conec_form.addRow(
            "Modo:",
            radio_widget
        )

        conec_group.setLayout(
            conec_form
        )


        
        # ==================================================================================================================================
        #                                                            RED/Internet (TCP/IP)
        # ==================================================================================================================================
        
        self.TCP_group = QGroupBox("TCP/IP")

        TCP_layout = QFormLayout()

        self.TCP_label = QLabel(
            "192.168.12.XX"
        )

        self.TCP_Equipo = QLineEdit() 

        self.TCP_boton = QPushButton(
            "Conectar"
        )

        self.TCP_boton.clicked.connect(
            self.handle_connect
        )

        TCP_layout.addRow(
            "Dirección IP:",
            self.TCP_label
        )

        TCP_layout.addRow(
            "No. Equipo:",
            self.TCP_Equipo
        )

        TCP_layout.addRow(
            self.TCP_boton
        )

        self.TCP_group.setLayout(
            TCP_layout
        )

        # ==================================================================================================================================
        #                                                               Puerto COM
        # ==================================================================================================================================

        self.com_group = QGroupBox("Serial") #crea un borde que delimita los elementos

        com_layout = QFormLayout() #layout horizontal → "H"


        self.com_combo = QComboBox() #cuadro de opciones

        ports = (
            self.connection_manager #habla con el connection manager
            .serial_manager #se va directo al apartado de com serial
            .get_available_ports() #obtiene los puertos
        ) #obtiene los puertos obtenidos del archivo "serial_manager"

        self.com_combo.addItems( #agrega los puertos al cuadro de opciones
            ports
        )


        self.refresh_button = QPushButton(
            "Actualizar"
        )

        self.refresh_button.clicked.connect( #conecta el boton a la funcion de actializar los puertos
            self.refresh_ports
        )


        self.serial_button = QPushButton( #boton de conectar
            "Conectar"
        )

        self.serial_button.clicked.connect( # se conecta el boton a la funcion de conexion
            self.handle_connect
        )


        #agregando los elementos al layout del grupo com

        com_layout.addRow(
            "Puerto COM",
            self.com_combo
        )

        com_layout.addRow(
            self.refresh_button
        )

        com_layout.addRow(
            self.serial_button
        )

        self.com_group.setLayout(
            com_layout
        )

        # ========================================================================================================================
        #                                                 Configuración general
        # ========================================================================================================================

        config_group = QGroupBox( #borde
            "Configuración"
        )

        form_layout = QFormLayout() #organiza automaticamente los elementos

        self.amperaje = QLineEdit() #cuadro texto

        self.microstep = QComboBox()

        self.microstep.addItems(
            ["128", "64", "32", "16", "8", "4", "2", "1"] #disponibles TMC2209: 128, 64, 32, 16, 8, 4, 2, FULLSTEP
        )

        #estableciendo "16" como microstep predeterminada
        self.microstep.setCurrentIndex(3)

        self.velocidad_maxima = QLineEdit()

        self.aceleracion = QLineEdit()

        self.control_period_us = QLineEdit()

        self.telemetry_period_ms = QLineEdit()

        self.offset_AS5600 = QLineEdit()

        
    #************************************** Valores predeterminados *************************************
        self.amperaje.setText(
            "800" #mA / max motor 17HD40005H-22B: 1.6 A
        )

        self.velocidad_maxima.setText(
            "32000" # N-mm / max: ±32000
        )

        self.aceleracion.setText(
            "150000" #N-mm^2
        )

        self.control_period_us.setText(
            "1000" # us
        )

        self.telemetry_period_ms.setText(
            "20" # ms
        )

        self.offset_AS5600.setText(
            "283" #°
        )

    #************************************** Validadores de texto *************************************
        self.amperaje.setValidator( #valida que sea un entero y rango de valores
            QIntValidator(
                300,
                1600
            )
        )

        self.velocidad_maxima.setValidator(
            QIntValidator(
                300,
                100000
            )
        )

        self.aceleracion.setValidator(
            QIntValidator(
                300,
                150000
            )
        )

        self.offset_AS5600.setValidator(
            QDoubleValidator(
                0.0,
                360,
                3
            )
        )

        self.control_period_us.setValidator(
            QIntValidator(
                500,
                100000
            )
        )

        self.telemetry_period_ms.setValidator(
            QIntValidator(
                10,
                1000
            )
        )

    #****************************************************************************************************

        # agregando los elementos al layout del grupo

        form_layout.addRow(
            "Amperaje (mA)",
            self.amperaje
        )

        form_layout.addRow(
            "Microstep",
            self.microstep
        )

        form_layout.addRow(
            "Velocidad Máxima",
            self.velocidad_maxima
        )

        form_layout.addRow(
            "Aceleración",
            self.aceleracion
        ) 

        form_layout.addRow(
            "Período de control (µs)",
            self.control_period_us
        )

        form_layout.addRow(
            "Período de Telemetría (ms)",
            self.control_period_us
        )

        form_layout.addRow(
            "Offset AS5600",
            self.offset_AS5600
        )

        self.modify_button = QPushButton(
            "Guardar Configuración"
        )

        self.modify_button.clicked.connect(
            self.save_config
        )

        form_layout.addRow(
            self.modify_button
        )

        config_group.setLayout(
            form_layout
        )


        #************************************** juntando cuadros de conexion *******************************
        layout_tipos_conexiones = QHBoxLayout()

        layout_tipos_conexiones.addWidget(
                self.com_group,
                1 #es para indicar que el widget ocupa 1 parte, sirve para el tamaño del cuadro
        )          # es lo mismo a decir 50% (para este caso donde solo hay 2 cuadros)

        layout_tipos_conexiones.addWidget(
               self.TCP_group,
               1
        )
        
        # ========================================================================================================
        #                                          Widgets style
        # ========================================================================================================

        # QlineEdits & QComboBox 
       
        set_control_height(

            self.amperaje,

            self.microstep,

            self.velocidad_maxima,

            self.aceleracion,

            self.control_period_us,

            self.telemetry_period_ms,

            self.offset_AS5600,

            self.com_combo,

            self.TCP_Equipo
        )

        # QPushButton
        set_primary_button(self.modify_button)
        set_secondary_button(
            self.TCP_boton,
            self.refresh_button,
            self.serial_button
            
        )
        
        # espaciado y margen de ventana
        configure_layout(
            main_layout
        )

        configure_sub_layout(
            layout_tipos_conexiones
        )

        # ========================================================================================================
        #                                          Agregar al layout principal
        # ========================================================================================================
        #nota: anteriormente se crearon los gruposy sus objetos al layout de cada grupo
        #PERO en ningun momento se esta mostrando en la ventana principal, esto solo
        #se  puede hacer mediante el layout del mainwindow > "main_layout"

        main_layout.addWidget(
            conec_group
        )

        main_layout.addLayout(
            layout_tipos_conexiones
        )

        main_layout.addWidget(
            config_group
        )

        main_layout.addStretch() #empuja todo hacia arriba

        self.setLayout(
            main_layout
            
        )

        #**************************** habilitar/deshabilitar grupos *******************************
        self.serial_radio.setChecked(True) #valor predefinido

        #al marcar la seleccion del radio button llama a la funcion
        self.serial_radio.toggled.connect(
            self.actualizar_metodo_conexion
        )

        self.network_radio.toggled.connect(
            self.actualizar_metodo_conexion
        )

        self.actualizar_metodo_conexion()
        #********************************************************************************************************


    def actualizar_metodo_conexion(self): #selecciona el metodo de conexion para el microcontrolador
        

        if self.serial_radio.isChecked():

            self.com_group.setEnabled(True)

            self.TCP_group.setEnabled(False)

        else:

            self.com_group.setEnabled(False)

            self.TCP_group.setEnabled(True)


    def handle_connect(self): #realiza la conexion/desconexion del puerto designado

        if not self.connection_manager.connected: #si no se encuentra conectado a ningun puerto
            
            if self.serial_radio.isChecked():
            
                self.connection_manager.set_mode( # manda a connection_manager la opcion serial
                    self.connection_manager.SERIAL
                )

                target = (
                    self.com_combo.currentText() #obtiene el puerto elegido del cudro de opciones
                )

            else:
                
                self.connection_manager.set_mode( #modo
                    self.connection_manager.NETWORK
                )

                equipo = (
                    self.TCP_Equipo.text() #No. dispositivo a conectar
                )

                target = (
                    f"192.168.12.{equipo}" # direccion IP completa del equipo
                )


            self.connection_manager.connect( #manda a conectar el equipo> connection manager determina el metodo y manda a llamar segun el caso
                target
            )

        else:

            self.connection_manager.disconnect()
 

    def refresh_ports(self):    #actualiza los puertos encontrados

        self.com_combo.clear()

        ports = (
            self.connection_manager
            .get_available_ports()
        )

        self.com_combo.addItems(
            ports
        )


    def update_connection_status(self,connected):   #cambia el estado de indicadores visuales relacionados a la conexion

        if connected:

            set_status(self.connection_status,"● Conectado", STATUS_GREEN)

            self.serial_button.setText( #cambia el texto del boton (conectar/desconectar)
                "Desconectar"
            )

            self.TCP_boton.setText(
                "Desconectar"
            )

            self.com_combo.setEnabled(False) #deshabilita el menu de puertos (previene cambiar de puerto mientras se usa el micro)
            self.TCP_Equipo.setEnabled(False)

        else:

            set_status(self.connection_status,"● Desconectado", STATUS_RED)

            self.serial_button.setText(
                "Conectar"
            )

            self.TCP_boton.setText(
                "Conectar"
            )

            self.com_combo.setEnabled(True)
            self.TCP_Equipo.setEnabled(True)


    def show_connection_error(self, message):
        QMessageBox.critical(self,"Error de conexión", message)


    def save_config(self): #hace el envio de configuraciones de actuadores al esp32
        
        #Amperaje
        if not self.amperaje.hasAcceptableInput(): #valida que el dato se encuentre en los parametros definidos> sino envia alerta
            QMessageBox.warning(
                self,
                "Amperaje Invalido",
                "Valores permitidos: 300 - 1600 mA"
            )
            return
        self.config.amperaje = int(
            self.amperaje.text()
        )

        #Microstep
        self.config.microstep = int(
            self.microstep.currentText()
        )

        #Vel. Max
        if not self.velocidad_maxima.hasAcceptableInput():
            QMessageBox.warning(self,"Velocidad Máxima Invalida","Valores permitidos: 300 - 100000 steps/s")
            return
        self.config.velocidad_maxima = int(
            self.velocidad_maxima.text()
        )

        #Aceleracion
        if not self.aceleracion.hasAcceptableInput():
            QMessageBox.warning(self, "Aceleracion Invalida","Valores permitidos: 300 - 150000 steps/s^2")
            return
        self.config.aceleracion = int(
            self.aceleracion.text()
        )

        #t_muestreo
        if not self.control_period_us.hasAcceptableInput():
            QMessageBox.warning(self,"Período de Control Inválido", "Ingrese un período de control válido.")           
            return
        self.config.control_period_us= int(
            self.control_period_us.text()
        )

        if not self.telemetry_period_ms.hasAcceptableInput():
            QMessageBox.warning(self,"Período de Telemetría Inválido", "Ingrese un período de telemetría válido.")           
            return
        self.config.telemetry_period_ms = int(
            self.telemetry_period_ms.text()
        )

        #offset angular AS5600
        if not self.offset_AS5600.hasAcceptableInput():
            QMessageBox.warning(self,"Offset Del Sensor Invalido","Valores permitidos: 0.0 - 360.00 grados")
            return
        self.config.offset_AS5600 = float(
            self.offset_AS5600.text()
        )


        #envio de datos

        self.connection_manager.send_model(
            self.config
        )

        print(
        self.config.to_json()
)
        