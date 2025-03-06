import numpy as np
import os

###############################################################
# Write logic to load OBJ Files:
    # Will depend on type of object. For example if normals needed along with vertex positions 
    # then will need to load slightly differently.

# Can use the provided OBJ files from assignment_2_template/assets/objects/models/
# Can also download other assets or model yourself in modelling softwares like blender

###############################################################
# Create Transporter, Pirates, Stars(optional), Minimap arrow, crosshair, planet, spacestation, laser

def load_obj_file(file_path):
    vertices = []
    normals = []
    indices = []
    
    vertex_dict = {}
    vertex_count = 0
    
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('v '):  
                v = list(map(float, line.strip().split()[1:]))
                vertices.append(v)
            elif line.startswith('vn '):  
                vn = list(map(float, line.strip().split()[1:]))
                normals.append(vn)
            elif line.startswith('f '):  
                face = line.strip().split()[1:]
                triangle = []
                for vertex in face:
                    parts = vertex.split('/')
                    v_idx = int(parts[0]) - 1  

                    # Check if normal index exists
                    vn_idx = int(parts[-1]) - 1 if len(parts) > 2 and parts[-1].isdigit() else None

                    key = (v_idx, vn_idx)
                    if key not in vertex_dict:
                        vertex_dict[key] = vertex_count
                        vertex_count += 1
                    
                    triangle.append(vertex_dict[key])

                indices.extend(triangle[:3])
                if len(triangle) == 4:
                    indices.extend([triangle[0], triangle[2], triangle[3]])

    final_vertices = []
    for (v_idx, vn_idx), _ in vertex_dict.items():
        final_vertices.extend(vertices[v_idx])  # Add vertex position
        if vn_idx is not None and vn_idx < len(normals):  
            final_vertices.extend(normals[vn_idx])  # Add normal
        else:
            final_vertices.extend([0.0, 0.0, 1.0])  # Default normal (pointing up)
    return np.array(final_vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)


def create_transporter():
    model_path = os.path.join("assets", "objects", "models", "transporter.obj")
    return load_obj_file(model_path)

def create_pirate():
    model_path = os.path.join("assets", "objects", "models", "pirate.obj")
    return load_obj_file(model_path)

def create_planet():
    model_path = os.path.join("assets", "objects", "models", "planet.obj")
    return load_obj_file(model_path)

def create_space_station():
    model_path = os.path.join("assets", "objects", "models", "spacestation.obj")
    return load_obj_file(model_path)

def create_laser():
    model_path = os.path.join("assets", "objects", "models", "laser.obj")
    return load_obj_file(model_path)

def create_arrow():
    vertices = np.array([
        0.0,  0.5, 0.0,  0.0, 0.0, 1.0,  
       -0.5, -0.5, 0.0,  0.0, 0.0, 1.0,  
        0.5, -0.5, 0.0,  0.0, 0.0, 1.0,  
        -0.2, 0.0, 0.0, 0.0, 0.0, 1.0,
        0.2, 0.0, 0.0, 0.0, 0.0, 1.0,
        -0.2, -2.0, 0.0, 0.0, 0.0, 1.0,
        0.2, -2.0, 0.0, 0.0, 0.0, 1.0,
    ], dtype=np.float32)

    indices = np.array([ 0, 1, 2,
                3, 4, 5,
                4, 5, 6
    ], dtype=np.uint32)
    
    return vertices, indices

def create_crosshair():
    size = 0.01
    vertices = np.array([
        # Vertical line
        -size, -size*5, 0.0,  0.0, 0.0, 1.0,
         size, -size*5, 0.0,  0.0, 0.0, 1.0,
         size,  size*5, 0.0,  0.0, 0.0, 1.0,
        -size,  size*5, 0.0,  0.0, 0.0, 1.0,
        # Horizontal line
        -size*4, -size, 0.0,  0.0, 0.0, 1.0,
         size*4, -size, 0.0,  0.0, 0.0, 1.0,
         size*4,  size, 0.0,  0.0, 0.0, 1.0,
        -size*4,  size, 0.0,  0.0, 0.0, 1.0,
    ], dtype=np.float32)
    
    indices = np.array([
        0, 1, 2, 2, 3, 0,  # Vertical
        4, 5, 6, 6, 7, 4   # Horizontal
    ], dtype=np.uint32)
    
    return vertices, indices 
 

###############################################################