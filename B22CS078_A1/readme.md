## CSL7450 : Computer Graphics
## Assignment-1 : 2D Game (Portal Adventurer)
### Name: Krishna Balaji Patil 
### Roll No.: B22CS078

### Details to run the game:
#### Required libraries (Recommended python 3.9):
PyOpenGL PyOpenGL_accelerate pyrr glfw imgui

#### Steps to run 
Required libraries (Recommended python 3.9):
PyOpenGL PyOpenGL_accelerate pyrr glfw imgui
```
Navigate to game_data folder and run the main python file in it.
```sh
cd game_data/
python main.py
```
#### Files and Folder details:
Folder structure: 
```
B22CS078_A1/
├── game_data/
    ├── assets/
    ├── saved_files/
    ├── utils/
├── imgui.ini
└── readme.md
```
* game_data/assets folder contains object and shader files.
* game_data/assets/objects/objects.py contains all the graphic objects used in the game.
* utlis folder contains template files for graphics classes and window management.
* saved_files folder will contain all the saved game files.
* Different functions of the game class (game.py) implement the different mechanics of the game.

#### Levels and description:
* Level1: River Biome
```
Platforms - vertcally moving rocks
Enemies - Alligators
Unique Mechanic - Press Space to become invincible to enimies (This ability persists to the following levels)
```
* Level2: Magma Trench
```
Platforms - horizontally moving platforms
Enemies - falling rocks
Unique Mechanic - Press E to hook up to a platform directly above over the immediate platform (moves to next to next platform)
This ability has a cool down time
```
* Level3: Space
```
Platforms - UFOs 
Enemies - Meteors
Unique Mechanic - Health potions spawn in the map which give +30 health points
```