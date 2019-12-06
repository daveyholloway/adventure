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
# A function that returns a row from the map file for the location id
# passed in as a parameter.
#
# **********************************************************************    
def getLocationRow(locationId, mapFile = r"C:/\Users/\d7998/\Desktop/\Adventure/\map.txt"):

    # Variables to store the return values
    exitNorth = 0
    exitEast = 0
    exitSouth = 0
    exitWest = 0
    exitUp = 0
    exitDown = 0
    locationName = ""
    locationDescription = ""

    # A boolean to record whether we found anything
    found = False
    
    # Open the map file
    with open(mapFile, mode='r') as mapData:
        mapReader = csv.reader(mapData, delimiter=',')
        for mapDataRow in mapReader:
            if mapDataRow[0] == str(locationId):
                exitNorth = mapDataRow[1]
                exitEast = mapDataRow[2]
                exitSouth = mapDataRow[3]
                exitWest = mapDataRow[4]
                exitUp = mapDataRow[5]
                exitDown = mapDataRow[6]
                locationName = mapDataRow[7]
                locationDescription = mapDataRow[8]

                found = True
                
    # If we found a row, return it, other wise return a room id of 0
    if found:
        return locationId, exitNorth, exitEast, exitSouth, exitWest, exitUp, exitDown, locationName, locationDescription
    else:
        return 0,0,0,0,0,0,0,"",""

# **********************************************************************
# A procedure that displays the current location details.
#
# **********************************************************************    
def showLocation(locationId):

    # Variables to store the return values
    exitNorth = 0
    exitEast = 0
    exitSouth = 0
    exitWest = 0
    exitUp = 0
    exitDown = 0
    locationName = ""
    locationDescription = ""    

    # Find location info for the current location
    locationId, exitNorth, exitEast, exitSouth, exitWest, exitUp, exitDown, locationName, locationDescription = getLocationRow(locationId)

    # Check to see if details were found
    if locationId != 0:

        print(locationName)
        print("===================")
        print(locationDescription)

    else:

        print("You're completely lost, ask the programmer!")
        print(locationId)


# **********************************************************************
# Start of the main program
#
# **********************************************************************

# Create a few variables
# A boolean to indicate if we're finished
finished = False

# Current location details:
locationId = 1       # The ID of the current room

# Keep on going until we're finished
while not(finished):

    # Print some info about the current location
    showLocation(locationId)
    
    # Read the first keyboard input
    userCommand = input("What next? : ")
    
    # Check for nothing
    if userCommand == "" :
        print("Don't be shy!")
    
    # Check for "North"
    elif userCommand.lower() in  ("north","n") :
        print("You go North.")

    # Check for "East"
    elif userCommand.lower() in ("east","e") :
        print("You go East.")
    
    # Check for "South"
    elif userCommand.lower() in ("south","s") :
        print("You go South.")

    # Check for "West"
    elif userCommand.lower() in ("west","w") :
        print("You go West.")

    # Check for "bye"
    elif userCommand.lower() in ("bye") :
        finished = areYouSure("Do you really want to exit? : ")
        
    # If we don't understand, print this
    else :
        print("Sorry! I don't understand " + userCommand)

print("Thanks for playing!") 
