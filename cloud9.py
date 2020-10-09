import random
import os

# This should let files in the current folder be accessible
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Game settings
def initGame():
    global player,hasMonster,roomMsg,gameStop,monsters,lastmonster,progress,levelup,lastboss,itemdeath,victory,fireqty,firemax,windqty,progressbar,items,hpmax
    player = {"hpmax":20,"hp":20,"atk":5,"lvl":1,"xp":1,"xpnext":20}
    hasMonster = False
    roomMsg = "You see a stairway leading down to the catacombs of dooooom! Move to the next area to begin your adventure."
    gameStop = 0
    monsters=[]
    lastmonster=""
    progress=0
    levelup=False
    lastboss=False
    itemdeath=""
    victory=False
    fireqty=3
    firemax=3
    windqty=1
    progressbar = " | | | | | | | | | | | | | | | | | | | |"

    # Loot!
    hpmax = player["hpmax"]
    items = [
            {"name":"Red Potion","stattype":"hp","statnum":10,"positive":1,"desc":"Yum, red potions are great. Gained 10 HP!","qty":8},
            {"name":"Green Potion","stattype":"hp","statnum":5,"positive":0,"desc":"You drank a poison potion and lost 5 HP!","qty":15},
            {"name":"Coffee","stattype":"hp","statnum":20,"positive":1,"desc":"You drink the coffee and feel much better, gained 20 HP!","qty":5},
            {"name":"Power Scroll","stattype":"atk","statnum":2,"positive":1,"desc":"The power scroll increases your Atk by 2!","qty":5},
            {"name":"Power Glove","stattype":"atk","statnum":3,"positive":1,"desc":"The power gloves increases your Atk by 3, it's so bad!","qty":3},
            {"name":"Magic Hero Sword","stattype":"atk","statnum":4,"positive":1,"desc":"You equip the hero sword to gain 4 Atk!","qty":2},
            {"name":"Slime on a stick","stattype":"atk","statnum":1,"positive":0,"desc":"Your equipment is covered in slime, lost 2 Atk!","qty":4},
            {"name":"Cure Scroll","stattype":"hp","statnum":20,"positive":1,"desc":"The cure scroll heals you for 20 HP!","qty":5},
            {"name":"Legendary Battle Staff","stattype":"atk","statnum":10,"positive":1,"desc":"The battle staff raises your Atk by 10!","qty":1}
        ]

initGame()

# Display the currently available player-commands
def showCommands():
    global command
    if hasMonster == True:
        if player["lvl"] >= 6:
            command = input("Available Commands: [Q]uit [L]ook [A]ttack [F]ire Spell({}/{}) [W]ind Spell {}/1 >> ".format(fireqty,firemax,windqty))
        elif player["lvl"] >= 3:
            command = input("Available Commands: [Q]uit [L]ook [A]ttack [F]ire Spell({}/{}) >> ".format(fireqty,firemax))
        elif player["lvl"] < 3:
            command = input("Available Commands: [Q]uit [L]ook [A]ttack >> ")
    elif lastboss == True:
        command = input("Available Commands: [Q]uit [Look]")
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
    elif command.upper() == "F" and player["lvl"] >= 3 and fireqty > 0:
        firespell()
    elif command.upper() == "W" and player["lvl"] >= 6 and windqty > 0:
        windspell()

# Check the room for loot
# Going to try a system of randomly finding good or bad items based on a find-roll
# Items will activate or equip upon finding them, maybe we'll work on an inventory system another day.
def lookRoom():
    global roomMsg
    global items
    global itemdeath
    global gameStop
    statmod = ""
    stype = ""
    if player["hp"] > 1:
        findroll = random.randint(1,20)
        if findroll > 10:
            if len(items) > 0:
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
                roomMsg = roomMsg + "No items left to find!"
                
        else:
            # Reducing player's HP by one if they don't find anything, just to be mean.
            player["hp"] = player["hp"] - 1
            roomMsg = "You can't find anything here.\nLost 1 HP from disappointment.\n"
    else:
        roomMsg = "You don't have enough energy to find things right now.\n"
    

# Load a new area, this should generate monster(s) and item(s)
def moveNext():
    global roomMsg
    global hasMonster
    global progress
    global progressbar
    roomMsg = "You step into the next room.\n"
    progress = progress + 1
    progressbar = "|=|" + progressbar[:-1]

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
    os.system('clear')

def spawnMonster():
    global monsters
    global lastboss
    if progress == 20:
        monstername = "Spirit of Billy Bob"
        monsters.append({"name":monstername,"hp":500})
        lastboss = True
    else:
        lines = open(os.path.join(__location__, 'monsters.txt')).read().splitlines()
        monstername = random.choice(lines)
        limit = player["lvl"] * 14
        hproll = random.randint(5,limit)
        monsters.append({"name":monstername,"hp":hproll})

def windspell():
    global hasMonster
    global roomMsg
    global windqty
    global monsters
    monsters = []
    roomMsg = "Wind magic blows away all monsters in the room. No XP gained, but you're safe for now..."
    hasMonster = False
    windqty=0
    
def firespell():
    global fireqty
    global hasMonster
    global roomMsg
    global levelup
    fireqty-=1
    for monster in monsters:
        dmg = random.randint(10,30)
        monster["hp"] -= dmg

        if monster["hp"] < 1:
            xpmax = player["lvl"] * 10
            xpmin = player["lvl"] * 5
            xpgain = random.randint(xpmin,xpmax)
            player["xp"] += xpgain
            roomMsg="{} defeated!\n{} XP gained!\n".format(monster["name"],xpgain)

            #Check to see if player leveled up
            if player["xp"] >= player["xpnext"]:
                levelUp()

            monsters.remove(monster)
    roomMsg = roomMsg = "\nThe fire spell blasts all the monsters in the room!"
    if len(monsters) < 1:
        hasMonster=0

def levelUp():
    global fireqty
    global player
    global roomMsg
    global levelup
    global windqty
    fireqty+=1
    if fireqty > firemax:
        fireqty = firemax
    player["lvl"] += 1
    if player["lvl"] % 2 == 0:
        windqty = 1
    player["atk"] += 2
    player["hpmax"] += 5 * player["lvl"]
    player["hp"] = player["hpmax"]
    player["xpnext"] = (player["xpnext"] * 2) + (player["lvl"] * 5)
    roomMsg = roomMsg + "\nYou've reached level {}!".format(player["lvl"])
    levelup=True

def attack():
    global lastmonster
    global roomMsg
    global hasMonster
    global levelup
    global gameStop
    global victory
    for monster in monsters:
        # Attacking the monster
        atk = random.randint(1,player["atk"])
        monster["hp"] = monster["hp"] - atk

        roomMsg = roomMsg + "You hit the {} for {} HP\n".format(monster["name"],atk)

        if monster["hp"] > 0:
            # Modifier to generate monster damage rolls...
            # TODO: turn this into a function, make it a little more dynamic
            level = player["lvl"] * random.randint(1,3)
            # Monster counter-attacking the player
            counter = random.randint(1,level)
            roomMsg = roomMsg + "You take {} damage from the {}!\n".format(counter,monster["name"])
            player["hp"] = player["hp"] - counter
            if player["hp"] < 1:
                lastmonster = monster["name"]
        elif monster["hp"] <= 0:
            #Modifier to generate xp gain
            # TODO: turn this into a function, maybe the same function as monster atk modifier?
            xpmax = player["lvl"] * 10
            xpmin = player["lvl"] * 5
            xpgain = random.randint(xpmin,xpmax)
            player["xp"] += xpgain

            if victory == True:
                gameStop=1

            roomMsg=roomMsg + "\n{} defeated!\n{} XP gained!\n".format(monster["name"],xpgain)

            #Check to see if player leveled up
            if player["xp"] >= player["xpnext"]:
                levelUp()

            monsters.remove(monster)

    if len(monsters) < 1:
        hasMonster=0

    
# Check to see if player has died or leveled up
def statCheck():
    global gameStop
    if player["hp"] <= 0:

        print("\n ¯\_(ツ)_/¯")
        if itemdeath != "":
            print("You've been thwarted by a {}!".format(itemdeath))
        else:
            print("You've been eaten by a {}! Game Over!".format(lastmonster))
        print("You traveled through {} areas and reached level {}".format(progress,player["lvl"]))

        gameStop = 1

while True:
    os.system('clear')
    print("-=-=-=-=-=-=-=-=-=-=-=-")
    print("-= Caves & Catacombs =-")
    print("-=-=-=-=-=-=-=-=-=-=-=-")
    playername = input("Please enter your name: ")
    # os.system('clear')
    # Start a game loop
    while gameStop == 0:

        # Check for any room-loading messages, then clear it.
        if roomMsg:
            if levelup is True:
                levelup = False
            print(roomMsg)
            roomMsg=""

        # Check to see if we need to list our monsters
        if len(monsters) > 0:
            print("\nMonsters in this room:")
            for monster in monsters:
                print("* {} HP {}".format(monster["hp"],monster["name"]))
        else:
            hasMonster=False

        # Display the player stats
        print("\n{} -- HP:{}/{} Atk:{} Lvl:{}".format(playername,player["hp"],player["hpmax"],player["atk"],player["lvl"]))
        print("\n{}\n".format(progressbar))

        # Display the available commands.
        showCommands()

        os.system('clear')

        # Check for user input commands
        parseCommand(command)

        # Make sure player is still alive
        statCheck()

    if victory == True:
        print("You've finished the game and stolen Billy Bob's treasure, good job!")
        print("Purchase our DLC for a better ending!")

    reset = input("\nTry again? Y or N: ")
    if reset.upper() == "N":
        break
    elif reset.upper() == "Y":
        initGame()
        continue