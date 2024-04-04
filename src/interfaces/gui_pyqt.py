from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

class GUIPyQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Gra w statki - PyQt5')
        self.setGeometry(100, 100, 400, 300)

        # Dodajemy etykietę
        self.label = QLabel('Witaj w grze w statki!', self)
        self.label.setGeometry(100, 100, 200, 30)

        # Dodajemy przycisk
        self.button = QPushButton('Kliknij mnie!', self)
        self.button.setGeometry(100, 150, 200, 30)
        self.button.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        self.label.setText('Przycisk został kliknięty!')

def main():
    app = QApplication([])
    gui = GUIPyQt()
    gui.show()
    app.exec_()

if __name__ == "__main__":
    main()
