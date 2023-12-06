# Game Testing Documentation

## Overview

This documentation outlines the purposes and functionalities of different files used in the game testing process, emphasizing the complexity of game testing and the need for visual confirmation of various functionalities.

### `test_main.py`

- **Purpose**: This file is primarily designed to display in-game behavior on the command line. It aids in understanding what the program is executing.
- **Functionalities**:
  - **Function Calls**: Indicates whether a specific function has been called.
  - **Player Actions**: Shows what actions the player has taken.
  - **Conditional Judgments**: Provides results of conditional decisions.
  - **Behind-the-Scenes**: Details what is happening during program black screens.
  - **Problem Identification**: Assists in more intuitively identifying game issues by confirming command line outputs correspond with the game window visuals.

### `simulated_test_end_game.py`

- **Purpose**: To significantly simplify and test one of the functions in the game.
- **Note**: This file serves solely as a test example.

### `test_output.txt`

- **Contents**: Contains the output displayed in the command line when `test_main.py` is executed, capturing the results and behaviors during the test.
