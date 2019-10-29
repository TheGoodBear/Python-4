# Maze v1.1

# Modules importation
# -------------------
import os
import json
import random


# Variables (must be declared BEFORE using them)
# ---------

# Variables for player data
PlayerName: str = ""
PlayerImage: str = "☻" # alt+2
# Variables for maze and maze elements
MazeFilePath: str = "Mazes/"
MazeFileName: str = "Maze 1"
Maze = list()
MazeElements = list()
# Variables for player character
PlayerX: int = 0
PlayerY: int = 0
PlayerBackpack = list()


# Methods (must be declared BEFORE using them)
# -------

def ApplicationStart():
    """ 
        Initialize application and show initial message
    """

    print("\nBonjour humain, merci de t'identifier afin que je puisse interagir avec toi.")


def GetPlayerData() -> str:
    """ 
        Get player data

        :return: Player name
        :rtype: string
    """

    Name: str = ""

    # Ask for name until it is filled
    while(Name == ""):
        Name = input("\nMerci d'entrer ton nom : ")

    # Return Name
    return Name


def SayWelcome():
    """ 
        Say Welcome to player
    """

    print(
        "\nEnchanté {0}, j'espère que tu vas bien t'amuser." 
        .format(PlayerName))


def StartGame():
    """ 
        Give rules to player
    """

    print(
        "\nTon objectif est de sortir du labyrinthe." + 
        "\nPour cela il te faudra trouver la sortie et avoir collecté les objets nécessaires à l'ouverture de la porte." + 
        "\nTu es représenté par {0} et la porte de sortie par {1}.".format(PlayerImage, GetMazeElement("Sortie")["Image"]) + 
        "\nÀ chaque tour tu peux effectuer l'une des actions suivantes :" + 
        "\nTe déplacer vers le (H)aut, le (B)as, la (G)auche, la (D)roite ou (Q)uitter le jeu (et perdre...)" + 
        "\nBonne chance.")


def LoadMazeFromFile(FileName: str):
    """ 
        Load maze from text file and store it into a 2 dimensional list

        :param arg1: The name of the file
        :type arg1: string
    """

    # Use global Maze variable
    global Maze

    # try/exception block to trap errors
    try:
        # Open file in read mode (and automatically close it when finished)
        with open(MazeFilePath + FileName + ".maz", "r") as MyFile:
            for Line in MyFile:
                # Ignore blank lines and comments
                if(Line[0] == "\n" or Line[0] == "#"):
                    continue
                # Define temporary list to store every character in a line
                LineCharacters = list()
                # For each Character in Line
                for Character in Line:
                    # Store Character in LineCharacters list (except new line \n)
                    if (Character != "\n"):
                        # Search in maze elements for matching symbol
                        CurrentElement = GetMazeElement(Symbol=Character)
                        if(CurrentElement != None):
                            # If an element was found, append element's image
                            LineCharacters.append(CurrentElement["Image"])
                        else:
                            # If no element was found append character
                            LineCharacters.append(Character)
                # Store LineCharacters list in Maze list (2 dimensional list)
                Maze.append(LineCharacters)

    except OSError:
        # If there is an OSError exception
        print("\nLe labyrinthe demandé n'a pas été trouvé !\n")
        # exit application
        os._exit(1)


def LoadMazeElementsFromFile(FileName: str):
    """ 
        Load maze elements from json file and store them into list of dictionaries

        :param arg1: The name of the file
        :type arg1: string
    """

    # Use global Maze variable
    global MazeElements

    # try/exception block to trap errors
    try:
        # Open JSON file in read mode (and automatically close it when finished)
        with open(MazeFilePath + FileName + " Elements.json", "r", encoding='utf-8') as MyFile:
            # Load them into maze elements list of dictionary
            MazeElements = json.load(MyFile)
            #print(MazeElements)

        # # Code sample to write to JSON file
        # # Open JSON file in write mode (and automatically close it when finished)
        # with open("MazeElements.json", "w", encoding="utf-8") as WriteFile:
        #     # Write to file using proper ascii encoding (with accents) and indentation
        #     json.dump(MazeElements, WriteFile, ensure_ascii=False, indent=4)

    except OSError:
        # If there is an OSError exception
        print("\nLes éléments du labyrinthe demandé n'ont pas été trouvés !\n")
        # exit application
        os._exit(1)


def GetMazeElement(
    Name: str = "",
    Symbol: str = "",
    Image: str = "") -> {}:
    """ 
        Return a maze element by its name, symbol or image

        :param arg1: The element name
        :type arg1: string
        :param arg2: The element symbol
        :type arg2: string
        :param arg3: The element image
        :type arg3: string

        :return: The element (dictionary of all its properties)
        :rtype: dictionary
    """

    # # Alternative syntax with list comprehension
    # return next((ME for ME in MazeElements if ME["Symbol"] == Symbol), None)

    # Browse all elements to find the matching one
    for CurrentElement in MazeElements:
        if(Name != "" and CurrentElement["Name"] == Name):
            return CurrentElement
        elif(Symbol != "" and CurrentElement["Symbol"] == Symbol):
            return CurrentElement
        elif(Image != "" and CurrentElement["Image"] == Image):
            return CurrentElement

    # If no element matches, return none (null/nothing)
    return None


def PlaceMazeObjectsAtRandomPositions():
    """ 
        Place all objects from dictionary at random positions in maze
    """

    # Use global Maze variable
    global Maze

    # Browse every maze element
    for CurrentObject in MazeElements:
        if("Pick" in CurrentObject["Behavior"]):
            # the current object is pickable
            # draw random coordinates in maze limits
            ObjectX: int = random.randint(0, len(Maze)-1)
            ObjectY: int = random.randint(0, len(Maze[0])-1)
            while(Maze[ObjectY][ObjectX] != GetMazeElement("Sol")["Image"]):
                # do it again until random position is ground
                ObjectX = random.randint(0, len(Maze)-1)
                ObjectY = random.randint(0, len(Maze[0])-1)
            # place current object at this position (replace the ground with it)
            Maze[ObjectY][ObjectX] = CurrentObject["Image"]


def DrawMazeOnScreen():
    """ 
        Draw maze in console
        Including player
    """

    # Prints a blank line
    print()

    # With simple loop (gives only the content)
    # For each line (Y) in Maze
    for Line in Maze:
        # For each character (X) in line
        for Column in Line:
            # Print current maze element at Y, X without jumping a line
            print(Column, end="")
        # Jump a line for new Y
        print()
    
    # # With range and len (gives only the coordinates)
    # # For each line (Y) in Maze
    # for Y in range(len(Maze)):
    #     # For each character (X) in line
    #     for X in range(len(Maze[Y])):
    #         # Print current maze element at Y, X without jumping a line
    #         print(Maze[Y][X], end="")
    #     # Jump a line for new Y
    #     print()
    
    # # With enumerate (gives the content and the coordinates)
    # # For each line (Y) in Maze
    # for Y, Line in enumerate(Maze):
    #     # For each character (X) in line
    #     for X, Column in enumerate(Maze[Y]):
    #         # Print current maze element at Y, X without jumping a line
    #         print(Maze[Y][X], end="")
    #     # Jump a line for new Y
    #     print()


def PlacePlayerInMaze(
    PlayerNewX: int = 0,
    PlayerNewY: int = 0):
    """ 
        Place player in maze

        :param arg1: The new X position of player
        :type arg1: integer
        :param arg2: The new Y position of player
        :type arg2: integer
    """

    # Use global variables
    global Maze, PlayerX, PlayerY

    # Variables for maze coordinates
    X: int = 0
    Y: int = 0

    # Check if player is not already in the maze (coordinates set to 0)
    if (PlayerX == 0 and PlayerY == 0):
        # In that case put him at the entrance
        # find it by browsing maze list
        for Line in Maze:
            # New line, set X coordinate to 0
            X = 0
            for Character in Line:
                # If position contains entrance (E)
                if (Maze[Y][X] == GetMazeElement("Entrée")["Image"]):
                    # Save coordinates for player
                    PlayerX = X
                    PlayerY = Y
                    # Replace entrance with player
                    Maze[Y][X] = PlayerImage
                    # Exit loops (and method)
                    return
                # Increment X coordinate
                X += 1
            # Increment Y coordinate
            Y += 1

    else:
        # Player is already in maze
        # replace actual player position with a floor
        Maze[PlayerY][PlayerX] = GetMazeElement("Sol")["Image"]
        # and place player to new position
        Maze[PlayerNewY][PlayerNewX] = PlayerImage


def WaitForPlayerAction() -> str:
    """ 
        Wait player to make an action

        :return: The name of the action if the action is valid
        :rtype: string
    """

    # Show player backpack content
    print("\nContenu du sac à dos : ", end="")
    if (len(PlayerBackpack) == 0):
        # if backpack is empty (nothing in list)
        print("vide")
    else:
        # if backpack contains at least 1 object (* means every item in list)
        print(*PlayerBackpack, sep=', ')

    # Ask player input until it is a valid action
    while True:
        PlayerInput = input("\nQuelle est ta prochaine action ? ")

        # check if this is a valid action
        # show a message saying what player is doing
        # and return action name if valid
        if (PlayerInput.upper() == "H"):
            print("Tu te déplaces vers le haut...")
            return "MoveUp"
        elif (PlayerInput.upper() == "B"):
            print("Tu te déplaces vers le bas...")
            return "MoveDown"
        elif (PlayerInput.upper() == "G"):
            print("Tu te déplaces vers la gauche...")
            return "MoveLeft"
        elif (PlayerInput.upper() == "D"):
            print("Tu te déplaces vers la droite...")
            return "MoveRight"
        elif (PlayerInput.upper() == "Q"):
            print("Tu choisis de quitter le labyrinthe, tu as perdu !\n")
            return "QuitGame"
        else:
            print("Cette action n'est pas reconnue.")


def ExecutePlayerAction(PlayerAction: str) -> bool:
    """ 
        Execute player action and returns new position

        :param arg1: The action
        :type arg1: string

        :return: If this is the end of the game
        :rtype: boolean
    """

    # Use global variables
    global PlayerX, PlayerY

    # Variables for new player coordinates
    PlayerNewX: int = PlayerX
    PlayerNewY: int = PlayerY

    # Calculate player new coordinates
    if (PlayerAction == "MoveUp"):
        PlayerNewY -= 1
    elif (PlayerAction == "MoveDown"):
        PlayerNewY += 1
    elif (PlayerAction == "MoveLeft"):
        PlayerNewX -= 1
    elif (PlayerAction == "MoveRight"):
        PlayerNewX += 1
    elif (PlayerAction == "QuitGame"):
        # If action is QuitGame then return game end
        return True


    # Check if new coordinates are valid (into maze limits)
    if (PlayerNewX<0 or 
        PlayerNewX>len(Maze[0]) or 
        PlayerNewY<0 or 
        PlayerNewY>len(Maze)):
        # if player is out of maze limits
        print("Tu es en dehors des limites, tu ne peux pas aller par là !")
        # redraw maze
        DrawMazeOnScreen()
        return False

    # Get current maze element at new player coordinates
    CurrentElement = GetMazeElement(Image=Maze[PlayerNewY][PlayerNewX])

    # Check current element behavior or name
    if (CurrentElement["Name"] == "Sortie"):
        # If exit is reached
        # check if player has all needed objects
        MissingObjects: int = 0
        # for each element in maze
        for Element in MazeElements:
            if ("Combine" in Element["Behavior"]
                and not Element["Name"] in PlayerBackpack):
                # this element can be combined but is not in player backpack
                MissingObjects += 1
        if (MissingObjects == 0):
            # player has all objects
            # replace player in maze
            PlacePlayerInMaze(PlayerNewX,PlayerNewY)
            # assign new coordinates to player
            PlayerX = PlayerNewX
            PlayerY = PlayerNewY
            # redraw maze with new player position
            DrawMazeOnScreen()
            # say victory
            print(
                "\nOuiiii, bravo {0}, tu as trouvé la sortie et tu avais tous les objets nécessaires !\n"
                .format(PlayerName))
            # and return game end
            return True
        else:
            # some objects are missing
            # say how many
            print(
                "\nHa, tu as bien trouvé la sortie mais il te manque encore {0} objet(s) pour ouvrir la porte..."
                .format(MissingObjects))
    
    elif ("Block" in CurrentElement["Behavior"]):
        # If there is an obstacle, say it
        print("Oups un mur, tu ne peux pas bouger !")
        # and redraw maze
        DrawMazeOnScreen()
    
    elif ("Pick" in CurrentElement["Behavior"]):
        # If there is an object, put it in backpack
        PlayerBackpack.append(CurrentElement["Name"])
        # say it
        print(
            "Chouette, tu as trouvé un(e) {0}\n"
            .format(CurrentElement["Name"]))
        # remove it from maze (put floor at its place)
        Maze[PlayerNewY][PlayerNewX] = GetMazeElement("Sol")["Image"]
        # replace player in maze
        PlacePlayerInMaze(PlayerNewX,PlayerNewY)
        # assign new coordinates to player
        PlayerX = PlayerNewX
        PlayerY = PlayerNewY
        # and redraw maze with new player position
        DrawMazeOnScreen()
        
    else:
        # If nothing special
        # replace player in maze
        PlacePlayerInMaze(PlayerNewX,PlayerNewY)
        # assign new coordinates to player
        PlayerX = PlayerNewX
        PlayerY = PlayerNewY
        # and redraw maze with new player position
        DrawMazeOnScreen()

    # Game is not yet ended    
    return False


# Application
# -----------

# 1) Show initial message and get player data

# Application start
ApplicationStart()

# Ask for player data
PlayerName = GetPlayerData()

# Say welcome
SayWelcome()


# 2) Initialize Maze

# Load maze elements from json file
LoadMazeElementsFromFile(MazeFileName)
# Load maze from text file
LoadMazeFromFile(MazeFileName)

# Put objects in random positions
PlaceMazeObjectsAtRandomPositions()

# Place player in maze
PlacePlayerInMaze()

# Draw maze on screen
DrawMazeOnScreen()

# Start game
StartGame()


# 3) Game loop

# Variable for end of game
EndOfGame: bool = False

# Do this until end of game is triggered
while not EndOfGame:

    # Wait for a player action
    PlayerAction: str = WaitForPlayerAction()

    # Do action
    EndOfGame = ExecutePlayerAction(PlayerAction)
