import imgui, os, math, datetime, random, json
from tkinter import Tk, filedialog
import numpy as np
from utils.graphics import Object, Camera, Shader
from assets.shaders.shaders import object_shader
from imgui.integrations.glfw import GlfwRenderer

from utils.graphics import VBO, IBO, VAO, Shader, Object, Camera
from assets.objects.objects import playerProps, keyProps, potionProps, statBarProps, exitPortalProps, bgl1Props, bgl2Props, bgl3Props, bgl3_portal1Props, bgl3_portal2Props, platforml1Props, platforml2Props, platforml3Props, enemyl1Props, enemyl2Props, enemyl3Props
from assets.shaders.shaders import object_shader

class Game:
    def __init__(self, height, width, window):
        self.height = height - 100
        self.width = width
        self.screen = -1
        self.camera = Camera(height, width)
        self.shaders = [Shader(object_shader['vertex_shader'], object_shader['fragment_shader'])]
        self.objects = []
        imgui.create_context()
        self.imgui_renderer = GlfwRenderer(window)
        self.is_on_platform = False
        # Stats:
        self.health = 100
        self.lives = 3
        self.keys_collected = 0

        # Level-3: Platform Paths
        self.platform_paths = [
            [np.array([-430.0, -250.0, 0]), np.array([-430.0, 300.0, 0])],
            [np.array([-430.0, 300.0, 0]), np.array([-100.0, -300.0, 0])],
            [np.array([-100.0, -300.0, 0]), np.array([100.0, 300.0, 0])],
            [np.array([100.0, 300.0, 0]), np.array([430.0, -300.0, 0])],
            [np.array([430.0, -300.0, 0]), np.array([430.0, 250.0, 0])]
        ]
        # Level-3: Key Paths
        self.key_paths = [
            [np.array([-430.0, 300.0, 0]), np.array([-100.0, -300.0, 0])],
            [np.array([-100.0, -300.0, 0]), np.array([100.0, 300.0, 0])],
            [np.array([100.0, 300.0, 0]), np.array([430.0, -300.0, 0])]
        ]

        self.dash_cooldown_timer = 0
        self.dash_active = True

    def LoadGame(self, time):
        """Open a file dialog to select a saved game file and load the game state."""
        root = Tk()
        root.withdraw()  

        # Open the file dialog to select a JSON file
        file_path = filedialog.askopenfilename(
            initialdir="saved_files",
            title="Select a Saved Game File",
            filetypes=[("JSON Files", "*.json")]
        )

        if not file_path: 
            print("No file selected.")
            return

        # Load the game state from the selected file
        try:
            with open(file_path, "r") as save_file:
                game_state = json.load(save_file)

            # Initialize the game state from the loaded data
            self.screen = game_state.get("level",1)
            self.lives = game_state.get("lives", 3)
            self.health = game_state.get("health", 100)
            self.keys_collected = game_state.get("keys_collected", 0)
            # time["currentTime"] = game_state.get("time_elapsed", 0)  

            # Set the current level based on the saved data
            self.current_level = self.levels[self.screen]

            print(f"Game loaded from {file_path}")
            print(f"Level: {self.screen}, Lives: {self.lives}, Health: {self.health}, Keys: {self.keys_collected}")

        except Exception as e:
            print(f"Failed to load game: {e}")

    def ResetGame(self, time):
        self.is_on_platform = False
        # Stats:
        self.health = 100
        self.lives = 3
        self.keys_collected = 0

        # Level-3: Platform Paths
        self.platform_paths = [
            [np.array([-430.0, -250.0, 0]), np.array([-430.0, 300.0, 0])],
            [np.array([-430.0, 300.0, 0]), np.array([-100.0, -300.0, 0])],
            [np.array([-100.0, -300.0, 0]), np.array([100.0, 300.0, 0])],
            [np.array([100.0, 300.0, 0]), np.array([430.0, -300.0, 0])],
            [np.array([430.0, -300.0, 0]), np.array([430.0, 250.0, 0])]
        ]
        # Level-3: Key Paths
        self.key_paths = [
            [np.array([-430.0, 300.0, 0]), np.array([-100.0, -300.0, 0])],
            [np.array([-100.0, -300.0, 0]), np.array([100.0, 300.0, 0])],
            [np.array([100.0, 300.0, 0]), np.array([430.0, -300.0, 0])]
        ]

        self.level1_objects = []  
        self.level2_objects = []  
        self.level3_objects = []  
    
        self.dash_cooldown_timer = 0
        self.dash_active = True

    def InitScreen(self, time):
        if self.screen == 0:
            print("Home screen initiated!")
            self.health = 100
            self.lives = 3
            self.keys_collected = 0
        if self.screen == 1:
            print("New Game Started...")
        if self.screen == 2:
            print("Level2 Started")
        if self.screen == 3:
            print("Level3 Started")

    def DrawHomeScreen(self, inputs, time):          
        window_width, window_height = imgui.get_io().display_size
        imgui.set_next_window_position(window_width / 2 - 150, window_height / 2 - 100)
        imgui.set_next_window_size(300, 200) 
        imgui.begin("Portal Adventurer")
        imgui.text("Main Menu")
        
        imgui.separator()
        
        if imgui.button("Click button or Press 1 : New Game",300,30) or "1" in inputs:
            self.screen = 4
            self.InitScreen(time)
            self.ResetGame(time)
        if imgui.button("Click button or Press 2 : Load Game",300,30) or "2" in inputs:
            self.LoadGame(time)
            self.InitScreen(time)
        
        imgui.end()

    def DrawStartUpScreen(self, inputs, time, player1):
        window_width, window_height = imgui.get_io().display_size
        imgui.set_next_window_position(window_width / 2 - 300, window_height / 2 -100)
        imgui.set_next_window_size(600, 300) 
        imgui.begin("NEW GAME", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)
        imgui.same_line(spacing=270)
        imgui.text("NEW GAME")
        imgui.separator()
        imgui.text_wrapped("Rick, while sitting in his room, was suddenly teleported to an unknown part of the world via a portal. He needs to find a way back home")

        imgui.separator()
        imgui.text("")
        imgui.same_line(spacing=260)
        imgui.text(" CONTROLS ")
        imgui.text("                                    W = Move Up")
        imgui.text("                                    A = Move Left")
        imgui.text("                                    D = Move Right")
        imgui.text("                                    S = Move Down")
        imgui.text("                 SPACE = Unique Mechanic(Enemy evade(level1 onwards))")
        imgui.text("                     W = Unique Mechanic(hook up(level2 only))")

        imgui.separator()
        
        if imgui.button("Start (Press 1)",600,30) or "1" in inputs:
            self.screen = 1
            player1.properties["position"] = [-450,-370,0]
            self.InitScreen(time)
        
        imgui.end()

    def DrawGameOverScreen(self, inputs, time):
        window_width, window_height = imgui.get_io().display_size
        imgui.set_next_window_position(window_width / 2 - 300, window_height / 2 -100)
        imgui.set_next_window_size(600, 200) 
        imgui.begin("GAME OVER", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)
        imgui.same_line(spacing=270)
        imgui.text("GAME OVER")
        imgui.text_wrapped("Better luck next time...")
        
        imgui.separator()
        
        if imgui.button("Return to main menu (Press 1)",600,30) or "1" in inputs:
            self.screen = 0
            self.InitScreen(time)

        imgui.end()

    def DrawYouWonScreen(self, inputs, time):
        window_width, window_height = imgui.get_io().display_size
        imgui.set_next_window_position(window_width / 2 - 300, window_height / 2 -100)
        imgui.set_next_window_size(600, 200) 
        imgui.begin("YOU WON!!", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)
        imgui.same_line(spacing=270)
        imgui.text("YOU WON!!")
        imgui.text_wrapped("Rick has returned to his world from a thrilling adventure!")
        
        imgui.separator()
        
        if imgui.button("Return to main menu (Press 1)",600,30) or "1" in inputs:
            self.screen = 0
            self.InitScreen(time)
        
        imgui.end()

    def nextLevel(self, player, exitPortal):
        """Check collision with exit portal"""
        player_pos = player.properties["position"]
        portal_radius = 20  
        portal_pos = exitPortal.properties["position"]

        # Compute Euclidean distance
        distance = np.linalg.norm(player_pos[:2] - portal_pos[:2])

        if distance < portal_radius and self.keys_collected==3 :  # If collision occurs
            if self.screen == 3:
                self.screen = 6
            else:
                self.screen += 1
            self.keys_collected = 0

    def potionGen(self, obj_list):
        for i in range(3):
            key = Object(self.shaders[0], potionProps)
            key.properties["position"] = np.array([np.random.randint(-400,400),np.random.randint(-300,300),-0.05])
            obj_list.append(key)

    def initializeLevel(self, level):
        if level==1:
            if not hasattr(self, "level1_objects") or self.level1_objects is None or len(self.level1_objects)==0:
                self.level1_objects = [
                    Object(self.shaders[0], playerProps),
                    Object(self.shaders[0],statBarProps), 
                    Object(self.shaders[0], bgl1Props),
                    Object(self.shaders[0], exitPortalProps),
                    Object(self.shaders[0], exitPortalProps)
                ]  # Initialize with background and player
                self.level1_objects[0].properties["position"] = [-450,-370,0]
                self.level1_objects[3].properties["position"] = [-450,-370,0]

                self.platform_key_map1 = {}  # Dictionary to track keys per platform

                increment = 115
                for i in range(7):  # Creating 7 platforms
                    platform = Object(self.shaders[0], platforml1Props)
                    platform.properties["position"][0] += increment
                    increment += 115
                    platform.properties["velocity"] = np.array([0, random.uniform(30, 120), 0], dtype=np.float32)

                    self.level1_objects.append(platform)  

                    if i in {1, 3, 5}:  # Attach keys to some platforms
                        key = Object(self.shaders[0], keyProps)
                        key.properties["position"] = np.array([
                            platform.properties["position"][0], 
                            platform.properties["position"][1] + 10, 0
                        ])
                        key.properties["velocity"] = np.copy(platform.properties["velocity"])  # Sync movement

                        self.platform_key_map1[id(platform)] = key  # Track using platform's unique ID
                        self.level1_objects.append(key)  

                # Initialize enemy alligators list
                self.spawned_alligators = []
                self.last_spawn_time1 = 0  # Track last spawn time

        if level==2:
            # Level-2:
            if not hasattr(self, "level2_objects") or self.level2_objects is None or len(self.level2_objects)==0:
                self.level2_objects = [
                    Object(self.shaders[0], playerProps), 
                    Object(self.shaders[0],statBarProps), 
                    Object(self.shaders[0], bgl2Props),
                    Object(self.shaders[0], exitPortalProps),
                    Object(self.shaders[0], exitPortalProps)
                ]  # Initialize with background and player
                self.level2_objects[0].properties["position"] = [-450, -350, 0]
                self.level2_objects[3].properties["position"] = [-450, -350, 0]

                # Initialize Level 2 platforms (moving horizontally)
                self.platform_key_map2 = {}  # Dictionary to track keys per platform

                y_position = -265
                for i in range(8):  # Creating 8 platforms (indices 2 to 9)
                    platform = Object(self.shaders[0], platforml2Props)
                    platform.properties["position"] = np.array([0, y_position, -0.1], dtype=np.float32)
                    y_position += 75  
                    platform.properties["velocity"] = np.array([random.uniform(50, 150), 0, 0], dtype=np.float32)

                    self.level2_objects.append(platform)  

                    if i in {2, 4, 6}:  # Attach keys to some platforms
                        key = Object(self.shaders[0], keyProps)
                        key.properties["position"] = np.array([
                            platform.properties["position"][0]+5, 
                            platform.properties["position"][1] + 20, 0
                        ])
                        key.properties["velocity"] = np.copy(platform.properties["velocity"])  # Sync movement

                        self.platform_key_map2[id(platform)] = key  # Track using platform's unique ID
                        self.level2_objects.append(key)  

                # Initialize enemy rocks list
                self.falling_rocks = []
                self.last_spawn_time2 = 0  # Track last spawn time
        if level==3:
            if not hasattr(self, "level3_objects") or self.level3_objects is None or len(self.level3_objects)==0:
                self.level3_objects = [
                    Object(self.shaders[0], playerProps), 
                    Object(self.shaders[0],statBarProps), 
                    Object(self.shaders[0], bgl3Props),
                    Object(self.shaders[0], bgl3_portal1Props),
                    Object(self.shaders[0], bgl3_portal2Props),
                    Object(self.shaders[0], exitPortalProps),
                    Object(self.shaders[0], exitPortalProps)
                ]
                
                self.level3_objects[0].properties["position"] = [-430, -350, 0]
                self.level3_objects[5].properties["position"] = [-430, -350, 0]

                self.platform_key_map3 = {}
                for i in range(5):
                    platform_paths = self.platform_paths
                    platform = Object(self.shaders[0], platforml3Props)
                    platform.properties["position"] = np.copy(platform_paths[i][0])

                    # Compute velocity along path
                    start, end = platform_paths[i]
                    direction = end - start
                    slope = direction[1] / direction[0] if direction[0] != 0 else np.inf  # Handle vertical case

                    # Pick a random speed and compute the other component
                    random_speed_x = random.uniform(60, 90)
                    if slope == np.inf:  # Vertical movement
                        velocity = np.array([0, np.sign(direction[1]) * random_speed_x, 0], dtype=np.float32)
                    else:
                        velocity_y = slope * random_speed_x
                        velocity = np.array([np.sign(direction[0]) * random_speed_x, np.sign(direction[1]) * abs(velocity_y), 0], dtype=np.float32)

                    platform.properties["velocity"] = velocity
                    platform.properties["current_target"] = 1
                    
                    self.level3_objects.append(platform)

                    if i in {1, 2, 3}:
                        key = Object(self.shaders[0], keyProps)
                        key.properties["position"] = np.array([platform.properties["position"][0]+5,platform.properties["position"][1]+10,0])
                        key.properties["velocity"] = platform.properties["velocity"]
                        key.properties["current_target"] = 1
                        self.platform_key_map3[id(platform)] = key
                        self.level3_objects.append(key)

                self.potionGen(self.level3_objects)
                # Initialize enemy meteors list
                self.falling_meteors = []
                self.last_spawn_time3 = 0  # Track last spawn time

    def playerMovement(self, player, inputs, time):
        if self.dash_active==False and self.dash_cooldown_timer < 1000:
            self.dash_cooldown_timer +=1
        elif self.dash_cooldown_timer >= 1000:
            self.dash_cooldown_timer = 0
            self.dash_active = True

        # Player movement using inputs (Common for all Levels)
        if "W" in inputs and player.properties["position"][1] < self.height / 2 - player.properties["scale"][1]:
            player.properties["velocity"][1] = player.properties["sens"]
        if "S" in inputs and player.properties["position"][1] > -self.height / 2 + player.properties["scale"][1]:
            player.properties["velocity"][1] = -player.properties["sens"]
        if "A" in inputs and player.properties["position"][0] > -self.width / 2 + player.properties["scale"][0]:
            player.properties["velocity"][0] = -player.properties["sens"]
        if "D" in inputs and player.properties["position"][0] < self.width / 2 - player.properties["scale"][0]:
            player.properties["velocity"][0] = player.properties["sens"]
        if "SPACE" in inputs:
            player.properties["scale"] = [33,33,1]
        if "SPACE" not in inputs:
            player.properties["scale"] = [30,30,1]
        dash_c1 =  self.screen==2 and self.dash_active 

        # Apply velocity to player's position
        player.properties["position"] += player.properties["velocity"] * time["deltaTime"]
        if "E" in inputs and player.properties["position"][0] < self.width / 2 - player.properties["scale"][0] and dash_c1:
            player.properties["velocity"][1] = 500
            player.properties["position"] += player.properties["velocity"] * time["deltaTime"] * 150
            self.dash_active = False
                
    def platform_and_obstaclesl1(self, inputs, time):

        for obj in self.level1_objects:  
            if obj.properties.get("type") == "platform":  # Move only platforms
                position = obj.properties["position"]
                velocity = obj.properties["velocity"]

                # Update platform position
                position[1] += velocity[1] * time["deltaTime"]

                # Reverse direction if boundary reached
                if position[1] >= self.height / 2 or position[1] <= -self.height / 2:
                    obj.properties["velocity"][1] *= -1  # Reverse velocity

                # Move attached key (if exists)
                platform_id = id(obj)
                if platform_id in self.platform_key_map1:
                    key = self.platform_key_map1[platform_id]
                    key.properties["position"][1] += velocity[1] * time["deltaTime"]

        keys_to_remove = []

        for obj in self.level1_objects:
            if obj.properties.get("type") == "key":
                player_pos = self.level1_objects[0].properties["position"]
                key_pos = np.array([obj.properties["position"][0], obj.properties["position"][1]+5, 0])

                # Check collision
                if np.linalg.norm(player_pos[:2] - key_pos[:2]) < 20:
                    keys_to_remove.append(obj)  # Mark for removal

        # Remove keys without affecting list indexing
        for key in keys_to_remove:
            self.level1_objects.remove(key)

            # Also remove from the mapping
            for platform_id, k in list(self.platform_key_map1.items()):
                if k == key:
                    del self.platform_key_map1[platform_id]
                    break

        # === Spawning Alligators (enemyl1Props) ===
        spawn_interval1 = 5  # Spawn every 3 seconds
        if time["currentTime"] - self.last_spawn_time1 > spawn_interval1:
            self.last_spawn_time1 = time["currentTime"]
            spawn_from_top = random.choice([True, False])  # Decide if it spawns from top or bottom
            
            alligator = Object(self.shaders[0], enemyl1Props)
            x_pos = random.uniform(-self.width / 2 + 200, self.width / 2 - 200)
            y_pos = self.height / 2 if spawn_from_top else -self.height / 2
            alligator.properties["position"] = np.array([x_pos, y_pos, -0.09], dtype=np.float32)
            alligator.properties["velocity"] = np.array([0, -120 if spawn_from_top else 120, 0], dtype=np.float32)
            
            # Flip if coming from the bottom
            if not spawn_from_top:
                alligator.properties["rotation_z"] += 3.14
            
            self.spawned_alligators.append(alligator)
            self.level1_objects.append(alligator)
    
        for alligator in self.spawned_alligators:
            alligator.properties["position"][0] += alligator.properties["velocity"][0] * time["deltaTime"]
            alligator.properties["position"][1] += alligator.properties["velocity"][1] * time["deltaTime"]

        # Remove alligators that move out of screen
        self.spawned_alligators = [a for a in self.spawned_alligators if -self.height / 2 - 200 < a.properties["position"][1] < self.height / 2 + 200]
        self.level1_objects = [obj for obj in self.level1_objects if obj in self.spawned_alligators or obj not in self.spawned_alligators]

        # Update the player object based on inputs
        player1 = self.level1_objects[0]
        player1.properties["velocity"] = np.array([0, 0, 0], dtype=np.float32)
        player1_on_platform1 = None  # Track which platform the player is standing on

        # Check if the player is resting on a platform
        for platform1 in self.level1_objects[5:12]:  # Only check against platforms
            player1_bottom = player1.properties["position"][1] - player1.properties["scale"][1] / 2 + 15
            platform1_top = platform1.properties["position"][1] + platform1.properties["scale"][1] / 2 - 15
            platform1_left = platform1.properties["position"][0] - platform1.properties["scale"][0] / 2
            platform1_right = platform1.properties["position"][0] + platform1.properties["scale"][0] / 2
            player1_x = player1.properties["position"][0]

            # Make the landing area larger
            landing_tolerance1 = 30  # Increase tolerance for landing detection

            # Check if player is fully on top of the platform and aligned horizontally
            if abs(player1_bottom - platform1_top) < landing_tolerance1 and platform1_left - 10 <= player1_x <= platform1_right + 10:
                player1.properties["velocity"][1] = platform1.properties["velocity"][1]  # Inherit velocity
                player1_on_platform1 = platform1  # Store the platform reference

        # If the player is on a platform and the platform bounces, reverse the player's velocity
        upper_bound = self.height / 2  # Set appropriate upper boundary
        lower_bound = -self.height / 2  # Set appropriate lower boundary
        if player1_on_platform1:
            platform1 = player1_on_platform1
            if platform1.properties["position"][1] >= upper_bound or platform1.properties["position"][1] <= lower_bound:
                player1.properties["velocity"][1] *= -1  # Reverse player's velocity too

        player = player1
        if self.screen == 1:
            if ("E" in inputs) and not player.properties.get("water_dash_active", False):
                if player.properties.get("water_dash_cooldown", 0) <= 0:
                    dash_force = np.array([200, 0, 0], dtype=np.float32) * (1 if player.properties["facing_right"] else -1)
                    player.properties["velocity"] += dash_force
                    player.properties["water_dash_active"] = True
                    player.properties["water_dash_cooldown"] = 8  # Cooldown starts

            # Reset dash after execution
            if player.properties.get("water_dash_active", False):
                player.properties["water_dash_active"] = False  # Allow next dash after cooldown

            # Reduce cooldown timer
            if player.properties.get("water_dash_cooldown", 0) > 0:
                player.properties["water_dash_cooldown"] -= time["deltaTime"]

        return player1
            
    def platform_and_obstaclesl2(self, time):
        for obj in self.level2_objects:  
            if obj.properties.get("type") == "platform":  # Move only platforms
                position = obj.properties["position"]
                velocity = obj.properties["velocity"]

                # Update platform position
                position[0] += velocity[0] * time["deltaTime"]

                # Reverse direction if boundary is reached
                left_bound = -self.width / 2  # Set appropriate left boundary
                right_bound = self.width / 2  # Set appropriate right boundary

                if position[0] <= left_bound or position[0] >= right_bound:
                    obj.properties["velocity"][0] *= -1  # Reverse platform's velocity

                # Move attached key (if exists)
                platform_id = id(obj)
                if platform_id in self.platform_key_map2:
                    key = self.platform_key_map2[platform_id]
                    key.properties["position"][0] += velocity[0] * time["deltaTime"]

        keys_to_remove = []

        for obj in self.level2_objects:
            if obj.properties.get("type") == "key":
                player_pos = self.level2_objects[0].properties["position"]
                key_pos = np.array([obj.properties["position"][0], obj.properties["position"][1]+5, 0])

                # Check collision
                if np.linalg.norm(player_pos[:2] - key_pos[:2]) < 20:
                    keys_to_remove.append(obj)  # Mark for removal

        # Remove keys without affecting list indexing
        for key in keys_to_remove:
            self.level2_objects.remove(key)

        # Update the player object based on inputs in Level 2
        player2 = self.level2_objects[0]
        player2.properties["velocity"] = np.array([0, 0, 0], dtype=np.float32)
        player2_on_platform2 = None

        # Check if the player is on a horizontally moving platform
        for platform2 in self.level2_objects[5:13]:
            player2_bottom = player2.properties["position"][1] - player2.properties["scale"][1] / 2 + 15
            platform2_top = platform2.properties["position"][1] + platform2.properties["scale"][1] / 2 - 15
            platform2_left = platform2.properties["position"][0] - platform2.properties["scale"][0] / 2 
            platform2_right = platform2.properties["position"][0] + platform2.properties["scale"][0] / 2 
            player2_x = player2.properties["position"][0]

            if abs(player2_bottom - platform2_top) < 30 and platform2_left - 100 <= player2_x <= platform2_right + 100:
                player2.properties["velocity"][0] = platform2.properties["velocity"][0]  # Inherit horizontal velocity
                player2_on_platform2 = platform2

        # === Spawning Falling Rocks ===
        spawn_interval = 5  # Spawn new rock every 1.5 seconds
        if time["currentTime"] - self.last_spawn_time2 > spawn_interval:
            self.last_spawn_time2 = time["currentTime"]

            # Generate a new falling rock
            rock = Object(self.shaders[0], enemyl2Props)
            rock.properties["position"] = np.array([random.uniform(-self.width / 2 + 100, self.width / 2 - 100), self.height / 2, -0.09], dtype=np.float32)
            rock.properties["velocity"] = np.array([0, -random.uniform(80, 120), 0], dtype=np.float32)
            
            self.falling_rocks.append(rock)
            self.level2_objects.append(rock)

        # === Updating Falling Rocks ===
        for rock in self.falling_rocks:
            rock.properties["position"][0] += rock.properties["velocity"][0] * time["deltaTime"]
            rock.properties["position"][1] += rock.properties["velocity"][1] * time["deltaTime"]

        # Remove rocks that fall below the screen
        self.falling_rocks = [rock for rock in self.falling_rocks if rock.properties["position"][1] > -self.height / 2]

        # Remove rocks from level2_objects when they disappear
        self.level2_objects = [obj for obj in self.level2_objects if obj in self.falling_rocks or obj not in self.falling_rocks]

        return player2

    def platform_and_obstaclesl3(self, time):
        platform_paths = self.platform_paths
        platforms = [obj for obj in self.level3_objects if obj.properties.get("type") == "platform"]
        keys = [obj for obj in self.level3_objects if obj.properties.get("type") == "key"]

        # Move Platforms
        for i, platform in enumerate(platforms):
            target = platform_paths[i][platform.properties["current_target"]]
            direction = target - platform.properties["position"]
            distance = np.linalg.norm(direction)

            if distance < 10:  # If close to target, switch direction
                platform.properties["current_target"] = 1 - platform.properties["current_target"]
                platform.properties["velocity"] *= -1  # Reverse velocity

            platform.properties["position"] += platform.properties["velocity"] * time["deltaTime"]

        # Move Keys (Keys move with their respective platform)
        for key in keys:
            # Find the closest platform (Assuming each key is attached to a platform)
            closest_platform = min(platforms, key=lambda p: np.linalg.norm(p.properties["position"] - key.properties["position"]))
            key.properties["velocity"] = np.copy(closest_platform.properties["velocity"])
            key.properties["position"] += key.properties["velocity"] * time["deltaTime"]

        # Player Assignment
        player3 = self.level3_objects[0]
        player3.properties["velocity"] = np.array([0, 0, 0], dtype=np.float32)
        player3_on_platform3 = None

        # Check if the player is resting on a platform
        for platform3 in platforms:
            player3_bottom = player3.properties["position"][1] - player3.properties["scale"][1] / 2 + 30  # Increased tolerance
            platform3_top = platform3.properties["position"][1] + platform3.properties["scale"][1] / 2 - 20  # Slightly reduced
            platform3_left = platform3.properties["position"][0] - platform3.properties["scale"][0] / 2 + 30  # Less restrictive
            platform3_right = platform3.properties["position"][0] + platform3.properties["scale"][0] / 2 - 30  # More room for landing
            player3_x = player3.properties["position"][0]

            # Increase landing tolerance
            landing_tolerance3 = 60  # More forgiving landing zone

            # Check if the player is close enough to land
            if abs(player3_bottom - platform3_top) < landing_tolerance3 and platform3_left - 80 <= player3_x <= platform3_right + 80:
                # Player fully inside platform, inherit velocity
                player3.properties["velocity"] = np.copy(platform3.properties["velocity"])
                player3_on_platform3 = platform3  # Store platform reference
                # break  # Stop checking once we find a valid platform


        # If the player is on a platform and the platform reaches its path endpoint, reverse velocity properly
        if player3_on_platform3:
            i = platforms.index(player3_on_platform3)  # Find the correct index for platform_paths
            target = platform_paths[i][player3_on_platform3.properties["current_target"]]

            # Check if the platform reached its predefined path endpoint
            bounce_tolerance = 30  # Allow slight tolerance for bounce-back
            if np.linalg.norm(player3_on_platform3.properties["position"] - target) < 10 :
                # Flip both velocity components to stay on the predefined paths
                player3.properties["velocity"] *= -1

        # Remove Keys When Player Touches Them
        keys_to_remove = []
        for key in keys:
            key_x, key_y = key.properties["position"][0], key.properties["position"][1] - 5
            player_x, player_y = player3.properties["position"][0], player3.properties["position"][1]
            
            key_width, key_height = key.properties["scale"][0], key.properties["scale"][1]
            player_width, player_height = player3.properties["scale"][0], player3.properties["scale"][1]

            # Simple AABB collision detection
            if (abs(player_x - key_x) < (player_width + key_width) / 2) and (abs(player_y - key_y) < (player_height + key_height) / 2):
                keys_to_remove.append(key)

        # Remove collected keys from the object list
        self.level3_objects = [obj for obj in self.level3_objects if obj not in keys_to_remove]

        # === Spawning Falling Meteors (enemyl3Props) ===
        spawn_interval3 = 5  # Spawn every 3 seconds
        if time["currentTime"] - self.last_spawn_time3 > spawn_interval3:
            self.last_spawn_time3 = time["currentTime"]
            
            meteor = Object(self.shaders[0], enemyl3Props)
            x_pos = random.uniform(-self.width / 2 + 100, self.width / 2 - 100)
            meteor.properties["position"] = np.array([x_pos, self.height / 2, -0.08], dtype=np.float32)
            meteor.properties["velocity"] = np.array([0, -random.uniform(100, 120), 0], dtype=np.float32)
            
            self.falling_meteors.append(meteor)
            self.level3_objects.append(meteor)

        # === Updating Falling Meteors ===
        for meteor in self.falling_meteors:
            meteor.properties["position"][0] += meteor.properties["velocity"][0] * time["deltaTime"]
            meteor.properties["position"][1] += meteor.properties["velocity"][1] * time["deltaTime"]

        # Remove meteors that fall below the screen
        self.falling_meteors = [meteor for meteor in self.falling_meteors if meteor.properties["position"][1] > -self.height / 2 - 200]
        self.level3_objects = [obj for obj in self.level3_objects if obj in self.falling_meteors or obj not in self.falling_meteors]

        return player3

    def enemy_collisions(self, player, inputs):
        player_pos_wrt_enemy = player.properties["position"]
        player_radius = 20  

        # Check for collisions with enemies
        for enemy in self.spawned_alligators if self.screen == 1 else \
                    self.falling_rocks if self.screen == 2 else \
                    self.falling_meteors if self.screen == 3 else []:
            enemy_pos = enemy.properties["position"]
            enemy_radius = 25  

            # Compute Euclidean distance between player and enemy
            distance = np.linalg.norm(player_pos_wrt_enemy[:2] - enemy_pos[:2])

            # If collision occurs and space bar is not pressed
            if distance < player_radius + enemy_radius and "SPACE" not in inputs:
                self.health -= 0.5

                if self.health <= 0:    
                    self.lives -= 1

                    # Reset player position to initial position
                    if self.screen == 1:
                        player.properties["position"] = np.array([-450, -370, 0], dtype=np.float32)  # Initial position for Level 1
                    elif self.screen == 2:
                        player.properties["position"] = np.array([-450, -350, 0], dtype=np.float32)  # Initial position for Level 2
                    elif self.screen == 3:
                        player.properties["position"] = np.array([-430, -350, 0], dtype=np.float32)  # Initial position for Level 3

                    self.health = 100

    def keyCollection(self, player, obj_list):
        """Check if the player collides with any key and collect it."""
        player_pos = player.properties["position"]
        key_radius = 30  # Adjust based on key size

        keys_to_remove = []
        
        for key in obj_list:
            if key.properties.get("type") == "key":
                key_pos = key.properties["position"]

                # Compute Euclidean distance
                distance = np.linalg.norm(player_pos[:2] - key_pos[:2])

                if distance < key_radius:  # If collision occurs
                    self.keys_collected += 1
                    keys_to_remove.append(key)

        # Remove collected keys from the level objects
        for key in keys_to_remove:
            obj_list.remove(key)

    def ProcessFrame(self, inputs, time):
        # Level1:
        self.initializeLevel(1)
        player1 = self.platform_and_obstaclesl1(inputs, time)

        self.keyCollection(player1, self.level1_objects)

        # Level-2:
        self.initializeLevel(2)
        player2 = self.platform_and_obstaclesl2(time)

        self.keyCollection(player2, self.level2_objects)

        # Level-3:
        self.initializeLevel(3)
        player3 = self.platform_and_obstaclesl3(time)

        self.keyCollection(player3, self.level3_objects)

        """Check if the player collides with any key and collect it."""
        player_pos = player3.properties["position"]
        potion_radius = 30  # Adjust based on key size

        potions_to_remove = []
        
        for potion in self.level3_objects:
            if potion.properties.get("type") == "potion":
                potion_pos = potion.properties["position"]

                # Compute Euclidean distance
                distance = np.linalg.norm(player_pos[:2] - potion_pos[:2])

                if distance < potion_radius:  # If collision occurs
                    self.keys_collected += 1
                    potions_to_remove.append(potion)

        # Remove collected keys from the level objects
        for potion in potions_to_remove:
            self.health += 30
            if self.health > 100:
                self.health = 100
            self.level3_objects.remove(potion)

        player = player1
        exitPortal = self.level1_objects[3]
        # Set Player:
        if self.screen == 1:
            player = player1
            exitPortal = self.level1_objects[4]
        if self.screen == 2:
            player = player2
            exitPortal = self.level2_objects[4]
        if self.screen == 3:
            player = player3
            exitPortal = self.level3_objects[6]

        # Player movement using inputs (Common for all Levels)
        self.playerMovement(player,inputs,time)
        self.enemy_collisions(player,inputs)

        # Check if the player is not standing on any platform or portal
        is_on_platform = False
        is_on_portal = False

        # Check if the player is on a platform (level1)
        for platform in self.level1_objects[5:12]:  # Adjust indices for other levels
            player_bottom = player.properties["position"][1] - player.properties["scale"][1] / 2 + 15
            platform_top = platform.properties["position"][1] + platform.properties["scale"][1] / 2 - 15
            platform_left = platform.properties["position"][0] - platform.properties["scale"][0] / 2 
            platform_right = platform.properties["position"][0] + platform.properties["scale"][0] / 2 
            player_x = player.properties["position"][0]
            
            c1l1 = abs(player_bottom - platform_top) < 100 and platform_left - 50 <= player_x <= platform_right + 50
            c2l1 = player.properties["position"][0]<-400 or player.properties["position"][0]>400
            if c1l1 or c2l1:
                is_on_platform = True
                break

        # Check if the player is on a platform (level2)
        for platform in self.level2_objects[5:13]:  # Adjust indices for other levels
            player_bottom = player.properties["position"][1] - player.properties["scale"][1] / 2 + 15
            platform_top = platform.properties["position"][1] + platform.properties["scale"][1] / 2 - 15
            platform_left = platform.properties["position"][0] - platform.properties["scale"][0] / 2 
            platform_right = platform.properties["position"][0] + platform.properties["scale"][0] / 2 
            player_x = player.properties["position"][0]
            
            c1l2 = abs(player_bottom - platform_top) < 100 and platform_left - 50 <= player_x <= platform_right + 50
            c2l2 = player.properties["position"][1]<-300 or player.properties["position"][1]>300
            if c1l2 or c2l2:
                is_on_platform = True
                break

        # Check if the player is on a platform (level3)
        for platform in self.level3_objects[7:12]:  # Adjust indices for other levels
            player_bottom = player.properties["position"][1] - player.properties["scale"][1] / 2 + 15
            platform_top = platform.properties["position"][1] + platform.properties["scale"][1] / 2 - 15
            platform_left = platform.properties["position"][0] - platform.properties["scale"][0] / 2 
            platform_right = platform.properties["position"][0] + platform.properties["scale"][0] / 2 
            player_x = player.properties["position"][0]
            
            c1l3 = abs(player_bottom - platform_top) < 70 and platform_left - 50 <= player_x <= platform_right + 50
            c2l3 = player.properties["position"][1]<-300 or player.properties["position"][1]>300
            if c1l3 or c2l3:
                is_on_platform = True
                break

        # Check if the player is on a portal (if applicable)
        if self.screen == 3:
            for portal in [self.level3_objects[3], self.level3_objects[4]]:  # Portals are indices 3 and 4
                portal_pos = portal.properties["position"]
                portal_radius = 50  # Adjust based on portal size
                distance = np.linalg.norm(player.properties["position"][:2] - portal_pos[:2])
                if distance < portal_radius + 10:
                    is_on_portal = True
                    break

        # If the player is not on any platform or portal, reset their position and decrement lives
        if not is_on_platform and not is_on_portal:
            # Reset player position to the initial position
            if self.screen == 1:
                player.properties["position"] = np.array([-450, -370, 0], dtype=np.float32)  # Initial position for Level 1
            elif self.screen == 2:
                player.properties["position"] = np.array([-450, -350, 0], dtype=np.float32)  # Initial position for Level 2
            elif self.screen == 3:
                player.properties["position"] = np.array([-430, -350, 0], dtype=np.float32)  # Initial position for Level 3

            # Decrement lives
            self.lives -= 1
            self.health = 100

            # Check if lives are exhausted
            if self.lives <= 0:
                self.screen =  5
                print("Game Over!")
                # Handle game over logic (e.g., reset game or show game over screen)
        
        if self.screen == 1 or self.screen == 2 or self.screen==3:
            self.nextLevel(player, exitPortal)

        # Continue with UI and scene rendering
        imgui.set_current_context(imgui.get_current_context())
        self.imgui_renderer.process_inputs()
        imgui.new_frame()

        print(f"Updating Game Scene... Inputs: {inputs}")
        if self.screen == -1:
            self.screen = 0
            self.InitScreen(time)
        
        if self.screen == 0:
            self.DrawHomeScreen(inputs, time)
        
        if self.screen == 1:
            self.objects = self.level1_objects 
            self.RenderStatusBar(inputs, time)
            self.DrawScene()

        if self.screen == 2:
            self.objects = self.level2_objects 
            self.RenderStatusBar(inputs, time)
            self.DrawScene()

        if self.screen == 3:
            self.objects = self.level3_objects 
            self.RenderStatusBar(inputs, time)
            self.DrawScene()

        if self.screen == 4:
            self.DrawStartUpScreen(inputs, time, player1)
        
        if self.screen == 5:
            self.DrawGameOverScreen(inputs, time)

        if self.screen == 6:
            self.DrawYouWonScreen(inputs, time)

        imgui.render()
        self.imgui_renderer.render(imgui.get_draw_data())

    def SaveGame(self, time):
        """Save the current game state to a JSON file."""
        # Prepare the game state data
        game_state = {
            "level": self.screen,
            "lives": self.lives,
            "health": self.health,
            "keys_collected": self.keys_collected,
            "time_elapsed": time["currentTime"],  
            "save_timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp of the save
        }

        # Generate a unique filename for the save file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        save_filename = f"save_{timestamp}.json"
        if not os.path.exists("saved_files"):
            os.makedirs("saved_files")
        save_path = os.path.join("saved_files" , save_filename)

        # Write the game state to the JSON file
        with open(save_path, "w") as save_file:
            json.dump(game_state, save_file, indent=4)

        print(f"Game saved to {save_path}")

    def RenderStatusBar(self, inputs, time):
        level_names = [
            "River Biome",
            "Magma Trench",
            "Lost in Space"
        ]

        """Renders the status bar displaying game information."""
        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(1000, 50)
        
        # Remove window decorations and make it static
        imgui.begin("Status Bar", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)

        # Display game stats
        imgui.text(f"Level: {self.screen}")
        imgui.same_line(spacing=50)
        imgui.text(f"{level_names[self.screen-1]}")
        imgui.same_line(spacing=50)
        imgui.text(f"Health: {self.health}")
        imgui.same_line(spacing=50)
        imgui.text(f"Lives: {self.lives}")
        imgui.same_line(spacing=50)
        imgui.text(f"Keys: {self.keys_collected}")
        imgui.same_line(spacing=50)
        imgui.text(f"Time: {time['currentTime']:.1f}s")

        imgui.same_line(position=900)
        if imgui.button("Save Game", 90, 30):
            self.SaveGame(time)  

        imgui.end()

    def DrawScene(self):
        for shader in self.shaders:
            self.camera.Update(shader)

        for obj in self.objects:
            obj.Draw()

          




            
            
        


