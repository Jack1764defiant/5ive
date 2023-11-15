from AI import AI
import Game as g
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import pygame as p
import time
from Game import Network
import threading

class Main:
    def __init__(self):
        self.isGameRunning = True
        #How many frames per second to tick
        self.MAXFPS = 20
        self.clicks = []
        #What screen to load and display
        self.currentScreen = "menu"
        #This is used to ignore the first game click
        self.isFirstGameClick = True
        #The instance of the game class
        self.game = None
        #The current timer value
        self.timerValue = 0
        #The maximum timer value
        self.maxTimerTime = 0
        #The difficulty of the AI if you are playing against it
        self.AIDifficulty = 1
        #The instance of the AI class
        self.AI = None
        #Which colour the player is
        self.colour = 1
        # Switch which player is going
        self.player1Turn = True
        #Whether the game is taking place online
        self.Online = False
        #An instance of the move class representing a suggested move
        self.hintMove = None
        self.useThreading = True
        self.isThreading = False
        self.nextHintStorage = [None]
        self.isHintThreading = False


    def GoToMenu(self):
        self.player1Turn = True
        self.colour = 1
        self.UI.colourButton.text = "Colour: yellow"
        self.currentScreen = "menu"
        self.isFirstGameClick = True
        self.hintMove = None
        self.isThreading = False

    def LoadInstructions(self):
        self.currentScreen = "instructions"
        self.isFirstGameClick = True

    def LoadGame(self):
        self.game = g.Game()
        self.game.player1Turn = self.player1Turn
        #Is player 1 human or a bot?
        self.hasPlayer1 = True
        # Is player 2 human or a bot?
        self.hasPlayer2 = True
        #Is the game over?
        self.gameOver = False
        self.timerValue = self.UI.timeSlider.getValue()
        self.currentScreen = "game"
        self.clicks = []
        self.isFirstGameClick = True

    def LoadAIGame(self):
        self.game = g.Game()
        self.game.player1Turn = self.player1Turn
        # Is player 1 human or a bot?
        if self.colour == 1:
            self.hasPlayer1 = True
        else:
            self.hasPlayer1 = False
        # Is player 2 human or a bot?
        if self.colour == 2:
            self.hasPlayer2 = True
        else:
            self.hasPlayer2 = False
        # Is the game over?
        self.gameOver = False
        self.timerValue = self.UI.timeSlider.getValue()
        self.AIDifficulty = self.UI.difficultySlider.getValue()
        self.currentScreen = "game"
        self.clicks = []
        self.AI = AI(self.AIDifficulty)
        self.isFirstGameClick = True
        self.nextMoveStorage = [None]


    #Switch whether threading is used or not
    def switchThreading(self):
        self.useThreading = not self.useThreading
        if self.useThreading:
            self.UI.threadButton.text = "Threaded: True"
        else:
            self.UI.threadButton.text = "Threaded: False"

    #Gets a suggests a move
    def GetHint(self):
        #Check it is a player's go
        if (self.game.player1Turn and self.hasPlayer1) or ((not self.game.player1Turn) and self.hasPlayer2):
            #If the AI does not exist, initialise it.
            if self.AI is None:
                self.AI = AI(2)
            #Get a hint move
            if (self.useThreading):
                # If a second AI thread has not already been created
                if (not self.isHintThreading):
                    self.isHintThreading = True
                    # Create a list that can be used to store the best move, since threaded functions cannot return values
                    self.nextHintStorage = [None]
                    # Create a thread of the function findBestAIMove(), passing in parameters self.game and self.nextMoveStorage
                    self.hintThread = threading.Thread(target=self.AI.findBestAIMove,
                                                         args=(self.game, self.nextHintStorage))
                    # Start the thread
                    self.hintThread.start()
            else:
                self.hintMove = self.AI.findBestAIMove(self.game)

    def LoadOnlineGame(self):
        #THe instance of the game class
        self.game = g.Game()
        # initialise who's going first in the game
        self.game.player1Turn = self.player1Turn
        # Is player 1 human or a bot?
        self.hasPlayer1 = True
        # Is player 2 human or a bot?
        self.hasPlayer2 = True
        # Is the game over?
        self.gameOver = False
        #The maximum value the timer counts down from
        self.timerValue = self.UI.timeSlider.getValue()
        self.currentScreen = "game"
        self.clicks = []
        self.isFirstGameClick = True
        self.Online = True
        self.n = Network()
        self.isPlayer1 = str(self.n.player) == "0"
        self.myColour = "y" if str(self.n.player) == "0" else "r"
        self.updateServer = False
        self.messageToServer = None

    #Switch which colour goes first (and if in AI mode which colour the player is)
    def SwitchColours(self):
        #Switch which player goes first
        self.player1Turn = not self.player1Turn
        #Switch the number representing which colour the player is (1 = yellow, 2 = red)
        if self.colour == 1:
            self.colour = 2
            self.UI.colourButton.text = "Colour: red"
        else:
            self.colour = 1
            self.UI.colourButton.text = "Colour: yellow"

    #This is the main function that controls everything else. A while loop runs continuously in it to update the game
    def Run(self):
        p.init()
        self.UI = UI(self)
        clock = p.time.Clock()
        #This is the time the last frame ran at
        self.timeLastFrame = time.time()
        #This is the time since the last frame
        self.deltaTime = 0
        while self.isGameRunning:
            # if we are playing online, run the special update loop for an online game
            if self.Online:
                self.OnlineGame()
            else:
                #Calculate the time since the last frame
                self.deltaTime = time.time() - self.timeLastFrame
                #update the time the last frame ran at to be this frame
                self.timeLastFrame = time.time()
                #The timer should only update when a game is being played
                if self.currentScreen == "game" and ((self.hasPlayer1 and self.game.player1Turn) or (self.hasPlayer2 and not self.game.player1Turn)):
                    #set the timer value to the correct time
                    self.timerValue -= self.deltaTime
                    #If the timer has run out...
                    if self.timerValue <= 0:
                        #reset the timer
                        self.timerValue = self.maxTimerTime
                        #Switch which player is going
                        self.game.player1Turn = not self.game.player1Turn

            clock.tick(self.MAXFPS)
            #Handle inputs
            self.handleInputEvents()

            #Draw the appropriate screen
            if self.currentScreen =="instructions":
                self.UI.drawInstructionScreen()
            elif self.currentScreen == "game":
                self.UI.drawGameScreen(self.game)

                #Make the AI's turn if the AI is playing
                if (self.game.player1Turn and (not self.hasPlayer1)) or (
                        (not self.game.player1Turn) and (not self.hasPlayer2)):
                    # Reset the timer
                    self.deltaTime = 0
                    self.timeLastFrame = time.time()
                    self.timerValue = self.maxTimerTime
                    #If the AI decision making is carried out in a separate thread
                    if (self.useThreading):
                        #If a second AI thread has not already been created
                        if (not self.isThreading):
                            self.isThreading = True
                            p.display.update()
                            #Create a list that can be used to store the best move, since threaded functions cannot return values
                            self.nextMoveStorage = [None]
                            #Create a thread of the function findBestAIMove(), passing in parameters self.game and self.nextMoveStorage
                            self.AIMoveThread = threading.Thread(target=self.AI.findBestAIMove, args=(self.game,self.nextMoveStorage))
                            #Start the thread
                            self.AIMoveThread.start()
                        #print(self.nextMoveStorage[0])
                        # If the AI thread has generated a move
                        if (self.nextMoveStorage[0] != None and self.isThreading):
                            # Make the move
                            self.game.MakeMove(self.nextMoveStorage[0])
                            # Check if the AI has won
                            if self.game.CheckForWin():
                                if __name__ == '__main__':
                                    self.currentScreen = "lose"
                            self.isThreading = False


                    else:
                        p.display.update()
                        #If we are not threading, run the AI decision making process in the current thread.
                        self.game.MakeMove(self.AI.findBestAIMove(self.game))
                        # Check if the AI has won
                        if self.game.CheckForWin():
                            if __name__ == '__main__':
                                self.currentScreen = "lose"

            elif self.currentScreen == "menu":
                self.UI.drawIntroScreen()
            elif self.currentScreen == "win":
                self.UI.drawWinScreen(self.game)
            elif self.currentScreen == "lose":
                self.UI.drawLoseScreen(self.game)

            #update the display
            if (self.isThreading):
                self.deltaTime = 0
                self.timeLastFrame = time.time()
                self.timerValue = self.maxTimerTime
                p.display.update(p.Rect(370, 10, 240, 420))

                
            else:
                p.display.update()

    #Convert a coordinate into a string for sending to the server
    def CoordToString(self, coord):
        return str(coord[0]) + "," + str(coord[1])



    #Recieves data from and transmits data to the server to keep everything updated
    def OnlineGame(self):
        try:
            # If a move has been made, send it to the server
            if self.updateServer:
                self.updateServer = False
                tempGame = self.n.send(self.messageToServer)
            else:
                #Otherwise, get the current state of the game from the server in case the opponent made a move
                tempGame = self.n.send("get")
            if tempGame is not None:
                self.game = tempGame
        except:
            pass
        #Check if somebody won (this is normally updated when you make a move, but as moves are not made from your computer this has to be updated separately
        if self.game.CheckForWin() and self.currentScreen == "game":
                #Check if you are the colour that won
                if self.game.pegBoard[self.game.winCoords[0][0]][self.game.winCoords[0][1]][0] == self.myColour:
                    self.currentScreen = "win"
                else:
                    self.currentScreen = "lose"

    #Handle all inputs - mouse clicks, key presses etc
    def handleInputEvents(self):
        #Get all inputs/events
        events = p.event.get()
        #Update the widgets (I'm only using sliders) with the events
        pygame_widgets.update(events)
        #Get the position of the mouse on the screen
        pos = p.mouse.get_pos()
        #Loop through the buttons and check if the mouse is hovering over them
        for btn in self.UI.currentButtonsToUpdate:
            if btn.IsCoordInside(pos):
                btn.OnHover()
        #Loop through every input event
        for e in events:
            # Exit when they try to quit
            if e.type == p.QUIT:
                self.isGameRunning = False
                p.quit()
                # When the mouse is clicked
            elif e.type == p.MOUSEBUTTONDOWN:
                #Get mouse position
                pos = p.mouse.get_pos()
                #Check if the click is on a button
                for btn in self.UI.currentButtonsToUpdate:
                    if btn.IsCoordInside(pos):
                        btn.OnClick()
                #Update the timer value with the current input from the slider
                self.maxTimerTime = self.UI.timeSlider.getValue()
                #Update the AI difficulty value with the current input from the slider
                self.AIDifficulty = self.UI.difficultySlider.getValue()
                #Check if a game is running and try to move pieces
                if not self.isFirstGameClick and self.currentScreen == "game" and not self.gameOver and ((self.game.player1Turn and self.hasPlayer1) or (self.hasPlayer2 and not self.game.player1Turn)):
                    if not self.Online or (self.game.player1Turn == self.isPlayer1):
                        location = p.mouse.get_pos()
                        if len(self.clicks) == 0:
                            # Get the vertical mouse location and convert it to a slot position
                            row = (location[1] / self.UI.SLOTSIZE)
                            tempCol = ((location[0] + (self.UI.SLOTSIZE // 2)) / self.UI.SLOTSIZE) - 1
                            col = location[0] / self.UI.SLOTSIZE - 1
                            if row >= 11.5 or col >= 7.5 or tempCol >= 8.5:
                                self.clicks = []
                                continue
                            # if it is in player 1's storage
                            if self.game.player1Turn and row < 2.5:
                                # Compensate for the slots in storage being centered differently
                                col = ((location[0] + (self.UI.SLOTSIZE // 2)) // self.UI.SLOTSIZE) - 1
                                row = (location[1] // self.UI.SLOTSIZE)
                                self.clicks.append((row, col))
                                if row == 0:
                                    self.clicks.append(self.game.player1PegStorage)
                                else:
                                    self.clicks.append(self.game.player1CylinderStorage)
                                # if it is in player 2's storage
                            elif (not self.game.player1Turn) and 9 <= row < 11:
                                # Compensate for the slots in storage being centered differently
                                col = ((location[0] + (self.UI.SLOTSIZE // 2)) // self.UI.SLOTSIZE) - 1
                                row = (location[1] // self.UI.SLOTSIZE)
                                self.clicks.append((row, col))
                                if row == 10:
                                    self.clicks.append(self.game.player2PegStorage)
                                else:
                                    self.clicks.append(self.game.player2CylinderStorage)
                            elif 9 > row > 1:
                                 # The click is on the main board
                                 col = location[0] // self.UI.SLOTSIZE - 1
                                 row = (location[1] // self.UI.SLOTSIZE)-2
                                 self.clicks.append((row, col))
                                 if (self.game.pegBoard[row][col] == "yp" and self.game.player1Turn) or (self.game.pegBoard[row][col] == "rp" and not self.game.player1Turn):
                                    self.clicks.append(self.game.pegBoard)
                                 else:
                                    self.clicks.append(self.game.cylinderBoard)
                        elif len(self.clicks) >= 2:
                            #Check that the click is within the board. If it is not, deselect any pieces and skip trying to make a move.
                            row = (location[1] / self.UI.SLOTSIZE)
                            tempCol = ((location[0] + (self.UI.SLOTSIZE // 2)) / self.UI.SLOTSIZE) - 1
                            col = location[0] / self.UI.SLOTSIZE - 1
                            if row >= 11.5 or col >= 7 or tempCol >= 8 or row <= 2:
                                self.clicks = []
                                continue
                            # Get the vertical mouse location and convert it to a slot position
                            row = (location[1] // self.UI.SLOTSIZE)
                            #Check if the click is on the already selected piece to deselect
                            if row < 2:
                                # Compensate for the slots in storage being centered differently
                                col = ((location[0] + (self.UI.SLOTSIZE // 2)) // self.UI.SLOTSIZE) - 1
                                row = (location[1] // self.UI.SLOTSIZE)
                                if self.clicks[0] == (row, col):
                                    #clear the selected piece
                                    self.clicks = []
                                    #skip to the next event
                                    continue

                            elif 8 < row < 11:
                                # Compensate for the slots in storage being centered differently
                                col = ((location[0] + (self.UI.SLOTSIZE // 2)) // self.UI.SLOTSIZE) - 1
                                row = (location[1] // self.UI.SLOTSIZE)
                                if self.clicks[0] == (row, col):
                                    # clear the selected piece
                                    self.clicks = []
                                    # skip to the next event
                                    continue

                            #If we have reached this point, we are not deselecting, so make a move.
                            if 8 >= row >= 0:
                                # The click is on the main board
                                col = (location[0] - self.UI.SLOTSIZE) // self.UI.SLOTSIZE
                                row = (location[1] // self.UI.SLOTSIZE) - 2
                                # if we are playing online, convert the array the piece is being moved from to a string encoding so it can be sent as a message to the server
                                if self.Online:
                                    startArrayAsString = "pb"
                                    if self.clicks[1] == self.game.pegBoard:
                                        startArrayAsString = "pb"
                                    elif self.clicks[1] == self.game.cylinderBoard:
                                        startArrayAsString = "cb"
                                    elif self.clicks[1] == self.game.player1PegStorage:
                                        startArrayAsString = "1p"
                                    elif self.clicks[1] == self.game.player2PegStorage:
                                        startArrayAsString = "2p"
                                    elif self.clicks[1] == self.game.player1CylinderStorage:
                                        startArrayAsString = "1c"
                                    elif self.clicks[1] == self.game.player2CylinderStorage:
                                        startArrayAsString = "2c"

                                if self.game.MakeMove(g.Move(self.clicks[1], self.clicks[0], (row, col))):
                                    # Reset any hints once a move is made
                                    self.hintMove = None
                                    #Send the move to the server if online
                                    if self.Online:
                                        self.messageToServer = self.CoordToString(self.clicks[0]) + "," + self.CoordToString((row, col)) + "," + startArrayAsString
                                        self.updateServer = True

                                    #Reset the timer for the next player's turn
                                    self.timerValue = self.maxTimerTime
                                    if self.game.CheckForWin():
                                        if __name__ == '__main__':
                                            self.currentScreen = "win"
                                self.clicks = []
                #Ignore the first game click, as clicking on a button to load the game actually also carries over as a click in-game
                elif self.isFirstGameClick and self.currentScreen == "game":
                    self.clicks = []
                    self.isFirstGameClick = False
            elif e.type == p.KEYDOWN and not self.Online:
                # Undo a move when z is pressed (does not work online or against the AI)
                if e.key == p.K_z and (not self.Online) and self.hasPlayer1 and self.hasPlayer2:
                    #Reset the timer
                    self.timerValue = self.maxTimerTime
                    #Undo the move
                    self.game.UndoMove()



#Handles drawing the UI
class UI:
    def __init__(self, main):
        self.main = main
        #The sizes of the board and pieces
        self.BOARDWIDTH = 620
        self.BOARDHEIGHT = 440
        self.SLOTSIZE = 40
        self.PEGSIZE = 20
        self.amountOfSlots = 7
        #Initialise the game window
        self.screen = p.display.set_mode((self.BOARDWIDTH, self.BOARDHEIGHT))
        #A list buttons that need to be checked for input in the game loop
        self.currentButtonsToUpdate = []
        #Initialise buttons and sliders
        self.InitButtons()
        self.InitSliders()

    #Generate all needed buttons so they can be drawn later
    def InitButtons(self):
        #List of all buttons that need to be checked for input on the menu screen
        self.menuButtons = []
        # List of all buttons that need to be checked for input on the instructions screen
        self.instructionsButtons = []
        # List of all buttons that need to be checked for input on the game screen
        self.gameButtons = []
        # List of all buttons that need to be checked for input on the win and lose screens
        self.winOrLoseButtons = []
        # Create the buttons and append them to the appropriate list
        self.exitButton = Button("Quit", 380, 350, p.Color("Blue"), self.screen, "Return to the main menu",self.main.GoToMenu, height=70, width=220, windowHeight=25)
        self.gameButtons.append(self.exitButton)
        self.colourButton = Button("Colour: yellow", self.BOARDWIDTH / 2 - 75, 325, p.Color("Blue"), self.screen,
                                   "Switch colours.", self.main.SwitchColours, height=75, windowHeight=25)
        self.menuButtons.append(self.colourButton)
        self.threadButton = Button("Threaded: True", self.BOARDWIDTH - 160, 325, p.Color("Blue"), self.screen,"Run the AI in a separate thread", self.main.switchThreading, height=75, windowHeight=25)
        self.menuButtons.append(self.threadButton)
        self.instructionsButton = Button("Instructions", 10, 300, p.Color("Blue"), self.screen,
                                         "See instructions on how to play.", self.main.LoadInstructions, windowHeight=50)
        self.menuButtons.append(self.instructionsButton)
        self.twoPlayerButton = Button("Local 2 Player", 10, 100, p.Color("Blue"), self.screen,
                                      "Play against another person on the same computer.", self.main.LoadGame, windowHeight=75)
        self.menuButtons.append(self.twoPlayerButton)
        self.onlineButton = Button("Play online", self.BOARDWIDTH - 160, 100, p.Color("Blue"), self.screen,
                                   "Play against another person over the internet.", self.main.LoadOnlineGame, windowHeight=75)
        self.menuButtons.append(self.onlineButton)
        self.AIButton = Button("Play against AI", 235, 100, p.Color("Blue"), self.screen,
                               "Play a game against the computer.", self.main.LoadAIGame, windowHeight=50)
        self.menuButtons.append(self.AIButton)

        self.quitButton = Button("Quit", 380, 350, p.Color("Blue"), self.screen, "Return to the main menu",
                                 self.main.GoToMenu, height=70, width=220, windowHeight=25)
        self.winOrLoseButtons.append(self.quitButton)
        self.backButton = Button("Back", 388, 350, p.Color("Blue"), self.screen, "Return to the main menu",
                                 self.main.GoToMenu, height=60, width=220, windowHeight=25)
        self.instructionsButtons.append(self.backButton)

        self.hintButton = Button("Hint", 380, 280, p.Color("Blue"), self.screen, "Have the computer suggest a move",
                                 self.main.GetHint, height=60, width=220)
        self.gameButtons.append(self.hintButton)

    #Generate all needed sliders so they can be drawn later
    def InitSliders(self):
        #Create the slider
        self.difficultySlider = Slider(self.screen, self.BOARDWIDTH // 2 - 75, 270, 150, 20, min=1, max=3, step=1, colour=p.Color("white"))

        # Create the slider
        self.timeSlider = Slider(self.screen, self.BOARDWIDTH - 175, 270, 150, 20, min=10, max=120, step=1, colour=p.Color("white"))
        # Create the output box for the slider
        self.timeOutput = TextBox(self.screen, self.BOARDWIDTH - 60, 225, 50, 40, fontSize=30)
        self.timeOutput.disable()

    #Draws the game screen - the board and pieces
    def drawGameScreen(self, game):
        #Fill the background
        self.screen.fill(p.Color("white"))
        #Draw the board
        self.drawBoard()
        #Draw the hint
        self.drawHint()
        #Draw the pieces on the board
        self.drawPieces(game)
        #Draw the panel next to the board
        self.drawPanel()
        #Make sure that the buttons detecting clicks are the right buttons
        self.currentButtonsToUpdate = self.gameButtons


    #Draws the panel containing the back button and a list of possible patterns
    def drawPanel(self):
        #Draw the panel
        p.draw.rect(self.screen, p.Color("gray"), p.Rect(370, 10, 240, 420))
        #Draw the title of the panel
        font = p.font.SysFont("arial", 50)
        text = font.render("Patterns:", 1, (255, 255, 255))
        self.screen.blit(text, (440, 25))

        #Draw the timer
        p.draw.rect(self.screen, p.Color("black"), p.Rect(375, 20, 60, 70))
        font = p.font.SysFont("arial", 20)
        text = font.render("Timer", 1, (255, 255, 255))
        self.screen.blit(text, (383, 20))
        #Draw the timer value
        font = p.font.SysFont("arial", 45)
        text = font.render(str(int(self.main.timerValue)), 1, (255, 0, 0))
        self.screen.blit(text, (405 - round(text.get_width() / 2), 37))

        #Draw the patterns
        #Pattern 1
        #Draw the background
        p.draw.rect(self.screen, p.Color("white"), p.Rect(380, 110, 220, 40))
        #Draw the pattern
        p.draw.circle(self.screen, p.Color("grey"), (410, 130), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (410, 130), self.PEGSIZE / 2)

        p.draw.circle(self.screen, p.Color("red"), (450, 130), self.SLOTSIZE / 2)

        p.draw.circle(self.screen, p.Color("grey"), (490, 130), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (490, 130), self.PEGSIZE / 2)

        p.draw.circle(self.screen, p.Color("red"), (530, 130), self.SLOTSIZE / 2)

        p.draw.circle(self.screen, p.Color("grey"), (570, 130), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (570, 130), self.PEGSIZE / 2)

        # Pattern 2
        # Draw the background
        p.draw.rect(self.screen, p.Color("white"), p.Rect(380, 170, 220, 40))
        # Draw the pattern
        p.draw.circle(self.screen, p.Color("grey"), (410, 190), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (410, 190), self.PEGSIZE / 2)

        p.draw.circle(self.screen, p.Color("red"), (450, 190), self.SLOTSIZE / 2)

        p.draw.circle(self.screen, p.Color("red"), (490, 190), self.SLOTSIZE / 2)

        p.draw.circle(self.screen, p.Color("red"), (530, 190), self.SLOTSIZE / 2)

        p.draw.circle(self.screen, p.Color("grey"), (570, 190), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (570, 190), self.PEGSIZE / 2)

        # Pattern 3
        # Draw the background
        p.draw.rect(self.screen, p.Color("white"), p.Rect(380, 230, 220, 40))
        # Draw the pattern
        p.draw.circle(self.screen, p.Color("grey"), (410, 250), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (410, 250), self.PEGSIZE / 2)

        p.draw.circle(self.screen, p.Color("grey"), (450, 250), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (450, 250), self.PEGSIZE / 2)

        p.draw.circle(self.screen, p.Color("red"), (490, 250), self.SLOTSIZE / 2)

        p.draw.circle(self.screen, p.Color("grey"), (530, 250), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (530, 250), self.PEGSIZE / 2)

        p.draw.circle(self.screen, p.Color("grey"), (570, 250), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (570, 250), self.PEGSIZE / 2)


        #Generate and draw the button
        self.hintButton.draw()
        self.exitButton.draw()

    #Draws the board on the screen
    def drawBoard(self):
        color = p.Color("gray")
        #Highlight the last clicked location blue
        if len(main.clicks) >= 2:
            pos = main.clicks[0]
        else:
            pos = (999,999)
        # Player 1's storage
        for r in range(2):
            for c in range(8):
                if pos[0] == r and pos[1] == c and (main.clicks[1] == main.game.player1PegStorage or main.clicks[1] == main.game.player1CylinderStorage):
                    p.draw.circle(self.screen, p.Color("blue"), ((c * self.SLOTSIZE) + self.SLOTSIZE, (r * self.SLOTSIZE) + self.SLOTSIZE / 2), self.SLOTSIZE / 2 + 2)
                else:
                    p.draw.circle(self.screen, color,((c * self.SLOTSIZE) + self.SLOTSIZE, (r * self.SLOTSIZE) + self.SLOTSIZE / 2),self.SLOTSIZE / 2)
        # The main board
        for r in range(self.amountOfSlots):
            for c in range(self.amountOfSlots):
                if pos[0] == r and pos[1] == c and (main.clicks[1] == main.game.pegBoard or main.clicks[1] == main.game.cylinderBoard):
                    p.draw.circle(self.screen, p.Color("blue"), ((c * self.SLOTSIZE) + (self.SLOTSIZE * 1.5),(r * self.SLOTSIZE) + self.SLOTSIZE / 2 + (2 * self.SLOTSIZE)),self.SLOTSIZE / 2 + 2)
                else:
                    p.draw.circle(self.screen, color, ((c * self.SLOTSIZE) + (self.SLOTSIZE*1.5), (r * self.SLOTSIZE) + self.SLOTSIZE / 2 + (2 * self.SLOTSIZE)),self.SLOTSIZE / 2)
        # Player 2's storage
        for r in range(2):
            for c in range(8):
                if pos[0] == r+9 and pos[1] == c and (main.clicks[1] == main.game.player2PegStorage or main.clicks[1] == main.game.player2CylinderStorage):
                    p.draw.circle(self.screen, p.Color("blue"), ((c * self.SLOTSIZE) + self.SLOTSIZE, (r * self.SLOTSIZE) + self.SLOTSIZE / 2 + self.SLOTSIZE * 9),self.SLOTSIZE / 2 + 2)
                else:
                    p.draw.circle(self.screen, color, ((c * self.SLOTSIZE) + self.SLOTSIZE, (r * self.SLOTSIZE) + self.SLOTSIZE / 2 + self.SLOTSIZE * 9),self.SLOTSIZE / 2)
        # Draw the lines separating storage the main board
        p.draw.rect(self.screen, p.Color("black"), p.Rect(0, self.SLOTSIZE * 2, 360, 1))
        p.draw.rect(self.screen, p.Color("black"), p.Rect(0, self.SLOTSIZE * 9, 360, 1))



    #Draws the pieces to the screen
    def drawPieces(self, game):
        # Draw yellow's storage
        for r in range(2):
            for c in range(8):
                # Draw cylinders
                if r == 1:
                    # Draw full cylinders
                    if game.player1CylinderStorage[c][1] == "c":
                        p.draw.circle(self.screen, p.Color("yellow"),((c * self.SLOTSIZE) + self.SLOTSIZE, (r * self.SLOTSIZE) + self.SLOTSIZE / 2),self.SLOTSIZE / 2)
                    # Draw hollow cylinders
                    elif game.player1CylinderStorage[c][1] == "h":
                        p.draw.circle(self.screen, p.Color("yellow"),((c * self.SLOTSIZE) + self.SLOTSIZE, (r * self.SLOTSIZE) + self.SLOTSIZE / 2),self.SLOTSIZE / 2)
                        p.draw.circle(self.screen, p.Color("grey"),((c * self.SLOTSIZE) + self.SLOTSIZE, (r * self.SLOTSIZE) + self.SLOTSIZE / 2),self.PEGSIZE / 2)
                # Draw pegs
                elif r == 0:
                    if game.player1PegStorage[c] != "--":
                        p.draw.circle(self.screen, p.Color("yellow"),((c * self.SLOTSIZE) + self.SLOTSIZE, (r * self.SLOTSIZE) + self.SLOTSIZE / 2),self.PEGSIZE / 2)
        # Draw main board
        for r in range(self.amountOfSlots):
            for c in range(self.amountOfSlots):
                #Draw red cylinders
                # Draw full cylinder
                if game.cylinderBoard[r][c] == "rc":
                    p.draw.circle(self.screen, p.Color("red"), ((c * self.SLOTSIZE) + self.SLOTSIZE*1.5, (r * self.SLOTSIZE) + 5 * self.SLOTSIZE / 2),self.SLOTSIZE / 2)
                # Draw hollow cylinder
                elif game.cylinderBoard[r][c] == "rh":
                    p.draw.circle(self.screen, p.Color("red"), ((c * self.SLOTSIZE) + self.SLOTSIZE*1.5, (r * self.SLOTSIZE) + 5 * self.SLOTSIZE / 2),self.SLOTSIZE / 2)
                    p.draw.circle(self.screen, p.Color("grey"), ((c * self.SLOTSIZE) + self.SLOTSIZE*1.5, (r * self.SLOTSIZE) + 5 * self.SLOTSIZE / 2),self.PEGSIZE / 2)
                #Draw yellow cylinders
                # Draw full cylinder
                if game.cylinderBoard[r][c] == "yc":
                    p.draw.circle(self.screen, p.Color("yellow"), ((c * self.SLOTSIZE) + self.SLOTSIZE*1.5, (r * self.SLOTSIZE) + 5 * self.SLOTSIZE / 2), self.SLOTSIZE / 2)
                # Draw hollow cylinder
                elif game.cylinderBoard[r][c] == "yh":
                    p.draw.circle(self.screen, p.Color("yellow"), ((c * self.SLOTSIZE) + self.SLOTSIZE*1.5, (r * self.SLOTSIZE) + 5 * self.SLOTSIZE / 2),self.SLOTSIZE / 2)
                    p.draw.circle(self.screen, p.Color("grey"), ((c * self.SLOTSIZE) + self.SLOTSIZE*1.5, (r * self.SLOTSIZE) + 5 * self.SLOTSIZE / 2),self.PEGSIZE / 2)
                # Draw pegs
                #red
                if game.pegBoard[r][c] == "rp":
                    p.draw.circle(self.screen, p.Color("red"),((c * self.SLOTSIZE) + self.SLOTSIZE * 1.5, (r * self.SLOTSIZE) + 5 * self.SLOTSIZE / 2),self.PEGSIZE / 2)
                #yellow
                if game.pegBoard[r][c] == "yp":
                    p.draw.circle(self.screen, p.Color("yellow"), ((c * self.SLOTSIZE) + self.SLOTSIZE*1.5, (r * self.SLOTSIZE) + 5 * (self.SLOTSIZE / 2)),self.PEGSIZE / 2)

        # draw red's storage
        for r in range(2):
            for c in range(8):
                # Draw pegs
                if r == 0:
                    if game.player2PegStorage[c] != "--":
                        p.draw.circle(self.screen, p.Color("red"), ((c * self.SLOTSIZE) + self.SLOTSIZE,(r * self.SLOTSIZE) + self.SLOTSIZE / 2 + (self.SLOTSIZE * 10)), self.PEGSIZE / 2)
                # Draw cylinders
                elif r == 1:
                    # Draw full cylinders
                    if game.player2CylinderStorage[c][1] == "c":
                        p.draw.circle(self.screen, p.Color("red"), ((c * self.SLOTSIZE) + self.SLOTSIZE,(r * self.SLOTSIZE) + self.SLOTSIZE / 2 + (self.SLOTSIZE * 8)), self.SLOTSIZE / 2)
                    # Draw hollow cylinders
                    elif game.player2CylinderStorage[c][1] == "h":
                        p.draw.circle(self.screen, p.Color("red"), ((c * self.SLOTSIZE) + self.SLOTSIZE,(r * self.SLOTSIZE) + self.SLOTSIZE / 2 + (self.SLOTSIZE * 8)), self.SLOTSIZE / 2)
                        p.draw.circle(self.screen, p.Color("grey"), ((c * self.SLOTSIZE) + self.SLOTSIZE,(r * self.SLOTSIZE) + self.SLOTSIZE / 2 + (self.SLOTSIZE * 8)), self.PEGSIZE / 2)

    #Puts a green outline on the suggested position of a move
    def drawHint(self):
        if (self.main.nextHintStorage[0] != None and self.main.useThreading):
            self.main.hintMove = self.main.nextHintStorage[0]
            self.main.nextHintStorage = [None]
            self.main.isHintThreading = False
        if self.main.hintMove != None:
            if self.main.hintMove.pieceToMove[1] == "p":
                p.draw.circle(self.screen, p.Color("green"), (
                    (self.main.hintMove.endCol * self.SLOTSIZE) + self.SLOTSIZE * 1.5, (self.main.hintMove.endRow * self.SLOTSIZE) + 5 * self.SLOTSIZE / 2), (self.PEGSIZE / 2)*1.1)
            else:
                p.draw.circle(self.screen, p.Color("green"), (
                    (self.main.hintMove.endCol * self.SLOTSIZE) + self.SLOTSIZE * 1.5,
                    (self.main.hintMove.endRow * self.SLOTSIZE) + 5 * self.SLOTSIZE / 2), (self.SLOTSIZE / 2) * 1.1)
                if self.main.hintMove.pieceToMove[1] == "h":
                    p.draw.circle(self.screen, p.Color("grey"), (
                        (self.main.hintMove.endCol * self.SLOTSIZE) + self.SLOTSIZE * 1.5,
                        (self.main.hintMove.endRow * self.SLOTSIZE) + 5 * self.SLOTSIZE / 2), (self.PEGSIZE / 2) * 1.1)

    #Put a black outline on the winning pattern
    def drawWinCoords(self, game):
        for coord in game.winCoords:
            p.draw.circle(self.screen, p.Color("black"), (
                (coord[1] * self.SLOTSIZE) + self.SLOTSIZE * 1.5, (coord[0] * self.SLOTSIZE) + 5 * self.SLOTSIZE / 2), (self.SLOTSIZE / 2)*1.1)

    #Draws the intro screen - the title and buttons
    def drawIntroScreen(self):
        self.screen.fill(p.Color("grey"))
        # Draw the title of the screen
        font = p.font.SysFont("arial", 50)
        text = font.render("5ive", 1, (255, 255, 255))
        self.screen.blit(text, ((self.screen.get_width()/2) - round(text.get_width() / 2), 10))

        #Draw the appropriate difficulty underneath the slider
        font = p.font.SysFont("arial", 25)
        if self.difficultySlider.getValue() == 1:
            text = font.render("Easy", 1, (255, 255, 255))
        elif self.difficultySlider.getValue() == 2:
            text = font.render("Medium", 1, (255, 255, 255))
        elif self.difficultySlider.getValue() == 3:
            text = font.render("Hard", 1, (255, 255, 255))
        self.screen.blit(text, ((self.BOARDWIDTH / 2) - round(text.get_width() / 2), 230))

        font = p.font.SysFont("arial", 25)
        text = font.render("Timer Duration:", 1, (255, 255, 255))
        self.screen.blit(text, ((self.BOARDWIDTH - 205), 230))


        # Set the slider labels to the sliders' values
        self.timeOutput.setText(self.timeSlider.getValue())
        self.currentButtonsToUpdate = self.menuButtons

        #Draw the sliders and labels
        self.difficultySlider.draw()

        self.timeSlider.draw()
        self.timeOutput.draw()

        # draw the buttons
        self.twoPlayerButton.draw()
        self.AIButton.draw()

        self.onlineButton.draw()

        self.instructionsButton.draw()
        #self.threadButton.draw()
        self.colourButton.draw()


    #Draws the "You Win" text to the screen
    def drawWinScreen(self, game):
        #Fill the background
        self.screen.fill(p.Color("white"))
        #Draw the board
        self.drawBoard()
        #As someone must have won, highlight the winning pattern
        if len(game.winCoords) > 0:
            self.drawWinCoords(game)
        #Draw the pieces
        self.drawPieces(game)
        # Draw the panel
        p.draw.rect(self.screen, p.Color("gray"), p.Rect(370, 10, 240, 420))
        # Draw the title of the panel
        font = p.font.SysFont("arial", 45)
        text = font.render("You Win!", 1, (255, 255, 255))
        self.screen.blit(text, (490 - round(text.get_width() / 2), 20))
        # Draw the subtext
        font = p.font.SysFont("arial", 30)
        text = font.render("Well done!", 1, (255, 255, 255))
        self.screen.blit(text, (490 - round(text.get_width() / 2), 80))

        # Generate and draw the button

        self.quitButton.draw()
        self.currentButtonsToUpdate = self.winOrLoseButtons

    #Draws the "You Lose" text to the screen
    def drawLoseScreen(self, game):
        #Fill the background
        self.screen.fill(p.Color("white"))
        #Draw the board
        self.drawBoard()
        #Since someone has lost, someone must have won, so highlight the winning pattern
        if len(game.winCoords) > 0:
            self.drawWinCoords(game)
        #Draw the pieces
        self.drawPieces(game)
        # Draw the panel
        p.draw.rect(self.screen, p.Color("gray"), p.Rect(370, 10, 240, 420))
        # Draw the title of the panel
        font = p.font.SysFont("arial", 45)
        text = font.render("You Lose...", 1, (255, 255, 255))
        self.screen.blit(text, (490 - round(text.get_width() / 2), 20))
        #Draw the subtext
        font = p.font.SysFont("arial", 30)
        text = font.render("Better luck next time...", 1, (255, 255, 255))
        self.screen.blit(text, (490 - round(text.get_width() / 2), 80))

        # Generate and draw the button

        self.quitButton.draw()
        self.currentButtonsToUpdate = self.winOrLoseButtons

    #Draws the help screen, with the instructions about how to play the game
    def drawInstructionScreen(self):
        #Fill the background
        self.screen.fill(p.Color("white"))
        #Draw the panel
        p.draw.rect(self.screen, p.Color("black"), p.Rect(5, 10, 365, 420))
        # Draw the title of the panel
        font = p.font.SysFont("arial", 35)
        text = font.render("Rules:", 1, (255, 255, 255))
        self.screen.blit(text, (180 - round(text.get_width() / 2), 7))
        #Draw the text
        font = p.font.SysFont("arial", 17)

        rules = """
Each player has two rows used to store their pieces (large cylinders, large cylinders that are hollow to allow a peg to be placed inside, and smaller pegs).
On each go, a player places any one of his pieces from his storage onto the board. You can place your pegs inside your opponent's cylinders, but not inside your own, or place your hollow cylinders around your opponent's pegs but not around your own.
Once you have placed all of your cylinders from storage you can move a cylinder of yours that is on the board; equally, once you have placed all your pegs you can then move one of your pegs on the board.
The objective is to make any one of 3 five in a row formations with pieces of your colour, vertically, horizontally or diagonally. 
Hollow and full cylinders are equivalent in formations, even if an opponent's peg is in the cylinder. Pegs still count as pegs, even if an opponent's cylinder is around them. 
        """

        self.drawTextOnMultipleLines((365,420), rules, (15,24), (255,255,255), font)



        # Draw the panel
        p.draw.rect(self.screen, p.Color("gray"), p.Rect(380, 10, 234, 420))
        # Draw the title of the panel
        font = p.font.SysFont("arial", 35)
        text = font.render("Patterns:", 1, (255, 255, 255))
        self.screen.blit(text, (498 - round(text.get_width() / 2), 30))

        # Draw the patterns
        # Pattern 1
        # Draw the background
        p.draw.rect(self.screen, p.Color("white"), p.Rect(388, 100, 220, 40))
        # Draw the pattern
        p.draw.circle(self.screen, p.Color("grey"), (418, 120), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (418, 120), self.PEGSIZE / 2)

        p.draw.circle(self.screen, p.Color("red"), (458, 120), self.SLOTSIZE / 2)

        p.draw.circle(self.screen, p.Color("grey"), (498, 120), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (498, 120), self.PEGSIZE / 2)

        p.draw.circle(self.screen, p.Color("red"), (538, 120), self.SLOTSIZE / 2)

        p.draw.circle(self.screen, p.Color("grey"), (578, 120), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (578, 120), self.PEGSIZE / 2)

        # Pattern 2
        # Draw the background
        p.draw.rect(self.screen, p.Color("white"), p.Rect(388, 180, 220, 40))
        # Draw the pattern
        p.draw.circle(self.screen, p.Color("grey"), (418, 200), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (418, 200), self.PEGSIZE / 2)

        p.draw.circle(self.screen, p.Color("red"), (458, 200), self.SLOTSIZE / 2)

        p.draw.circle(self.screen, p.Color("red"), (498, 200), self.SLOTSIZE / 2)

        p.draw.circle(self.screen, p.Color("red"), (538, 200), self.SLOTSIZE / 2)

        p.draw.circle(self.screen, p.Color("grey"), (578, 200), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (578, 200), self.PEGSIZE / 2)

        # Pattern 3
        # Draw the background
        p.draw.rect(self.screen, p.Color("white"), p.Rect(388, 260, 220, 40))
        # Draw the pattern
        p.draw.circle(self.screen, p.Color("grey"), (418, 280), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (418, 280), self.PEGSIZE / 2)

        p.draw.circle(self.screen, p.Color("grey"), (458, 280), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (458, 280), self.PEGSIZE / 2)

        p.draw.circle(self.screen, p.Color("red"), (498, 280), self.SLOTSIZE / 2)

        p.draw.circle(self.screen, p.Color("grey"), (538, 280), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (538, 280), self.PEGSIZE / 2)

        p.draw.circle(self.screen, p.Color("grey"), (578, 280), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (578, 280), self.PEGSIZE / 2)

        # Generate and draw the button
        self.backButton.draw()
        self.currentButtonsToUpdate = self.instructionsButtons

    def drawTextOnMultipleLines(self, size, text, position, color, font):
        # An array of lists of the words in each line.
        words = []
        for word in text.splitlines():
            words.append(word.split(" "))
        # The width of a space.
        space = font.size(" ")[0]
        width = size[0]
        x = position[0]
        y = position[1]
        #Loop through each line in the words
        for line in words:
            #Loop through each word in the line
            for word in line:
                wordRendered = font.render(word, 0, color)
                wordWidth = wordRendered.get_size()[0]
                wordHeight = wordRendered.get_size()[1]
                if x + wordWidth >= width:
                    # Reset the x.coordinate to the far left
                    x = position[0]
                    # Set the y coordinate to that of the next row
                    y += wordHeight
                self.screen.blit(wordRendered, (x, y))
                x += wordWidth + space
            # Reset the x coordinate to the far left
            x = position[0]
            # Set the y coordinate to that of the next row.
            y += wordHeight


#Represents a clickable, rectangular button with a text overlay
class Button:
    def __init__(self, text, x, y, color, win, explanationText, functionToRun, width = 150, height = 100, showWindowAbove=False, windowHeight=0):
        #The text displayed in the center of the button
        self.text = text
        #The coordinates of the button
        self.x = x
        self.y = y
        #The size of the button
        self.width = width
        self.height = height
        #The color of the button
        self.color = color
        #The text shown when the mouse hovers on the button
        self.explanationText = explanationText
        #Whether the text shown on hover is shown above or below the button
        self.showWindowAbove = showWindowAbove
        #The function called when the button is clicked
        self.functionToRun = functionToRun
        #The window the button is drawn on
        self.win = win
        #The time the hover text has been shown for (-1 means it isn't being shown)
        self.windowShownTime = -1
        if windowHeight == 0:
            self.windowHeight = self.height
        else:
            self.windowHeight = windowHeight


    #Draw the button to the screen
    def draw(self):
        #Drawing the button
        #draw a rectangle
        p.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))
        font = p.font.SysFont("comicsans", 20)
        #Draw the text on the rectangle, centered
        self.drawTextOnMultipleLines((self.width, self.height), self.text, (self.x,self.y),p.Color("white") , font)
        #Run checks to detect whether the hover window needs to be rendered
        if self.windowShownTime > 0 and time.time() < self.windowShownTime + 0.1:
            #Show the window
            self.ShowTextWindow()
        else:
            #The window will stop being shown
            self.windowShownTime = -1

    def IsCoordInside(self, pos):
        #Get each coord from the tuple
        x1 = pos[0]
        y1 = pos[1]
        #Is it inside the boundaries of the button?
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

    def ShowTextWindow(self, fromClick=False):
        #Draw the hover text window above or below the button
        if not self.showWindowAbove:
            #Draw the rectangular window
            p.draw.rect(self.win, p.Color("red"), (self.x, self.y-self.windowHeight, self.width, self.windowHeight))
            font = p.font.SysFont("comicsans", 16)
            # Draw the explanatory text
            self.drawTextOnMultipleLines((self.width, self.windowHeight), self.explanationText, (self.x,self.y-self.windowHeight),p.Color("white") , font, False)

        else:
            # Draw the rectangular window
            p.draw.rect(self.win, p.Color("red"), (self.x, self.y+self.height, self.width, self.windowHeight))
            font = p.font.SysFont("comicsans", 16)
            #Draw the explanatory text
            self.drawTextOnMultipleLines((self.width, self.windowHeight), self.explanationText, (self.x, self.y+self.height), p.Color("white") , font, False)
        #Update the window shown time to start the countdown
        if fromClick:
            self.windowShownTime = time.time()

    #Run when the button is clicked
    def OnClick(self):
        self.functionToRun()

    #Run when the mouse hovers over the button
    def OnHover(self):
        #Show the explanatory text window
        self.ShowTextWindow(True)

    #Pygame does not default support rendering text across multiple lines so I am using this function to do so.
    def drawTextOnMultipleLines(self, size, text, position, color, font, centerHeight=True):
        # An array of lists of the words in each line.
        words = []
        for word in text.splitlines():
            words.append(word.split(" "))
        # The width of a space.
        space = font.size(" ")[0]
        width = size[0]
        x = 0
        y = position[1]
        #Loop through each line
        for line in words:
            #Loop through each word in the line
            for word in line:
                wordRendered = font.render(word, 0, color)
                wordWidth = wordRendered.get_size()[0]
                wordHeight = wordRendered.get_size()[1]
                if x + wordWidth >= width:
                    # Reset the x.coordinate to the far left
                    x = 0
                    # Set the y coordinate to that of the next row
                    y += wordHeight
                #If I need to center the text as well as rendering it on multiple lines
                if centerHeight:
                    text_rect = wordRendered.get_rect(center=(self.x + (self.width / 2), self.y + (self.height/2) + (line.index(word) - ((len(line)*0.5)-0.5))*25))
                    self.win.blit(wordRendered, text_rect)
                else:
                    self.win.blit(wordRendered, (x + position[0], y))
                x += wordWidth + space
            # Reset the x coordinate to the far left
            x = position[0]
            # Set the y coordinate to that of the next row.
            y += wordHeight


main = Main()
main.Run()
