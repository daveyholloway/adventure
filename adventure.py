# **********************************************************************
# Text adventures in python
# =========================
# 
# The main part of this is simply to read what the user has typed
# and try to interpret it.
#
# Modification History
# ====================
#
# When       Who                 Why
# ========== =================== =======================================
# 06/12/2019 Dave Hol'           Initial Release
#
# **********************************************************************

# **********************************************************************
# Libraries to import
#
# **********************************************************************
import csv                       # Handles CSV files
import time                      # Used for delays

# **********************************************************************
# Start of Functions and procedures
#
# **********************************************************************

# **********************************************************************
# A function that asks are you sure and returns True if y or yes is
# entered, anything else will be taken as False.
#
# **********************************************************************
def areYouSure(message = "Are you sure? : "):

    # Prompt the user for input
    userConfirmation = input(message)

    if userConfirmation.lower() in ("yes","y"):
        return True
    else:
        return False

# **********************************************************************
# Text formatting - Underline
#
# **********************************************************************  
def underline(message):
    return message + "\n" + ("=" * len(message))

# **********************************************************************
# A function that returns a list object containing the fields from the
# # map file for the location id passed in as a parameter.
#
# **********************************************************************    
def getLocationRow(locationId, mapFile = r"C:/\Users/\davey/\Documents/\GitHub/\adventure/\map.txt"):

    # An empty array to store the location details if found
    locationDetail = []
    
    # Open the map file
    with open(mapFile, mode='r') as mapData:
        mapReader = csv.reader(mapData, delimiter=',')
        # Loop through each line in the file
        for mapDataRow in mapReader:
            # Look for a matching location id
            if mapDataRow[0] == str(locationId):
                # Found a match so save the details to return to
                # the calling routine 
                locationDetail = mapDataRow

    # Return the location details, if any were found the array will 
    # have 9 elements, otherwise it'll have 0.
    return locationDetail
    

# **********************************************************************
# A procedure that displays the current location details. Pass in the
# array/list that contains all of the info fetched from the file for
# a given location id.
# **********************************************************************    
def showLocation(locationDetail):

    # Print a separator line
    print("=" * 72)

    # Check to see if details were found
    if len(locationDetail) != 0:
        print(underline(locationDetail[7]))
        print(locationDetail[8])
        print(showExits(locationDetail))

    else:
        print("You're completely lost, ask the programmer!")

    # Print a few empty lines
    for x in range(0, 4):
        print()
        time.sleep(.2)
    
# **********************************************************************
# A procedure that displays the exits from the current location.
# **********************************************************************    
def showExits(locationDetail):

    exits = []
    
    if int(locationDetail[1]) != 0:
        exits.append("North")

    if int(locationDetail[2]) != 0:
        exits.append("East")

    if int(locationDetail[3]) != 0:
        exits.append("South")

    if int(locationDetail[4]) != 0:
        exits.append("West")

    if int(locationDetail[5]) != 0:
        exits.append("Up")

    if int(locationDetail[6]) != 0:
        exits.append("Down")
    
    return "You can go " + formatExits(exits)

# **********************************************************************
# Format the exit list into "correct English"
#
# ********************************************************************** 
def formatExits(exitList):

    exits = ""

    if len(exitList) == 1:
        return exitList[0]
    elif len(exitList) == 2:
        return exitList[0] + " and " + exitList[1]
    else:
        exits = exitList[0]
        for x in range(1, len(exitList)):
            if x == len(exitList)-1:
                exits = exits + " and " + exitList[x]
            else:
                exits = exits + ", " + exitList[x]

        return exits

# **********************************************************************
# A function that handles moving the player around the map. The current
# location details are passed in and the new location id is returned.
#
# **********************************************************************    
def movePlayer(locationDetail, direction):
    # First of all, determine if the move is valid?
    # Check for all invalid combinations first
    if (direction == "n" and int(locationDetail[1]) == 0) or \
       (direction == "e" and int(locationDetail[2]) == 0) or \
       (direction == "s" and int(locationDetail[3]) == 0) or \
       (direction == "w" and int(locationDetail[4]) == 0) or \
       (direction == "u" and int(locationDetail[5]) == 0) or \
       (direction == "d" and int(locationDetail[6]) == 0):
        
        # Output an appropriate message, return the original
        # location id.
        print("You can't go that way!")
        return int(locationDetail[0])
    
    # Go North
    elif direction == "n":
        return int(locationDetail[1])

    # Go East
    elif direction == "e":
        return int(locationDetail[2])

    # Go South
    elif direction == "s":
        return int(locationDetail[3])

    # Go West
    elif direction == "w":
        return int(locationDetail[4])

    # Go Up
    elif direction == "u":
        return int(locationDetail[5])

    # Go Up
    elif direction == "d":
        return int(locationDetail[6])

# **********************************************************************
# Start of the main program
#
# **********************************************************************

# Create a few variables
# A boolean to indicate if we're finished
finished = False

# Current location reference:
locationId = 1       # The ID of the current location

# Current location information, this is currently an 9 item list
locationDetail = []

# Keep on going until we're finished
while not(finished):

    # Get details for the current location, store in a list so we only
    # have to fetch it from the file once per location
    locationDetail = getLocationRow(locationId)

    # Print some info about the current location
    showLocation(locationDetail)

    # If we don't have details, there must have been a problem so exit 
    # gracefully.
    if len(locationDetail) == 0:
        print("Logic has broken down, exiting to reality!")
        finished = True
    
    # Read the first keyboard input
    userCommand = input("What next? : ")
    
    # Check for nothing
    if userCommand == "" :
        print("Don't be shy!")
    
    # Check for "North"
    elif userCommand.lower() in  ("north","n") :
        print("You try to go North.")
        locationId = movePlayer(locationDetail,"n")

    # Check for "East"
    elif userCommand.lower() in ("east","e") :
        print("You try to go East.")
        locationId = movePlayer(locationDetail,"e")
    
    # Check for "South"
    elif userCommand.lower() in ("south","s") :
        print("You try to go South.")
        locationId = movePlayer(locationDetail,"s")

    # Check for "West"
    elif userCommand.lower() in ("west","w") :
        print("You try to go West.")
        locationId = movePlayer(locationDetail,"w")

    # Check for "Up"
    elif userCommand.lower() in ("up","u") :
        print("You try to climb up.")
        locationId = movePlayer(locationDetail,"u")

    # Check for "Down"
    elif userCommand.lower() in ("down","d") :
        print("You try to climb down.")
        locationId = movePlayer(locationDetail,"d")

    # Check for "bye"
    elif userCommand.lower() in ("bye") :
        finished = areYouSure("Do you really want to exit? : ")
        
    # If we don't understand, print this
    else :
        print("Sorry! I don't understand " + userCommand)

print("Thanks for playing!") 
