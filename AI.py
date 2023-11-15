import random

from Game import Move


#Generates a good move based of the board state
class AI:
    def __init__(self, AIDifficulty):
        #The depth of moves the NegaMax algorithm searches to
        self.depth = AIDifficulty
        #A table used for helping rate positions, to encourage the AI to play centrally - for use in ScoreBoard()
        self.positionsTable=[
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

    def findBestAIMove(self, gs, nextMoveStorage = [None]):
        global nextMove, count
        count = 0
        nextMove = None
        if not gs.player1Turn:
            #If it is the first few moves, automatically go in or around the center without consulting the AI
            #Go in the center
            if len(gs.movesStack) <= 2 and gs.pegBoard[3][3] == "--" and gs.cylinderBoard[3][3] == "--":
                for i in range(0, len(gs.player2CylinderStorage) - 3):
                    if gs.player2CylinderStorage[i][1] == "c":
                        nextMove = Move(gs.player2CylinderStorage, (999, i), (3, 3))
                        break
            #Go diagonally (left up) from the center
            elif len(gs.movesStack) <= 4 and gs.pegBoard[2][2] == "--" and gs.cylinderBoard[2][2] == "--":
                for i in range(0, len(gs.player2CylinderStorage) - 3):
                    if gs.player2CylinderStorage[i][1] == "c":
                        nextMove = Move(gs.player2CylinderStorage, (999, i), (2, 2))
                        break
            #Go in another random position around the center
            elif len(gs.movesStack) <= 4:
                listOfCoords = [(2,3),(3,2),(2,4),(4,2)]
                coords = random.choice(listOfCoords)
                if gs.pegBoard[coords[0]][coords[1]] != "--" or gs.cylinderBoard[coords[0]][coords[1]] != "--":
                    listOfCoords.remove(coords)
                    coords = random.choice(listOfCoords)
                for i in range(0, len(gs.player2CylinderStorage) - 3):
                    if gs.player2CylinderStorage[i][1] == "c":
                        nextMove = Move(gs.player2CylinderStorage, (999, i), (coords[0], coords[1]))
                        break
        else:
            # If it is the first few moves, automatically go in or around the center without consulting the AI
            # Go in the center
            if len(gs.movesStack) <= 2 and gs.pegBoard[3][3] == "--" and gs.cylinderBoard[3][3] == "--":
                for i in range(0, len(gs.player1CylinderStorage) - 3):
                    if gs.player2CylinderStorage[i][1] == "c":
                        nextMove = Move(gs.player1CylinderStorage, (999, i), (3, 3))
                        break
            # Go diagonally (left up) from the center
            elif len(gs.movesStack) <= 4 and gs.pegBoard[2][2] == "--" and gs.cylinderBoard[2][2] == "--":
                for i in range(0, len(gs.player1CylinderStorage) - 3):
                    if gs.player2CylinderStorage[i][1] == "c":
                        nextMove = Move(gs.player1CylinderStorage, (999, i), (2, 2))
                        break
            # Go in another random position around the center
            elif len(gs.movesStack) <= 4:
                listOfCoords = [(2,2), (2, 3), (3, 2), (2, 4), (4, 2)]
                coords = random.choice(listOfCoords)
                i = 0
                while gs.pegBoard[coords[0]][coords[1]] != "--" or gs.cylinderBoard[coords[0]][coords[1]] != "--":
                    listOfCoords.remove(coords)
                    coords = random.choice(listOfCoords)
                    i += 1
                    if i == 5:
                        nextMove = None
                        break
                for i in range(0, len(gs.player1CylinderStorage) - 3):
                    if gs.player2CylinderStorage[i][1] == "c":
                        nextMove = Move(gs.player1CylinderStorage, (999, i), (coords[0], coords[1]))
                        break
        #If no default starting move has been made, consult the AI
        if nextMove is None:
            self.findMoveNegaMaxAlphaBeta(gs, gs.GetAllValidMoves("y" if gs.player1Turn else "r"), self.depth, -999999999, 999999999, 1 if gs.player1Turn else -1)
            #print("Moves skipped: " + str(count))
        nextMoveStorage[0] = nextMove
        return nextMove



    #Returns the best move as evaluated by the NegaMax algorithm
    def findMoveNegaMaxAlphaBeta(self, gs, validMoves, depth, alpha, beta, turnMultiplier):
        global nextMove, count
        maxScore = -999999999
        #Loop through the moves
        for move in validMoves:
            #If the move can't be made, it is probably illegal, skip this move
            if not gs.MakeMove(move):
                continue
            # The base case
            #if it has recursed to the maximum depth, rate the board in the current state
            if depth <= 1:
                score = self.ScoreBoard(gs) * turnMultiplier
            else:
                #Check if a player has already won - if someone won we do not need to go any deeper
                if self.depth % 2 == 0 and depth % 2 == 0:
                    if gs.CheckForWin():
                        # if the AI won, this is good, return a big negative score (as the AI is negative)
                        if gs.pegBoard[gs.winCoords[0][0]][gs.winCoords[0][1]][0] == "r":
                            score = -999999 * turnMultiplier
                        # if the AI lost, this is bad, return a big score (as the player is positive)
                        else:
                            score = 999999 * turnMultiplier
                    else:
                        # Call itself with reduced depth
                        score = -self.findMoveNegaMaxAlphaBeta(gs, gs.GetAllValidMoves("y" if gs.player1Turn else "r"),depth - 1, -beta, -alpha, -turnMultiplier)
                else:
                    # Call itself with reduced depth
                    score = -self.findMoveNegaMaxAlphaBeta(gs, gs.GetAllValidMoves("y" if gs.player1Turn else "r"), depth - 1, -beta, -alpha, -turnMultiplier)
            #If the move is better than that currently selected, select it
            if score > maxScore:
                maxScore = score
                if depth == self.depth:
                    nextMove = move
                    if score >= 999999:
                        break
            #Undo the move to revert the board to its original state.
            gs.UndoMove()
            #Alpha-beta pruning
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:
                count +=1
                break
        return maxScore


    #Rates the boards in a certain state
    def ScoreBoard(self, gs):
        #has someone won?
        if gs.CheckForWin():
            # if the AI won, this is good, return a big negative score (as the AI is negative)
            if gs.pegBoard[gs.winCoords[0][0]][gs.winCoords[0][1]][0] == "r":
                return -999999
            # if the AI lost, this is bad, return a big score (as the player is positive)
            else:
                return 999999
        #No one has won so
        score = 0
        maxPattern = min((len(gs.movesStack)+1)//2,5)
        #Calculate the largest pattern yellow has made
        for i in range(maxPattern, 0, -1):
            if self.CountPossiblePatterns(i, "y", gs):
                score += i * i * i
                break
        # Calculate the largest pattern red has made
        for i in range(maxPattern, 0, -1):
            if self.CountPossiblePatterns(i, "r", gs):
                score -= i * i * i
                break
        #Assign bonuses for pieces closer to the center
        for row in range(2, len(gs.pegBoard)-2):
            for col in range(2, len(gs.pegBoard[row])-2):
                if gs.pegBoard[row][col][0] == "r":
                    score -= self.positionsTable[row][col] * self.positionDamping
                elif gs.pegBoard[row][col][0] == "y":
                    score += self.positionsTable[row][col] * self.positionDamping
                if gs.cylinderBoard[row][col][0] == "r":
                    score -= self.positionsTable[row][col] * self.positionDamping
                elif gs.cylinderBoard[row][col][0] == "y":
                    score += self.positionsTable[row][col] * self.positionDamping
        return score

#Count the number of patterns of a certain length a player of a specific colour has made
    def CountPossiblePatterns(self, numberInPattern, colour, game):
        #Check verticals
        for row in range(0, len(game.pegBoard)-4):
            for col in range(0, len(game.pegBoard[row])):
                if self.CountCoordVertical(row, col,game.pegBoard, game.cylinderBoard, numberInPattern, colour):
                    return True

        #Check horizontals
        for row in range(0, len(game.pegBoard)):
            for col in range(0, len(game.pegBoard[row])-4):
                if self.CountCoordHorizontal(row, col,game.pegBoard, game.cylinderBoard, numberInPattern, colour):
                    return True

        #Check positive diagonals
        for row in range(0, len(game.pegBoard)-4):
            for col in range(0, len(game.pegBoard[row])-4):
                if self.CountCoordPosDiagonal(row, col,game.pegBoard, game.cylinderBoard, numberInPattern, colour):
                    return True

        #Check negative diagonals
        for row in range(0, len(game.pegBoard)-4):
            for col in range(4, len(game.pegBoard[row])):
                if self.CountCoordNegDiagonal(row, col,game.pegBoard, game.cylinderBoard, numberInPattern, colour):
                    return True
        return False

    # check if there is a pattern of a certain length a player of a specific colour has made horizontally
    def CountCoordHorizontal(self, row, col, pegBoard, cylinderBoard, number, colour):
        #Check for each pattern
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

    # check if there is a pattern of a certain length a player of a specific colour has made vertically
    def CountCoordVertical(self, row, col, pegBoard, cylinderBoard, number, colour):
        # Check for each pattern
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

    # check if there is a pattern of a certain length a player of a specific colour has made diagonally (right and downwards)
    def CountCoordPosDiagonal(self, row, col, pegBoard, cylinderBoard, number, colour):
        # Check for each pattern
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
                    elif winCondition[1][i] != "-" and (cylinderBoard[row+i][col + i] != "--" or pegBoard[row+i][col+i][0] == colour):
                        successCount = 0
                        fail = True
                        break
                elif winCondition[0][i] != "-" and (pegBoard[row+i][col + i] != "--"or cylinderBoard[row+i][col+i][1] == "c"):
                    successCount = 0
                    fail = True
                    break
            if successCount == number and not fail:
                return True
        return False

    # check if there is a pattern of a certain length a player of a specific colour has made diagonally (right and upwards)
    def CountCoordNegDiagonal(self, row, col, pegBoard, cylinderBoard, number, colour):
        # Check for each pattern
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
                    elif winCondition[1][i] != "-" and (cylinderBoard[row + i][col - i] != "--"or pegBoard[row+i][col-i][0] == colour):
                        successCount = 0
                        fail = True
                        break
                elif winCondition[0][i] != "-" and (pegBoard[row + i][col - i] != "--"or cylinderBoard[row+i][col-i][1] == "c"):
                    successCount = 0
                    fail = True
                    break
            if successCount == number and not fail:
                return True

        return False
