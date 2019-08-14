import sys
from communication import ModbusTcp
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from main_ui import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
    
    def record_on_click(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.run)
        self.timer.start(int(self.lineEdit_cyclical_times.text()))
    
    def stop_on_click(self):
        self.timer.stop()
    
    def run(self):
        sensor = ModbusTcp(self.lineEdit_ip.text(), self.lineEdit_port.text(), self.lineEdit_device_address.text())
        self.data = sensor.read_holding_registers(self.lineEdit_sensor_address.text(), 1)
        print(self.data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    record = MainWindow()
    record.setWindowTitle('TemperatureRecorder')
    record.show()
    sys.exit(app.exec_())