## CSL7450 : Computer Graphics
## Assignment-2 : 3D Game (Space Heist)
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
B22CS078_A2/
├── game_data/
    ├── assets/
    ├── utils/
    ├── game.py
    ├── main.py
└── readme.md
```
* game_data/assets folder contains object and shader files.
* game_data/assets/objects/objects.py contains all the graphic objects used in the game.
* utlis folder contains template files for graphics classes and window management.
* Different functions of the game class (game.py) implement the different mechanics of the game.

#### Game Description and Controls:
* Objective:
```
An interplanetary civilization often transports goods from a space station
orbiting one planet, to a space station orbiting another, via a manned spaceship (transporter).
The objective of this 3D game is to successfully transport goods between planets. 
```
* Description:
```
- The transporter ship can perform all 3D maneuvers and is also equipped with a laser to 
  defend against attacking pirate ships which will try to collide with the transporter. 
- There is a arrow at the bottom right corner of the window which acts as a map for the transport craft.
    Red color indicates the destination planet is further up wrt the transporter.
    Blue color indicates the destination planet is further down wrt the transporter.
    White color indicates the destination planet is in-line wrt the transporter.
- There are 2 views of operation.
    i. 3rd person view: In this mode the player can only maneuver the
    transporter, and not use the laser blaster.
    ii. 1st person view: In this view the player cannot maneuver the
    spacecraft but can control the laser blaster with their mouse, and
    use Left Click to shoot the lasers. A crossheir appears at the
    center of the screen in this view to denote the shooting direction.
```
* Controls:
```
-W: Pitch Up
-S: Pitch Down
-A: Yaw Left
-D: Yaw Right
-Q: Roll right down
-E: Roll left down
-SPACE: Move forward
-L_SHIFT: Switch to 1st person view (keep pressed)
-RIHGT_CLICK: Shoot laser (only works in 1st person view)
```