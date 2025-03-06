import imgui, random
import numpy as np
from OpenGL.GL import *  
from utils.graphics import Object, Camera, Shader
from assets.shaders.shaders import standard_shader, ui_shader
from assets.objects.objects import (create_transporter, create_pirate, create_planet, 
                                  create_space_station, create_laser, create_arrow, create_crosshair)

class Game:
    def __init__(self, height, width, gui):
        self.gui = gui
        self.height = height
        self.width = width
        self.screen = 0
        self.gameState = {} # Object list
        self.cameraYaw = 0.0  # Initial yaw
        self.cameraPitch = 0.0  # Initial pitch

    def InitScene(self):
        if self.screen == 1:            
            # Initialize shaders
            self.shaders = {
                'standard': Shader(standard_shader["vertex_shader"], standard_shader["fragment_shader"]),
                'ui': Shader(ui_shader["vertex_shader"], ui_shader["fragment_shader"])
            }
            
            # Initialize camera with proper lookAt vector
            self.camera = Camera(self.height, self.width)
            self.camera.position = np.array([0, -20, 8], dtype=np.float32)
            self.camera.lookAt = np.array([0, 0, 0], dtype=np.float32)  # Look at origin
            
            # Define world boundaries
            self.worldMin = np.array([-10000, -10000, -10000], dtype=np.float32)
            self.worldMax = np.array([10000, 10000, 10000], dtype=np.float32)
            
            # Set up light position
            self.lightPos = np.array([1000, 1000, 1000], dtype=np.float32)

            # Initialize planets and space stations:
            self.n_planets = 25 
            self.gameState["planets"] = []
            self.gameState["spaceStations"] = []
            self.gameState["lasers"] = []
            self.init_planets_spacestations()

            # Initialize transporter
            transporter_vertices, transporter_indices = create_transporter()
            print(f"Transporter mesh created with {len(transporter_vertices)/6} vertices")
            self.gameState["transporter"] = Object("transporter", self.shaders['standard'], {
                'vertices': transporter_vertices,
                'indices': transporter_indices,
                'position': self.gameState["planets"][0].properties["position"] + np.array([0,0,35]),
                'rotation': np.array([0, 0, np.pi/2], dtype=np.float32), 
                'scale': np.array([3, 3, 3], dtype=np.float32),
                'colour': np.array([0.69, 0.69, 0.702, 1.0], dtype=np.float32),
                'velocity': np.array([0, 0, 0], dtype=np.float32),
                'view': 1
            })

            # Set destination planet/spacestation
            self.des_planet = self.gameState["spaceStations"][1]

            # Initialize minimap arrow
            arrow_vertices, arrow_indices = create_arrow()
            self.gameState["arrow"] = Object("arrow", self.shaders['ui'], {
                'vertices': arrow_vertices,
                'indices': arrow_indices,
                'position': np.array([0.8, -0.8, 0], dtype=np.float32),  # Bottom right corner
                'rotation': np.array([0, 0, 0], dtype=np.float32),
                'scale': np.array([0.05, 0.05, 0.05], dtype=np.float32),
                'colour': np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)
            })

            #Initialize pirates:
            self.init_pirates(15)

            # Initialize crosshair
            crosshair_vertices, crosshair_indices = create_crosshair()
            self.gameState["crosshair"] = Object("crosshair", self.shaders['ui'], {
                'vertices': crosshair_vertices,
                'indices': crosshair_indices,
                'position': np.array([0,0,0], dtype=np.float32),
                'rotation': np.array([0, 0, 0], dtype=np.float32),
                'scale': np.array([1, 1, 1], dtype=np.float32),
                'colour': np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)
            })

            print("\nScene initialization complete")
        
        if self.screen == 2:
            pass

        if self.screen == 3:
            pass

    def init_planets_spacestations(self):
        planet_vertices, planet_indices = create_planet()
        station_vertices, station_indices = create_space_station()
        
        # Create planets at random positions
        for i in range(self.n_planets):
            # Random position within world bounds (but not too close to center)
            min_dist = 1000  # Minimum distance from center
            max_dist = 10000  # Maximum distance from center
            
            angle = np.random.uniform(0, 2 * np.pi)
            distance = np.random.uniform(min_dist, max_dist)
            height = np.random.uniform(-3000, 3000)
            
            position = np.array([
                distance * np.cos(angle),
                distance * np.sin(angle),
                height
            ], dtype=np.float32)
            
            # Create planet
            planet = Object("planet", self.shaders['standard'], {
                'vertices': planet_vertices,
                'indices': planet_indices,
                'position': position,
                'rotation': np.random.uniform(0, 2 * np.pi, 3),
                'scale': np.array([35, 35, 35], dtype=np.float32),
                'colour': np.array([
                    np.random.uniform(0.3, 0.8),
                    np.random.uniform(0.2, 0.5),
                    np.random.uniform(0.2, 0.5),
                    1.0
                ], dtype=np.float32)
            })
            self.gameState["planets"].append(planet)
            
            # Create space station orbiting the planet
            orbit_radius = 70  
            station_angle = np.random.uniform(0, 2 * np.pi)
            station_pos = position + np.array([
                orbit_radius * np.cos(station_angle),
                orbit_radius * np.sin(station_angle),
                10
            ], dtype=np.float32)
            
            station = Object("spacestation", self.shaders['standard'], {
                'vertices': station_vertices,
                'indices': station_indices,
                'position': station_pos,
                'rotation': np.array([0, station_angle, 0], dtype=np.float32),
                'scale': np.array([5, 5, 5], dtype=np.float32),
                'colour': np.array([0.8, 0.8, 0.8, 1.0], dtype=np.float32),
                'orbit_center': position,
                'orbit_radius': orbit_radius,
                'orbit_angle': station_angle,
                'orbit_speed': 0.001  # Radians per frame
            })
            self.gameState["spaceStations"].append(station)

    def init_pirates(self, num_pirates=10):
        self.gameState["pirates"] = []

        min_dist = 1000  # Minimum distance from center
        max_dist = 10000  # Maximum distance from center
        
        angle = np.random.uniform(0, 2 * np.pi)
        distance = np.random.uniform(min_dist, max_dist)
        height = np.random.uniform(-3000, 3000)
        
        position = np.array([
            distance * np.cos(angle),
            distance * np.sin(angle),
            height
        ], dtype=np.float32)
        
        for _ in range(num_pirates):
            pir_ver, pir_ind = create_pirate()
            pirate = Object("pirate", self.shaders['standard'], {
                'vertices': pir_ver,
                'indices': pir_ind,
                'position': position,
                'rotation': np.array([0, 0, 0], dtype=np.float32),
                'velocity': np.array([0, 0, 0], dtype=np.float32),
                'scale': np.array([5,5,5]),
                'colour': np.array([
                    np.random.uniform(0.3, 0.8),
                    np.random.uniform(0.2, 0.5),
                    np.random.uniform(0.2, 0.5),
                    1.0
                ], dtype=np.float32)
            })
            self.gameState["pirates"].append(pirate)

    def ProcessFrame(self, inputs, time):
        self.UpdateScene(inputs, time)
        self.DrawScene()
        self.DrawText()

    def DrawText(self):
        if self.screen == 0:  # Start screen
            window_w, window_h = 400, 200
            x_pos = (self.width - window_w) / 2
            y_pos = (self.height - window_h) / 2

            imgui.new_frame()
            imgui.set_next_window_position(x_pos, y_pos)
            imgui.set_next_window_size(window_w, window_h)
            imgui.begin("Main Menu", False, imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE)

            imgui.set_cursor_pos_x((window_w - imgui.calc_text_size("Press 1: New Game")[0]) / 2)
            imgui.button("Press 1: New Game")

            imgui.end()
            imgui.render()
            self.gui.render(imgui.get_draw_data())

        if self.screen == 2:    # Game Over Screen
            window_w, window_h = 400, 200
            x_pos = (self.width - window_w) / 2
            y_pos = (self.height - window_h) / 2

            imgui.new_frame()
            imgui.set_next_window_position(x_pos, y_pos)
            imgui.set_next_window_size(window_w, window_h)
            imgui.begin("GAME OVER!", False, imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE)

            imgui.set_cursor_pos_x((window_w - imgui.calc_text_size("Press 1: Main Menu")[0]) / 2)
            imgui.button("Press 1: Main Menu")

            imgui.end()
            imgui.render()
            self.gui.render(imgui.get_draw_data())

        if self.screen == 3:    # You Won Screen
            window_w, window_h = 400, 200
            x_pos = (self.width - window_w) / 2
            y_pos = (self.height - window_h) / 2

            imgui.new_frame()
            imgui.set_next_window_position(x_pos, y_pos)
            imgui.set_next_window_size(window_w, window_h)
            imgui.begin("YOU WON!", False, imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE)

            imgui.set_cursor_pos_x((window_w - imgui.calc_text_size("Press 1: Main Menu")[0]) / 2)
            imgui.button("Press 1: Main Menu")

            imgui.end()
            imgui.render()
            self.gui.render(imgui.get_draw_data())

    def UpdateScene(self, inputs, time):
        if self.screen == 0:  # Start screen
            if inputs["1"]:
                self.screen = 1
                self.InitScene()
        
        if self.screen == 1:  # Game screen
            # Update space stations orbits
            if "spaceStations" in self.gameState:
                for station in self.gameState["spaceStations"]:
                    # Update orbit angle
                    station.properties["orbit_angle"] += station.properties["orbit_speed"]
                    
                    # Calculate new position
                    center = station.properties["orbit_center"]
                    radius = station.properties["orbit_radius"]
                    angle = station.properties["orbit_angle"]
                    
                    station.properties["position"] = center + np.array([
                        radius * np.cos(angle),
                        radius * np.sin(angle),
                        10
                    ], dtype=np.float32)
                    
                    # Update rotation to face orbit direction
                    station.properties["rotation"][1] = angle

            # Transporter motion and position updates:
            if "transporter" in self.gameState:
                transporter = self.gameState["transporter"]
                
                # Rotation speeds (in radians per frame)
                rotation_speed = 0.01
                
                # Calculate current nose direction before rotation
                forward = np.array([0, 1, 0], dtype=np.float32)  # Base forward vector
                yaw = transporter.properties["rotation"][1]
                pitch = transporter.properties["rotation"][0]
                roll = transporter.properties["rotation"][2]
                
                # Create rotation matrices
                yaw_matrix = np.array([
                    [np.cos(yaw), 0, np.sin(yaw)],
                    [0, 1, 0],
                    [-np.sin(yaw), 0, np.cos(yaw)]
                ], dtype=np.float32)
                
                pitch_matrix = np.array([
                    [1, 0, 0],
                    [0, np.cos(pitch), -np.sin(pitch)],
                    [0, np.sin(pitch), np.cos(pitch)]
                ], dtype=np.float32)
                
                roll_matrix = np.array([
                    [np.cos(roll), -np.sin(roll), 0],
                    [np.sin(roll), np.cos(roll), 0],
                    [0, 0, 1]
                ], dtype=np.float32)
                
                # Calculate current nose direction
                nose_direction = roll_matrix @ pitch_matrix @ yaw_matrix @ forward
                print(f"Current nose direction: {nose_direction}")
                
                view_cond = self.gameState["transporter"].properties["view"] == 1

                # Handle rotations
                if inputs["W"] and view_cond:  # Pitch up
                    transporter.properties["rotation"][1] -= rotation_speed  # Use Y-axis for pitch, inverted
                if inputs["S"] and view_cond:  # Pitch down
                    transporter.properties["rotation"][1] += rotation_speed  # Use Y-axis for pitch, inverted
                if inputs["A"] and view_cond:  # Yaw left
                    transporter.properties["rotation"][2] += rotation_speed  # Use Z-axis for yaw
                if inputs["D"] and view_cond:  # Yaw right
                    transporter.properties["rotation"][2] -= rotation_speed  # Use Z-axis for yaw
                if inputs["Q"] and view_cond:  # Roll clockwise
                    transporter.properties["rotation"][0] -= rotation_speed  # Use X-axis for roll, inverted
                if inputs["E"] and view_cond:  # Roll counterclockwise
                    transporter.properties["rotation"][0] += rotation_speed  # Use X-axis for roll, inverted

            # Other updates
            self.update_minimap_arrow()
            self.update_transporter_and_camera(transporter, inputs, self.camera)
            self.handle_view_mode(inputs)
            self.des_reach_update()
            self.handle_mouse_input(inputs)
            self.update_laser(time)

        if self.screen == 2:  # Game Over screen
            if inputs["1"]:
                self.screen = 0
                self.InitScene()
        
        if self.screen == 3:  # You Won screen
            if inputs["1"]:
                self.screen = 0
                self.InitScene()

    def DrawScene(self):
        if self.screen == 1:
            # Update camera for standard shader
            self.camera.Update(self.shaders['standard'])
            
            # Set lighting uniforms for standard shader
            self.shaders['standard'].Use()
            lightPosLoc = glGetUniformLocation(self.shaders['standard'].ID, "lightPos".encode('utf-8'))
            viewPosLoc = glGetUniformLocation(self.shaders['standard'].ID, "viewPos".encode('utf-8'))
            
            if lightPosLoc == -1 or viewPosLoc == -1:
                print("Warning: Could not find light/view position uniforms in shader")
            
            glUniform3f(lightPosLoc, self.lightPos[0], self.lightPos[1], self.lightPos[2])
            glUniform3f(viewPosLoc, self.camera.position[0], self.camera.position[1], self.camera.position[2])
            
            # Draw planets
            if "planets" in self.gameState:
                for planet in self.gameState["planets"]:
                    planet.Draw()
            
            # Draw space stations
            if "spaceStations" in self.gameState:
                for station in self.gameState["spaceStations"]:
                    station.Draw()
            
            # Draw transporter
            if "transporter" in self.gameState:
                self.gameState["transporter"].Draw()

            # Draw pirates:
            if "pirates" in self.gameState:
                for pirate in self.gameState["pirates"]:
                    pirate.Draw()
            
            # Draw lasers:
            if "lasers" in self.gameState:
                for laser in self.gameState["lasers"]:
                    laser.Draw()
                    print("LASER SHOT! no of lasers = ", len(self.gameState["lasers"]))
                    

            # Draw UI elements
            if "arrow" in self.gameState:
                self.gameState["arrow"].Draw()
            
            if "crosshair" in self.gameState and self.gameState["transporter"].properties["view"] == 2:
                # glDisable(GL_DEPTH_TEST)  # Disable depth testing to keep it on top
                self.gameState["crosshair"].Draw()
                # glEnable(GL_DEPTH_TEST)   # Re-enable depth testing after drawing

    def get_rotation_matrix(self, yaw, pitch, roll):
        cos_yaw, sin_yaw = np.cos(yaw), np.sin(yaw)
        cos_pitch, sin_pitch = np.cos(pitch), np.sin(pitch)
        cos_roll, sin_roll = np.cos(roll), np.sin(roll)

        # Rotation matrices for each axis
        yaw_matrix = np.array([
            [cos_yaw, 0, sin_yaw],
            [0, 1, 0],
            [-sin_yaw, 0, cos_yaw]
        ])

        pitch_matrix = np.array([
            [1, 0, 0],
            [0, cos_pitch, sin_pitch],
            [0, -sin_pitch, cos_pitch]
        ])

        roll_matrix = np.array([
            [cos_roll, -sin_roll, 0],
            [sin_roll, cos_roll, 0],
            [0, 0, 1]
        ])

        return roll_matrix @ pitch_matrix @ yaw_matrix

    def update_transporter_and_camera(self, transporter, inputs, camera):
        # Retrieve transporter position and rotation
        transporter_pos = transporter.properties["position"]
        yaw, pitch, roll = transporter.properties["rotation"]  

        rotation_matrix = self.get_rotation_matrix(yaw, pitch, roll)

        # Fix for 90-degree rotation around Z-axis (so the "head" points correctly)
        z_fix_matrix = np.array([
            [0, 1, 0],  # Rotates by 90° counterclockwise
            [-1,  0, 0],
            [0,  0, 1]
        ])
        corrected_rotation = z_fix_matrix @rotation_matrix  

        # Handle forward movement (only on SPACE)
        if inputs["SPACE"]:
            forward = np.array([0, 1, 0], dtype=np.float32)  # Local Y-axis (head direction)
            forward = corrected_rotation @ forward  

            # Apply acceleration and speed limit
            acceleration = 0.005
            max_speed = 3.0

            new_velocity = transporter.properties["velocity"] + forward * acceleration
            speed = np.linalg.norm(new_velocity)
            if speed > max_speed:
                new_velocity = (new_velocity / speed) * max_speed
            
            transporter.properties["velocity"] = new_velocity

        # Apply velocity to position
        transporter.properties["position"] += transporter.properties["velocity"]

        # Apply drag for gradual slowdown
        drag = 0.99
        transporter.properties["velocity"] *= drag

        # Camera handling
        camera_offset = np.array([0, -37, 15])  # [Right, Up, Back]

        camera_world_offset = corrected_rotation @ camera_offset

        # Compute the camera's final position
        camera_position = transporter_pos + camera_world_offset

        # Align camera view with the transporter’s new orientation
        look_at_position = transporter_pos + (corrected_rotation @ np.array([0, 10, 0]))  # Forward in local space

        # Ensure camera keeps the transporter aligned in the XY plane
        camera_up = corrected_rotation @ np.array([0, 0, 1])  # Global Z-axis stays up

        # Apply transformations to the camera
        camera.position = camera_position
        camera.lookAt = look_at_position
        camera.up = camera_up

    def handle_view_mode(self, inputs):
        z_fix_matrix = np.array([
            [0, 1, 0],  # Rotates by 90° counterclockwise
            [-1,  0, 0],
            [0,  0, 1]
        ])
        
        # Handle view mode switching
        if inputs["L_SHIFT"]:
            self.gameState["transporter"].properties["view"] = 2
        else:
            self.gameState["transporter"].properties["view"] = 1
        
        transporter = self.gameState["transporter"]
        camera = self.camera
        
        if self.gameState["transporter"].properties["view"] == 1:
            # Enable movement, disable crosshair
            self.update_transporter_and_camera(transporter, inputs, camera)
            self.gameState["crosshair"].properties["scale"] = np.array([0, 0, 0], dtype=np.float32)  # Hide crosshair
        else:
            # First-person mode: Disable movement, enable crosshair
            transporter.properties["velocity"] = np.array([0, 0, 0], dtype=np.float32)
            self.gameState["crosshair"].properties["scale"] = np.array([0.3, 0.3, 0.3], dtype=np.float32)  # Show crosshair
            
            # Position camera on top of the transporter (closer to surface)
            transporter_pos = transporter.properties["position"]
            transporter_rot = z_fix_matrix @ self.get_rotation_matrix(*transporter.properties["rotation"]) 
            
            # Bring the camera slightly closer while keeping it on top
            top_offset = np.array([0, -5, 15], dtype=np.float32)  # Raised position on top surface
            camera.position = transporter_pos + (transporter_rot @ top_offset) 
            
            # Look forward in the direction of the transporter
            camera.lookAt = transporter_pos + (transporter_rot @ np.array([0, 10, 0]))
            camera.up = transporter_rot @ np.array([0, 0, 1])  # Maintain proper "up" direction

        
        # Update pirates
        self.update_pirates()

    def update_pirates(self):
        transporter_pos = self.gameState["transporter"].properties["position"]
        if "pirates" in self.gameState:
            for pirate in self.gameState["pirates"]:
                pirate_pos = pirate.properties["position"]
                direction = transporter_pos - pirate_pos
                direction /= np.linalg.norm(direction)  # Normalize
                pirate.properties["position"] += direction * 0.3  # Movement speed
                
                # Check collision with transporter (Game Over)
                if np.linalg.norm(pirate.properties["position"] - transporter_pos) < 8.0:
                    self.screen = 2
                    print("GAME OVER")  

    def des_reach_update(self):
        transporter_pos = self.gameState["transporter"].properties["position"]
        des_pos = self.gameState["spaceStations"][1].properties["position"]

        if np.linalg.norm(des_pos - transporter_pos) < 20.0:
            self.screen = 3
            print("YOU WON!")

    def update_crosshair(self, inputs):
        # """
        # Updates the crosshair position based on mouse movement.
        # """
        # mouse_dx, mouse_dy = inputs["mouseDelta"]
        
        # # Normalize mouse movement (-1 to 1 range)
        # norm_x = (mouse_dx / self.width) * 2
        # norm_y = -(mouse_dy / self.height) * 2  # Inverted Y-axis

        # # Limit crosshair movement within a small region in the center
        # max_offset = 1  # Crosshair movement range
        # crosshair_pos = np.array([
        #     np.clip(norm_x * max_offset, -max_offset, max_offset),
        #     np.clip(norm_y * max_offset, -max_offset, max_offset),
        #     -1
        # ], dtype=np.float32)

        # # Update crosshair position
        # self.gameState["crosshair"].properties["position"] = crosshair_pos

        pass

    def shoot_laser(self):
        transporter = self.gameState["transporter"]

        # Transporter's world position (shooting origin)
        laser_origin = np.copy(transporter.properties["position"])

        # Apply slight upward offset
        laser_origin[2] += 12 

        # Get camera forward, right, and up vectors
        forward = self.camera.lookAt - self.camera.position
        forward /= np.linalg.norm(forward)  

        right = np.cross(forward, self.camera.up)  # Rightward direction
        up = np.cross(right, forward)  # Upward direction

        crosshair_offset = self.gameState["crosshair"].properties["position"]

        # Compute world-space direction using crosshair offsets
        crosshair_world_dir = (
            forward + crosshair_offset[0] * right + crosshair_offset[1] * up
        )
        crosshair_world_dir /= np.linalg.norm(crosshair_world_dir)  # Normalize

        # Laser starts from transporter and moves in crosshair direction
        laser_position = laser_origin + (crosshair_world_dir * 10)

        # Laser velocity
        laser_speed = 75  
        laser_velocity = crosshair_world_dir * laser_speed

        # Create laser object
        laser_vertices, laser_indices = create_laser()
        laser = Object("laser", self.shaders['standard'], {
            'vertices': laser_vertices,
            'indices': laser_indices,
            'position': laser_position,
            'rotation': np.array([0, 0, 0], dtype=np.float32),
            'velocity': laser_velocity,
            'scale': np.array([0.4, 0.4, 0.4], dtype=np.float32),  # Adjust for visibility
            'colour': np.array([1, 0, 0, 1], dtype=np.float32)                             
        })

        # Add laser to game state
        self.gameState["lasers"].append(laser)

    def handle_mouse_input(self, inputs):
        if self.gameState["transporter"].properties["view"] == 2:  # First-person mode
            if inputs["mouseDelta"] != (0, 0):  # Only update if mouse moved
                self.update_camera_rotation(inputs)
                self.update_camera_position()
            
                # Reset mouse position to prevent continuous movement
                inputs["mouseDelta"] = (0, 0)

        if inputs["L_CLICK"]:
            self.shoot_laser()

    def update_camera_rotation(self, inputs):
        sensitivity = 0.00001  # Adjust sensitivity
        mouse_dx, mouse_dy = inputs["mouseDelta"]

        if mouse_dx != 0 or mouse_dy != 0:  # Update only if the mouse moved
            self.cameraYaw -= mouse_dx * sensitivity
            self.cameraPitch -= mouse_dy * sensitivity  

            # Limit pitch to prevent flipping
            max_pitch = np.radians(89)
            self.cameraPitch = np.clip(self.cameraPitch, -max_pitch, max_pitch)

    def update_camera_position(self):
        transporter = self.gameState["transporter"]
        transporter_pos = transporter.properties["position"]

        # Compute new forward direction from yaw and pitch
        forward = np.array([
            np.cos(self.cameraYaw) * np.cos(self.cameraPitch),
            np.sin(self.cameraYaw) * np.cos(self.cameraPitch),
            np.sin(self.cameraPitch)
        ], dtype=np.float32)

        forward /= np.linalg.norm(forward)  # Normalize

        # Set camera position just above the transporter
        camera_offset = np.array([0, -5, 15], dtype=np.float32)  
        camera_pos = transporter_pos + camera_offset

        # Set camera look direction
        self.camera.position = camera_pos
        self.camera.lookAt = camera_pos + forward
        self.camera.up = np.array([0, 0, 1], dtype=np.float32)  # Global up

    def update_laser(self, time):
        if "lasers" in self.gameState:
            lasers_to_remove = []
            pirates_to_remove = []

            for laser in self.gameState["lasers"]:
                # Move laser
                laser.properties["position"] += laser.properties["velocity"] * time["deltaTime"]

                # Check collision with pirates
                for pirate in self.gameState["pirates"]:
                    pirate_pos = pirate.properties["position"]
                    laser_pos = laser.properties["position"]

                    if np.linalg.norm(laser_pos - pirate_pos) < 5.0:  # Collision threshold
                        print(f"Pirate destroyed at {pirate_pos}!")
                        pirates_to_remove.append(pirate)
                        lasers_to_remove.append(laser)

            # Remove hit lasers and pirates
            self.gameState["lasers"] = [l for l in self.gameState["lasers"] if l not in lasers_to_remove]
            self.gameState["pirates"] = [p for p in self.gameState["pirates"] if p not in pirates_to_remove]

    def update_minimap_arrow(self):

        z_fix_matrix = np.array([
            [0, 1, 0],  # Rotates by 90° counterclockwise
            [-1,  0, 0],
            [0,  0, 1]
        ])

        transporter = self.gameState["transporter"]
        
        transporter_pos = transporter.properties["position"]
        destination_pos = self.des_planet.properties["position"]

        # Compute direction vector from transporter to destination
        to_destination = destination_pos - transporter_pos
        to_destination /= np.linalg.norm(to_destination)  

        yaw, pitch, roll = transporter.properties["rotation"]

        # Compute transporter's forward direction using rotation matrix
        rotation_matrix = z_fix_matrix @ self.get_rotation_matrix(yaw, pitch, roll)
        forward = rotation_matrix @ np.array([0, 1, 0], dtype=np.float32)  

        dot_product = np.clip(np.dot(forward[:2], to_destination[:2]), -1.0, 1.0)  
        angle = np.arccos(dot_product)  

        # Determine if transporter is facing towards or away from destination
        cross_product = np.cross(forward[:2], to_destination[:2])
        if cross_product < 0:
            angle = -angle  

        # Update the arrow rotation (Z-axis rotation)
        self.gameState["arrow"].properties["rotation"] = np.array([0, 0, angle])

        # Determine elevation difference
        z_diff = destination_pos[2] - transporter_pos[2]

        # Set arrow color based on elevation difference
        if z_diff > 5:  # Need to go higher
            self.gameState["arrow"].properties["colour"] = np.array([1.0, 0.0, 0.0, 1.0])  # Red
        elif z_diff < -5:  # Need to go lower
            self.gameState["arrow"].properties["colour"] = np.array([0.0, 0.0, 1.0, 1.0])  # Blue
        else:  # Correct elevation
            self.gameState["arrow"].properties["colour"] = np.array([1.0, 1.0, 1.0, 1.0])  # White

