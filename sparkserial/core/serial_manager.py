import serial
import serial.tools.list_ports
from PyQt6.QtCore import QThread, pyqtSignal, QObject
import time

class SerialWorker(QObject):
    data_received = pyqtSignal(bytes)
    error_occurred = pyqtSignal(str)
    connection_status = pyqtSignal(bool)

    def __init__(self, port_name, baudrate, bytesize, parity, stopbits, flowcontrol):
        super().__init__()
        self.port_name = port_name
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.flowcontrol = flowcontrol
        self.serial_port = None
        self.running = False

    def run(self):
        try:
            self.serial_port = serial.Serial(
                port=self.port_name,
                baudrate=self.baudrate,
                bytesize=self.bytesize,
                parity=self.parity,
                stopbits=self.stopbits,
                xonxoff=False,
                rtscts=self.flowcontrol == "Hardware (RTS/CTS)",
                dsrdtr=False,
                timeout=0.1
            )
            self.running = True
            self.connection_status.emit(True)

            while self.running:
                if self.serial_port.in_waiting > 0:
                    data = self.serial_port.read(self.serial_port.in_waiting)
                    if data:
                        self.data_received.emit(data)
                time.sleep(0.01)

        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()
            self.connection_status.emit(False)

    def stop(self):
        self.running = False

    def send_data(self, data):
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.write(data)
            except Exception as e:
                self.error_occurred.emit(str(e))

class SerialManager(QObject):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.thread = None

    def get_available_ports(self):
        return [port.device for port in serial.tools.list_ports.comports()]

    def connect(self, settings):
        if self.thread and self.thread.isRunning():
            return

        self.thread = QThread()
        self.worker = SerialWorker(
            settings['port'],
            settings['baudrate'],
            settings['bytesize'],
            settings['parity'],
            settings['stopbits'],
            settings['flowcontrol']
        )
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.run)
        self.worker.connection_status.connect(self._handle_status)
        
        self.thread.start()
        return self.worker

    def disconnect(self):
        if self.worker:
            self.worker.stop()
        if self.thread:
            self.thread.quit()
            self.thread.wait()

    def _handle_status(self, status):
        if not status:
            self.disconnect()
