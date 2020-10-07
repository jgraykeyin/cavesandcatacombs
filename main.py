import random
import os
from playsound import playsound

# This should let files in the current folder be accessible
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Setup the player starts
########$ HP,Atk,Lvl,XP
player = {"hpmax":20,"hp":20,"atk":5,"lvl":1,"xp":1,"xpnext":20}

# Game settings
hasMonster = False
roomMsg = "You see a stairway leading down to the catacombs of dooooom! Move to the next area to begin your adventure."
gameStop = 0
monsters=[]
lastmonster=""
progress=0
levelup=False
lastboss=False
itemdeath=""

# Loot!
items = [
        {"name":"Red Potion","stattype":"hp","statnum":10,"positive":1,"desc":"Yum, red potions are great. Gained 10 HP!","qty":8},
        {"name":"Green Potion","stattype":"hp","statnum":5,"positive":0,"desc":"You drank a poison potion and lost 5 HP!","qty":15},
        {"name":"Coffee","stattype":"hp","statnum":20,"positive":1,"desc":"You drink the coffee and feel much better, gained 20 HP!","qty":5},
        {"name":"Power Scroll","stattype":"atk","statnum":2,"positive":1,"desc":"The power scroll increases your Atk by 2!","qty":3}
]

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
    elif command.upper() == "A" and hasMonster == True:
        attack()

# Check the room for loot
# Going to try a system of randomly finding good or bad items based on a find-roll
# Items will activate or equip upon finding them, maybe we'll work on an inventory system another day.
def lookRoom():
    global roomMsg
    global items
    global itemdeath
    statmod = ""
    stype = ""
    if player["hp"] > 1:
        findroll = random.randint(1,20)
        if findroll > 10:
            item = random.choice(items)
            if item["stattype"] == "atk":
                stype="atk"
            else:
                stype="hp"

            if item["positive"] == 1:
                statmod="+"
                player[stype] += item["statnum"]
            else:
                statmod="-"
                player[stype] -= item["statnum"]

            if player["hp"] <= 0:
                itemdeath = item["name"]
                gameStop=1

            if player["hp"] > player["hpmax"]:
                player["hp"] = player["hpmax"]

            roomMsg = "You found: {} ({}{} {})\n{}".format(item["name"],statmod,item["statnum"],item["stattype"].upper(),item["desc"])

            # Delete the item from the list if we've found all of them
            item["qty"] -= 1
            if item["qty"] < 1:
                items.remove(item)
            
        else:
            # Reducing player's HP by one if they don't find anything, just to be mean.
            player["hp"] = player["hp"] - 1
            roomMsg = "You can't find anything here.\nLost 1 HP from disappointment.\n"
    else:
        roomMsg = "You don't have enough energy to find things right now.\n"
    
    try:
        playsound(os.path.join(__location__, 'find.mp3'))
    except:
        # Disable the sound effects if it's having trouble playing them
        pass   

# Load a new area, this should generate monster(s) and item(s)
def moveNext():
    global roomMsg
    global hasMonster
    global progress
    roomMsg = "You step into the next room.\n"
    progress = progress + 1

    # Creating a new room will always contain at least 1 monster, so set hasMonster to true
    hasMonster = True

    # Let's spawn our monsters here
    x=0
    y=player["lvl"] * 2
    monsterRoll = random.randint(1,y)
    if progress == 20:
        spawnMonster()
    else:
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
    global lastboss
    if progress == 20:
        monstername = "Cyber-Billy Bob"
        monsters.append({"name":monstername,"hp":250})
        lastboss = True
    else:
        lines = open(os.path.join(__location__, 'monsters.txt')).read().splitlines()
        monstername = random.choice(lines)
        limit = player["lvl"] * 14
        hproll = random.randint(5,limit)
        monsters.append({"name":monstername,"hp":hproll})

def attack():
    global lastmonster
    global roomMsg
    global hasMonster
    global levelup
    for monster in monsters:
        # Attacking the monster
        atk = random.randint(1,player["atk"])
        monster["hp"] = monster["hp"] - atk

        if monster["hp"] > 0:
            # Modifier to generate monster damage rolls...
            # TODO: turn this into a function, make it a little more dynamic
            level = player["lvl"] * random.randint(1,3)

            # Monster counter-attacking the player
            counter = random.randint(1,level)
            player["hp"] = player["hp"] - counter
            if player["hp"] < 1:
                lastmonster = monster["name"]
        elif monster["hp"] <= 0:
            #Modifier to generate xp gain
            # TODO: turn this into a function, maybe the same function as monster atk modifier?
            xpmod = player["lvl"] * 10
            xpgain = random.randint(player["lvl"],xpmod)
            player["xp"] = player["xp"] + xpmod

            roomMsg="{} defeated!\n{} XP gained!\n".format(monster["name"],xpgain)
            try:
                playsound(os.path.join(__location__, 'defeat.mp3'))
            except:
                # Disable the sound effects if it's having trouble playing them
                pass

            #Check to see if player leveled up
            if player["xp"] >= player["xpnext"]:
                player["lvl"] += 1
                player["atk"] += 2
                player["hpmax"] += 5 * player["lvl"]
                player["hp"] = player["hpmax"]
                player["xpnext"] = (player["xpnext"] * 2) + (player["lvl"] * 5)
                roomMsg = roomMsg + "\nYou've reached level {}!".format(player["lvl"])
                levelup=True

            monsters.remove(monster)

    if len(monsters) < 1:
        hasMonster=0

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

        fpath = (os.path.join(__location__, "highscores.txt"))
        highscore = open(fpath,"a")
        print(" ¯\_(ツ)_/¯")
        if itemdeath != "":
            print("You've been thwarted by a {}!".format(itemdeath))
        else:
            print("You've been eaten by a {}! Game Over!".format(lastmonster))
        print("You traveled through {} areas and reached level {}".format(progress,player["lvl"]))

        highscore.write("{} =-= Areas Explored: {}/20 =-= Level: {}\n".format(playername,progress, player["lvl"]))
        highscore.close
        try:
            playsound(os.path.join(__location__, 'gameover.mp3'))
        except:
        # Disable the sound effects if it's having trouble playing them
            pass

        fpath = (os.path.join(__location__, "highscores.txt"))
        highscore = open(fpath,"r")
        print("Adventure Log:")
        scores = highscore.readlines()
        for score in scores:
            print(score)
        highscore.close()
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
        if levelup is True:
            # Trigger the level-up sound
            try:
                playsound(os.path.join(__location__, 'levelup.mp3'))
            except:
                # Disable the sound effects if it's having trouble playing them
                pass
            levelup = False
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
    print("\n{} -- HP:{}/{} Atk:{} Lvl:{}".format(playername,player["hp"],player["hpmax"],player["atk"],player["lvl"]))

    # Display the available commands.
    showCommands()
    os.system('clear')

    # Check for user input commands
    parseCommand(command)

    # Make sure player is still alive
    statCheck()



