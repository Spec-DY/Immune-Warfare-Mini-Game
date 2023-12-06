# Final Project Report

* Student Name:
* Github Username:
* Semester:
* Course:



## Description 
This Python-based game titled "Immune Warfare: Cells vs. Viruses." The game is an arcade-style shooter where the player controls a white blood cell, aiming to eliminate viruses and ultimately face a boss virus. 
### Game background story
As a white blood cell, you are the body's silent protector. Your first battle unfolds in the upper respiratory tract, confronting a formidable virus. This encounter is just a hint of the lurking threats. 
Remember, these viruses may harbor a grander plot. Your vigilant journey into the body's hidden depths begins.


## Key Features
- **Dynamic Enemy Movement:** Viruses move down the screen at varying speeds.
- **Boss Fight:** A challenging boss fight occurs once a certain score is reached.
- **Health Bars:** Both the player and boss have visual health bars.
- **Scoring System:** The game tracks the number of viruses eliminated.
- **Timed Gameplay:** Players have a set amount of time to reach the boss level.
- **Customizable Difficulty:** Player can adjust status for different objects like boss health, player health, etc.

## Guide
To play the game, click "Immune War.exe", you can also run the main.py file and click start in the start menu. Once the game begins, use the left and right arrow keys to move the white blood cell. Press space to shoot at incoming viruses. The aim is to destroy enough viruses before time runs out to trigger the boss fight, 30 kills in this case. Win if boss defeated, while loss if runing out of time or player dead.
Player may customize difficulties by acessing some constant at the begining of the main.py file:

**MIN_SCORE**: The score required for boss fight, set it **lower for easier game**.<br>
**TIME_LIMIT**: Certain score should be reached before this time runout, set it **higher for easier game**.<br>
**BOSS_SHOOT_RATE**: Boss shooting frequency divisor, set it **higher for easier game**.<br>
**FRESH_RATE**: Adjust game fresh rate, set it **lower for easier game**.


## Installation Instructions
  ### Execute exe:
  Path: "Immune Warfare/dist/Immune Warfare.exe"
  Double click "Immune Warfare.exe"
  ##### OR
  ### Execute code:
  - Clone the repository from GitHub.
  - Ensure Python is installed on your device.
  - Install Pygame: `pip install pygame`
  - Run the script: `python main.py`
  - 'immuart' folder must be same path with main.py.

## Code Review
Go over key aspects of code in this section. Both link to the file, include snippets in this report (make sure to use the [coding blocks](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#code)).  Grading wise, we are looking for that you understand your code and what you did. 

### Major Challenges
Key aspects could include pieces that your struggled on and/or pieces that you are proud of and want to show off.


## Example Runs
Explain how you documented running the project, and what we need to look for in your repository (text output from the project, small videos, links to videos on youtube of you running it, etc)

## Testing
How did you test your code? What did you do to make sure your code was correct? If you wrote unit tests, you can link to them here. If you did run tests, make sure you document them as text files, and include them in your submission. 

> _Make it easy for us to know you *ran the project* and *tested the project* before you submitted this report!_


## Missing Features / What's Next
Focus on what you didn't get to do, and what you would do if you had more time, or things you would implement in the future. 

## Final Reflection
Write at least a paragraph about your experience in this course. What did you learn? What do you need to do to learn more? Key takeaways? etc.
