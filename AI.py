

#Generates a good move based of the board state
class AI:
    def __init__(self, AIDifficulty):
        #The depth of moves the NegaMax algorithm searches to
        self.depth = 2
        #The difficulty of the AI
        self.difficulty = AIDifficulty
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
        self.positionDamping = 0.01
        self.winConditions = [(["p", "-", "-", "-", "p"], ["-", "c", "c", "c", "-"]),
                              (["p", "-", "p", "-", "p"], ["-", "c", "-", "c", "-"]),
                              (["p", "p", "-", "p", "p"], ["-", "-", "c", "-", "-"])]

    def findBestAIMove(self, gs, validMoves):
        global nextMove, count
        nextMove = None
        count = 0
        self.findMoveNegaMaxAlphaBeta(gs, validMoves, self.depth, -999, 999, 1 if gs.player1Turn else -1)
        print(count)
        return nextMove

    #Returns the best move as evaluated by the NegaMax algorithm
    def findMoveNegaMaxAlphaBeta(self, gs, validMoves, depth, alpha, beta, turnMultiplier):
        global nextMove, count
        if depth <= 0:
            return self.ScoreBoard(gs) * turnMultiplier
        maxScore = -999
        for move in validMoves:
            if (not gs.MakeMove(move)):
                continue
            score = -self.findMoveNegaMaxAlphaBeta(gs, gs.GetAllValidMoves("y" if gs.player1Turn else "r"), depth - 1, -beta, -alpha, -turnMultiplier)
            if score > maxScore:
                maxScore = score
                if depth == self.depth:
                    nextMove = move
            gs.UndoMove()
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:

                break
            count += 1
        return maxScore


    #Rates the boards in a certain state
    def ScoreBoard(self, gs):
        #has someone won?
        if self.CheckForWin(gs):
            #if the AI won, this is good, return a big score
            if (gs.player1Turn):
                return -999
            #if the AI lost this is bad, return a big negative score
            else:
                return 999
        score = 0
        for i in range(1, 4):
            score += self.CountPossiblePatterns(gs.pegBoard, gs.cylinderBoard, i, "y")*i*i
            score -= self.CountPossiblePatterns(gs.pegBoard, gs.cylinderBoard, i, "r") * i*i
        for row in range(0, len(gs.pegBoard)):
            for col in range(0, len(gs.pegBoard[row])):
                if (gs.pegBoard[row][col][1] == "p"):
                    if (gs.pegBoard[row][col][0] == "y"):
                        score += self.positionsTable[row][col]*self.positionDamping
                    else:
                        score -= self.positionsTable[row][col]*self.positionDamping
                if (gs.cylinderBoard[row][col][1] == "c"):
                    if (gs.cylinderBoard[row][col][0] ==  "y"):
                        score += self.positionsTable[row][col]*self.positionDamping
                    else:
                        score -= self.positionsTable[row][col]*self.positionDamping
                elif (gs.cylinderBoard[row][col][1] == "h"):
                    if (gs.cylinderBoard[row][col][0] == "y"):
                        score += self.positionsTable[row][col]*self.positionDamping
                    else:
                        score -= self.positionsTable[row][col]*self.positionDamping
        return score


#Check to see if a player has won
    def CheckForWin(self, gs):
        #Check verticals
        for row in range(0, len(gs.pegBoard)-4):
            for col in range(0, len(gs.pegBoard[row])):
                if (self.CheckCoordVertical(row, col, gs.pegBoard, gs.cylinderBoard)):
                    return True
        #Check horizontals
        for row in range(0, len(gs.pegBoard)):
            for col in range(0, len(gs.pegBoard[row])-4):
                if (self.CheckCoordHorizontal(row, col, gs.pegBoard, gs.cylinderBoard)):
                    return True

        #Check positive diagonals
        for row in range(0, len(gs.pegBoard)-4):
            for col in range(0, len(gs.pegBoard[row])-4):
                if (self.CheckCoordPosDiagonal(row, col, gs.pegBoard, gs.cylinderBoard)):
                    return True

        #Check negative diagonals
        for row in range(0, len(gs.pegBoard)-4):
            for col in range(4, len(gs.pegBoard[row])):
                if (self.CheckCoordNegDiagonal(row, col, gs.pegBoard, gs.cylinderBoard)):
                    return True

        #If no win has been found, return false
        return False

    def CheckCoordHorizontal(self, row, col, pegBoard, cylinderBoard):
        #Check for each pattern
        for winCondition in self.winConditions:
            #Check red
            colour = "r"
            successCount = 0
            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (
                        pegBoard[row][col + i][0] == colour and pegBoard[row][col + i][1] == winCondition[0][i]):
                    #Check cylinders
                    if winCondition[1][i] == "-" or (cylinderBoard[row][col + i][0] == colour and (
                            cylinderBoard[row][col + i][1] == winCondition[1][i] or
                            cylinderBoard[row][col + i][1] == "h")):
                        successCount += 1
            if successCount == 5:
                return True

            #Check yellow
            colour = "y"
            successCount = 0

            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (pegBoard[row][col+i][0] == colour and pegBoard[row][col+i][1] == winCondition[0][i]):
                    # Check cylinders
                    if winCondition[1][i] == "-" or (cylinderBoard[row][col+i][0] == colour and (cylinderBoard[row][col+i][1] == winCondition[1][i] or cylinderBoard[row][col+i][1] == "h")):
                        successCount += 1
            if successCount == 5:
                return True


    def CheckCoordVertical(self, row, col, pegBoard, cylinderBoard):
        # Check for each pattern
        for winCondition in self.winConditions:
            # Check red
            colour = "r"
            successCount = 0
            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (
                        pegBoard[row + i][col][0] == colour and pegBoard[row + i][col][1] == winCondition[0][i]):
                    # Check cylinders
                    if winCondition[1][i] == "-" or (cylinderBoard[row + i][col][0] == colour and (
                            cylinderBoard[row + i][col][1] == winCondition[1][i] or
                            cylinderBoard[row + i][col][1] == "h")):
                        successCount += 1
            if successCount == 5:
                return True

            # Check yellow
            colour = "y"
            successCount = 0
            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (pegBoard[row + i][col][0] == colour and pegBoard[row + i][col][1] == winCondition[0][i]):
                    # Check cylinders
                    if winCondition[1][i] == "-" or (cylinderBoard[row + i][col][0] == colour and (cylinderBoard[row + i][col][1] == winCondition[1][i] or cylinderBoard[row+i][col][1] == "h")):
                        successCount += 1
            if successCount == 5:
                return True


    def CheckCoordPosDiagonal(self, row, col, pegBoard, cylinderBoard):
        # Check for each pattern
        for winCondition in self.winConditions:
            # Check red
            colour = "r"
            successCount = 0
            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (pegBoard[row + i][col+i][0] == colour and pegBoard[row + i][col+i][1] == winCondition[0][i]):
                    # Check cylinders
                    if winCondition[1][i] == "-" or (cylinderBoard[row + i][col+i][0] == colour and (cylinderBoard[row + i][col+i][1] == winCondition[1][i] or cylinderBoard[row+i][col+i][1] == "h")):
                        successCount += 1
            if successCount == 5:
                return True

            # Check yellow
            colour = "y"
            successCount = 0
            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (pegBoard[row + i][col+i][0] == colour and pegBoard[row + i][col+i][1] == winCondition[0][i]):
                    # Check cylinders
                    if winCondition[1][i] == "-" or (cylinderBoard[row + i][col+i][0] == colour and (cylinderBoard[row + i][col+i][1] == winCondition[1][i] or cylinderBoard[row+i][col+i][1] == "h")):
                        successCount += 1
            if successCount == 5:
                return True


    def CheckCoordNegDiagonal(self, row, col, pegBoard, cylinderBoard):
        # Check for each pattern
        for winCondition in self.winConditions:
            # Check red
            colour = "r"
            successCount = 0
            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (pegBoard[row + i][col-i][0] == colour and pegBoard[row + i][col-i][1] == winCondition[0][i]):
                    # Check cylinders
                    if winCondition[1][i] == "-" or (cylinderBoard[row + i][col-i][0] == colour and (cylinderBoard[row + i][col-i][1] == winCondition[1][i] or cylinderBoard[row+i][col-i][1] == "h")):
                        successCount += 1
            if successCount == 5:
                return True

            # Check yellow
            colour = "y"
            successCount = 0
            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (pegBoard[row + i][col-i][0] == colour and pegBoard[row + i][col-i][1] == winCondition[0][i]):
                    # Check cylinders
                    if winCondition[1][i] == "-" or (cylinderBoard[row + i][col-i][0] == colour and (cylinderBoard[row + i][col-i][1] == winCondition[1][i] or cylinderBoard[row+i][col-i][1] == "h")):
                        successCount += 1
            if successCount == 5:
                return True


#Check to see if a player has won
    def CountPossiblePatterns(self, pegBoard, cylinderBoard, numberInPattern, colour):
        #Check verticals
        count = 0
        for row in range(0, len(pegBoard)-4):
            for col in range(0, len(pegBoard[row])):
                count += self.CountCoordVertical(row, col,pegBoard, cylinderBoard, numberInPattern, colour)

        #Check horizontals
        for row in range(0, len(pegBoard)):
            for col in range(0, len(pegBoard[row])-4):
                count += self.CountCoordHorizontal(row, col,pegBoard, cylinderBoard, numberInPattern, colour)

        #Check positive diagonals
        for row in range(0, len(pegBoard)-4):
            for col in range(0, len(pegBoard[row])-4):
                count += self.CountCoordPosDiagonal(row, col,pegBoard, cylinderBoard, numberInPattern, colour)

        #Check negative diagonals
        for row in range(0, len(pegBoard)-4):
            for col in range(4, len(pegBoard[row])):
                count += self.CountCoordNegDiagonal(row, col,pegBoard, cylinderBoard, numberInPattern, colour)
        return count

    def CountCoordHorizontal(self, row, col, pegBoard, cylinderBoard, number, colour):
        #Check for each pattern
        amount = 0
        for winCondition in self.winConditions:
            successCount = 0
            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (
                        pegBoard[row][col + i][0] == colour and pegBoard[row][col + i][1] == winCondition[0][i]):
                    #Check cylinders
                    if winCondition[1][i] == "-" or (cylinderBoard[row][col + i][0] == colour and (
                            cylinderBoard[row][col + i][1] == winCondition[1][i] or
                            cylinderBoard[row][col + i][1] == "h")):
                        successCount += 1
            for i in range(0, 5):
                # check if the pattern can never be completed
                if winCondition[0][i] != "-" and ((pegBoard[row][col + i][0] != colour and pegBoard[row][col + i][0] != "-") or cylinderBoard[row][col + i][1] == "c" or cylinderBoard[row][col + i][1] == colour + "h"):
                    successCount = 0
                elif winCondition[1][i] != "-" and cylinderBoard[row][col + i][0] != colour:
                    successCount = 0
            if successCount == number:
                amount += 1
        return amount


    def CountCoordVertical(self, row, col, pegBoard, cylinderBoard, number, colour):
        # Check for each pattern
        amount = 0
        for winCondition in self.winConditions:
            successCount = 0
            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (pegBoard[row + i][col][0] == colour and pegBoard[row + i][col][1] == winCondition[0][i]):
                    # Check cylinders
                    if winCondition[1][i] == "-" or (cylinderBoard[row + i][col][0] == colour and (cylinderBoard[row + i][col][1] == winCondition[1][i] or cylinderBoard[row + i][col][1] == "h")):
                        successCount += 1
            for i in range(0, 5):
                # check if the pattern can never be completed
                if winCondition[0][i] != "-" and ((pegBoard[row+i][col ][0] != colour and pegBoard[row+i][col][0] != "-") or cylinderBoard[row+i][col][1] == "c" or cylinderBoard[row+i][col][1] == colour + "h"):
                    successCount = 0
                elif winCondition[1][i] != "-" and cylinderBoard[row+i][col][0] != colour:
                    successCount = 0
            if successCount == number:
                amount += 1

        return amount


    def CountCoordPosDiagonal(self, row, col, pegBoard, cylinderBoard, number, colour):
        # Check for each pattern
        amount = 0
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
            for i in range(0, 5):
                # check if the pattern can never be completed
                if winCondition[0][i] != "-" and ((pegBoard[row+i][col + i][0] != colour and pegBoard[row+i][col + i][0] != "-") or cylinderBoard[row+i][col + i][1] == "c" or cylinderBoard[row+i][col + i][1] == colour + "h"):
                    successCount = 0
                elif winCondition[1][i] != "-" and cylinderBoard[row+i][col + i][0] != colour:
                    successCount = 0
            if successCount == number:
                amount += 1

        return amount


    def CountCoordNegDiagonal(self, row, col, pegBoard, cylinderBoard, number, colour):
        # Check for each pattern
        amount = 0
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
            for i in range(0, 5):
                # check if the pattern can never be completed
                #if winCondition[0][i] != "-" and ((pegBoard[row + i][col - i][0] != colour or cylinderBoard[row+i][col - i][1] == "c")) or (winCondition[1][i] != "-" and (cylinderBoard[row + i][col - i][0] != colour)):
                    #successCount = 0
                if winCondition[0][i] != "-" and ((pegBoard[row+i][col -i][0] != colour and pegBoard[row+i][col -i][0] != "-") or cylinderBoard[row+i][col -i][1] == "c" or cylinderBoard[row+i][col -i][1] == colour + "h"):
                    successCount = 0
                elif winCondition[1][i] != "-" and cylinderBoard[row+i][col -i][0] != colour:
                    successCount = 0
            if successCount == number:
                amount += 1

        return amount