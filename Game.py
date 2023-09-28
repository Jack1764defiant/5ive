import socket
import pickle


#Represents a game, handles making moves
class Game:
    def __init__(self, main):
        #y stands for yellow, r for red.
        #c stands for cylinder, h for hollow cylinder and p for peg.
        #This represents the section of the board on which pegs can be placed
        self.pegBoard = [
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"]
        ]
        # This represents the section of the board on which cylinders can be placed
        self.cylinderBoard = [
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"]
        ]
        #Each player's storage is represented by arrays
        self.player1PegStorage = ["yp", "yp", "yp", "yp", "yp", "yp", "yp", "yp"]
        self.player1CylinderStorage = ["yc", "yc", "yc", "yc", "yh", "yh", "yh", "yh"]

        self.player2PegStorage = ["rp", "rp", "rp", "rp", "rp", "rp", "rp", "rp"]
        self.player2CylinderStorage = ["rc", "rc", "rc", "rc", "rh", "rh", "rh", "rh"]
        #A stack containing every move that has been made, for use in UndoMove()
        self.movesStack = []
        self.main = main
        # Is it player 1s turn?
        self.player1Turn = True
        #The patterns you can make to win
        self.winConditions = [(["p", "-", "-", "-", "p"],["-", "c", "c", "c", "-"]), (["p", "-", "p", "-", "p"],["-", "c", "-", "c", "-"]), (["p", "p", "-", "p", "p"],["-", "-", "c", "-", "-"])]
        self.winCoords = []

    #Carries out the input move on the boards and updates the movesStack
    def MakeMove(self, move):
        # Try acting as though the array is 2D
        try:
            #Test by getting a value that would be out of bounds on the 1D arrays I am using
            move.startArray[6][6]
            # If it succeeds, the array is 2D
            pieceToMove = move.startArray[move.startRow][move.startCol]
            #Check if it is the correct turn for a yellow piece to be moved
            if ((pieceToMove[0] == "y" and self.player1Turn) or (pieceToMove[0] == "r" and not self.player1Turn)) and self.ValidateMove(move, pieceToMove):
                # Set the end location to the piece you want there
                if (pieceToMove[1] == "p"):
                    self.pegBoard[move.endRow][move.endCol] = pieceToMove
                else:
                    self.cylinderBoard[move.endRow][move.endCol] = pieceToMove
                # Remove that piece from the original array
                move.startArray[move.startRow][move.startCol] = "--"
                self.movesStack.append(move)
                # Switch which player is going
                self.player1Turn = not self.player1Turn
                return True
            else:
                return False
        except:
            # If it fails, the array is 1D, so access it only using column.
            pieceToMove = move.startArray[move.startCol]
            # Check if it is the correct turn for a red piece to be moved
            if ((pieceToMove[0] == "y" and self.player1Turn) or (pieceToMove[0] == "r" and not self.player1Turn)) and self.ValidateMove(move, pieceToMove):
                # Set the end location to the piece you want there
                if (pieceToMove[1] == "p"):
                    self.pegBoard[move.endRow][move.endCol] = pieceToMove
                else:
                    self.cylinderBoard[move.endRow][move.endCol] = pieceToMove
                # Remove that piece from the original array
                move.startArray[move.startCol] = "--"
                self.movesStack.append(move)
                # Switch which player is going
                self.player1Turn = not self.player1Turn
                return True
            else:
                return False



    #Undoes the last move made
    def UndoMove(self):
        #Check that a move has been made
        if (len(self.movesStack) > 0):
            #Get the last move made from the movesStack
            moveToUndo = self.movesStack.pop()
            #Try acting as if it was a 2D array
            try:
                # Place the piece in its original location
                moveToUndo.startArray[moveToUndo.startRow][moveToUndo.startCol] = moveToUndo.pieceToMove
            # If that fails, act as if it is a 1D array
            except:
                # Place the piece in its original location
                moveToUndo.startArray[moveToUndo.startCol] = moveToUndo.pieceToMove
            #Remove the piece from its ending position
            #If it's a peg, remove it from the peg board
            if (moveToUndo.pieceToMove[1] == "p"):
                self.pegBoard[moveToUndo.endRow][moveToUndo.endCol] = "--"
            # Otherwise, it's a cylinder - remove it from the cylinder board
            else:
                self.cylinderBoard[moveToUndo.endRow][moveToUndo.endCol] = "--"

            #Switch which player's move it is as we need to go back to how it was before the player made the move
            self.player1Turn = not self.player1Turn
        else:
            print("Attempted to undo when no moves have been made...")

    # Gets a list of every legal move
    def GetAllValidMoves(self, colour):
        moves = []
        # Loop through every position on the board
        for row in range(0, len(self.pegBoard)):
            for col in range(0, len(self.pegBoard[row])):
                if (self.pegBoard[row][col] == "--" or (self.cylinderBoard[row][col][0] != colour and self.cylinderBoard[row][col][1] == "h")) and (
                        self.cylinderBoard[row][col] == "--" or self.pegBoard[row][col][0] != colour):
                    # this slot on the board is available
                    if (colour == "y"):
                        hasCylinder = False
                        if (self.cylinderBoard[row][col] == "--"):
                            if (self.pegBoard[row][col] == "--"):
                                for i in range(0, len(self.player1CylinderStorage)):
                                    if (self.player1CylinderStorage[i][1] == "c"):
                                        moves.append(Move(self.player1CylinderStorage, (999, i), (row, col)))
                                        hasCylinder = True
                                        break
                            for i in range(0, len(self.player1CylinderStorage)):
                                if (self.player1CylinderStorage[i][1] == "h"):
                                    moves.append(Move(self.player1CylinderStorage, (999, i), (row, col)))
                                    hasCylinder = True
                                    break
                        else:
                            hasCylinder = True
                        hasPeg = False
                        if (self.pegBoard[row][col] == "--" and self.cylinderBoard[row][col][1] != "f" and self.cylinderBoard[row][col][0] != colour):
                            for i in range(0, len(self.player1PegStorage)):
                                if (self.player1PegStorage[i][1] == "p"):
                                    moves.append(Move(self.player1PegStorage, (999, i), (row, col)))
                                    hasPeg = True
                                    break
                        else:
                            hasPeg = True
                        if (not hasCylinder):
                            for row2 in range(0, len(self.cylinderBoard)):
                                for col2 in range(0, len(self.cylinderBoard[row2])):
                                    if self.cylinderBoard[row2][col2] == colour + "c":
                                        moves.append(Move(self.cylinderBoard, (row2, col2), (row, col)))
                        if (not hasCylinder):
                            for row2 in range(0, len(self.cylinderBoard)):
                                for col2 in range(0, len(self.pegBoard[row2])):
                                    if self.cylinderBoard[row2][col2] == colour + "h":
                                        moves.append(Move(self.cylinderBoard, (row2, col2), (row, col)))
                        if (not hasPeg):
                            for row2 in range(0, len(self.pegBoard)):
                                for col2 in range(0, len(self.pegBoard[row2])):
                                    if self.pegBoard[row2][col2] == colour + "p":
                                        moves.append(Move(self.pegBoard, (row2, col2), (row, col)))
                    else:
                        hasCylinder = False

                        if (self.cylinderBoard[row][col] == "--"):
                            if (self.pegBoard[row][col] == "--"):
                                for i in range(0, len(self.player2CylinderStorage)):
                                    if (self.player2CylinderStorage[i][1] == "c"):
                                        moves.append(Move(self.player2CylinderStorage, (999, i), (row, col)))
                                        hasCylinder = True
                                        break
                            for i in range(0, len(self.player2CylinderStorage)):
                                if (self.player2CylinderStorage[i][1] == "h"):
                                    moves.append(Move(self.player2CylinderStorage, (999, i), (row, col)))
                                    hasCylinder = True
                                    break
                        else:
                            hasCylinder = True
                        hasPeg = False
                        if (self.pegBoard[row][col] == "--" and self.cylinderBoard[row][col][1] != "f" and self.cylinderBoard[row][col][0] != colour):
                            for i in range(0, len(self.player2PegStorage)):
                                if (self.player2PegStorage[i][1] == "p"):
                                    moves.append(Move(self.player2PegStorage, (999, i), (row, col)))
                                    hasPeg = True
                                    break
                        else:
                            hasPeg = True
                        if (not hasCylinder):
                            for row2 in range(0, len(self.cylinderBoard)):
                                for col2 in range(0, len(self.cylinderBoard[row2])):
                                    if self.cylinderBoard[row2][col2] == colour + "c":
                                        moves.append(Move(self.cylinderBoard, (row2, col2), (row, col)))

                        if (not hasCylinder):
                            for row2 in range(0, len(self.cylinderBoard)):
                                for col2 in range(0, len(self.pegBoard[row2])):
                                    if self.cylinderBoard[row2][col2] == colour + "h":
                                        moves.append(Move(self.cylinderBoard, (row2, col2), (row, col)))
                        if (not hasPeg):
                            for row2 in range(0, len(self.pegBoard)):
                                for col2 in range(0, len(self.pegBoard[row2])):
                                    if self.pegBoard[row2][col2] == colour + "p":
                                        moves.append(Move(self.pegBoard, (row2, col2), (row, col)))

        return moves


    #Checks if a move is legal
    def ValidateMove(self, move, pieceToMove):
        # If the piece is a peg
        if (move.startArray == self.cylinderBoard):
            if (self.player1Turn and self.player1CylinderStorage == ["--", "--", "--", "--", "--", "--", "--", "--"]) or (not self.player1Turn and self.player2CylinderStorage == ["--", "--", "--", "--", "--", "--", "--", "--"]):
                pass
            else:
                return False
        elif (move.startArray == self.pegBoard):
            if (self.player1Turn and self.player1PegStorage == ["--", "--", "--", "--", "--", "--", "--", "--"]) or (not self.player1Turn and self.player2PegStorage == ["--", "--", "--", "--", "--", "--", "--", "--"]):
                pass
            else:
                return False

        if (pieceToMove[1] == "p"):
            #Check that the ending destination is either empty or contains only a hollow cylinder of the opposite colour
            if ((self.cylinderBoard[move.endRow][move.endCol] == "--" or (self.cylinderBoard[move.endRow][move.endCol][0] != pieceToMove[0] and self.cylinderBoard[move.endRow][move.endCol][1] == "h")) and self.pegBoard[move.endRow][move.endCol] == "--"):
                return True
            else:
                return False
        #if the piece is a hollow cyinder
        elif pieceToMove[1] == "h":
            # Check that the ending destination is either empty or contains only a peg of the opposite colour
            if ((self.pegBoard[move.endRow][move.endCol] == "--" or (self.pegBoard[move.endRow][move.endCol][0] != pieceToMove[0] and self.pegBoard[move.endRow][move.endCol][1] == "p")) and self.cylinderBoard[move.endRow][move.endCol] == "--"):
                return True
            else:
                return False
        #if the piece is a full cylinder
        elif pieceToMove[1] == "c":
            # Check that the ending destination is empty
            if (self.pegBoard[move.endRow][move.endCol] == "--" and self.cylinderBoard[move.endRow][move.endCol] == "--"):
                return True
            else:
                return False
        #The piece is not recognised so the move is not valid
        else:
            return False

    #Check to see if a player has won
    def CheckForWin(self):
        #Check verticals
        for row in range(0, len(self.pegBoard)-4):
            for col in range(0, len(self.pegBoard[row])):
                if (self.CheckCoordVertical(row, col)):
                    return True
        #Check horizontals
        for row in range(0, len(self.pegBoard)):
            for col in range(0, len(self.pegBoard[row])-4):
                if (self.CheckCoordHorizontal(row, col)):
                    return True

        #Check positive diagonals
        for row in range(0, len(self.pegBoard)-4):
            for col in range(0, len(self.pegBoard[row])-4):
                if (self.CheckCoordPosDiagonal(row, col)):
                    return True

        #Check negative diagonals
        for row in range(0, len(self.pegBoard)-4):
            for col in range(4, len(self.pegBoard[row])):
                if (self.CheckCoordNegDiagonal(row, col)):
                    return True

        #If no win has been found, return false
        return False

    def CheckCoordHorizontal(self, row, col):
        #Check for each pattern
        for winCondition in self.winConditions:
            #Check red
            colour = "r"
            successCount = 0
            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (
                        self.pegBoard[row][col + i][0] == colour and self.pegBoard[row][col + i][1] == winCondition[0][i]):
                    #Check cylinders
                    if winCondition[1][i] == "-" or (self.cylinderBoard[row][col + i][0] == colour and (
                            self.cylinderBoard[row][col + i][1] == winCondition[1][i] or
                            self.cylinderBoard[row][col + i][1] == "h")):
                        successCount += 1
            if successCount == 5:
                self.winCoords = []
                for i in range(0, 5):
                    self.winCoords.append((row, col+i))
                return True

            #Check yellow
            colour = "y"
            successCount = 0

            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (self.pegBoard[row][col+i][0] == colour and self.pegBoard[row][col+i][1] == winCondition[0][i]):
                    # Check cylinders
                    if winCondition[1][i] == "-" or (self.cylinderBoard[row][col+i][0] == colour and (self.cylinderBoard[row][col+i][1] == winCondition[1][i] or self.cylinderBoard[row][col+i][1] == "h")):
                        successCount += 1
            if successCount == 5:
                self.winCoords = []
                for i in range(0, 5):
                    self.winCoords.append((row, col+i))
                return True


    def CheckCoordVertical(self, row, col):
        # Check for each pattern
        for winCondition in self.winConditions:
            # Check red
            colour = "r"
            successCount = 0
            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (
                        self.pegBoard[row + i][col][0] == colour and self.pegBoard[row + i][col][1] == winCondition[0][i]):
                    # Check cylinders
                    if winCondition[1][i] == "-" or (self.cylinderBoard[row + i][col][0] == colour and (
                            self.cylinderBoard[row + i][col][1] == winCondition[1][i] or
                            self.cylinderBoard[row + i][col][1] == "h")):
                        successCount += 1
            if successCount == 5:
                self.winCoords = []
                for i in range(0, 5):
                    self.winCoords.append((row + i, col))
                return True

            # Check yellow
            colour = "y"
            successCount = 0
            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (self.pegBoard[row + i][col][0] == colour and self.pegBoard[row + i][col][1] == winCondition[0][i]):
                    # Check cylinders
                    if winCondition[1][i] == "-" or (self.cylinderBoard[row + i][col][0] == colour and (self.cylinderBoard[row + i][col][1] == winCondition[1][i] or self.cylinderBoard[row+i][col][1] == "h")):
                        successCount += 1
            if successCount == 5:
                self.winCoords = []
                for i in range(0, 5):
                    self.winCoords.append((row + i, col))
                return True


    def CheckCoordPosDiagonal(self, row, col):
        # Check for each pattern
        for winCondition in self.winConditions:
            # Check red
            colour = "r"
            successCount = 0
            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (self.pegBoard[row + i][col+i][0] == colour and self.pegBoard[row + i][col+i][1] == winCondition[0][i]):
                    # Check cylinders
                    if winCondition[1][i] == "-" or (self.cylinderBoard[row + i][col+i][0] == colour and (self.cylinderBoard[row + i][col+i][1] == winCondition[1][i] or self.cylinderBoard[row+i][col+i][1] == "h")):
                        successCount += 1
            if successCount == 5:
                self.winCoords = []
                for i in range(0, 5):
                    self.winCoords.append((row + i, col+i))
                return True

            # Check yellow
            colour = "y"
            successCount = 0
            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (self.pegBoard[row + i][col+i][0] == colour and self.pegBoard[row + i][col+i][1] == winCondition[0][i]):
                    # Check cylinders
                    if winCondition[1][i] == "-" or (self.cylinderBoard[row + i][col+i][0] == colour and (self.cylinderBoard[row + i][col+i][1] == winCondition[1][i] or self.cylinderBoard[row+i][col+i][1] == "h")):
                        successCount += 1
            if successCount == 5:
                self.winCoords = []
                for i in range(0, 5):
                    self.winCoords.append((row + i, col+i))
                return True


    def CheckCoordNegDiagonal(self, row, col):
        # Check for each pattern
        for winCondition in self.winConditions:
            # Check red
            colour = "r"
            successCount = 0
            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (self.pegBoard[row + i][col-i][0] == colour and self.pegBoard[row + i][col-i][1] == winCondition[0][i]):
                    # Check cylinders
                    if winCondition[1][i] == "-" or (self.cylinderBoard[row + i][col-i][0] == colour and (self.cylinderBoard[row + i][col-i][1] == winCondition[1][i] or self.cylinderBoard[row+i][col-i][1] == "h")):
                        successCount += 1
            if successCount == 5:
                self.winCoords = []
                for i in range(0, 5):
                    self.winCoords.append((row + i, col-i))
                return True

            # Check yellow
            colour = "y"
            successCount = 0
            for i in range(0, 5):
                # check pegs
                if winCondition[0][i] == "-" or (self.pegBoard[row + i][col-i][0] == colour and self.pegBoard[row + i][col-i][1] == winCondition[0][i]):
                    # Check cylinders
                    if winCondition[1][i] == "-" or (self.cylinderBoard[row + i][col-i][0] == colour and (self.cylinderBoard[row + i][col-i][1] == winCondition[1][i] or self.cylinderBoard[row+i][col-i][1] == "h")):
                        successCount += 1
            if successCount == 5:
                self.winCoords = []
                for i in range(0, 5):
                    self.winCoords.append((row + i, col-i))
                return True

#Used to represent an individual move
class Move:
    def __init__(self, startArray, startCoord, endCoord):
        #The array the piece is being removed from
        self.startArray = startArray
        #The position in the array the piece is being removed from
        self.startRow = startCoord[0]
        self.startCol = startCoord[1]
        #The position on the board the piece is being moved to
        self.endRow = endCoord[0]
        self.endCol = endCoord[1]
        self.pieceToMove = "--"
        try:
            self.pieceToMove = startArray[self.startRow][self.startCol]
        except:
            self.pieceToMove = startArray[self.startCol]

class EndPosMove:
    def __init__(self, pieceToMove, endCoord):

        #The position on the board the piece is being moved to
        self.endRow = endCoord[0]
        self.endCol = endCoord[1]
        self.pieceToMove = pieceToMove

#Handles connecting to a server and sending/recieving data
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.244"

        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        pass

    def send(self, data):
        pass

