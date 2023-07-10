from Game import Game

#Generates a good move based of the board state
class AI:
    def __init__(self):
        self.depth = 4
        self.positionsTable= [
            [0, 1, 1, 1, 1, 1, 0],
            [1, 1, 2, 2, 2, 1, 1],
            [1, 2, 2, 3, 2, 2, 1],
            [1, 2, 3, 4, 3, 2, 1],
            [1, 2, 2, 3, 2, 2, 1],
            [1, 1, 2, 2, 2, 1, 1],
            [0, 1, 1, 1, 1, 1, 0]
        ]


    def GetNegaMaxAlphaBetaMove(self, game, validMoves, alpha, beta, turnMultiplier):
        pass

    def ScoreBoard(self, pegBoard, cylinderBoard):
        pass