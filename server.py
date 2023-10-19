import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import socket


class ReceiverThread(QThread):
    signal_received = pyqtSignal()

    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    def run(self):
        while True:
            data = self.connection.recv(1024)
            if data == b"signal":
                self.signal_received.emit()
                break


class ReceiverWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Receiver Window")
        self.setGeometry(0, 0, 325, 75)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, 0, 1000, 750)

        self.ip_input = QLineEdit(self)
        self.ip_input.setGeometry(10, 10, 200, 30)

        self.start_button = QPushButton("Start Server", self)
        self.start_button.setGeometry(220, 10, 100, 30)
        self.start_button.clicked.connect(self.start_server)

        self.socket = None
        self.connection = None
        self.address = None
        self.receiver_thread = None

    def start_server(self):
        ip = self.ip_input.text()
        if ip:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((ip, 12345))
            self.socket.listen(1024)
            self.connection, self.address = self.socket.accept()

            self.receiver_thread = ReceiverThread(self.connection)
            self.receiver_thread.signal_received.connect(self.show_image)
            self.receiver_thread.start()
            self.start_button.hide()
            self.ip_input.hide()

    def show_image(self):
        pixmap = QPixmap("banana.jpeg")
        self.label.setPixmap(pixmap.scaled(1000, 750, Qt.AspectRatioMode.KeepAspectRatio))
        self.label.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    receiver_window = ReceiverWindow()
    receiver_window.show()
    sys.exit(app.exec())