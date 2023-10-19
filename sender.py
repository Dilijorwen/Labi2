from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit
import socket
import sys


class SenderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sender Window")
        self.setGeometry(100, 100, 400, 200)

        self.button = QPushButton("Send Signal", self)
        self.button.setGeometry(150, 130, 100, 30)
        self.button.clicked.connect(self.send_signal)

        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(100, 50, 200, 30)
        self.textbox.setText("")

    def send_signal(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.textbox.text(), 12345))
        self.socket.sendall(b"signal")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    receiver_window = SenderWindow()
    receiver_window.show()
    sys.exit(app.exec())