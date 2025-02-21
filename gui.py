from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
import sys

class VoiceAssistantApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel("Click to Start Listening", self)
        self.button = QPushButton("Start", self)
        self.button.clicked.connect(self.start_listening)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.setWindowTitle("Voice Assistant")
        self.show()

    def start_listening(self):
        self.label.setText("Listening...")  # Call your voice assistant function here

app = QApplication(sys.argv)
window = VoiceAssistantApp()
sys.exit(app.exec_())
