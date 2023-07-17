import socket
import pickle


#Represents a game, handles making moves
class Game:
    def __init__(self):
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

    #Carries out the input move on the boards and updates the movesStack
    def MakeMove(self, move):
        # Try acting as though the array is 2D
        try:
            # If it succeeds, the array is 2D
            pieceToMove = move.startArray[move.startRow][move.startCol]
            # Set the end location to the piece you want there
            if (pieceToMove[1] == "p"):
                self.pegBoard[move.endRow][move.endCol] = pieceToMove
            else:
                self.cylinderBoard[move.endRow][move.endCol] = pieceToMove
            # Remove that piece from the original array
            move.startArray[move.startRow][move.startCol] = "--"
        except:
            # If it fails, the array is 1D, so access it only using row.
            pieceToMove = move.startArray[move.startCol]
            # Set the end location to the piece you want there
            if (pieceToMove[1] == "p"):
                self.pegBoard[move.endRow][move.endCol] = pieceToMove
            else:
                self.cylinderBoard[move.endRow][move.endCol] = pieceToMove
            # Remove that piece from the original array
            move.startArray[move.startCol] = "--"

        self.movesStack.append(move)

    #Undoes the last move made
    def UndoMove(self):
        pass

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