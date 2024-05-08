from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont

class GameWindow(QMainWindow):
    def __init__(self, game_logic):
        super().__init__()
        self.game_logic = game_logic
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Battleship Game - Player Mode')
        self.setFixedSize(QSize(800, 600))

        grid_layout = self.createGrid()

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(grid_layout)

        self.show()

    def createGrid(self):
        # Tworzymy layouty
        main_layout = QVBoxLayout()
        grid_layout = QHBoxLayout()

        #grid_layout.setSpacing(0)

        for i in range(1, 12):
            row_layout = QVBoxLayout()
            for j in range(1, 12):
                if i == 1 and j == 1:
                    label = QLabel("", self)
                    label.setAlignment(Qt.AlignCenter)
                elif i == 1:
                    label = QLabel(chr(64 + j - 1), self)
                    label.setAlignment(Qt.AlignCenter)
                elif j == 1:
                    label = QLabel(str(i - 1), self)
                    label.setAlignment(Qt.AlignCenter)
                else:
                    label = QPushButton("", self)
                    label.setStyleSheet("border: 1px solid black;")
                    label.clicked.connect(lambda state, i=i, j=j: self.gridButtonClicked(i, j))  # Połącz funkcję z przyciskiem
                label.setFixedSize(QSize(40, 40))
                row_layout.addWidget(label)
            grid_layout.addLayout(row_layout)

        main_layout.addLayout(grid_layout)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Dodajemy przestrzeń na dole

        self.position_label = QLabel("", self)
        self.position_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.position_label)

        # Dodajemy przyciski orientacji statku
        orientation_layout = QHBoxLayout()
        orientation_layout.addStretch(1)
        vertical_button = QPushButton("Vertical", self)
        vertical_button.clicked.connect(self.setVerticalOrientation)
        orientation_layout.addWidget(vertical_button)
        horizontal_button = QPushButton("Horizontal", self)
        horizontal_button.clicked.connect(self.setHorizontalOrientation)
        orientation_layout.addWidget(horizontal_button)
        orientation_layout.addStretch(1)
        main_layout.addLayout(orientation_layout)

        # Dodajemy przycisk "Set"
        set_button = QPushButton("Set", self)
        set_button.clicked.connect(self.setShip)
        main_layout.addWidget(set_button)

        # Dodajemy przyciski statków
        ship_buttons_layout = QHBoxLayout()
        #ship_buttons_layout.addStretch(1)  # Dodajemy przestrzeń na początku
        ship_buttons_layout.addWidget(self.createShipButton('Carrier: 5', 5))
        ship_buttons_layout.addWidget(self.createShipButton('Battleship: 4', 4))
        ship_buttons_layout.addWidget(self.createShipButton('Cruiser: 3', 3))
        ship_buttons_layout.addWidget(self.createShipButton('Submarine: 3', 3))
        ship_buttons_layout.addWidget(self.createShipButton('Destroyer: 2', 2))
        main_layout.addLayout(ship_buttons_layout)

        return main_layout

    def createShipButton(self, ship_name, size):
        button = QPushButton(ship_name)
        button.setFixedSize(QSize(100, 30))
        button.setStyleSheet("background-color: lightgray; border: 1px solid black;")
        button.setToolTip(f"Size: {size}")
        button.clicked.connect(lambda state, ship=ship_name: self.shipButtonClicked(ship))
        return button
    
    def shipButtonClicked(self, ship_name):
        self.selected_ship = ship_name
        self.game_logic.set_ship_placement_mode(True)
        self.position_label.setText(f"Choose position for: {ship_name}")
    
    # def chooseShip(self, ship_name):
    #     self.selected_ship = ship_name
    #     self.info_label.setText(f"Choose position for: {ship_name}")

    def setVerticalOrientation(self):
        self.orientation = "vertical"

    def setHorizontalOrientation(self):
        self.orientation = "horizontal"

    def gridClicked(self, event):
        if hasattr(self, 'selected_ship') and self.selected_ship:
            self.game_logic.place_ship(self.selected_ship, 1, 1, 'H')  # Przykładowe współrzędne i kierunek
            self.position_label.setText("")
            self.game_logic.set_ship_placement_mode(False)
            self.selected_ship = None

    def setShip(self):
        if hasattr(self, 'selected_ship'):
            # Tutaj zatwierdź ustawienie statku na planszy
            pass

class GUIPyQt(QMainWindow):
    def __init__(self, game_logic):
        super().__init__()
        self.game_logic = game_logic
        self.initUI()
        self.game_window = None

    def initUI(self):
        self.setWindowTitle('Battleship Game - PyQt5')
        self.setFixedSize(QSize(800, 600))

        self.label = QLabel('Welcome to the Battleship Game!', self)
        self.label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setGeometry(200, 200, 400, 30)

        self.label = QLabel('Choose game mode', self)
        self.label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setGeometry(300, 240, 200, 30)

        # Dodajemy przycisk
        self.button1 = QPushButton('1 player', self)
        self.button1.setGeometry(240, 280, 150, 50)
        self.button1.clicked.connect(self.button1Clicked)

        self.button2 = QPushButton('2 players', self)
        self.button2.setGeometry(410, 280, 150, 50)
        self.button2.clicked.connect(self.button2Clicked)

    def button1Clicked(self):
        self.label.setText('1 player clicked!')
        self.game_window = GameWindow(self.game_logic)

    def button2Clicked(self):
        self.label.setText('2 players clicked!')
        self.game_window = GameWindow(self.game_logic)


