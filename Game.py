import socket
import pickle


#Represents a game, handles making moves
class Game:
    def __init__(self, main):
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

    #Carries out the input move on the boards and updates the movesStack
    def MakeMove(self, move, isPlayer1Turn):
        # Try acting as though the array is 2D
        try:
            #Test by getting a value that would be out of bounds on the 1D arrays I am using
            move.startArray[6][6]
            # If it succeeds, the array is 2D
            pieceToMove = move.startArray[move.startRow][move.startCol]
            #Check if it is the correct turn for a yellow piece to be moved
            if ((pieceToMove[0] == "y" and isPlayer1Turn) or (pieceToMove[0] == "r" and not isPlayer1Turn)) and self.ValidateMove(move, pieceToMove):
                # Set the end location to the piece you want there
                if (pieceToMove[1] == "p"):
                    self.pegBoard[move.endRow][move.endCol] = pieceToMove
                else:
                    self.cylinderBoard[move.endRow][move.endCol] = pieceToMove
                # Remove that piece from the original array
                move.startArray[move.startRow][move.startCol] = "--"
                self.movesStack.append(move)
                return True
            else:
                return False
        except:
            # If it fails, the array is 1D, so access it only using column.
            pieceToMove = move.startArray[move.startCol]
            # Check if it is the correct turn for a red piece to be moved
            if ((pieceToMove[0] == "y" and isPlayer1Turn) or (pieceToMove[0] == "r" and not isPlayer1Turn)) and self.ValidateMove(move, pieceToMove):
                # Set the end location to the piece you want there
                if (pieceToMove[1] == "p"):
                    self.pegBoard[move.endRow][move.endCol] = pieceToMove
                else:
                    self.cylinderBoard[move.endRow][move.endCol] = pieceToMove
                # Remove that piece from the original array
                move.startArray[move.startCol] = "--"
                self.movesStack.append(move)
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
            self.main.player1Turn = not self.main.player1Turn

    # Gets a list of every legal move
    def GetAllValidMoves(self):
        pass

    #Gets a list of everywhere a full cylinder could be placed
    def GetFullCylinderMoves(self):
        pass

    # Gets a list of everywhere a hollow cylinder could be placed
    def GetHollowCylinderMoves(self):
        pass

    # Gets a list of everywhere a peg could be placed
    def GetPegMoves(self):
        pass

    #Checks if a move is legal
    def ValidateMove(self, move, pieceToMove):
        # If the piece is a peg
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