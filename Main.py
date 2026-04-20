## This code is our final uploaded interation of our Robocon
## I hope it helps any other teams

## ------ Initialisation ------

import time
import robot
import math

R = robot.Robot(max_motor_voltage=12)

R.servos[0].mode = robot.PWM_SERVO
R.servos[1].mode = robot.PWM_SERVO
R.servos[2].mode = robot.PWM_SERVO
R.servos[3].mode = robot.PWM_SERVO

if R.zone == robot.TEAM.RED:
    colour = "R"
elif R.zone == robot.TEAM.YELLOW:
    colour = "Y"
elif R.zone == robot.TEAM.GREEN:
    colour = "G"
elif R.zone == robot.TEAM.BLUE:
    colour = "B"
else:
    print("Colour isn't set, defaulting to red. \n")
    colour = "R"
    

## ------ Marker Map ------

marker_map = {
    # North Wall (Top)
    100: ("Top", 0.5, 6.0), 101: ("Top", 1.5, 6.0), 102: ("Top", 2.5, 6.0),
    103: ("Top", 3.5, 6.0), 104: ("Top", 4.5, 6.0), 105: ("Top", 5.5, 6.0),
    # East Wall (Right)
    106: ("Right", 6.0, 5.5), 107: ("Right", 6.0, 4.5), 108: ("Right", 6.0, 3.5),
    109: ("Right", 6.0, 2.5), 110: ("Right", 6.0, 1.5), 111: ("Right", 6.0, 0.5),
    # South Wall (Bottom)
    112: ("Bottom", 5.5, 0.0), 113: ("Bottom", 4.5, 0.0), 114: ("Bottom", 3.5, 0.0),
    115: ("Bottom", 2.5, 0.0), 116: ("Bottom", 1.5, 0.0), 117: ("Bottom", 0.5, 0.0),
    # West Wall (Left)
    118: ("Left", 0.0, 0.5), 119: ("Left", 0.0, 1.5), 120: ("Left", 0.0, 2.5),
    121: ("Left", 0.0, 3.5), 122: ("Left", 0.0, 4.5), 123: ("Left", 0.0, 5.5)
}

wall_facing = {"Top": 270, "Bottom": 90, "Right": 180, "Left": 0}

# Below are IDs for wall markers for our journey home

red1Home = 103
red2Home = 123

blue1Home = 121
blue2Home = 117

green1Home = 115
green2Home = 111

yellow1Home = 109
yellow2Home = 105

current_pos2 = 38
current_pos3 = -38
   
## ------ Constants ------

MoveCalibration = 1.09 # m/s
smallTurnCalibration = 135 # degrees/s
sMoveCalibration = 0.62
largeTurnCalibration = 140 # degrees/s

MoveSpeed = 50
sMoveSpeed = 30
smallTurnSpeed = 30
largeTurnSpeed = 25

baseDistance = 0.34
certaintyDistance = 0.35 # Distance for insuring ingestion
certaintyDistance2 = 0.4

grabCalibration = 0.55

noFoundAngle = -45
noFoundTime = 0.8

## ------ Variables ------

clawOpened = False

## ------ Movement Functions ------

def w(t):
  time.sleep(abs(t))

def move(dist): 
    if dist / abs(dist) == -1: # Checks if it is a reverse movement
        sleepTime = abs(dist) / MoveCalibration # Calculation to find out time to keep motors on for speed
        R.motors[0] = -MoveSpeed
        R.motors[1] = MoveSpeed
        time.sleep(sleepTime)
        R.motors[0] = 0
        R.motors[1] = 0
        print("Movement | Moved ", dist, " meters")
    else:
        sleepTime = abs(dist) / MoveCalibration # Calculation to find out time to keep motors on for speed
        R.motors[0] = MoveSpeed
        R.motors[1] = -MoveSpeed
        time.sleep(sleepTime)
        R.motors[0] = 0
        R.motors[1] = 0
        print("Movement | Moved ", dist, " meters")

def sMove(dist):
    if dist / abs(dist) == -1: # Checks if it is a reverse movement
        sleepTime = abs(dist) / sMoveCalibration # Calculation to find out time to keep motors on for speed
        R.motors[0] = -sMoveSpeed
        R.motors[1] = sMoveSpeed
        time.sleep(sleepTime)
        R.motors[0] = 0
        R.motors[1] = 0
        print("Movement | Moved ", dist, " meters")
    else:
        sleepTime = abs(dist) / sMoveCalibration # Calculation to find out time to keep motors on for speed
        R.motors[0] = sMoveSpeed
        R.motors[1] = -sMoveSpeed
        time.sleep(sleepTime)
        R.motors[0] = 0
        R.motors[1] = 0
        print("Movement | Moved ", dist, " meters")

def turn(degrees): # Turning in degrees (left is negative, right is positive)
    if abs(degrees) < 0.5:  # Skip micro-turns to avoid division by zero error
        return
    if abs(degrees) <= 45: # Checks if turn is small for better movement
        print("Movement | Small Turn")
        if degrees / abs(degrees) == -1: # Checks direction of turn
            print("Movement | Turning Left", degrees)
                # to be calibrated
            sleepTime = abs(degrees) / smallTurnCalibration # Calculation for finding time to sleep while turning
            R.motors[0] = smallTurnSpeed
            R.motors[1] = smallTurnSpeed
            time.sleep(sleepTime)
            R.motors[0] = 0
            R.motors[1] = -0
        else:
            print("Movement | Turning Right", degrees)
            sleepTime = degrees / smallTurnCalibration  # Calculation for finding time to sleep while turning
            R.motors[0] = -smallTurnSpeed
            R.motors[1] = -smallTurnSpeed
            time.sleep(sleepTime)
            R.motors[0] = 0
            R.motors[1] = -0
    else:
        print("Movement | Large Turn")
        if degrees / abs(degrees) == -1: # Checks direction of turn
            print("Movement | Turning Left", degrees)
            sleepTime = abs(degrees) / largeTurnCalibration # Calculation for finding time to sleep while turning
            R.motors[0] = largeTurnSpeed
            R.motors[1] = largeTurnSpeed
            time.sleep(sleepTime)
            R.motors[0] = 0
            R.motors[1] = -0
        else:
            print("Movement | Turning Right", degrees)
            sleepTime = degrees / largeTurnCalibration # Calculation for finding time to sleep while turning
            R.motors[0] = -largeTurnSpeed
            R.motors[1] = -largeTurnSpeed
            time.sleep(sleepTime)
            R.motors[0] = 0
            R.motors[1] = -0

def level(level): ## Sets an arm to a level with a slow time
    print("Arm | Moving Level ", level, "\n")
    global current_pos2, current_pos3
    levels = {
        1:(38, -38),
        1.5:(0, -5),
        2:(-70,75),
        3:(-135, 140)
    }
    target2, target3 = levels[level]
    steps =  100
    delay = 0.005
    for i in range(1, steps + 1):
        fraction = i/steps
        R.servos[2] = current_pos2 + (target2 - current_pos2) * fraction
        R.servos[3] = current_pos3 + (target3 - current_pos3) * fraction
        time.sleep(delay)
    current_pos2, current_pos3 = target2, target3
    print("Arm | Set Level ", level)

def flevel(level):
    levels = {
        1:(38, -38),
        1.5:(0, -5),
        2:(-70,75),
        3:(-135, 140)
    }

    target2, target3 = levels[level]

    R.servos[2] = target2
    R.servos[3] = target3


def openClaw(): # opens the servo to an open claw posotion
    current_pos = 135
    steps = 50
    delay = 0.01
    target = 70
    for i in range (1, steps + 1):
        fraction = i/steps
        R.servos[0] = current_pos + (target - current_pos) * fraction
        w(delay)
    R.servos[0] = 70

def closeClaw():
    current_pos = 70
    steps = 50
    delay = 0.01
    target = 135
    for i in range (1, steps + 1):
        fraction = i/steps
        R.servos[0] = current_pos + (target - current_pos) * fraction
        w(delay)
    R.servos[0] = 135


## ------ Advanced Functions ------

def deposit(): # This function stacks and places a marker and TURNS clear
    level(3)
    w(1)
    level(2) # Lifts clear to place
    sMove(-(baseDistance))
    w(0.2) # Aligns cube over the top
    openClaw() # Releases cube
    w(0.2)
    move(-(certaintyDistance2))
    w(0.2)
    turn(180) # Ensuring ready


def collectCube(): # Ingestion
    
    foundCube = False
    closestDist = 10
    mostValuable = 0
    valuedSeen = {}

    level(3)

    markers = R.see()

    while foundCube == False:
        w(noFoundTime)
        markers = R.see()
        valuedSeen = []
        
        for marker in markers: # Lists through markers
            if marker.info.id > 31: # Checks if a valid drop or supply
                print("Markers | Arena, Skipping")
                continue
            else:
                if marker.info.id <= 31 and marker.info.id >= 24:
                    valuedSeen.append(marker)
                     ## Else goes for normal list
            for marker in markers:
                if marker.info.id > 31: # Checks if a valid drop or supply
                    print("Markers | Arena, Skipping")
                    continue
                if marker.dist < closestDist:
                    selMarker = marker
                    closestDist = marker.dist
                    foundCube = True
                    break

        if foundCube:
            break    

        
        turn(noFoundAngle)
        w(noFoundTime)
        
            
                    
    turn(selMarker.bearing.y)
    if (selMarker.dist) > 1:
        move(((selMarker.dist)/2))
        w(0.5)
        markers = R.see()
        for marker in markers:
            if marker.info.id == selMarker.info.id:
                turn(marker.bearing.y)
                w(0.5)
                move(((selMarker.dist) + certaintyDistance))
            else:
                continue
    else:
        w(0.5)
        move(((selMarker.dist) + certaintyDistance))
    
    move(0.3)
    w(0.5)
    flevel(2)
    w(0.5)
    flevel(1)
    w(0.5)
    move(-0.5)
    w(0.5)
    flevel(2)
    w(0.5)
    flevel(1)

def graspCube():

    level(1)
    foundCube = False
    closestDist = 10
    mostValuable = 0
    valuedSeen = []
    openClaw()
    level(1)

    markers = R.see()

    while foundCube == False:
        markers = R.see()
        for marker in markers: # Lists through markers
            if marker.info.id > 31: # Checks if a valid drop or supply
                print("Markers | Arena, Skipping")
                continue
            else:
                if marker.info.id <= 31 and marker.info.id >= 24:
                    valuedSeen.append(marker)
                    
       
        ## Else goes for normal list
            for marker in markers:
                if marker.info.id > 31: # Checks if a valid drop or supply
                    print("Markers | Arena, Skipping")
                    continue
                if marker.dist < closestDist:
                    selMarker = marker
                    closestDist = marker.dist
                    foundCube = True
                    break

        if foundCube:
            break  


        turn(noFoundAngle)
        w(noFoundTime)

    print("first turn")
    turn(selMarker.bearing.y)


    print(selMarker.dist)
    if (selMarker.dist) > 1:
        w(0.5)
        move((selMarker.dist)/ 2)
        w(0.5)
        markers = R.see()
        for marker in markers:
            if marker.info.id == selMarker.info.id:
                print("Got to half beat on grasp pickup")
                turn(marker.bearing.y)
                w(0.5)
                move(((marker.dist)))
            else:
                continue
    else:
        w(0.5)
        move(selMarker.dist)



    w(0.5)
    move(0.50)
    w(0.5)
    move(-0.5)
    w(0.5)
    sMove(grabCalibration) ## Moves excatluy onto the grab position 
    closeClaw()
    level(1.5)


def goToMiddle():
    Found = False

    markers = R.see()
    if colour == "R": # Finds the right tree marker for that colour
        while Found == False: # Loops until it is found
            markers = R.see()
            for marker in markers:
                if marker.info.id == 91 or marker.info.id == 88 or marker.info.id == 89 or marker.info.id == 90: # If it sees the tree for 3/4 movement for this speciic colour
                    turn(marker.bearing.y)
                    w(1)
                    move((marker.dist) * 0.75)
                    Found = True
                else:
                    print("Cubes | Couldn't find tree")
                    continue

            if Found == True:
                break
            turn(noFoundAngle)
            w(noFoundTime)

                    
    elif colour == "B": # Finds the right tree marker for that colour
        while Found == False: # Loops until it is found
            markers = R.see()
            for marker in markers:
                if marker.info.id == 86 or marker.info.id == 84 or marker.info.id = 85 or marker.info.id == 87: # If it sees the tree for 3/4 movement for this speciic colour
                    turn(marker.bearing.y)
                    w(1)
                    move((marker.dist)*0.75)
                    Found = True
                else:
                    print("Cubes | Couldn't find tree")
                    continue

            if Found == True:
                break
            turn(noFoundAngle)
            w(noFoundTime)

                    
    elif colour == "G": # Finds the right tree marker for that colour
        while Found == False: # Loops until it is found
            markers = R.see()
            for marker in markers:
                
                if marker.info.id == 81 or marker.info.id == 80 or marker.info.id == 82 or marker.info.id == 83: # If it sees the tree for 3/4 movement for this speciic colour
                    turn(marker.bearing.y)
                    w(1)
                    move((marker.dist)*0.75)
                    Found = True
                else:
                    print("Cubes | Couldn't find tree")
                    continue

            if Found == True:
                break
            turn(noFoundAngle)
            w(noFoundTime)

                    
    elif colour == "Y": # Finds the right tree marker for that colour
        while Found == False: # Loops until it is found
            markers = R.see()
            if not markers:
                print("Marker List Empty")
                Found = False
                next
            for marker in markers:
                if marker.info.id == 76 or marker.info.id == 77 or marker.info.id == 78 or marker.info.id == 79: # If it sees the tree for 3/4 movement for this speciic colour
                    turn(marker.bearing.y)
                    w(1)
                    move((marker.dist)*0.75)
                    Found = True
                else:
                    print("Cubes | Couldn't find tree")
                    continue


            if Found == True:
                break
            turn(noFoundAngle)
            w(noFoundTime)
    turn(-45)

def home():
    Found = False
    Found2 = False

    if colour == "R":
        ID1 = red1Home
        ID2 = red2Home
    if colour == "B":
        ID1 = blue1Home
        ID2 = blue2Home
    if colour == "G":
        ID1 = green1Home
        ID2 = green2Home
    if colour == "Y":
        ID1 = yellow1Home
        ID2 = yellow2Home


    while Found == False: # Loops until it is found
        markers = R.see()
        for marker in markers:
                
            if marker.info.id == ID1: # searches for our part home marker
                turn(marker.bearing.y)
                move((marker.dist)*0.75)
                Found = True
            else:
                print("Cubes | Couldn't find first marker")


        if Found == True:
                break

        turn(noFoundAngle)
        w(noFoundTime)
    while Found2 == False: # Loops until it is found
        markers = R.see()
        for marker in markers:
            if marker.info.id == ID2: # searches for our part home marker
                turn(marker.bearing.y)
                move((marker.dist)*(5/6))
                Found2 = True
            else:
                print("Cubes | Couldn't find second home marker")
                continue
            
        if Found2 == True:
            break

        turn(noFoundAngle)
        w(noFoundTime)


level(3)


# openClaw()
# w(1)
# closeClaw()               


    
# openClaw()
# level(1)

# w(1)

# closeClaw()
# w(0.5)

# w(1)
# openClaw()
# w(0.5)

# w(1)
# level(3)



goToMiddle()
openClaw()
collectCube()
graspCube()
home()
deposit()
