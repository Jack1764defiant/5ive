from AI import AI
from Game import Game
import pygame
import time


class Main:
    def __init__(self):
        self.isGameRunning = True
        #Is player 1 human or a bot?
        self.player1Human = True
        # Is player 2 human or a bot?
        self.player2Human = True
        # Is it player 1s turn?
        self.player1Turn = True

    #This is the main function that controls everything else. A while loop runs continously in it to update the game
    def Run(self):
        while self.isGameRunning:
            pass

#Handles drawing the UI
class UI:
    def __init__(self):
        #The sizes of the board and pieces
        self.boardWidth = 800
        self.boardHeight = 1600
        self.slotSize = 50
        self.pegSize = 25
        self.amountOfSlots = 7

    #Draws the game screen - the board and pieces
    def DrawGameScreen(self, win, game):
        self.DrawBoard(win)
        self.DrawPieces(win,game)

    #Draws the board on the screen
    def DrawBoard(self, win):
        pass

    #Draws the pieces to the screen
    def DrawPieces(self, win, game):
        pass

    #Draws the intro screen - the title and buttons
    def DrawIntroScreen(self, win):
        pass

    #Draws the You Win text to the screen
    def DrawWinScreen(self, win):
        pass

    #Draws the You Lose text to the screen
    def DrawLoseScreen(self, win):
        pass

    #Draws the help screen, with the instructions about how to play the game
    def DrawInstructionScreen(self, win):
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
        pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
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
            pygame.draw.rect(self.win, self.color, (self.x, self.y-self.height, self.width, self.height))
            font = pygame.font.SysFont("comicsans", 40)
            text = font.render(self.explanationText, 1, (255, 255, 255))
            # Draw the explanatory text
            self.win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),self.y - self.height + round(self.height / 2) - round(text.get_height() / 2)))

        else:
            # Draw the rectangular window
            pygame.draw.rect(self.win, self.color, (self.x, self.y+self.height, self.width, self.height))
            font = pygame.font.SysFont("comicsans", 40)
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


