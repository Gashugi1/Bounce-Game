________________________________________
Obstacle Avoidance Game

Overview
The Obstacle Avoidance Game is a fun, interactive game where you control a bouncing ball and try to avoid obstacles. Each obstacle you dodge adds to your score. The longer you avoid obstacles, the higher your score will be!

Game Highlights
•	Easy Controls: Use the arrow keys on your keyboard to move left, right, and jump.
•	Score Tracking: Keep track of your highest score, which will be saved for your next game.
•	Simple Start and End: Begin from the main menu and start over after a game over.

What You Need
To play the game, you’ll need to set up two things:
1.	Python: A programming tool.
2.	Pygame: A game tool that helps make this game work.
3.	
Step 1: Install Python
Python is the language used to make this game. Follow these steps:
1.	Download Python: Go to Python’s download page and click the download button for your computer. Follow the instructions to install Python.
2.	Important: When installing, check the box that says “Add Python to PATH.” This makes it easier to use Python later.
3.	Test if Python is installed: After installation, open your computer’s command line:
o	On Windows: Open “Command Prompt” (search for it in the Start menu).
o	On Mac: Open “Terminal” (you can find it in Applications > Utilities).
In the command line, type:
python --version
If Python is installed correctly, this will show the version number. For example, you might see “Python 3.10.4.”

Step 2: Set Up a Game Space (Optional)
This step is for organization and keeps things tidy, especially if you plan to try other Python projects later.
1.	Make a Game Folder: Create a new folder on your desktop and name it something like “MyGames.”
2.	Navigate to the Game Folder: In your command line, go to this folder. Type cd followed by the path to your new folder. For example:
cd /Users/YourName/Desktop/MyGames

Step 3: Install Pygame
Pygame helps make the game’s visuals and controls work. Here’s how to set it up:
1.	Type This Command: In the command line, type the following command and press Enter:
pip install pygame
2.	Wait for Installation: This may take a few moments. Once it’s done, Pygame will be ready to use.
   
Step 4: Play the Game
1.	Download the Game File: Place the game file (Obstacle_Avoidance_Game.py) in your game folder.
2.	Start the Game: In the command line, make sure you’re inside your game folder, then type:
python Obstacle_Avoidance_Game.py
3.	Controls:
o	Left Arrow: Move left
o	Right Arrow: Move right
o	Up Arrow: Jump
4.	Objective: Avoid the black obstacles as they come towards you. Each one you avoid adds a point to your score.
5.	Game Over: If you hit an obstacle, the game ends, and you can see your score. You’ll have the option to restart or quit.
   
Code Structure
Here's a quick overview of how the game's code is set up. You don’t need to touch these files, but it’s good to know!
•	Main.py: This file runs the main parts of the game, like movement and scoring.
•	Sphere Class: Controls the player’s sphere, helping it move and detect collisions.
•	Obstacle Class: Manages the obstacles, making them appear randomly.
•	Menus: Includes start and game over menus to help you easily start or restart the game.
Credits
Developed by Miguel Gashugi, Ian Imbuki, Jordan Miiro.
License
This project is licensed under the MIT License, which allows anyone to freely use, modify, and share the game.

