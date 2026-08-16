# Esta clase muestra los gráficos de "angulo" y "esfuerzo de control" para el controlador PID perteneciente a la pestaña 
# "pid_tab"

from PySide6.QtWidgets import (
    QWidget,
    QGridLayout
)

from plots.live_plot import LivePlot

class PIDPlots(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        layout = QGridLayout()

        self.angle_plot = LivePlot(
            "Ángulo",
            "grados"
        )

        self.control_plot = LivePlot(
            "Esfuerzo de Control",
            "PWM"
        )

        layout.addWidget(
            self.angle_plot,
            0,      #fila
            0       #columna
        )

        layout.addWidget(
            self.control_plot,
            1,
            0
        )

        self.setLayout(
            layout
        )

    def update_plots(
        self,
        angle,
        control_effort
    ):

        self.angle_plot.update(
            angle
        )

        self.control_plot.update(
            control_effort
        )