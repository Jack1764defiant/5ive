from Game import Game, Move
import socket
from _thread import *
import sys
import pickle

# server = "10.131.129.221"#"192.168.1.244"
import socket
from _thread import *
import sys
import pickle

server = "192.168.1.244"#"10.131.129.221"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen()
print("Waiting for a connection, server started.")

connected = set()
games = {}
idCount = 0

def threadedClient(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))
    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if data is None or not data:
                    break
                else:
                    # Example of data = "1,1,6,6,1c" first 2 numbers are startCoords, second 2 endCoords, last coord represents a startArray
                    if ("," in data):
                        print(data)
                        startArray = game.pegBoard
                        if (data[8:10] == "1c"):
                            startArray = game.player1CylinderStorage
                        elif (data[8:10] == "2c"):
                            startArray = game.player2CylinderStorage
                        elif (data[8:10] == "1p"):
                            startArray = game.player1PegStorage
                        elif (data[8:10] == "2p"):
                            startArray = game.player2PegStorage
                        elif (data[8:10] == "cb"):
                            startArray = game.cylinderBoard
                        elif (data[8:10] == "pb"):
                            startArray = game.pegBoard
                        game.MakeMove(Move(startArray, (int(data[0]), int(data[2])), (int(data[4]), int(data[6]))))
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except error as e:
            print(e)
            break

    print("Lost connection.")

    try:
        del games[gameId]
        print("Closing game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to", addr)
    idCount += 1
    p = 0
    gameId = (idCount-1)//2
    if idCount % 2 == 1:
        games[gameId] = Game()
        print("Creating new game.")
    else:
        games[gameId].ready = True
        p = 1
    start_new_thread(threadedClient, (conn, p, gameId))
