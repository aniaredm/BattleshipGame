import random 

class GameLogic:
    def __init__(self):
        self.board_size = 10
        self.player_board = [[0] * self.board_size for _ in range(self.board_size)] 
        self.computer_board = [[0] * self.board_size for _ in range(self.board_size)]
        self.player_guesses_board = [[0] * self.board_size for _ in range(self.board_size)]
        self.computer_guesses_board = [[0] * self.board_size for _ in range(self.board_size)]
        self.ships = {'Carrier: 5': 5, 'Battleship: 4': 4, 'Cruiser: 3': 3, 'Submarine: 3': 3, 'Destroyer: 2': 2} 
        self.player_ships = {ship: False for ship in self.ships}  
        self.computer_ships = {ship: False for ship in self.ships}
        self.hits = []  # list to store hits for the Target Phase

    def set_ship_placement_mode(self, mode):
        self.ship_placement_mode = mode

    def place_ship(self, ship, x, y, direction):
        if self.ship_placement_mode:
            if self.check_valid_placement(ship, x, y, direction, 1):
                size = self.get_ship_size(ship)
                ship_number = self.get_ship_number(ship)
                if direction == 'horizontal':
                    for i in range(size):
                        self.player_board[y - 1][x + i - 1] = ship_number
                elif direction == 'vertical':
                    for i in range(size):
                        self.player_board[y + i - 1][x - 1] = ship_number
                # print(f"Placed {ship} at position ({x}, {y}) with direction {direction}")
                self.player_ships[ship] = True
        #     else:
        #         print(f"Invalid placement for {ship} at position ({x}, {y}) with direction {direction}")
        # else:
        #     print("Ship placement mode is not enabled.")
        
    def remove_ship(self, ship_name):
        ship = self.get_ship_by_name(ship_name)
        ship_number = self.get_ship_number(ship)
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.player_board[i][j] == ship_number:
                    self.player_board[i][j] = 0
        self.player_ships[ship] = True
         
    def get_ship_number(self, ship):
        ship_numbers = {"Carrier: 5": 1, "Battleship: 4": 2, "Cruiser: 3": 3, "Submarine: 3": 4, "Destroyer: 2": 5}
        number = ship_numbers.get(ship)
        return number
        
    def get_ship_size(self, ship):
        size = int(ship.split(':')[-1].strip())
        return size
    
    def get_ship_name(self, ship_number):
        ship_names = {1: 'Carrier: 5', 2: 'Battleship: 4', 3: 'Cruiser: 3', 4: 'Submarine: 3', 5: 'Destroyer: 2'}
        name = ship_names.get(ship_number)
        return name

    def get_ship_by_name(self, ship_name):
        for ship in self.ships.items():
            chosen_ship = ship[0]
            ship_number = self.get_ship_number(chosen_ship)
            name = self.get_ship_name(ship_number)
            if name == ship_name:
                return chosen_ship
        return None

    def check_valid_placement(self, ship, x, y, direction, player):
        x -= 1
        y -= 1
        ship_number = self.get_ship_number(ship)
        size = self.get_ship_size(ship)

        if direction == 'horizontal':
            if x + size > self.board_size:
                return False  # the ship goes beyond the boundaries of the board
            for i in range(size):
                if player == 1:
                    if self.player_board[y][x + i] != 0 and self.player_board[y][x + i] != ship_number:
                        # print(f"Invalid placement for {ship} at position ({x+1}, {y+1}) with direction {direction}")
                        return False  # there is already a ship in this position
                else:
                    if self.computer_board[y][x + i] != 0 and self.computer_board[y][x + i] != ship_number:
                        # print(f"Invalid placement for {ship} at position ({x+1}, {y+1}) with direction {direction}")
                        return False  # there is already a ship in this position

        elif direction == 'vertical':
            if y + size > self.board_size:
                return False  # the ship goes beyond the boundaries of the board
            for i in range(size):
                if player == 1:
                    if self.player_board[y + i][x] != 0 and self.player_board[y + i][x] != ship_number:
                        # print(f"Invalid placement for {ship} at position ({x+1}, {y+1}) with direction {direction}")
                        return False  # there is already a ship in this position
                else:
                    if self.computer_board[y + i][x] != 0 and self.computer_board[y + i][x] != ship_number:
                        # print(f"Invalid placement for {ship} at position ({x+1}, {y+1}) with direction {direction}")
                        return False  # there is already a ship in this position
        return True


    def generate_computer_board(self):
        for ship, size in self.ships.items():
            placed = False
            while not placed:
                x = random.randint(1, self.board_size)
                y = random.randint(1, self.board_size)
                direction = random.choice(['horizontal', 'vertical'])
                if self.check_valid_placement(ship, x, y, direction, 2):
                    placed = True
                    # add ship to the computer board
                    ship_number = self.get_ship_number(ship)
                    if direction == 'horizontal':
                        for i in range(size):
                            self.computer_board[y - 1][x + i - 1] = ship_number
                    elif direction == 'vertical':
                        for i in range(size):
                            self.computer_board[y + i - 1][x - 1] = ship_number
                    self.computer_ships[ship] = True

    def computer_turn(self):
        if self.hits:
            ship_number, game_over = self.target_phase()
        else:
            ship_number, game_over = self.hunt_phase()
        return ship_number, game_over
        
    def hunt_phase(self):
        while True:
            x = random.randint(1, self.board_size)
            y = random.randint(1, self.board_size)
            if self.is_valid_target(x - 1, y - 1):
                ship_number, game_over = self.receive_attack(y, x, 2) 
                if ship_number is not None:
                    self.hits.append((x - 1, y - 1))
                return ship_number, game_over
            
    def is_valid_target(self, x, y):
        if self.computer_guesses_board[x][y] == 0:
            if x >= 0 and x < self.board_size:
                if x == 0 and self.computer_guesses_board[x + 1][y] != -1:
                    return True
                elif x == 9 and self.computer_guesses_board[x - 1][y] != -1:
                    return True
                elif 0 < x < self.board_size - 1 and self.computer_guesses_board[x + 1][y] != -1 or self.computer_guesses_board[x - 1][y] != -1:
                    return True
            if y >= 0 and y < self.board_size:
                if y == 0 and self.computer_guesses_board[x][y + 1] != -1:
                    return True
                elif y == 9 and self.computer_guesses_board[x][y - 1] != -1:
                    return True
                elif 0 < y < self.board_size - 1 and self.computer_guesses_board[x][y + 1] != -1 or self.computer_guesses_board[x][y - 1] != -1:
                    return True
        return False
    
    def is_valid_target_around(self, x, y):
        if 0 <= x < self.board_size and 0 <= y < self.board_size:
            if self.computer_guesses_board[x][y] == 0:
                return True
        return  False
            
    def target_phase(self):
        if not self.hits:
            return self.hunt_phase()
    
        orientation = None

        if len(self.hits) > 1:
            # Determine the orientation and the boundaries of the hits
            min_x = min(self.hits, key=lambda hit: hit[0])[0]
            max_x = max(self.hits, key=lambda hit: hit[0])[0]
            min_y = min(self.hits, key=lambda hit: hit[1])[1]
            max_y = max(self.hits, key=lambda hit: hit[1])[1]

            if min_x == max_x:
                orientation = 'horizontal'
            elif min_y == max_y:
                orientation = 'vertical'
            
            possible_moves = []

        if orientation == 'horizontal':
            if self.is_valid_target_around(min_x, min_y - 1):
                possible_moves.append((min_x, min_y - 1))
            if self.is_valid_target_around(max_x, max_y + 1):
                possible_moves.append((max_x, max_y + 1))
        elif orientation == 'vertical':
            if self.is_valid_target_around(min_x - 1, min_y):
                possible_moves.append((min_x - 1, min_y))
            if self.is_valid_target_around(max_x + 1, max_y):
                possible_moves.append((max_x + 1, max_y))
        else:
            # If orientation is not known, check all adjacent cells
            last_hit = self.hits[-1]
            possible_moves = [
                (last_hit[0] + dx, last_hit[1] + dy)
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                if self.is_valid_target_around(last_hit[0] + dx, last_hit[1] + dy)
            ]

        random.shuffle(possible_moves)

        move = possible_moves[0]
        nx, ny = move[0], move[1]
        ship_number, game_over = self.receive_attack(ny + 1, nx + 1, 2)
        if ship_number is not None:
            self.hits.append((nx, ny))
            ship_name = self.get_ship_name(ship_number)
            ship = self.get_ship_by_name(ship_name)
            if self.player_ships[ship] == False:
                ship_size = self.get_ship_size(ship)
                # if there are adjacent ships computer may have attacked different ship while trying to take down the other one
                sunk_ship_positions = self.get_sunk_ship_positions(ship_number)
                if len(self.hits) > ship_size:
                    # Remove hits that belong to the sunk ship
                    self.hits = [hit for hit in self.hits if hit not in sunk_ship_positions]
                else:
                    self.hits = []
        return ship_number, game_over
    
    def get_sunk_ship_positions(self, ship_number):
        positions = []
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.computer_guesses_board[x][y] == ship_number:
                    positions.append((x, y))
        return positions
    
    def receive_attack(self, y, x, player):
        x -= 1
        y -= 1
        if player == 1:
            if self.computer_board[x][y] > 0:  
                ship_number = self.computer_board[x][y]
                self.computer_board[x][y] = -1  
                self.player_guesses_board[x][y] = ship_number
                ship_name = self.get_ship_name(ship_number)
                ship = self.get_ship_by_name(ship_name)
                ship_sank = self.check_if_ship_sank(self.computer_board, ship_number)
                if ship_sank:
                    self.computer_ships[ship] = False
                    if self.check_game_over(self.computer_ships):
                        return ship_number, True
                return ship_number, False
            else:
                self.player_guesses_board[x][y] = -1
                return None, False
        elif player == 2:
            if self.player_board[x][y] > 0: 
                ship_number = self.player_board[x][y] 
                self.player_board[x][y] = -1  
                self.computer_guesses_board[x][y] = ship_number
                ship_name = self.get_ship_name(ship_number)
                ship = self.get_ship_by_name(ship_name)
                ship_sank = self.check_if_ship_sank(self.player_board, ship_number)
                if ship_sank:
                    self.player_ships[ship] = False
                    if self.check_game_over(self.player_ships):
                        return ship_number, True
                return ship_number, False  
            else:
                self.computer_guesses_board[x][y] = -1
                return None, False 
        
    def check_if_ship_sank(self, board, ship_number):
        for row in board:
            if ship_number in row:
                return False
        return True
    
    def is_ship_sunk(self, ship_number, player):
        if player == 1:
            for row in self.computer_board:
                if ship_number in row:
                    return False
            return True
        else:
            for row in self.player_board:
                if ship_number in row:
                    return False
            return True

    def check_game_over(self, ships_to_ckeck):
        for ship in ships_to_ckeck:
            if ships_to_ckeck[ship] == True:
                return False
        return True

