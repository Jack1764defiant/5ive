from AI import AI
import Game as g
import pygame as p
import time


class Main:
    def __init__(self):
        self.isGameRunning = True
        #Is player 1 human or a bot?
        self.hasPlayer1 = True
        # Is player 2 human or a bot?
        self.hasPlayer2 = True
        # Is it player 1s turn?
        self.player1Turn = True
        #Is the game over?
        self.gameOver = False
        self.MAXFPS = 20
        self.clicks = []

    #This is the main function that controls everything else. A while loop runs continously in it to update the game
    def Run(self):
        p.init()
        clock = p.time.Clock()
        self.game = g.Game()
        self.UI = UI()
        while self.isGameRunning:
            self.handleInputEvents()
            self.UI.drawGameScreen(self.game)
            clock.tick(self.MAXFPS)
            p.display.flip()

    def handleInputEvents(self):
        for e in p.event.get():
            # Exit when they try to quit
            if e.type == p.QUIT:
                self.isGameRunning = False
                # When the mouse is clicked
            elif e.type == p.MOUSEBUTTONDOWN:
                if not self.gameOver and ((self.player1Turn and self.hasPlayer1) or (self.hasPlayer2 and not self.player1Turn)):
                    location = p.mouse.get_pos()
                    if (len(self.clicks) == 0):
                        # Get the vertical mouse location and convert it to a slot position
                        row = (location[1] // self.UI.SLOTSIZE) - 2
                        # if it is in player 1's storage
                        if (row < 2):
                            # Compensate for the slots in storage being centered differently
                            col = ((location[0] + (self.UI.SLOTSIZE // 2)) // self.UI.SLOTSIZE) - 1
                            row = (location[1] // self.UI.SLOTSIZE)
                            self.clicks.append((row, col))
                            if (row < 1):
                                self.clicks.append(self.game.player1PegStorage)
                            else:
                                self.clicks.append(self.game.player1CylinderStorage)
                            # if it is in player 2's storage
                        elif (row > 9):
                            # Compensate for the slots in storage being centered differently
                            col = ((location[0] + (self.UI.SLOTSIZE // 2)) // self.UI.SLOTSIZE) - 1
                            row = (location[1] // self.UI.SLOTSIZE)
                            self.clicks.append((row, col))
                            if (row > 10):
                                self.clicks.append(self.game.player2CylinderStorage)
                            else:
                                self.clicks.append(self.game.player2PegStorage)

                        else:
                            # The click is on the main board
                            col = location[0] // self.UI.SLOTSIZE
                            row = (location[1] // self.UI.SLOTSIZE) - 2
                            self.clicks.append((row, col))
                            #if (self.game)
                    else:
                        # Get the vertical mouse location and convert it to a slot position
                        row = (location[1] // self.UI.SLOTSIZE) - 2
                        # if it is in player 1's storage
                    if (row < 2):
                        # Compensate for the slots in storage being centered differently
                        col = ((location[0] + (self.UI.SLOTSIZE // 2)) // self.UI.SLOTSIZE) - 1
                        row = (location[1] // self.UI.SLOTSIZE)
                        # if it is in player 2's storage
                    elif (row > 11):
                        # Compensate for the slots in storage being centered differently
                        col = ((location[0] + (self.UI.SLOTSIZE // 2)) // self.UI.SLOTSIZE) - 1
                        row = (location[1] // self.UI.SLOTSIZE)
                    else:
                        # The click is on the main board
                        col = location[0] // self.UI.SLOTSIZE
                        row = (location[1] // self.UI.SLOTSIZE) - 2
                        #self.game.MakeMove(self.clicks[1], self.clicks[0], (row, col)))

                    self.clicks = []


            elif e.type == p.KEYDOWN:
                # Undo a move when z is pressed
                if e.key == p.K_z:
                    self.game.UndoMove()
                # Restart game when r is pressed
                elif e.key == p.K_r:
                    pass



#Handles drawing the UI
class UI:
    def __init__(self):
        #The sizes of the board and pieces
        self.BOARDWIDTH = 620
        self.BOARDHEIGHT = 440
        self.SLOTSIZE = 40
        self.PEGSIZE = 20
        self.amountOfSlots = 7
        self.screen = p.display.set_mode((self.BOARDWIDTH, self.BOARDHEIGHT))

    #Draws the game screen - the board and pieces
    def drawGameScreen(self, game):
        self.drawBoard()
        self.drawPieces(game)
        self.drawPanel()

    #Draws the panel containing the back button and a list of makeable patterns
    def drawPanel(self):
        #Draw the panel
        p.draw.rect(self.screen, p.Color("gray"), p.Rect(370, 10, 240, 420))
        #Draw the title of the panel
        font = p.font.SysFont("comicsans", 40)
        text = font.render("Patterns:", 1, (255, 255, 255))
        self.screen.blit(text, (490 - round(text.get_width() / 2), 20))

        #Draw the patterns
        #Pattern 1
        #Draw the background
        p.draw.rect(self.screen, p.Color("white"), p.Rect(380, 100, 220, 40))
        #Draw the pattern
        p.draw.circle(self.screen, p.Color("grey"), (410, 120), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (410, 120), self.PEGSIZE / 2)

        p.draw.circle(self.screen, p.Color("red"), (450, 120), self.SLOTSIZE / 2)

        p.draw.circle(self.screen, p.Color("grey"), (490, 120), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (490, 120), self.PEGSIZE / 2)

        p.draw.circle(self.screen, p.Color("red"), (530, 120), self.SLOTSIZE / 2)

        p.draw.circle(self.screen, p.Color("grey"), (570, 120), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (570, 120), self.PEGSIZE / 2)

        # Pattern 2
        # Draw the background
        p.draw.rect(self.screen, p.Color("white"), p.Rect(380, 180, 220, 40))
        # Draw the pattern
        p.draw.circle(self.screen, p.Color("grey"), (410, 200), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (410, 200), self.PEGSIZE / 2)

        p.draw.circle(self.screen, p.Color("red"), (450, 200), self.SLOTSIZE / 2)

        p.draw.circle(self.screen, p.Color("red"), (490, 200), self.SLOTSIZE / 2)

        p.draw.circle(self.screen, p.Color("red"), (530, 200), self.SLOTSIZE / 2)

        p.draw.circle(self.screen, p.Color("grey"), (570, 200), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (570, 200), self.PEGSIZE / 2)

        # Pattern 2
        # Draw the background
        p.draw.rect(self.screen, p.Color("white"), p.Rect(380, 260, 220, 40))
        # Draw the pattern
        p.draw.circle(self.screen, p.Color("grey"), (410, 280), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (410, 280), self.PEGSIZE / 2)

        p.draw.circle(self.screen, p.Color("grey"), (450, 280), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (450, 280), self.PEGSIZE / 2)

        p.draw.circle(self.screen, p.Color("red"), (490, 280), self.SLOTSIZE / 2)

        p.draw.circle(self.screen, p.Color("grey"), (530, 280), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (530, 280), self.PEGSIZE / 2)

        p.draw.circle(self.screen, p.Color("grey"), (570, 280), self.SLOTSIZE / 2)
        p.draw.circle(self.screen, p.Color("red"), (570, 280), self.PEGSIZE / 2)


        #Generate and draw the button
        self.exitButton = Button("Quit", 380, 350, p.Color("Blue"), self.screen, "Return to the main menu", self.drawIntroScreen, height=70, width=220)
        self.exitButton.draw()

    #Draws the board on the screen
    def drawBoard(self):
        self.screen.fill(p.Color("white"))
        color = p.Color("gray")
        # Player 1's storage
        for r in range(2):
            for c in range(8):
                p.draw.circle(self.screen, color, ((c * self.SLOTSIZE) + self.SLOTSIZE, (r * self.SLOTSIZE) + self.SLOTSIZE / 2), self.SLOTSIZE / 2)
        # The main board
        for r in range(self.amountOfSlots):
            for c in range(self.amountOfSlots):
                p.draw.circle(self.screen, color, ((c * self.SLOTSIZE) + (self.SLOTSIZE*1.5), (r * self.SLOTSIZE) + self.SLOTSIZE / 2 + (2 * self.SLOTSIZE)),self.SLOTSIZE / 2)
        # Player 2's storage
        for r in range(2):
            for c in range(8):
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
                if (r == 1):
                    # Draw full cylinders
                    if (game.player1CylinderStorage[c][1] == "c"):
                        p.draw.circle(self.screen, p.Color("yellow"),((c * self.SLOTSIZE) + self.SLOTSIZE, (r * self.SLOTSIZE) + self.SLOTSIZE / 2),self.SLOTSIZE / 2)
                    # Draw hollow cylinders
                    elif game.player1CylinderStorage[c][1] == "h":
                        p.draw.circle(self.screen, p.Color("yellow"),((c * self.SLOTSIZE) + self.SLOTSIZE, (r * self.SLOTSIZE) + self.SLOTSIZE / 2),self.SLOTSIZE / 2)
                        p.draw.circle(self.screen, p.Color("grey"),((c * self.SLOTSIZE) + self.SLOTSIZE, (r * self.SLOTSIZE) + self.SLOTSIZE / 2),self.PEGSIZE / 2)
                # Draw pegs
                elif (r == 0):
                    if (game.player1PegStorage[c] != "--"):
                        p.draw.circle(self.screen, p.Color("yellow"),((c * self.SLOTSIZE) + self.SLOTSIZE, (r * self.SLOTSIZE) + self.SLOTSIZE / 2),self.PEGSIZE / 2)
        # Draw main board
        for r in range(self.amountOfSlots):
            for c in range(self.amountOfSlots):
                # if the piece is red
                #Draw peg
                if game.pegBoard[r][c] == "rp":
                    p.draw.circle(self.screen, p.Color("red"), ((c * self.SLOTSIZE) + self.SLOTSIZE*1.5, (r * self.SLOTSIZE) + 5 * self.SLOTSIZE / 2),self.PEGSIZE / 2)
                # Draw cylinders
                # Draw full cylinder
                elif game.cylinderBoard[r][c] == "rc":
                    p.draw.circle(self.screen, p.Color("red"), ((c * self.SLOTSIZE) + self.SLOTSIZE*1.5, (r * self.SLOTSIZE) + 5 * self.SLOTSIZE / 2),self.SLOTSIZE / 2)
                # Draw hollow cylinder
                elif game.cylinderBoard[r][c] == "rh":
                    p.draw.circle(self.screen, p.Color("red"), ((c * self.SLOTSIZE) + self.SLOTSIZE*1.5, (r * self.SLOTSIZE) + 5 * self.SLOTSIZE / 2),self.SLOTSIZE / 2)
                    p.draw.circle(self.screen, p.Color("grey"), ((c * self.SLOTSIZE) + self.SLOTSIZE*1.5, (r * self.SLOTSIZE) + 5 * self.SLOTSIZE / 2),self.PEGSIZE / 2)
                # if the piece is yellow
                # Draw cylinders
                # Draw full cylinder
                if game.cylinderBoard[r][c] == "yc":
                    p.draw.circle(self.screen, p.Color("yellow"), ((c * self.SLOTSIZE) + self.SLOTSIZE*1.5, (r * self.SLOTSIZE) + 5 * self.SLOTSIZE / 2), self.SLOTSIZE / 2)
                # Draw hollow cylinder
                elif game.cylinderBoard[r][c] == "yh":
                    p.draw.circle(self.screen, p.Color("yellow"), ((c * self.SLOTSIZE) + self.SLOTSIZE*1.5, (r * self.SLOTSIZE) + 5 * self.SLOTSIZE / 2),self.SLOTSIZE / 2)
                    p.draw.circle(self.screen, p.Color("grey"), ((c * self.SLOTSIZE) + self.SLOTSIZE*1.5, (r * self.SLOTSIZE) + 5 * self.SLOTSIZE / 2),self.PEGSIZE / 2)
                # Draw pegs
                elif game.pegBoard[r][c] == "yp":
                    p.draw.circle(self.screen, p.Color("yellow"), ((c * self.SLOTSIZE) + self.SLOTSIZE*1.5, (r * self.SLOTSIZE) + 5 * (self.SLOTSIZE / 2)),self.PEGSIZE / 2)

        # draw red's storage
        for r in range(2):
            for c in range(8):
                # Draw pegs
                if (r == 0):
                    if (game.player2PegStorage[c] != "--"):
                        p.draw.circle(self.screen, p.Color("red"), ((c * self.SLOTSIZE) + self.SLOTSIZE,(r * self.SLOTSIZE) + self.SLOTSIZE / 2 + (self.SLOTSIZE * 10)), self.PEGSIZE / 2)
                # Draw cylinders
                elif (r == 1):
                    # Draw full cylinders
                    if (game.player2CylinderStorage[c][1] == "c"):
                        p.draw.circle(self.screen, p.Color("red"), ((c * self.SLOTSIZE) + self.SLOTSIZE,(r * self.SLOTSIZE) + self.SLOTSIZE / 2 + (self.SLOTSIZE * 8)), self.SLOTSIZE / 2)
                    # Draw hollow cylinders
                    elif game.player2CylinderStorage[c][1] == "h":
                        p.draw.circle(self.screen, p.Color("red"), ((c * self.SLOTSIZE) + self.SLOTSIZE,(r * self.SLOTSIZE) + self.SLOTSIZE / 2 + (self.SLOTSIZE * 8)), self.SLOTSIZE / 2)
                        p.draw.circle(self.screen, p.Color("grey"), ((c * self.SLOTSIZE) + self.SLOTSIZE,(r * self.SLOTSIZE) + self.SLOTSIZE / 2 + (self.SLOTSIZE * 8)), self.PEGSIZE / 2)

    #Draws the intro screen - the title and buttons
    def drawIntroScreen(self):
        pass

    #Draws the You Win text to the screen
    def drawWinScreen(self):
        pass

    #Draws the You Lose text to the screen
    def drawLoseScreen(self):
        pass

    #Draws the help screen, with the instructions about how to play the game
    def drawInstructionScreen(self):
        pass

#Represents a clickable, rectangular button with a text overlay
class Button:
    def __init__(self, text, x, y, color, win, explanationText, functionToRun, width = 150, height = 100, showWindowAbove=True):
        #The text displayed on the center of the button
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
        #The time the hover text has been shown for (-1 means it isnt being shown)
        self.windowShownTime = -1

    #Run every "frame" or equivalent so that the button can close the hover text once 5 seconds have passed
    def Update(self):
        if self.windowShownTime > 0 and time.time() < self.windowShownTime + 5:
            #Show the window
            self.ShowTextWindow()
        else:
            #The window will stop being shown
            self.windowShownTime = -1

    #Draw the button to the screen
    def draw(self):
        #draw a rectangle
        p.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))
        font = p.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        #Draw the text on the rectangle, centered
        self.win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def IsCoordInside(self, pos):
        #Get each coord from the tuple
        x1 = pos[0]
        y1 = pos[1]
        #Is it inside the boundaries of the button?
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

    def ShowTextWindow(self):
        #Draw the hover text window above or below the button
        if not self.showWindowAbove:
            #Draw the rectangular window
            p.draw.rect(self.win, self.color, (self.x, self.y-self.height, self.width, self.height))
            font = p.font.SysFont("comicsans", 40)
            text = font.render(self.explanationText, 1, (255, 255, 255))
            # Draw the explanatory text
            self.win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),self.y - self.height + round(self.height / 2) - round(text.get_height() / 2)))

        else:
            # Draw the rectangular window
            p.draw.rect(self.win, self.color, (self.x, self.y+self.height, self.width, self.height))
            font = p.font.SysFont("comicsans", 40)
            text = font.render(self.explanationText, 1, (255, 255, 255))
            #Draw the explanatory text
            self.win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),self.y + self.height + round(self.height / 2) - round(text.get_height() / 2)))
        #Update the window shown time to start the countdown
        self.windowShownTime = time.time()

    #Run when the button is clicked
    def OnClick(self):
        self.functionToRun()

    #Run when the mouse hovers over the button
    def OnHover(self):
        #Show the explanatory text window
        self.ShowTextWindow()


main = Main()
main.Run()

