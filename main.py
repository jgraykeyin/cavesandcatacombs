import random
import os

# Setup the player starts
########$ HP,Atk,Lvl,XP
player = [20,1,1,1]

# Game settings
hasMonster = False
hasLoot = False
roomMsg = ""
gameStop = 0

# Display the currently available player-commands
def showCommands():
    global command
    if hasMonster == True:
        command = input("Available Commands: [Q]uit [L]ook [A]ttack >> ")
    else:
        command = input("Available Commands: [Q]uit [L]ook [M]ove >> ")

# Map the input commands to their functions
def parseCommand(command):
    global gameStop
    if command.upper() == "M" and hasMonster == False:
        moveNext()
    elif command.upper() == "L":
        lookRoom()
    elif command.upper() == "Q":
        gameStop = 1

# Check the room for monsters and loot
def lookRoom():
    if hasLoot == False:
        print("You can't find any loot in this area.\n")

    if hasMonster == False:
        print("You can't see any monsters in this area.\n")

# Load a new area, this should generate monster(s) and item(s)
def moveNext():
    global roomMsg
    global hasMonster
    roomMsg = "You continue into the next room...\n"
    hasMonster = True
    
# Check to see if player has died or leveled up
def statCheck():
    global gameStop
    if player[0] < 0:
        gameStop = 1

os.system('clear')
print("----------------------")
print("Welcome to The Really Dangerous Place!\nFind the amazing secret treasure to become the hero of all the things!\n")
playername = input("Player Name: ")

# Start a game loop
while gameStop == 0:

    if roomMsg:
        print(roomMsg)

    # Display the player stats
    print("{} -- HP:{} Atk:{} Lvl:{}".format(playername,player[0],player[1],player[2]))

    # Display the available commands.
    showCommands()
    os.system('clear')

    # Check for user input commands
    parseCommand(command)

    # Make sure player is still alive
    statCheck()



