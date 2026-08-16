from PySide6.QtCore import (
    QThread
)

import time

class SerialReaderThread(QThread):

    def __init__(self, serial_manager):

        super().__init__()

        self.serial_manager = serial_manager

        self.running = False

    def run(self):  

        self.running = True

        while self.running:

            self.serial_manager.read_once()

            time.sleep(0.001)

    def stop(self):

        self.running = False

        self.wait()