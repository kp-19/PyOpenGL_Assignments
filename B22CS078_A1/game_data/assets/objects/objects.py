import numpy as np

## BASIC SHAPE CONSTRUCTS:

def CreateRectangle(center, width, height, colour, offset=0):
    vertices = [
        center[0] - width / 2, center[1] - height / 2, center[2], colour[0], colour[1], colour[2],  
        center[0] + width / 2, center[1] - height / 2, center[2], colour[0], colour[1], colour[2],  
        center[0] + width / 2, center[1] + height / 2, center[2], colour[0], colour[1], colour[2],  
        center[0] - width / 2, center[1] + height / 2, center[2], colour[0], colour[1], colour[2],  
    ]

    indices = [
        0 + offset, 1 + offset, 2 + offset,  
        0 + offset, 2 + offset, 3 + offset   
    ]

    return vertices, indices

def CreateCircle(center, radius, colour, points = 10, offset = 0, semi = False):
    vertices = [center[0], center[1], center[2], colour[0], colour[1], colour[2]]
    indices = []

    if semi == True:
        for i in range(points+1):
            vertices += [
                center[0] + radius * np.cos(float(i * np.pi)/points),
                center[1] + radius * np.sin(float(i * np.pi)/points),
                center[2],
                colour[0],
                colour[1],
                colour[2],
                ]
            
            ind1 = i+1
            ind2 = i+2 if i != points else 1
            indices += [0 + offset, ind1 + offset, ind2 + offset]
    else:
        for i in range(points):
            vertices += [
                center[0] + radius * np.cos(float(i * 2* np.pi)/points),
                center[1] + radius * np.sin(float(i * 2* np.pi)/points),
                center[2],
                colour[0],
                colour[1],
                colour[2],
                ]
            
            ind1 = i+1
            ind2 = i+2 if i != points-1 else 1
            indices += [0 + offset, ind1 + offset, ind2 + offset]

    return (vertices, indices)    

## FUNCTIONS TO CREATE OBJECTS:

def CreatePlayer():

    vertices, indices = CreateCircle([0.0, 0.0, 0.0], 1.0, [220/255, 183/255, 139/255], 50, 0)

    mustache_verts = [
        0, -0.8, 0.05, 0,0,0,
        -0.3, -0.8, 0.05, 0,0,0,
        -0.3, -1, 0.05, 0,0,0,
        0, -0.8, 0.05, 0,0,0,
        0.3, -0.8, 0.05, 0,0,0,
        0.3, -1, 0.05, 0,0,0,
    ]

    mustache_inds = [
        0+(len(vertices)/6),1+(len(vertices)/6),2+(len(vertices)/6),
        3+(len(vertices)/6),4+(len(vertices)/6),5+(len(vertices)/6)
    ]
    vertices += mustache_verts
    indices += mustache_inds

    eye_verts1, eye_inds1 = CreateCircle([0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts1
    indices += eye_inds1

    eye_verts2, eye_inds2 = CreateCircle([-0.4, -0.5, 0.05], 0.3, [1,1,1], 20, len(vertices)/6)
    vertices += eye_verts2
    indices += eye_inds2

    eye_verts3, eye_inds3 = CreateCircle([-0.4, -0.5, 0.10], 0.12, [0,0,0], 10, len(vertices)/6)
    vertices += eye_verts3
    indices += eye_inds3

    eye_verts4, eye_inds4 = CreateCircle([0.4, -0.5, 0.10], 0.12, [0,0,0], 10, len(vertices)/6)
    vertices += eye_verts4
    indices += eye_inds4

    eye_verts5, eye_inds5 = CreateCircle([0.0, 0.0, 0.2], 1.0, [0.871, 0.09, 0.341], 25, len(vertices)/6, True)
    vertices += eye_verts5
    indices += eye_inds5

    eye_verts6, eye_inds6 = CreateCircle([0.0, 0.95, 0.3], 0.3, [0.961, 0.949, 0.357], 20, len(vertices)/6)
    vertices += eye_verts6
    indices += eye_inds6

    return vertices, indices

def CreateKey():
    keyColor = [0.8, 0.796, 0.859]

    vertices = []
    indices = []

    rect1_Vertices, rect1_Indices = CreateRectangle([2,6,0],4,12,keyColor)
    vertices += rect1_Vertices
    indices += rect1_Indices

    rect2_Vertices, rect2_Indices = CreateRectangle([5,8,0],2,2,keyColor,len(vertices)/6)
    vertices += rect2_Vertices
    indices += rect2_Indices

    rect3_Vertices, rect3_Indices = CreateRectangle([5,11,0],2,2,keyColor,len(vertices)/6)
    vertices += rect3_Vertices
    indices += rect3_Indices

    circle_Vertices, circle_Indices = CreateCircle([2,3,0],4,keyColor,10,len(vertices)/6)
    vertices += circle_Vertices
    indices += circle_Indices

    return vertices, indices

def CreateStatBar():
    statBarColor = [0.275, 0.263, 0.451]

    vertices = [
        -500.0, 500, 0, statBarColor[0], statBarColor[1], statBarColor[2],
        500.0, 500, 0, statBarColor[0], statBarColor[1], statBarColor[2],
        -500.0, 400, 0, statBarColor[0], statBarColor[1], statBarColor[2],
        500.0, 400, 0, statBarColor[0], statBarColor[1], statBarColor[2]
    ]

    indices = [
        0,1,2, 1,2,3
    ]

    return vertices, indices

def CreateExitPortal():
    shineColor = [0.122, 0.78, 0.949]
    innerColor = [0.122, 0.482, 0.949]
    outerColor = [0.318, 0.122, 0.949]

    vertices = []
    indices = []

    innerVertices, innerIndices = CreateCircle([0,0,-0.1],40,innerColor,30)
    vertices += innerVertices
    indices += innerIndices

    outerVertices, outerIndices = CreateCircle([0,0,-0.2],50,outerColor,30, len(vertices)/6)
    vertices += outerVertices
    indices += outerIndices

    shineVertices, shineIndices = CreateCircle([0,0,-0.09],30,shineColor,20, len(vertices)/6)
    vertices += shineVertices
    indices += shineIndices

    return vertices, indices

def CreatePotion():
    potionColor = [0.373, 0.91, 0.176]

    vertices = []
    indices = []

    rect1_Vertices, rect1_Indices = CreateRectangle([0,0,0],5,12,potionColor)
    vertices += rect1_Vertices
    indices += rect1_Indices

    circle_Vertices, circle_Indices = CreateCircle([0,-2,0],5,potionColor,10,len(vertices)/6)
    vertices += circle_Vertices
    indices += circle_Indices

    return vertices, indices

# Level-1 Object functions:
def Createbgl1():
    grassColour = [0.153, 0.6, 0.086]
    waterColour = [0.125, 0.584, 0.761]

    vertices = [
        -500.0, 500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        -400.0, 500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        -400.0, -500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        -500.0, -500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],

        500.0, 500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        400.0, 500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        400.0, -500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],
        500.0, -500.0, -0.9, grassColour[0], grassColour[1], grassColour[2],

        -400.0, 500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        400.0, 500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        400.0, -500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
        -400.0, -500.0, -0.9, waterColour[0], waterColour[1], waterColour[2],
    ]

    indices = [
        0,1,2, 0,3,2,
        8,9,10, 8,11,10,
        4,5,6, 4,7,6
    ]

    return vertices, indices

def CreateEnemyl1():
    bodyColor = [0.051, 0.51, 0.22]
    teethColor = [1,1,1]
    eyeColor = [0,0,0]

    vertices = [
        # Body coordinates:
        0, 0, 0, bodyColor[0], bodyColor[1], bodyColor[2],
        70, 0, 0, bodyColor[0], bodyColor[1], bodyColor[2],
        5, 10, 0, bodyColor[0], bodyColor[1], bodyColor[2],
        25, 10, 0, bodyColor[0], bodyColor[1], bodyColor[2],
        25, 35, 0, bodyColor[0], bodyColor[1], bodyColor[2],

        # Teeth coordinates:
        10, 10, 0, teethColor[0], teethColor[1], teethColor[2],
        14, 10, 0, teethColor[0], teethColor[1], teethColor[2],
        18, 10, 0, teethColor[0], teethColor[1], teethColor[2],
        12, 6, 0, teethColor[0], teethColor[1], teethColor[2],
        16, 6, 0, teethColor[0], teethColor[1], teethColor[2]
    ]

    indices = [
        0,3,1 ,3,4,1,
        3,4,2, 5,6,8,
        6,7,9
    ]

    # Eye coordinates:
    eye_Vertices, eye_Indices = CreateCircle([25,25,0],3,eyeColor,10,len(vertices)/6)
    vertices += eye_Vertices
    indices += eye_Indices

    return vertices, indices

# Level-2 Object functions:
def Createbgl2(): 
    portalColour = [0.125, 0.243, 0.451]
    lavabgColor = [0.51, 0.02, 0]
    baseColor = [0.329, 0.239, 0, 0.941]

    vertices = [
        # Portals First (To Ensure They Draw on Top)
        -500.0, -400.0, -0.7, portalColour[0], portalColour[1], portalColour[2],
        -350.0, -400.0, -0.7, portalColour[0], portalColour[1], portalColour[2],
        -350.0, -250.0, -0.7, portalColour[0], portalColour[1], portalColour[2],
        -500.0, -250.0, -0.7, portalColour[0], portalColour[1], portalColour[2],

        500.0,  250.0, -0.7, portalColour[0], portalColour[1], portalColour[2],
        500.0,  400.0, -0.7, portalColour[0], portalColour[1], portalColour[2],
        350.0,  400.0, -0.7, portalColour[0], portalColour[1], portalColour[2],
        350.0,  250.0, -0.7, portalColour[0], portalColour[1], portalColour[2],

        # Safe Base:
        500.0,  -400.0, -0.8, baseColor[0], baseColor[1], baseColor[2],
        -500.0,  -400.0, -0.8, baseColor[0], baseColor[1], baseColor[2],
        -500.0,  -300.0, -0.8, baseColor[0], baseColor[1], baseColor[2],
        500.0,  -300.0, -0.8, baseColor[0], baseColor[1], baseColor[2],

        # Lava Background Last
        -500.0,  500.0, -0.85, lavabgColor[0], lavabgColor[1], lavabgColor[2],
        500.0,  500.0, -0.85, lavabgColor[0], lavabgColor[1], lavabgColor[2],
        500.0, -400.0, -0.85, lavabgColor[0], lavabgColor[1], lavabgColor[2],
        -500.0, -400.0, -0.85, lavabgColor[0], lavabgColor[1], lavabgColor[2],
    ]

    indices = [
        0,1,2, 0,3,2,
        8,9,10, 8,11,10,
        4,5,6, 4,7,6,
        12,13,14, 12,15,14
    ]

    return vertices, indices

def CreateEnemyl2():
    enemyl2Color = [0,0,0]

    vertices = [
        -20.0, 0.0, -0.09, enemyl2Color[0], enemyl2Color[1], enemyl2Color[2],
        20.0, 0.0, -0.09, enemyl2Color[0], enemyl2Color[1], enemyl2Color[2],
        0.0, -60.0, -0.09, enemyl2Color[0], enemyl2Color[1], enemyl2Color[2]
    ]
    indices = [0,1,2]

    return vertices, indices

# Level-3 Object functions:
def Createbgl3(): 
    spaceColor = [0,0,0]

    vertices = [
        # Space Background 
        -500.0,  500.0, -0.85, spaceColor[0], spaceColor[1], spaceColor[2],
        500.0,  500.0, -0.85, spaceColor[0], spaceColor[1], spaceColor[2],
        500.0, -500.0, -0.85, spaceColor[0], spaceColor[1], spaceColor[2],
        -500.0, -500.0, -0.85, spaceColor[0], spaceColor[1], spaceColor[2],
    ]

    indices = [
        0,1,2, 0,3,2,
    ]

    lb1_vertices, lb1_indices = CreateCircle([-100, -200, -0.85],5,[1,1,1],15,len(vertices)/6)
    vertices += lb1_vertices
    indices += lb1_indices

    lb2_vertices, lb2_indices = CreateCircle([-400, -110, -0.85],5,[1,1,1],15,len(vertices)/6)
    vertices += lb2_vertices
    indices += lb2_indices

    lb3_vertices, lb3_indices = CreateCircle([-320, 200, -0.85],5,[1,1,1],15,len(vertices)/6)
    vertices += lb3_vertices
    indices += lb3_indices

    lb4_vertices, lb4_indices = CreateCircle([100, 200, -0.85],5,[1,1,1],15,len(vertices)/6)
    vertices += lb4_vertices
    indices += lb4_indices

    lb5_vertices, lb5_indices = CreateCircle([0, -102, -0.85],5,[1,1,1],15,len(vertices)/6)
    vertices += lb5_vertices
    indices += lb5_indices

    lb6_vertices, lb6_indices = CreateCircle([300, 200, -0.85],5,[1,1,1],15,len(vertices)/6)
    vertices += lb6_vertices
    indices += lb6_indices

    lb6_vertices, lb6_indices = CreateCircle([300, 200, -0.85],5,[1,1,1],15,len(vertices)/6)
    vertices += lb6_vertices
    indices += lb6_indices

    lb7_vertices, lb7_indices = CreateCircle([400, -280, -0.85],5,[1,1,1],15,len(vertices)/6)
    vertices += lb7_vertices
    indices += lb7_indices

    return vertices, indices

def CreatePlatforml3():
    innerColor = [0.557, 0.757, 0.761]
    outerColor = [0.525, 0.514, 0.62]
    shineColor = [1,1,1]

    vertices = []
    indices = []

    innerVertices, innerIndices = CreateCircle([0,0,-0.1],40,innerColor,30)
    vertices += innerVertices
    indices += innerIndices

    outerVertices, outerIndices = CreateCircle([0,0,-0.2],75,outerColor,30, len(vertices)/6)
    vertices += outerVertices
    indices += outerIndices

    shineVertices, shineIndices = CreateCircle([20,20,-0.09],5,shineColor,20, len(vertices)/6)
    vertices += shineVertices
    indices += shineIndices

    return vertices, indices

def CreateEnemyl3():
    meteorColor = [0.878, 0.325, 0.02]

    vertices = [
        -30.0, 0.0, -0.09, meteorColor[0],meteorColor[1],meteorColor[2],
        30.0, 0.0, -0.09, meteorColor[0], meteorColor[1], meteorColor[2],
        0.0, -60.0, -0.09, meteorColor[0], meteorColor[1], meteorColor[2]
    ]
    indices = [0,1,2]

    head_vertices, head_indices = CreateCircle([0,0,-0.09],30,meteorColor,25,3)
    vertices += head_vertices
    indices += head_indices

    return vertices, indices
    

# OBJECTS:
# Common Objects:
playerVerts, playerInds = CreatePlayer()
playerProps = {
    'vertices' : np.array(playerVerts, dtype = np.float32),
    
    'indices' : np.array(playerInds, dtype = np.uint32),

    'position' : np.array([-450, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([30, 30, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32),

    'dash_active' : True,
    
    'dash_cooldown_timer' : 8
}

keyVerts, keyInds = CreateKey()
keyProps = {
    'vertices' : np.array(keyVerts, dtype = np.float32),
    
    'indices' : np.array(keyInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 3.14,

    'scale' : np.array([5, 5, 1], dtype = np.float32),

    'sens' : 1,

    'velocity' : np.array([0, 0, 0], dtype = np.float32),

    'type' : "key"
}

statBarVerts, statBarInds = CreateStatBar()
statBarProps = {
    'vertices' : np.array(statBarVerts, dtype = np.float32),
    
    'indices' : np.array(statBarInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([1, 1, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32)
}

exitPortalVerts, exitPortalInds = CreateExitPortal()
exitPortalProps = {
    'vertices' : np.array(exitPortalVerts, dtype = np.float32),
    
    'indices' : np.array(exitPortalInds, dtype = np.uint32),

    'position' : np.array([450, 320, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([1, 1, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32)
}

potionVerts, potionInds = CreatePotion()
potionProps = {
    'vertices' : np.array(potionVerts, dtype = np.float32),
    
    'indices' : np.array(potionInds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0,

    'scale' : np.array([5, 5, 1], dtype = np.float32),

    'sens' : 1,

    'velocity' : np.array([0, 0, 0], dtype = np.float32),

    'type' : "potion"
}

# Level-1 Objects:
bgl1Verts, bgl1Inds = Createbgl1()
bgl1Props = {
    'vertices' : np.array(bgl1Verts, dtype = np.float32),
    
    'indices' : np.array(bgl1Inds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([1, 1, 1], dtype = np.float32),

    'boundary' : [500.0, -500.0, 500.0, 500.0],

    'river_banks': [-400.0, 400.0]
}

platforml1Color = [0.4, 0.0, 0.0]
platforml1Verts, platforml1Inds = CreateCircle([0,0,-0.1], 3.0, platforml1Color, 30)
platforml1Props = {
    'vertices' : np.array(platforml1Verts, dtype = np.float32),
    
    'indices' : np.array(platforml1Inds, dtype = np.uint32),

    'position' : np.array([-460, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([20, 20, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32),

    'type' : "platform"
}

enemyl1Verts, enemyl1Inds = CreateEnemyl1()
enemyl1Props = {
    'vertices' : np.array(enemyl1Verts, dtype = np.float32),
    
    'indices' : np.array(enemyl1Inds, dtype = np.uint32),

    'position' : np.array([0, 0, -0.09], dtype = np.float32),

    'rotation_z' : 1.57,

    'scale' : np.array([2, 2, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32)
}

# Level-2 Objects:
bgl2Verts, bgl2Inds = Createbgl2()
bgl2Props = {
    'vertices' : np.array(bgl2Verts, dtype = np.float32),
    
    'indices' : np.array(bgl2Inds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([1, 1, 1], dtype = np.float32),

    'boundary' : [500.0, -500.0, 500.0, 500.0],

    'river_banks': [-400.0, 400.0]
}

platforml2Color = [0.251, 0.098, 0.098]
platforml2Verts, platforml2Inds = CreateRectangle([0,0,-0.1],150,70,platforml2Color)
platforml2Props = {
    'vertices' : np.array(platforml2Verts, dtype = np.float32),
    
    'indices' : np.array(platforml2Inds, dtype = np.uint32),

    'position' : np.array([0, -265, -0.1], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([1, 1, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32),

    'type' : "platform"
}

enemyl2Verts, enemyl2Inds = CreateEnemyl2()
enemyl2Props = {
    'vertices' : np.array(enemyl2Verts, dtype = np.float32),
    
    'indices' : np.array(enemyl2Inds, dtype = np.uint32),

    'position' : np.array([0, 0, -0.09], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([2, 2, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32)
}

# Level-3 Objects:
bgl3Verts, bgl3Inds = Createbgl3()
bgl3Props = {
    'vertices' : np.array(bgl3Verts, dtype = np.float32),
    
    'indices' : np.array(bgl3Inds, dtype = np.uint32),

    'position' : np.array([0, 0, -1], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([1, 1, 1], dtype = np.float32),

    'boundary' : [500.0, -500.0, 500.0, 500.0],

    'river_banks': [-400.0, 400.0]
}

bgl3_portal1Verts, bgl3_portal1Inds = CreateCircle([-500,-400,-0.9], 200, [1,1,1], 25)
bgl3_portal1Props = {
    'vertices' : np.array(bgl3_portal1Verts, dtype = np.float32),
    
    'indices' : np.array(bgl3_portal1Inds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([1, 1, 1], dtype = np.float32),

    'boundary' : [500.0, -500.0, 500.0, 500.0],

    'river_banks': [-400.0, 400.0]
}

bgl3_portal2Verts, bgl3_portal2Inds = CreateCircle([500,400,-0.9], 200, [1,1,1], 25)
bgl3_portal2Props = {
    'vertices' : np.array(bgl3_portal2Verts, dtype = np.float32),
    
    'indices' : np.array(bgl3_portal2Inds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([1, 1, 1], dtype = np.float32),

    'boundary' : [500.0, -500.0, 500.0, 500.0],

    'river_banks': [-400.0, 400.0]
}

platforml3Verts, platforml3Inds = CreatePlatforml3()
platforml3Props = {
    'vertices' : np.array(platforml3Verts, dtype = np.float32),
    
    'indices' : np.array(platforml3Inds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 0.0,

    'scale' : np.array([1, 1, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32),

    'type' : "platform"
}

enemyl3Verts, enemyl3Inds = CreateEnemyl3()
enemyl3Props = {
    'vertices' : np.array(enemyl3Verts, dtype = np.float32),
    
    'indices' : np.array(enemyl3Inds, dtype = np.uint32),

    'position' : np.array([0, 0, 0], dtype = np.float32),

    'rotation_z' : 3.14,

    'scale' : np.array([1.3, 1.3, 1], dtype = np.float32),

    'sens' : 125,

    'velocity' : np.array([0, 0, 0], dtype = np.float32)
}

