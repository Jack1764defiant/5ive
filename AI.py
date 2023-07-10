from Game import Game

#Generates a good move based of the board state
class AI:
    def __init__(self):
        #The depth of moves the NegaMax algorithm searches to
        self.depth = 4
        #A table used for helping rate positions, to encourage the AI to play centrally - for use in ScoreBoard()
        self.positionsTable= [
            [0, 1, 1, 1, 1, 1, 0],
            [1, 1, 2, 2, 2, 1, 1],
            [1, 2, 2, 3, 2, 2, 1],
            [1, 2, 3, 4, 3, 2, 1],
            [1, 2, 2, 3, 2, 2, 1],
            [1, 1, 2, 2, 2, 1, 1],
            [0, 1, 1, 1, 1, 1, 0]
        ]

    #Returns the best move as evaluated by the NegaMax algorithm
    def GetNegaMaxAlphaBetaMove(self, game, validMoves, alpha, beta, turnMultiplier):
        pass

    #Rates the boards in a certain state
    def ScoreBoard(self, pegBoard, cylinderBoard, colour):
        pass