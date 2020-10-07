import random
import os
from playsound import playsound

# This should let files in the current folder be accessible
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Setup the player starts
########$ HP,Atk,Lvl,XP
player = {"hp":20,"atk":4,"lvl":1,"xp":1}

# Game settings
hasMonster = False
hasLoot = False
roomMsg = "You see a stairway leading down to the catacombs of dooooom! Move to the next area to begin your adventure."
gameStop = 0
monsters=[]
lastmonster=""

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
    elif command.upper() == "A":
        attack()

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
    roomMsg = "You step into the next room.\n"

    # Creating a new room will always contain at least 1 monster, so set hasMonster to true
    hasMonster = True

    # Let's spawn our monsters here
    x=0
    y=player["lvl"] * 2
    monsterRoll = random.randint(1,y)
    while x < monsterRoll:
        spawnMonster()
        x+=1

    print("Searching for the next area...")
    try:
        playsound(os.path.join(__location__, "steps.mp3"))
    except:
        pass
    os.system('clear')

def spawnMonster():
    global monsters
    lines = open(os.path.join(__location__, 'monsters.txt')).read().splitlines()
    monstername = random.choice(lines)
    hproll = random.randint(5,25)
    monsters.append({"name":monstername,"hp":hproll})

def attack():
    global lastmonster
    for monster in monsters:
        # Attacking the monster
        atk = random.randint(1,player["atk"])
        monster["hp"] = monster["hp"] - atk

        if monster["hp"] > 0:
            # Modifier to generate monster damage rolls...
            # TODO: turn this into a function, make it a little more dynamic
            level = player["lvl"] * random.randint(1,4)

            # Monster counter-attacking the player
            counter = random.randint(1,level)
            player["hp"] = player["hp"] - counter
            if player["hp"] < 1:
                lastmonster = monster["name"]
    
    for i in range(len(monsters)):
        if monsters[i]["hp"] < 1:
            #Modifier to generate xp gain
            # TODO: turn this into a function, maybe the same function as monster atk modifier?
            xpmod = player["lvl"] * 10
            xpgain = random.randint(player["lvl"],xpmod)
            player["xp"] = player["xp"] + xpmod

            print("{} defeated!".format(monsters[i]["name"]))
            print("{} XP gained!".format(xpgain))
            #roomMsg="{} defeated!".format(monsters[i]["name"])
            del monsters[i]
            break

    # Trigger the really cool 8bit attack sound
    try:
        playsound(os.path.join(__location__, 'hit.mp3'))
    except:
        # Disable the sound effects if it's having trouble playing them
        pass
    
# Check to see if player has died or leveled up
def statCheck():
    global gameStop
    if player["hp"] <= 0:
        print("\nYou've been eaten by a {}! Game Over! ¯\_(ツ)_/¯\n".format(lastmonster))
        gameStop = 1

os.system('clear')
print("----------------------")
print("Welcome to The Really Dangerous Place!\nFind the amazing secret treasure to become the hero of all the things!\n")
playername = input("Player Name: ")
os.system('clear')
# Start a game loop
while gameStop == 0:

    # Check for any room-loading messages, then clear it.
    if roomMsg:
        print(roomMsg)
        roomMsg=""

    # Check to see if we need to list our monsters
    if len(monsters) > 0:
        print("Monsters in this room:")
        for monster in monsters:
            print("* {} HP {}".format(monster["hp"],monster["name"]))
    else:
        hasMonster=False

    # Display the player stats
    print("\n{} -- HP:{} Atk:{} Lvl:{}".format(playername,player["hp"],player["atk"],player["lvl"]))

    # Display the available commands.
    showCommands()
    os.system('clear')

    # Check for user input commands
    parseCommand(command)

    # Make sure player is still alive
    statCheck()



