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
# Classes
#
# **********************************************************************

# The item class
class item(object):

    def __init__(self, id, description, location):
        self.id = id
        self.description = description
        self.location = location

# The location class
class location(object):

    def __init__(self, locationFileRow):
        self.id = locationFileRow[0]
        self.locationIDNorth = locationFileRow[1]
        self.locationIDEast = locationFileRow[2]
        self.locationIDSouth = locationFileRow[3]
        self.locationIDWest = locationFileRow[4]
        self.locationIDUp = locationFileRow[5]
        self.locationIDDown = locationFileRow[6]
        self.name = locationFileRow[7]
        self.description = locationFileRow[8]

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
# Scroll a few lines
#
# ********************************************************************** 
def scroll(lines=4):
    # Print a few empty lines
    for x in range(0, lines):
        print()
        time.sleep(.2)  

# **********************************************************************
# Format a list into "correct English", with comma's and ands in the 
# right place.
#
# ********************************************************************** 
def formatList(itemList):

    items = ""

    if len(itemList) == 1:
        return itemList[0]
    elif len(itemList) == 2:
        return itemList[0] + " and " + itemList[1]
    else:
        items = itemList[0]
        for x in range(1, len(itemList)):
            if x == len(itemList)-1:
                items = items + " and " + itemList[x]
            else:
                items = items + ", " + itemList[x]

        return items      

# **********************************************************************
# Load the game objects into a 2D list so they're in memory all the
# time because they can move around once the game starts.
# **********************************************************************    
def getObjects(objFile = r"C:/\Users/\davey/\Documents/\GitHub/\adventure/\objects.txt"):

    # An empty array to store the object list
    objectList = []

    # Open the object file
    with open(objFile, mode='r') as objData:
        objReader = csv.reader(objData, delimiter=',')
        # Loop through each line in the file
        for objDataRow in objReader:
            # Ignore comments
            if not objDataRow[0].startswith('#'):
                # Add item info to the list
                objectList.append(item(int(objDataRow[0]),objDataRow[1],int(objDataRow[2])))

    # Return the object list
    return objectList

# Used for debugging
def showAllObjects(objectList):
    for x in range(0,len(objectList)):
        for y in range(0,len(objectList[x])):
            print(str(x) + ", " + str(y) + " : " + objectList[x][y])

# **********************************************************************
# A procedure that displays any objects for the given location.
# **********************************************************************    
def showObjects(objectList, locationId):

    # An list to hold the names of  objects found at the given location
    objectsHere = []

    # Loop thru all objects
    for x in range(0,len(objectList)):
        # Find any items for the given location id
        if objectList[x].location == locationId:
            # ... and add the description to the objectsHere list
            objectsHere.append(objectList[x].description)

    if len(objectsHere) > 0:
        print("The following items are here:")
        print(formatList(objectsHere))

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
    
    return "You can go " + formatList(exits) + "."

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
locationId = 1       # The ID of the current location, start at 1

# Load the game objects
objectList = getObjects()

# Current location information, this is currently a 9 item list
# Get details for the current location, store in a list so we only
# have to fetch it from the file once per location visit.
locationDetail = getLocationRow(locationId)

# Print some info about the current location
showLocation(locationDetail)

# Show any items here
# showAllObjects(objectList)
showObjects(objectList, locationId)

# Keep on going until we're finished
while not(finished):

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
        scroll()
    
    # Check for "North"
    elif userCommand.lower() in  ("north","n") :
        print("You try to go North.")
        locationId = movePlayer(locationDetail,"n")
        # Get new location details
        locationDetail = getLocationRow(locationId) 
        # Display new location details       
        showLocation(locationDetail)  
        # Show any items here
        showObjects(objectList, locationId)         
        # Print a few empty lines
        scroll()     

    # Check for "East"
    elif userCommand.lower() in ("east","e") :
        print("You try to go East.")
        locationId = movePlayer(locationDetail,"e")
        # Get new location details
        locationDetail = getLocationRow(locationId) 
        # Display new location details       
        showLocation(locationDetail)  
        # Show any items here
        showObjects(objectList, locationId)         
        # Print a few empty lines
        scroll()  

    # Check for "South"
    elif userCommand.lower() in ("south","s") :
        print("You try to go South.")
        locationId = movePlayer(locationDetail,"s")
        # Get new location details
        locationDetail = getLocationRow(locationId) 
        # Display new location details       
        showLocation(locationDetail)  
        # Show any items here
        showObjects(objectList, locationId)         
        # Print a few empty lines
        scroll()  

    # Check for "West"
    elif userCommand.lower() in ("west","w") :
        print("You try to go West.")
        locationId = movePlayer(locationDetail,"w")
        # Get new location details
        locationDetail = getLocationRow(locationId) 
        # Display new location details       
        showLocation(locationDetail)  
        # Show any items here
        showObjects(objectList, locationId)         
        # Print a few empty lines
        scroll()  

    # Check for "Up"
    elif userCommand.lower() in ("up","u") :
        print("You try to climb up.")
        locationId = movePlayer(locationDetail,"u")
        # Get new location details
        locationDetail = getLocationRow(locationId) 
        # Display new location details       
        showLocation(locationDetail)  
        # Show any items here
        showObjects(objectList, locationId)         
        # Print a few empty lines
        scroll()  

    # Check for "Down"
    elif userCommand.lower() in ("down","d") :
        print("You try to climb down.")
        locationId = movePlayer(locationDetail,"d")
        # Get new location details
        locationDetail = getLocationRow(locationId) 
        # Display new location details       
        showLocation(locationDetail)  
        # Show any items here
        showObjects(objectList, locationId)         
        # Print a few empty lines
        scroll()  

    # Check for "Look"
    elif userCommand.lower() in ("look","l") :
        print("You look around...")
        scroll()
        # Just re-show the current location details
        showLocation(locationDetail)  
        # Show any items here
        showObjects(objectList, locationId)         
        # Print a few empty lines
        scroll()          

    # Check for "bye"
    elif userCommand.lower() in ("bye") :
        finished = areYouSure("Do you really want to exit? : ")
        
    # If we don't understand, print this
    else :
        print("Sorry! I don't understand " + userCommand)
        scroll()

print("Thanks for playing!") 
