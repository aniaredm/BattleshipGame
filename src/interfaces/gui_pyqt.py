from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox, QAction, QActionGroup
from PyQt5.QtCore import Qt, QSize, QCoreApplication, QTranslator
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
        self.start_text = True

    def initUI(self):
        self.setWindowTitle('Battleship Game - Player Mode')
        self.setFixedSize(QSize(700, 860))

        grid_layout = self.createGrid()

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(grid_layout)

        self.show()

    def createGrid(self):
        main_layout = QVBoxLayout()
        grid_layout = QHBoxLayout()

        self.buttons_grid = []
        
        self.ship_label = QLabel("Select the ship and its direction using buttons at the bottom.", self)
        self.ship_label.setStyleSheet("font-size: 20px;")
        self.ship_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.ship_label)
        self.position_label = QLabel("Then select its location by clicking on the grid.", self)
        self.position_label.setStyleSheet("font-size: 20px;")
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
                    # set letters for each row
                    label = QLabel(chr(64 + j - 1), self)
                    label.setAlignment(Qt.AlignCenter)
                    label.setStyleSheet("font-size: 20px;")
                elif j == 1:
                    # set number for each column
                    label = QLabel(str(i - 1), self)
                    label.setAlignment(Qt.AlignCenter)
                    label.setStyleSheet("font-size: 20px;")
                else:
                    label = QPushButton("", self)
                    label.setStyleSheet("background-color: white; border: 1px solid black;")
                    label.clicked.connect(lambda state, i=i, j=j: self.gridButtonClicked(i, j)) 
                    row_buttons.append(label) 
                label.setFixedSize(QSize(50, 50))
                row_layout.addWidget(label)
            grid_layout.addLayout(row_layout)
            self.buttons_grid.append(row_buttons)

        main_layout.addLayout(grid_layout)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # add ship buttons
        self.ship_buttons_layout = QHBoxLayout()
        self.ship_buttons_layout.addWidget(self.createShipButton('Carrier: 5', 5))
        self.ship_buttons_layout.addWidget(self.createShipButton('Battleship: 4', 4))
        self.ship_buttons_layout.addWidget(self.createShipButton('Cruiser: 3', 3))
        self.ship_buttons_layout.addWidget(self.createShipButton('Submarine: 3', 3))
        self.ship_buttons_layout.addWidget(self.createShipButton('Destroyer: 2', 2))
        self.ship_buttons_layout.setContentsMargins(20,20,10,5)
        main_layout.addLayout(self.ship_buttons_layout)

        # add buttons to set ship orientation
        orientation_layout = QHBoxLayout()
        orientation_layout.addStretch(1)
        self.vertical_button = QPushButton("Vertical", self)
        self.vertical_button.setStyleSheet("font-size: 20px;")
        self.vertical_button.clicked.connect(self.setVerticalOrientation)
        orientation_layout.addWidget(self.vertical_button)
        self.horizontal_button = QPushButton("Horizontal", self)
        self.horizontal_button.setStyleSheet("font-size: 20px;")
        self.horizontal_button.clicked.connect(self.setHorizontalOrientation)
        orientation_layout.addWidget(self.horizontal_button)
        orientation_layout.addStretch(1)
        main_layout.addLayout(orientation_layout)

        # add set - start game button
        self.set_button = QPushButton("Set Board", self)
        self.set_button.setStyleSheet("font-size: 20px;")
        self.set_button.clicked.connect(self.startGame)
        main_layout.addWidget(self.set_button)

        return main_layout

    def createShipButton(self, ship_name, size):
        self.create_ship_button = QPushButton(ship_name)
        self.create_ship_button.setFixedSize(QSize(125, 35))
        font = QFont()
        font.setPointSize(10)
        self.create_ship_button.setFont(font)
        ship_number = self.game_logic.get_ship_number(ship_name)
        color = self.getShipColor(ship_number)
        self.setButtonColor(self.create_ship_button, color)
        self.create_ship_button.setToolTip(f"Size: {size}")
        self.create_ship_button.clicked.connect(lambda state, ship=ship_name: self.shipButtonClicked(ship))
        return self.create_ship_button
    
    def shipButtonClicked(self, ship_name):
        if self.start_text:
            self.position_label.setText(f"")
        self.start_text = False
        self.selected_ship = ship_name
        self.game_logic.set_ship_placement_mode(True)
        self.ship_label.setText(f"Choose position for: {ship_name}")

    def removeShip(self, ship_name):
        # remove ship in GUI
        ship_number = self.game_logic.get_ship_number(ship_name)
        ship_color = self.getShipColor(ship_number)
        for i in range(len(self.buttons_grid)):
            for j in range(len(self.buttons_grid[i])):
                button = self.buttons_grid[i][j]
                if button:
                    button_color = button.palette().button().color().name()
                    if button_color == ship_color:
                        button.setStyleSheet("background-color: white; border: 1px solid black;")

        # remove ship in game logic
        self.game_logic.remove_ship(ship_name)
        self.selected_ship = ship_name
        self.ship_label.setText(f"Choose position for: {ship_name}")

    def setVerticalOrientation(self):
        if self.start_text:
            self.ship_label.setText(f"")
        self.start_text = False
        self.orientation = "vertical"
        self.position_label.setText(f"Chosen position: vertical")

    def setHorizontalOrientation(self):
        if self.start_text:
            self.ship_label.setText(f"")
        self.start_text = False
        self.orientation = "horizontal"
        self.position_label.setText(f"Chosen position: horizontal")
    
    def gridButtonClicked(self, row, column):
        # place ship on the board when grid button clicked and not in game mode
        if not self.game_mode:
            if hasattr(self, 'selected_ship') and self.selected_ship:
                if hasattr(self, 'orientation') and self.orientation:
                    ship_number = self.game_logic.get_ship_number(self.selected_ship)
                    color = self.getShipColor(ship_number)
                    if self.orientation == "horizontal":
                        if self.game_logic.check_valid_placement(self.selected_ship, row - 1, column - 1, self.orientation, self.current_player):
                            if self.ships_placed[self.selected_ship]:
                                # if selected ship has already been placed delete id before moving to a new position
                                self.removeShip(self.selected_ship)
                                self.ships_placed[self.selected_ship] = False 
                            for i in range(row, row + self.game_logic.get_ship_size(self.selected_ship)):
                                button = self.buttons_grid[i - 1][column - 2] 
                                if button:
                                    self.setButtonColor(button, color)
                            self.ships_placed[self.selected_ship] = True
                            self.game_logic.place_ship(self.selected_ship, row - 1, column - 1, self.orientation)
                    elif self.orientation == "vertical":
                        if self.game_logic.check_valid_placement(self.selected_ship, row - 1, column - 1, self.orientation, self.current_player):
                            if self.ships_placed[self.selected_ship]:
                                # if selected ship has already been placed delete id before moving to a new position
                                self.removeShip(self.selected_ship)
                                self.ships_placed[self.selected_ship] = False 
                            for i in range(column, column + self.game_logic.get_ship_size(self.selected_ship)):
                                button = self.buttons_grid[row - 1][i - 2]  
                                if button:
                                    self.setButtonColor(button, color)
                            self.ships_placed[self.selected_ship] = True
                            self.game_logic.place_ship(self.selected_ship, row - 1, column - 1, self.orientation)
                else:
                    QMessageBox.information(self, "Information", "Choose vertical or horizontal position")
            else:
                QMessageBox.information(self, "Informatsion", "Select a ship first")
        # attack the grid field when grid button clicked and in game mode
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
        msg_box.resize(200, 150)
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
        for i in range(10):
            for j in range(10):
                button = self.buttons_grid[j + 1][i]
                if button:
                    if self.current_player == 1:
                        ship_number = self.game_logic.player_guesses_board[i][j]
                    else:
                        ship_number = self.game_logic.computer_guesses_board[i][j]
                    if ship_number == -1:
                        button.setStyleSheet("background-color: #dadad9; border: 1px solid black;") # light grey color for attacked field with no ship on it
                    elif ship_number == 0: 
                        button.setStyleSheet("background-color: white; border: 1px solid black;") # white color for fields that has not been attacked yet
                    elif ship_number > 0:
                        if not self.game_logic.is_ship_sunk(ship_number, self.current_player):
                            button.setStyleSheet(f"background-color: #7f1734; border: 1px solid black;") # dark red color for attacked but not sunk ship fileds 
                        else:
                            ship_color = self.getShipColor(ship_number)
                            button.setStyleSheet(f"background-color: {ship_color}; border: 1px solid black;") # ship color for fields that belong given sunk ship 
    
    def startGame(self):
        if all(self.ships_placed.values()):
            self.game_logic.generate_computer_board()
            self.current_player = random.randint(1,2)
            self.updateUI()
            QApplication.processEvents()
            self.game_mode = True
            if self.current_player == 2:
                self.displayFunction()
                self.computerMove()
        else:
            QMessageBox.information(self, "Information", "Place all your ships first")
    
    def updateUI(self):
        # before starting new game remove all buttons related to placing ships on the grid
        for i in reversed(range(self.ship_buttons_layout.count())):
            widget = self.ship_buttons_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.ship_buttons_layout.deleteLater() 
        self.layout().removeWidget(self.vertical_button)  
        self.vertical_button.deleteLater() 
        self.layout().removeWidget(self.horizontal_button) 
        self.horizontal_button.deleteLater()
        self.layout().removeWidget(self.set_button) 
        self.set_button.deleteLater()

        for i in range(len(self.buttons_grid)):
            for j in range(len(self.buttons_grid[i])):
                button = self.buttons_grid[i][j]
                if button:
                    button.setStyleSheet("background-color: white; border: 1px solid black;")

        if self.current_player == 1:
            self.ship_label.setText("Your turn")
            self.position_label.setText("")
        else:
            self.ship_label.setText("Computer's turn")
            self.position_label.setText("")

class GUIPyQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.game_window = None
        self.create_menu()

    def initUI(self):
        self.setWindowTitle('Battleship Game - PyQt5')
        self.setFixedSize(QSize(800, 600))

        self.label = QLabel('Welcome to the Battleship Game!', self)
        self.label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setGeometry(100, 200, 600, 50)

        self.button1 = QPushButton('Start game', self)
        self.button1.setGeometry(240, 280, 150, 50)
        self.button1.setStyleSheet("font-size: 20px;")
        self.button1.clicked.connect(self.button1Clicked)

        self.button2 = QPushButton('Exit game', self)
        self.button2.setGeometry(410, 280, 150, 50)
        self.button2.setStyleSheet("font-size: 20px;")
        self.button2.clicked.connect(self.button2Clicked)

    def create_menu(self):
        menubar = self.menuBar()

        # Add "File" menu
        file_menu = menubar.addMenu('File')

        # Add action to "File" menu
        start_game_action = QAction('Start game', self)
        start_game_action.triggered.connect(self.button1Clicked)
        file_menu.addAction(start_game_action)

        file_menu.addSeparator()

        exit_action = QAction('Exit game', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Add "Help" menu
        help_menu = menubar.addMenu('Help')

        about_action = QAction('Description', self)
        about_action.triggered.connect(self.show_description)
        help_menu.addAction(about_action)


    def show_description(self):
        description = (
            "BattleshipGame\n\n"
            "Battleship is a classic strategy game where the player competes against the computer. "
            "Ships are placed horizontally or vertically on the grid. The player's fleet consists of different types of ships, "
            "such as a carrier, battleship, cruiser, submarine, and destroyer. "
            "The player and the computer take turns calling out grid coordinates to try and hit each other's ships. "
            "The goal is to sink all of the computer's ships by correctly guessing their locations before the computer sinks yours."
        )
        QMessageBox.information(self, "Application Description", description)


    def button1Clicked(self):
        self.game_logic = GameLogic()
        self.game_window = GameWindow(self.game_logic)

    def button2Clicked(self):
        QCoreApplication.quit()


