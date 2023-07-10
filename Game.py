import socket
import pickle


#Represents a game, handles making moves
class Game:
    def __init__(self):
        self.pegBoard = [
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"]
        ]
        self.cylinderBoard = [
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--"]
        ]
        self.player1PegStorage = ["yp", "yp", "yp", "yp", "yp", "yp", "yp", "yp"]
        self.player1CylinderStorage = ["yc", "yc", "yc", "yc", "yh", "yh", "yh", "yh"]

        self.player2PegStorage = ["rp", "rp", "rp", "rp", "rp", "rp", "rp", "rp"]
        self.player2CylinderStorage = ["rc", "rc", "rc", "rc", "rh", "rh", "rh", "rh"]
        self.movesStack = []

    def MakeMove(self, move):
        pass

    def UndoMove(self):
        pass

    def GetAllValidMoves(self):
        pass

    def GetFullCylinderMoves(self):
        pass

    def GetHollowCylinderMoves(self):
        pass

    def GetPegMoves(self):
        pass

#Used to represent an individual move
class Move:

    def __init__(self, startArray, startCoord, endCoord):
        self.startArray = startArray
        self.startRow = startCoord[0]
        self.startCol = startCoord[1]
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