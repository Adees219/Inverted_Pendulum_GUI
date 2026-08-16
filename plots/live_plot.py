# esta clase se encarga de crear los gráficos de cualquier variable bajo los parametros dados

from collections import deque

from PySide6.QtWidgets import (
    QWidget,    
    QVBoxLayout
)

import pyqtgraph as pg

from ui.constants.ui_constants import (
    PLOT_BUFFER_SIZE,
    GRAPH_MIN_HEIGHT
)

class LivePlot(QWidget):

    def __init__(
        self,
        title,
        ylabel,
        max_samples=PLOT_BUFFER_SIZE #muestras maximas del buffer
    ):

        super().__init__()

        self.buffer = deque(maxlen = max_samples) #buffer graficos

        self.setup_ui(title,ylabel)


    def setup_ui(self,title,ylabel):

        self.plot = pg.PlotWidget()  # objetos/widgets de tipo pyqtgraph

        self.plot.setTitle(title)   # titulo del grafico

        self.plot.setLabel( # titulo eje y
            "left",
            ylabel
        )

        self.plot.setLabel( # titulo eje x
            "bottom",
            "Muestras"
        )

        self.plot.showGrid( # cuadricula
            x=True,
            y=True
        )

        self.curve = self.plot.plot(  #creacion de curvas (linea)
            pen="y"
        )


        # agregando al layout

        self.setMinimumHeight(
            GRAPH_MIN_HEIGHT
        )

        layout = QVBoxLayout()

        layout.addWidget(  
            self.plot
        )

        self.setLayout(layout)


    def update(
            self,
            value
    ):

        self.buffer.append(
            value
        )

        self.curve.setData(
            list(self.buffer)
        )