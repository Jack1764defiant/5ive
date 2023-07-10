from AI import AI
from Game import Game


class Main:
    def __init__(self):
        self.isGameRunning = True
        self.player1Human = True
        self.player2Human = True
        self.player1Turn = True

    def Run(self):
        while self.isGameRunning:
            pass

#Handles drawing the UI
class UI:
    def __init__(self):
        self.boardWidth = 800
        self.boardHeight = 1600
        self.slotSize = 50
        self.pegSize = 25
        self.amountOfSlots = 7

    def DrawBoard(self, win):
        pass

    def DrawPieces(self, win, game):
        pass

    def DrawIntroScreen(self, win):
        pass

    def DrawWinScreen(self, win):
        pass

    def DrawLoseScreen(self, win):
        pass

    def DrawInstructionScreen(self, win):
        pass

#Represents a clickable, rectangular button with a text overlay
class Button:
    def __init__(self, text, x, y, color, explanationText, width = 150, height = 100):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.explanationText = explanationText


    def draw(self, win):
        pass


    def IsCoordInside(self, pos):
        pass

    def OnClick(self):
        pass

    def OnHover(self):
        pass


