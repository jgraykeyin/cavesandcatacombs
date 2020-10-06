print("----------------------")
print("Welcome to Not Diablo!")
playername = input("Player Name: ")

# Setup the player starts
########$ HP,Atk,Lvl,XP
player = [20,1,1,1]

# Game settings
hasMonster = False
hasLoot = False
introMessage = True

# Function to display the currently available player-commands
def showCommands():
    global command
    command = input("Available Commands: [M]ove [L]ook >> ")

def parseCommand(command):
    if command.upper() == "M":
        pass
        # Trigger a move function to allow the user to progress
        # moveNext()
    if command.upper() == "L":
        pass
        # Trigger a look function to inspect the current room
        # lookRoom()


# Start a game loop
while True:
    if introMessage is True:
        print("Welcome to The Really Dangerous Place!\nFind the amazing secret treasure to become the hero of all the things!\n")
        print("{} -- HP:{} Atk:{} Lvl:{}".format(playername,player[0],player[1],player[2]))
        introMessage=False
    
    # Display the available commands.
    showCommands()

    # Check for user input commands
    parseCommand(command)


    #Just using this break while testing, remove this to let the game loop run
    break
