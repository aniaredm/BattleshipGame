import gi
import os
import random
import time
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Pango, GLib
from src.game_logic import GameLogic

class GameWindow(Gtk.Window):
    def __init__(self, game_logic):
        super().__init__(title="Battleship Game - Player Mode")
        self.game_logic = game_logic
        self.ships_placed = {ship: False for ship in self.game_logic.player_ships}
        self.current_player = 1
        self.game_mode = False
        self.button_clicked = [[False for _ in range(10)] for _ in range(10)]
        self.set_default_size(700, 950)
        self.set_resizable(False)
        self.start_text = True

        self.initUI()

    def initUI(self):
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        self.ship_label = Gtk.Label(label="Select the ship and its direction using buttons at the bottom.")
        self.ship_label.set_alignment(0.5, 0.5)
        self.ship_label.set_size_request(150, -1)
        self.ship_label.modify_font(Pango.FontDescription("Sans 12"))
        self.ship_label.set_margin_top(20)
        self.main_box.pack_start(self.ship_label, False, False, 0)

        self.position_label = Gtk.Label(label="Then select its location by clicking on the gri.")
        self.ship_label.set_alignment(0.5, 0.5)
        self.position_label.set_size_request(150, -1)
        self.position_label.modify_font(Pango.FontDescription("Sans 12"))
        self.main_box.pack_start(self.position_label, False, False, 0)

        # Box for game grid
        grid_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.buttons_grid = []
        for i in range(1, 12):
            row_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            for j in range(1, 12):
                if i == 1 and j == 1:
                    event_box = Gtk.EventBox()
                    event_box.set_size_request(50, 50)
                    label = Gtk.Label(label="")
                    event_box.add(label)
                elif i == 1:
                    # set letters for each row
                    event_box = Gtk.EventBox()
                    event_box.set_size_request(50, 50)
                    label = Gtk.Label(label=chr(64 + j - 1))
                    event_box.add(label)
                elif j == 1:
                    # set number for each column
                    event_box = Gtk.EventBox()
                    event_box.set_size_request(50, 50)
                    label = Gtk.Label(label=str(i - 1))
                    event_box.add(label)
                else:
                    event_box = Gtk.EventBox()
                    event_box.set_size_request(50, 50)
                    event_box.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(1, 1, 1, 1))
                    event_box.get_style_context().add_class("event-box-border")
                    event_box.connect("button-release-event", self.gridButtonClicked, i, j)
                    label = Gtk.Label(label="")
                    label.set_justify(Gtk.Justification.CENTER)
                    label.set_name("frame")
                    event_box.add(label)
                    self.buttons_grid.append(event_box)
                row_box.pack_start(event_box, False, False, 0)
            grid_box.pack_start(row_box, False, False, 0)
            grid_box.set_margin_start(50)
            grid_box.set_margin_end(30)
        self.main_box.pack_start(grid_box, False, False, 0)

         # add ship buttons
        self.ship_buttons_box = Gtk.Box(spacing=10)

        ship_info = [
            ("Carrier: 5", "Carrier_5", 5),
            ("Battleship: 4", "Battleship_4", 4),
            ("Cruiser: 3", "Cruiser_3", 3),
            ("Submarine: 3", "Submarine_3", 3),
            ("Destroyer: 2", "Destroyer_2", 2)
        ]

        for ship_label, button_name, size in ship_info:
            button = Gtk.Button(label=ship_label)
            button.modify_font(Pango.FontDescription("Sans 10"))
            button.set_size_request(120, -1)
            button.set_name(button_name)
            button.set_tooltip_text(f"Size: {size}")
            button.connect("clicked", self.shipButtonClicked, ship_label)
            self.ship_buttons_box.pack_start(button, False, True, 0)

        self.ship_buttons_box.set_margin_start(30)
        self.ship_buttons_box.set_margin_end(30)
        self.ship_buttons_box.set_margin_top(20)

        self.main_box.pack_start(self.ship_buttons_box, False, False, 0)

        # add buttons to set ship orientation
        self.orientation_box = Gtk.Box(spacing=10)
        self.vertical_button = Gtk.Button(label="Vertical")
        self.vertical_button.modify_font(Pango.FontDescription("Sans 10"))
        self.vertical_button.connect("clicked", self.setVerticalOrientation)
        self.vertical_button.set_margin_top(5)
        self.vertical_button.set_margin_start(235)
        self.vertical_button.set_margin_end(5)
        self.vertical_button.set_size_request(150, -1)
        self.orientation_box.pack_start(self.vertical_button, False, True, 0)

        self.horizontal_button = Gtk.Button(label="Horizontal")
        self.horizontal_button.modify_font(Pango.FontDescription("Sans 10"))
        self.horizontal_button.connect("clicked", self.setHorizontalOrientation)
        self.horizontal_button.set_margin_top(5)
        self.horizontal_button.set_margin_start(5)
        self.horizontal_button.set_margin_end(215)
        self.horizontal_button.set_size_request(150, -1)
        self.orientation_box.pack_start(self.horizontal_button, False, True, 0)

        self.main_box.pack_start(self.orientation_box, False, False, 0)

        # add set - start game button
        self.set_board_button_box = Gtk.Box(spacing=10)
        self.set_button = Gtk.Button(label="Start Game")
        self.set_button.modify_font(Pango.FontDescription("Sans 10"))
        self.set_button.set_size_request(400, -1)
        self.set_button.set_margin_top(5)
        self.set_button.set_margin_bottom(20)
        self.set_button.set_margin_start(190)
        self.set_button.set_margin_end(150)
        self.set_button.connect("clicked", self.startGame)
        self.set_board_button_box.pack_start(self.set_button, False, False, 0)

        self.main_box.pack_start(self.set_board_button_box, False, False, 0)

        self.add(self.main_box)

    def shipButtonClicked(self, button, ship_name):
        if self.start_text:
            self.position_label.set_text(f"")
        self.start_text = False
        self.selected_ship = ship_name
        self.game_logic.set_ship_placement_mode(True)
        self.ship_label.set_text(f"Choose position for: {ship_name}")

    def removeShip(self, ship_name):
        # remove ship in GUI
        ship_number = self.game_logic.get_ship_number(ship_name)
        ship_color = self.getShipColor(ship_number)
        for i in range(len(self.buttons_grid)):
                button = self.buttons_grid[i]
                if button:
                    button_color = button.get_style_context().get_background_color(Gtk.StateType.NORMAL)
                    color_hex = self.rgba_to_hex(button_color)
                    if color_hex == ship_color:
                        button.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("white"))

        # remove ship in game logic
        self.game_logic.remove_ship(ship_name)
        self.selected_ship = ship_name
        self.ship_label.set_text(f"Choose position for: {ship_name}")

    def setVerticalOrientation(self, button):
        if self.start_text:
            self.ship_label.set_text(f"")
        self.start_text = False
        self.orientation = "vertical"
        self.position_label.set_text(f"Chosen position: vertical")

    def setHorizontalOrientation(self, button):
        if self.start_text:
            self.ship_label.set_text(f"")
        self.start_text = False
        self.orientation = "horizontal"
        self.position_label.set_text(f"Chosen position: horizontal")

    def gridButtonClicked(self, a, b, row, column):
        row -= 1
        column -= 1
        #a.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("blue"))
        # place ship on the board when grid button clicked and not in game mode
        if not self.game_mode:
            if hasattr(self, 'selected_ship') and self.selected_ship:
                if hasattr(self, 'orientation') and self.orientation:
                    ship_number = self.game_logic.get_ship_number(self.selected_ship)
                    color = self.getShipColor(ship_number)
                    #rgb_color = self.hex_to_rgb(color)
                    if self.orientation == "horizontal":
                        if self.game_logic.check_valid_placement(self.selected_ship, row, column, self.orientation, self.current_player):
                            if self.ships_placed[self.selected_ship]:
                                # if selected ship has already been placed delete id before moving to a new position
                                self.removeShip(self.selected_ship)
                                self.ships_placed[self.selected_ship] = False 
                            for i in range(self.game_logic.get_ship_size(self.selected_ship)):
                                button = self.buttons_grid[10*(row-1+i)+(column-1)]
                                button.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(color))
                            self.ships_placed[self.selected_ship] = True
                            self.game_logic.place_ship(self.selected_ship, row, column, self.orientation)
                    elif self.orientation == "vertical":
                        if self.game_logic.check_valid_placement(self.selected_ship, row, column, self.orientation, self.current_player): 
                            if self.ships_placed[self.selected_ship]:
                                # if selected ship has already been placed delete id before moving to a new position
                                self.removeShip(self.selected_ship)
                                self.ships_placed[self.selected_ship] = False 
                            for i in range(self.game_logic.get_ship_size(self.selected_ship)):
                                button = self.buttons_grid[(10*(row-1)+(column-1)) + i]
                                button.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(color))
                            self.ships_placed[self.selected_ship] = True
                            self.game_logic.place_ship(self.selected_ship, row, column, self.orientation)
                else:
                    self.showMessageBox("Information", "Choose vertical or horizontal position")
            else:
                self.showMessageBox("Information", "Select a ship first")
        # attack the grid field when grid button clicked and in game mode
        else:
            if self.current_player == 1:
                if not self.button_clicked[column-1][row-1]:  
                    self.button_clicked[column-1][row-1] = True
                    ship_number, game_over = self.game_logic.receive_attack(row, column, self.current_player)
                    self.updateBoard()
                    while Gtk.events_pending():
                        Gtk.main_iteration_do(False)
                    if game_over:
                        self.showEndMessage(self.current_player)
                    self.current_player = 2
                    self.ship_label.set_text("Computer's turn")
                    self.displayFunction()
                    self.computerMove()

    def showMessageBox(self, title, message):
        dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text=title)
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def computerMove(self):
        ship_number, game_over = self.game_logic.computer_turn()
        self.displayFunction()
        if game_over:
            self.showEndMessage(self.current_player)
        self.current_player = 1
        self.ship_label.set_text("Your turn")
        self.displayFunction()

    def displayFunction(self):
        time.sleep(1)
        self.updateBoard()
        while Gtk.events_pending():
            Gtk.main_iteration_do(False)
        #GLib.timeout_add(1000, self._updateBoardAndProcessEvents)
    
    # def _updateBoardAndProcessEvents(self):
    #     self.updateBoard()
    #     while Gtk.events_pending():
    #         Gtk.main_iteration_do(False)
    #     return False

    def showEndMessage(self, current_player):
        dialog = Gtk.MessageDialog(
            parent=self,
            flags=Gtk.DialogFlags.MODAL,
            type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            message_format="Game over!"
        )

        if current_player == 1:
            dialog.format_secondary_text("Congratulations! You won!")
        else:
            dialog.format_secondary_text("You lost!")

        dialog.set_default_size(200, 150)
        dialog.run()
        dialog.destroy()
        self.closeGameWindow()

    def closeGameWindow(self, *args):
        self.destroy()

    def getShipColor(self, ship_number):
        ship_colors = {1: "#add8e6", 2: "#ffb6c1", 3: "#90ee90", 4: "#ffffe0", 5: "#e0ffff"}
        return ship_colors.get(ship_number)
    
    def updateBoard(self):
        button_index = 0
        for i in range(10):
            for j in range(10):
                button = self.buttons_grid[button_index]
                if button:
                    if self.current_player == 1:
                        ship_number = self.game_logic.player_guesses_board[j][i]
                    else:
                        ship_number = self.game_logic.computer_guesses_board[j][i]
                    color = None
                    if ship_number == -1:
                        color = "#dadad9" # light grey color for attacked field with no ship on it
                    elif ship_number == 0: 
                        color = "white" # white color for fields that has not been attacked yet
                    elif ship_number > 0:
                        if not self.game_logic.is_ship_sunk(ship_number, self.current_player):
                            color = "#7f1734" # dark red color for attacked but not sunk ship fileds 
                        else:
                            color = self.getShipColor(ship_number) # ship color for fields that belong given sunk ship 
                    if color:
                        button.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(color))
                    button_index += 1

    def rgba_to_hex(self, button_color):
        red_hex = format(int(button_color.red * 255), '02x')
        green_hex = format(int(button_color.green * 255), '02x')
        blue_hex = format(int(button_color.blue * 255), '02x')
        color_hex = f"#{red_hex}{green_hex}{blue_hex}"
        return color_hex

    def startGame(self, button):
        if all(self.ships_placed.values()):
            self.game_logic.generate_computer_board()
            self.current_player = random.randint(1, 2)
            self.updateUI()
            while Gtk.events_pending():
                Gtk.main_iteration()
            self.game_mode = True
            if self.current_player == 2:
                self.computerMove()
        else:
            self.showMessageBox("Information", "Place all your ships first")

    def updateUI(self):
        # remove all buttons related to placing ships on the grid before starting new game
        self.main_box.remove(self.orientation_box)
        self.main_box.remove(self.set_board_button_box)
        self.main_box.remove(self.ship_buttons_box)

        for i in range(len(self.buttons_grid)):
            button = self.buttons_grid[i]
            button.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("white"))

        if self.current_player == 1:
            self.ship_label.set_text("Your turn")
            self.position_label.set_text("")
        else:
            self.ship_label.set_text("Computer's turn")
            self.position_label.set_text("")


class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Battleship Game - PyGTK")
        self.set_default_size(700, 840)
        
        self.label = Gtk.Label(label="Welcome to the Battleship Game!")
        self.label.set_justify(Gtk.Justification.CENTER)
        self.label.set_margin_top(280)
        self.label.set_margin_bottom(20)
        self.label.set_margin_start(100)
        self.label.set_margin_end(100)
        self.label.set_name("main_label")
        self.label.modify_font(Pango.FontDescription("Sans 25"))

        self.button1 = Gtk.Button(label="Start game")
        self.button1.modify_font(Pango.FontDescription("Sans 12"))
        self.button1.connect("clicked", self.button1Clicked)
        self.button1.set_margin_start(180)
        self.button1.set_margin_end(20)
        self.button1.set_margin_top(10)
        self.button1.set_margin_bottom(350)

        self.button2 = Gtk.Button(label="Exit game")
        self.button2.modify_font(Pango.FontDescription("Sans 12"))
        self.button2.connect("clicked", self.button2Clicked)
        self.button2.set_margin_start(20)
        self.button2.set_margin_end(180)
        self.button2.set_margin_top(10)
        self.button2.set_margin_bottom(350)

        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.grid.attach(self.label, 0, 0, 2, 1)
        self.grid.attach(self.button1, 0, 1, 1, 1)
        self.grid.attach(self.button2, 1, 1, 1, 1)

        self.add(self.grid)

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        css_path = os.path.join("styles", "styles.css")

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(css_path)

        context = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


    def button1Clicked(self, widget):
        self.game_logic = GameLogic()
        self.game_window = GameWindow(self.game_logic)
        self.game_window.show_all()

    def button2Clicked(self, widget):
        Gtk.main_quit()

if __name__ == "__main__":
    win = MyWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


