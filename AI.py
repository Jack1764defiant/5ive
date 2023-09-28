from Game import Move
#Generates a good move based of the board state
class AI:
    def __init__(self, AIDifficulty):
        #The depth of moves the NegaMax algorithm searches to
        self.depth = 2
        #The difficulty of the AI
        self.difficulty = AIDifficulty
        #A table used for helping rate positions, to encourage the AI to play centrally - for use in ScoreBoard()
        self.positionsTable= [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 1],
            [1, 2, 3, 3, 3, 2, 1],
            [1, 2, 3, 4, 3, 2, 1],
            [1, 2, 3, 3, 3, 2, 1],
            [1, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        self.positionDamping = 0.01
        self.winConditions = [(["p", "-", "-", "-", "p"], ["-", "c", "c", "c", "-"]),
                              (["p", "-", "p", "-", "p"], ["-", "c", "-", "c", "-"]),
                              (["p", "p", "-", "p", "p"], ["-", "-", "c", "-", "-"])]

    def findBestAIMove(self, gs, validMoves):
        global nextMove
        nextMove = None
        if (gs.pegBoard[3][3] == "--" and gs.cylinderBoard[3][3] == "--"):
            for i in range(0, len(gs.player2CylinderStorage) - 3):
                if (gs.player2CylinderStorage[i][1] == "c"):
                    nextMove = Move(gs.player2CylinderStorage, (999, i), (3, 3))
                    break
        if (nextMove == None):
            self.findMoveNegaMaxAlphaBeta(gs, validMoves, self.depth, -999999999, 999999999, 1 if gs.player1Turn else -1)
        return nextMove

    #Returns the best move as evaluated by the NegaMax algorithm
    def findMoveNegaMaxAlphaBeta(self, gs, validMoves, depth, alpha, beta, turnMultiplier):
        global nextMove, count
        if depth <= 0:
            return self.ScoreBoard(gs) * turnMultiplier
        maxScore = -999999999
        for move in validMoves:
            if (not gs.MakeMove(move)):
                continue
            score = -self.findMoveNegaMaxAlphaBeta(gs, gs.GetAllValidMoves("y" if gs.player1Turn else "r"), depth - 1, -beta, -alpha, -turnMultiplier)
            if score > maxScore:
                maxScore = score
                if depth == self.depth:
                    nextMove = move
                    if score >= 999999:
                        gs.UndoMove()
                        return maxScore
            gs.UndoMove()
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:
                break
        return maxScore


    #Rates the boards in a certain state
    def ScoreBoard(self, gs):
        #has someone won?
        if gs.CheckForWin():
            # if the AI won, this is good, return a big negative score (as the ai is negative)
            if (gs.pegBoard[gs.winCoords[0][0]][gs.winCoords[0][1]][0] == "r"):
                return -999999
            # if the AI lost, this is bad, return a big score (as the player is postive)
            else:
                return 999999
        #No one has won so
        score = 0
        for i in range(5, 0, -1):
            if (self.CountPossiblePatterns(i, "y", gs)):
                score += i * i * i
                break
        for i in range(5, 0, -1):
            if (self.CountPossiblePatterns(i, "r", gs)):
                score -= i * i * i
                break
        for row in range(2, len(gs.pegBoard)-2):
            for col in range(2, len(gs.pegBoard[row])-2):
                if (gs.pegBoard[row][col][0] == "r"):
                    score -= self.positionsTable[row][col] * self.positionDamping
                elif (gs.pegBoard[row][col][0] == "y"):
                    score += self.positionsTable[row][col] * self.positionDamping
                if (gs.cylinderBoard[row][col][0] == "r"):
                    score -= self.positionsTable[row][col] * self.positionDamping
                elif (gs.cylinderBoard[row][col][0] == "y"):
                    score += self.positionsTable[row][col] * self.positionDamping

        return score

#Check to see if a player has won
    def CountPossiblePatterns(self, numberInPattern, colour, game):
        #Check verticals
        count = 0
        for row in range(0, len(game.pegBoard)-4):
            for col in range(0, len(game.pegBoard[row])):
                if (self.CountCoordVertical(row, col,game.pegBoard, game.cylinderBoard, numberInPattern, colour, game)):
                    return True

        #Check horizontals
        for row in range(0, len(game.pegBoard)):
            for col in range(0, len(game.pegBoard[row])-4):
                if (self.CountCoordHorizontal(row, col,game.pegBoard, game.cylinderBoard, numberInPattern, colour, game)):
                    return True

        #Check positive diagonals
        for row in range(0, len(game.pegBoard)-4):
            for col in range(0, len(game.pegBoard[row])-4):
                if(self.CountCoordPosDiagonal(row, col,game.pegBoard, game.cylinderBoard, numberInPattern, colour, game)):
                    return True

        #Check negative diagonals
        for row in range(0, len(game.pegBoard)-4):
            for col in range(4, len(game.pegBoard[row])):
                if(self.CountCoordNegDiagonal(row, col,game.pegBoard, game.cylinderBoard, numberInPattern, colour,game )):
                    return True
        return count

    def CountCoordHorizontal(self, row, col, pegBoard, cylinderBoard, number, colour, game):
        #Check for each pattern
        amount = 0
        fail = False
        for winCondition in self.winConditions:
            successCount = 0
            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or pegBoard[row][col + i] == colour + "p":
                    #Check cylinders
                    if winCondition[1][i] == "-" or (cylinderBoard[row][col + i][0] == colour and (
                            cylinderBoard[row][col + i][1] == "c" or
                            cylinderBoard[row][col + i][1] == "h")):
                        successCount += 1
                    elif (winCondition[1][i] != "-" and (cylinderBoard[row][col+i] != "--" or pegBoard[row][col+i][0] == colour)):
                        successCount = 0
                        fail = True
                        break
                elif (winCondition[0][i] != "-" and (pegBoard[row][col+i] != "--" or cylinderBoard[row][col+i][1] == "c")):
                    successCount = 0
                    fail = True
                    break
            if successCount == number and not fail:
                return True

        return False


    def CountCoordVertical(self, row, col, pegBoard, cylinderBoard, number, colour, game):
        # Check for each pattern
        amount = 0
        fail = False
        for winCondition in self.winConditions:
            successCount = 0
            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (pegBoard[row + i][col][0] == colour and pegBoard[row + i][col][1] == winCondition[0][i]):
                    # Check cylinders
                    if winCondition[1][i] == "-" or (cylinderBoard[row + i][col][0] == colour and (cylinderBoard[row + i][col][1] == winCondition[1][i] or cylinderBoard[row + i][col][1] == "h")):
                        successCount += 1
                    elif (winCondition[1][i] != "-" and (cylinderBoard[row+i][col] != "--"or pegBoard[row+i][col][0] == colour)):
                        successCount = 0
                        fail = True
                        break
                elif (winCondition[0][i] != "-" and (pegBoard[row+i][col] != "--"or cylinderBoard[row+i][col][1] == "c")):
                    successCount = 0
                    fail = True
                    break
            if successCount == number and not fail:
                return True

        return False


    def CountCoordPosDiagonal(self, row, col, pegBoard, cylinderBoard, number, colour, game):
        # Check for each pattern
        amount = 0
        fail = False
        for winCondition in self.winConditions:
            successCount = 0
            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (
                        pegBoard[row+i][col + i][0] == colour and pegBoard[row+i][col + i][1] == winCondition[0][i]):
                    # Check cylinders
                    if winCondition[1][i] == "-" or (cylinderBoard[row+i][col + i][0] == colour and (
                            cylinderBoard[row+i][col + i][1] == winCondition[1][i] or
                            cylinderBoard[row+i][col + i][1] == "h")):
                        successCount += 1
                    elif (winCondition[1][i] != "-" and (cylinderBoard[row+i][col + i] != "--" or pegBoard[row+i][col+i][0] == colour)):
                        successCount = 0
                        fail = True
                        break
                elif (winCondition[0][i] != "-" and (pegBoard[row+i][col + i] != "--"or cylinderBoard[row+i][col+i][1] == "c")):
                    successCount = 0
                    fail = True
                    break
            if successCount == number and not fail:
                return True
        return False


    def CountCoordNegDiagonal(self, row, col, pegBoard, cylinderBoard, number, colour, game):
        # Check for each pattern
        amount = 0
        fail = False
        for winCondition in self.winConditions:
            successCount = 0
            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (
                        pegBoard[row + i][col - i][0] == colour and pegBoard[row + i][col - i][1] == winCondition[0][
                    i]):
                    # Check cylinders
                    if winCondition[1][i] == "-" or (cylinderBoard[row + i][col - i][0] == colour and (
                            cylinderBoard[row + i][col - i][1] == winCondition[1][i] or
                            cylinderBoard[row + i][col - i][1] == "h")):
                        successCount += 1
                    elif (winCondition[1][i] != "-" and (cylinderBoard[row + i][col - i] != "--"or pegBoard[row+i][col-i][0] == colour)):
                        successCount = 0
                        fail = True
                        break
                elif (winCondition[0][i] != "-" and (pegBoard[row + i][col - i] != "--"or cylinderBoard[row+i][col-i][1] == "c")):
                    successCount = 0
                    fail = True
                    break
            if successCount == number and not fail:
                return True

        return False