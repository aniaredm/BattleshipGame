# Battleship Game

**BattleshipGame** is a classic strategy game where the player competes against the computer.  
It has been implemented using two different GUI frameworks: **PyQt** and **GTK**, allowing the user to choose their preferred interface.  

## Game Description

Battleship is a strategic guessing game in which the player and the computer place their fleets on a grid.  
Each ship can be placed **horizontally or vertically**. The fleet consists of different types of ships:  

- **Carrier**  
- **Battleship**  
- **Cruiser**  
- **Submarine**  
- **Destroyer**  

The goal is to **sink all of the opponent's ships** before losing your own.  
Players take turns calling out grid coordinates to try and hit each other's ships.  

## Choose Your Interface (PyQt vs GTK)

The game supports two different GUI options:  

- **GTK**  
- **PyQt**  

Depending on your preference, you can launch the game in either mode.

---

## Installation & Running the Game  

### 1️. Clone the Repository  

```sh
git clone https://github.com/your_username/BattleshipGame.git
cd BattleshipGame
```

### 2. Install dependencies
Make sure you have **Python 3.8+** installed along with the required dependencies.  
To install them, run:

```sh
pip install -r requirements.txt
```

### 3. Run the Game
You can start the game using either the GTK or PyQt interface:

Run with GTK:

```sh
python main.py gtk
```

Run with PyQt:

```sh
python main.py qt
```

## Technologies Used
**Language:** Python

**GUI Frameworks:** PyQt, GTK

**Libraries:**   
  - `PyQt5` – for the Qt-based user interface  
  - `PyGObject` – for the GTK-based user interface