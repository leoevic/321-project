# Game structure

The game is written in Python and contains of multiple parts, which will be explained here.

## main.py

This is the entry point of the game application. It loads the `game.py` class, the actual game.

## game.py

This is the brain of the game. This class does the following things:

- Track game state and score
- Send game data over MQTT
- Register player controls
- Run ticks for fireballs and zombies

## controls.py

This class is resposible for game input. It registers inputs from the direction buttons and touch sensor and forwards them to the game class.

## screen.py

This class is responsible for controlling the 8x8 LED matrix. The game sends information to this class, and it renders those information on the matrix.