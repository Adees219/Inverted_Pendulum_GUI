# Esta clase muestra los gráficos de las variables de estados para el controlador por retroalimentacion de estado perteneciente a la pestaña 
# "state_tab"

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout
)

from plots.live_plot import LivePlot

class StatePlots(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()


    def setup_ui(self):


        layout = QGridLayout()

        # mandar a crear la grafica

        self.angle_plot = LivePlot(
            "Ángulo",
            "grados"
        )

        self.angular_plot = LivePlot(
            "Velocidad angular",
            "grados/s"
        )

        self.position_plot = LivePlot(
            "Posición",
            "mm"
        )

        self.linear_plot = LivePlot(
            "Velocidad lineal",
            "mm/s"
        )

        #agregando al layout

        layout.addWidget(
            self.angle_plot,
            0,
            0
        )

        layout.addWidget(
            self.angular_plot,
            0,
            1
        )

        layout.addWidget(
            self.position_plot,
            1,
            0
        )

        layout.addWidget(
            self.linear_plot,
            1,
            1
        )

        self.setLayout(layout)


    
    def update_plots(self, state):
        
        self.angle_plot.update(
            state.angle
        )

        self.angular_plot.update(
            state.angular_velocity
        )

        self.position_plot.update(
            state.position
        )

        self.linear_plot.update(
            state.linear_velocity
        )