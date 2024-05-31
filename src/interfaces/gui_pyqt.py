from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
from PyQt5.QtCore import Qt, QSize, QCoreApplication
from PyQt5.QtGui import QFont, QColor
import random
from src.game_logic import GameLogic
from PyQt5.QtCore import QTimer
import time

class GameWindow(QMainWindow):
    def __init__(self, game_logic):
        super().__init__()
        self.game_logic = game_logic
        self.ships_placed = {ship: False for ship in self.game_logic.player_ships}
        self.current_player = 1
        self.game_mode = False
        self.button_clicked = [[False for _ in range(10)] for _ in range(10)]
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Battleship Game - Player Mode')
        self.setFixedSize(QSize(500, 600))

        grid_layout = self.createGrid()

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(grid_layout)

        self.show()

    def createGrid(self):
        # Tworzymy layouty
        main_layout = QVBoxLayout()
        grid_layout = QHBoxLayout()

        self.buttons_grid = []
        
        self.ship_label = QLabel("", self)
        self.ship_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.ship_label)
        self.position_label = QLabel("", self)
        self.position_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.position_label)

        for i in range(1, 12):
            row_layout = QVBoxLayout()
            row_buttons = [] 
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
                    label.setStyleSheet("background-color: white; border: 1px solid black;")
                    label.clicked.connect(lambda state, i=i, j=j: self.gridButtonClicked(i, j))  # Połącz funkcję z przyciskiem
                    row_buttons.append(label) 
                label.setFixedSize(QSize(40, 40))
                row_layout.addWidget(label)
            grid_layout.addLayout(row_layout)
            self.buttons_grid.append(row_buttons)

        main_layout.addLayout(grid_layout)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Dodajemy przestrzeń na dole

        # Dodajemy przyciski orientacji statku
        orientation_layout = QHBoxLayout()
        orientation_layout.addStretch(1)
        self.vertical_button = QPushButton("Vertical", self)
        self.vertical_button.clicked.connect(self.setVerticalOrientation)
        orientation_layout.addWidget(self.vertical_button)
        self.horizontal_button = QPushButton("Horizontal", self)
        self.horizontal_button.clicked.connect(self.setHorizontalOrientation)
        orientation_layout.addWidget(self.horizontal_button)
        orientation_layout.addStretch(1)
        main_layout.addLayout(orientation_layout)

        # Dodajemy przycisk "Set"
        self.set_button = QPushButton("Set Board", self)
        self.set_button.clicked.connect(self.startGame)
        main_layout.addWidget(self.set_button)

        # Dodajemy przyciski statków
        self.ship_buttons_layout = QHBoxLayout()
        #ship_buttons_layout.addStretch(1)  # Dodajemy przestrzeń na początku
        self.ship_buttons_layout.addWidget(self.createShipButton('Carrier: 5', 5))
        self.ship_buttons_layout.addWidget(self.createShipButton('Battleship: 4', 4))
        self.ship_buttons_layout.addWidget(self.createShipButton('Cruiser: 3', 3))
        self.ship_buttons_layout.addWidget(self.createShipButton('Submarine: 3', 3))
        self.ship_buttons_layout.addWidget(self.createShipButton('Destroyer: 2', 2))
        main_layout.addLayout(self.ship_buttons_layout)

        return main_layout

    def createShipButton(self, ship_name, size):
        self.create_ship_button = QPushButton(ship_name)
        self.create_ship_button.setFixedSize(QSize(100, 30))
        ship_number = self.game_logic.get_ship_number(ship_name)
        color = self.getShipColor(ship_number)
        self.setButtonColor(self.create_ship_button, color)
        self.create_ship_button.setToolTip(f"Size: {size}")
        self.create_ship_button.clicked.connect(lambda state, ship=ship_name: self.shipButtonClicked(ship))
        return self.create_ship_button
    
    def shipButtonClicked(self, ship_name):
        print('tutaj')

        # if self.ships_placed[ship_name]:
        #     # Jeśli statek już istnieje na planszy, usuń go
        #     self.removeShip(ship_name)
        #     self.ships_placed[ship_name] = False    

        self.selected_ship = ship_name
        self.game_logic.set_ship_placement_mode(True)
        self.ship_label.setText(f"Choose position for: {ship_name}")

    def removeShip(self, ship_name):
        # Iteruj po całej tablicy player_board
        ship_number = self.game_logic.get_ship_number(ship_name)
        ship_color = self.getShipColor(ship_number)
        for i in range(len(self.buttons_grid)):
            for j in range(len(self.buttons_grid[i])):
                button = self.buttons_grid[i][j]
                if button:
                    button_color = button.palette().button().color().name()
                    if button_color == ship_color:
                        button.setStyleSheet("background-color: white; border: 1px solid black;")

        # Usuń statek z planszy gracza w obiekcie game_logic
        self.game_logic.remove_ship(ship_name)
        self.selected_ship = ship_name
        self.ship_label.setText(f"Choose position for: {ship_name}")

    def setVerticalOrientation(self):
        self.orientation = "vertical"
        print("selected orientation: ", self.orientation)
        self.position_label.setText(f"Chosen position: vertical")

    def setHorizontalOrientation(self):
        self.orientation = "horizontal"
        print("selected orientation: ", self.orientation)
        self.position_label.setText(f"Chosen position: horizontal")
    
    def gridButtonClicked(self, row, column):
        print(row, " ", column)
        if not self.game_mode:
            if hasattr(self, 'selected_ship') and self.selected_ship:
                if hasattr(self, 'orientation') and self.orientation:
                    ship_number = self.game_logic.get_ship_number(self.selected_ship)
                    color = self.getShipColor(ship_number)
                    if self.orientation == "horizontal":
                        if self.game_logic.check_valid_placement(self.selected_ship, row - 1, column - 1, self.orientation, self.current_player):
                            if self.ships_placed[self.selected_ship]:
                                self.removeShip(self.selected_ship)
                                self.ships_placed[self.selected_ship] = False 
                            for i in range(row, row + self.game_logic.get_ship_size(self.selected_ship)):
                                button = self.buttons_grid[i - 1][column - 2]  # Indeksujemy od zera
                                if button:
                                    self.setButtonColor(button, color)
                            self.ships_placed[self.selected_ship] = True
                            self.game_logic.place_ship(self.selected_ship, row - 1, column - 1, self.orientation)
                    elif self.orientation == "vertical":
                        if self.game_logic.check_valid_placement(self.selected_ship, row - 1, column - 1, self.orientation, self.current_player):
                            if self.ships_placed[self.selected_ship]:
                                self.removeShip(self.selected_ship)
                                self.ships_placed[self.selected_ship] = False 
                            for i in range(column, column + self.game_logic.get_ship_size(self.selected_ship)):
                                button = self.buttons_grid[row - 1][i - 2]  # Indeksujemy od zera
                                if button:
                                    self.setButtonColor(button, color)
                            self.ships_placed[self.selected_ship] = True
                            self.game_logic.place_ship(self.selected_ship, row - 1, column - 1, self.orientation)
                else:
                    QMessageBox.information(self, "Information", "Choose vertical or horizontal position")
            else:
                QMessageBox.information(self, "Informatsion", "Select a ship first")
        else:
            if self.current_player == 1:
                if not self.button_clicked[column-2][row-2]:  
                    self.button_clicked[column-2][row-2] = True
                    ship_number, game_over = self.game_logic.receive_attack(row - 1, column - 1, self.current_player)
                    self.updateBoard()
                    QApplication.processEvents()
                    if game_over:
                        self.showEndMessage(self.current_player)
            self.current_player = 2
            self.ship_label.setText("Computer's turn")
            self.displayFunction()
            self.computerMove()  

    def computerMove(self):
        ship_number, game_over = self.game_logic.computer_turn()
        self.displayFunction()
        if game_over:
            self.showEndMessage(self.current_player)
        self.current_player = 1
        self.ship_label.setText("Your turn")
        self.displayFunction()

    def displayFunction(self):
        time.sleep(1)
        self.updateBoard()
        QApplication.processEvents()

    def showEndMessage(self, current_player):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Game over!")
        if current_player == 1:
            msg_box.setText("Congratulations! You won!")
        else:
            msg_box.setText("You lost!")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.buttonClicked.connect(self.closeGameWindow)
        msg_box.exec_()

    def closeGameWindow(self):
        self.close()


    def setButtonColor(self, button, color):
        button.setStyleSheet(f"background-color: {color}; border: 1px solid black;")

    def getButtonColor(self, button):
        color = button.palette().button().color()
        color_name = color.name()
        return color_name

    def getShipColor(self, ship_number):
        ship_colors = {1: "#add8e6", 2: "#ffb6c1", 3: "#90ee90", 4: "#ffffe0", 5: "#e0ffff"}
        return ship_colors.get(ship_number)
    
    def updateBoard(self):
        # for i in range(10):
        #     for j in range(10):
        #         button = self.buttons_grid[j + 1][i]
        #         if button:
        #             button.setStyleSheet("background-color: white; border: 1px solid black;")
        print("tutaj")
        for i in range(10):
            for j in range(10):
                button = self.buttons_grid[j + 1][i]
                if button:
                    if self.current_player == 1:
                        ship_number = self.game_logic.player_guesses_board[i][j]
                    else:
                        ship_number = self.game_logic.computer_guesses_board[i][j]
                    if ship_number == -1:
                        button.setStyleSheet("background-color: #dadad9; border: 1px solid black;")
                    elif ship_number == 0: 
                        button.setStyleSheet("background-color: white; border: 1px solid black;")
                    elif ship_number > 0:
                        if not self.game_logic.is_ship_sunk(ship_number):
                            button.setStyleSheet(f"background-color: #7f1734; border: 1px solid black;")  
                        else:
                            ship_color = self.getShipColor(ship_number)
                            button.setStyleSheet(f"background-color: {ship_color}; border: 1px solid black;")  
    
    def color_sunk_ship(self, ship_number):
        ship_color = self.getShipColor(ship_number)
        for i in range(10):
            for j in range(10):
                if self.game_logic.player_guesses_board[i][j] == ship_number:
                    button = self.buttons_grid[j + 1][i]
                    if button:
                        button.setStyleSheet(f"background-color: {ship_color}; border: 1px solid black;")
    
    def startGame(self):
        print('tutaj')
        if all(self.ships_placed.values()):
            self.game_logic.generate_computer_board()
            self.current_player = random.randint(1,2)
            self.updateUI()
            self.game_mode = True
            if self.current_player == 2:
                self.ship_label.setText("Computer's turn")
                self.displayFunction()
                self.computerMove()
        else:
            QMessageBox.information(self, "Information", "Place all your ships first")
    
    def updateUI(self):
        for i in reversed(range(self.ship_buttons_layout.count())):
            widget = self.ship_buttons_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.ship_buttons_layout.deleteLater()  # Zwolnij pamięć po przycisku
        self.layout().removeWidget(self.vertical_button)  # Usuń przycisk "Vertical" z interfejsu
        self.vertical_button.deleteLater()  # Zwolnij pamięć po przycisku
        self.layout().removeWidget(self.horizontal_button)  # Usuń przycisk "Horizontal" z interfejsu
        self.horizontal_button.deleteLater()  # Zwolnij pamięć po przycisku
        self.layout().removeWidget(self.set_button)  # Usuń przycisk "Set Board" z interfejsu
        self.set_button.deleteLater()

        for i in range(len(self.buttons_grid)):
            for j in range(len(self.buttons_grid[i])):
                button = self.buttons_grid[i][j]
                if button:
                    button.setStyleSheet("background-color: white; border: 1px solid black;")

        # Aktualizacja etykiety informującej o aktualnym graczu
        if self.current_player == 1:
            self.ship_label.setText("Your turn")
            self.position_label.setText("")
        else:
            self.ship_label.setText("Computer's turn")
            self.position_label.setText("")

class GUIPyQt(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.game_logic = game_logic
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

        # self.label = QLabel('', self)
        # self.label.setAlignment(Qt.AlignCenter)
        # font = QFont()
        # font.setPointSize(10)
        # self.label.setFont(font)
        # self.label.setGeometry(300, 240, 200, 30)

        # Dodajemy przycisk
        self.button1 = QPushButton('Start game', self)
        self.button1.setGeometry(240, 280, 150, 50)
        self.button1.clicked.connect(self.button1Clicked)

        self.button2 = QPushButton('Exit game', self)
        self.button2.setGeometry(410, 280, 150, 50)
        self.button2.clicked.connect(self.button2Clicked)

    def button1Clicked(self):
        #self.label.setText('1 player clicked!')
        self.game_logic = GameLogic()
        self.game_window = GameWindow(self.game_logic)

    def button2Clicked(self):
        #self.label.setText('2 players clicked!')
        QCoreApplication.quit()


