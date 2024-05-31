from PyQt5.QtWidgets import QApplication
from src.interfaces.gui_pyqt import GUIPyQt
from src.game_logic import GameLogic

def main():
    app = QApplication([])

    # Inicjalizacja logiki gry
    #game_logic = GameLogic()

    # Inicjalizacja interfejsu użytkownika
    gui = GUIPyQt()
    gui.show()

    # Rozpoczęcie pętli głównej
    app.exec_()

if __name__ == "__main__":
    main()
