---

# Python 2048 Game

This Python script implements the classic 2048 game using the Pygame library.

## Installation

To run the game, you need Python and Pygame installed on your system. If you haven't installed Pygame yet, you can do so using pip:

```
pip install pygame
```

Clone this repository to your local machine and navigate to the directory containing the script.

## Usage

Run the script using Python:

```
python 2048.py
```

Once the game starts, you can use the arrow keys to move the tiles on the board. Merge tiles with the same number to reach the 2048 tile and win the game.

## Features

- **GUI**: Utilizes Pygame for graphical user interface.
- **Score Management**: Tracks and displays the current score, best score, and number of rounds played.
- **Menu**: Provides options to start a new game or reset the current game.
- **Tile Generation**: Randomly generates new tiles (2 or 4) on the board after each move.
- **Game Over Detection**: Detects when the game is over by checking for available moves and a full board.

## File Structure

- `2048.py`: Main Python script containing the game logic.
- `images/`: Directory containing images used in the game.
  - `2048_logo.png`: Icon for the game.
  - `start_menu.png`: Image of the start menu.
  - `game.png`: Image of the game screen.
  - `game_over_menu.png`: Image of the game over menu.
- `2048.json`: JSON file used to store and load high scores and the number of rounds played.

## Screenshots

<table style="border: none; width: 100%;">
  <tr>
    <td style="text-align: center;">
      <h3>Start Menu</h3>
      <img src="images/start_menu.png" alt="Start Menu" width="300"/>
    </td>
    <td style="text-align: center;">
      <h3>Game</h3>
      <img src="images/game.png" alt="Game" width="300"/>
    </td>
    <td style="text-align: center;">
      <h3>Game Over Menu</h3>
      <img src="images/game_over_menu.png" alt="Game Over Menu" width="300"/>
    </td>
  </tr>
</table>




## Contributors

- [Mohammadk202](https://github.com/Mohammadk202)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
