class GameLogic:
    def __init__(self):
        self.board_size = 10
        self.player_board = [[0] * self.board_size for _ in range(self.board_size)]  # plansza gracza
        self.enemy_board = [[0] * self.board_size for _ in range(self.board_size)]  # plansza przeciwnika
        self.ships = {"Carrier": 5, "Battleship": 4, "Cruiser": 3, "Submarine": 3, "Destroyer": 2}  # słownik określający rodzaje statków i ich długość
        self.player_ships = {ship: False for ship in self.ships}  # słownik określający, czy gracz umieścił już dany statek na planszy

    def place_ship(self, ship, x, y, direction):
        """
        Umieszcza statek na planszy gracza.
        :param ship: Nazwa statku.
        :param x: Współrzędna x początkowego punktu umieszczenia statku.
        :param y: Współrzędna y początkowego punktu umieszczenia statku.
        :param direction: Kierunek umieszczenia statku ('H' dla poziomego, 'V' dla pionowego).
        :return: True, jeśli udało się umieścić statek, False w przeciwnym razie.
        """
        pass

    def check_valid_placement(self, ship, x, y, direction):
        """
        Sprawdza, czy umieszczenie statku na danej pozycji jest możliwe.
        :param ship: Nazwa statku.
        :param x: Współrzędna x początkowego punktu umieszczenia statku.
        :param y: Współrzędna y początkowego punktu umieszczenia statku.
        :param direction: Kierunek umieszczenia statku ('H' dla poziomego, 'V' dla pionowego).
        :return: True, jeśli umieszczenie jest możliwe, False w przeciwnym razie.
        """
        pass

    def receive_attack(self, x, y):
        """
        Sprawdza, czy atak przeciwnika trafił w statek na planszy gracza.
        :param x: Współrzędna x ataku.
        :param y: Współrzędna y ataku.
        :return: True, jeśli atak trafił w statek, False w przeciwnym razie.
        """
        pass

    def check_game_over(self):
        """
        Sprawdza, czy gra się zakończyła (czy wszystkie statki zostały zatopione).
        :return: True, jeśli gra się zakończyła, False w przeciwnym razie.
        """
        pass
