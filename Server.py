from Game import Game, Move
import socket
from _thread import *
import pickle
#get IP address of the machine this is running on to set up server
server = str(socket.gethostbyname(socket.gethostname()))
print(server)
#The port used
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Bind the server to the port
try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))
#Wait for a connection
s.listen()
print("Waiting for a connection, server started.")

#Dictionary of active games
games = {}
#Amount of active ids (players)
idCount = 0

#A game thread that handles sending and receiving data
def threadedClient(connection, player, gameId):
    global idCount
    #Send confirmation of connection
    connection.send(str.encode(str(player)))
    while True:
        try:
            #recieve data
            data = connection.recv(4096).decode()
            #Get which game the player we are receiving data from is playing
            if gameId in games:
                game = games[gameId]
                #If the data is empty, something has gone wrong, close the connection
                if data is None:
                    break
                else:
                    #decode the data
                    # Example of data = "1,1,6,6,1c" first 2 numbers are startCoords, second 2 endCoords, last coord represents a startArray
                    dataList = data.split(",")
                    if "," in data:
                        #Decode the startArray in the data
                        startArray = game.pegBoard
                        startArrayCode = dataList[4][:2]
                        if startArrayCode == "1c":
                            startArray = game.player1CylinderStorage
                        elif startArrayCode == "2c":
                            startArray = game.player2CylinderStorage
                        elif startArrayCode == "1p":
                            startArray = game.player1PegStorage
                        elif startArrayCode == "2p":
                            startArray = game.player2PegStorage
                        elif startArrayCode == "cb":
                            startArray = game.cylinderBoard
                        elif startArrayCode == "pb":
                            startArray = game.pegBoard
                        #Make the move send
                        game.MakeMove(Move(startArray, (int(dataList[0]), int(dataList[1])), (int(dataList[2]), int(dataList[3]))))
                    #Send the updated game back to the players
                    connection.sendall(pickle.dumps(game))
            else:
                break
        except error as e:
            print(e)
            break

    print("Lost connection with game " + str(gameId))
    #If we lose connection with one or both players, close the game
    try:
        del games[gameId]
        print("Closing game " + str(gameId))
    except:
        pass
    idCount -= 1
    connection.close()



while True:
    #Accepted an attempt to join the server
    connection, address = s.accept()
    print("Server connected to address " + str(address))
    idCount += 1
    player = 0
    gameId = (idCount-1)//2
    #if there are no players waiting, create a new game
    if idCount % 2 == 1:
        games[gameId] = Game()
        print("Initialising game " + str(gameId))
    #Else, add them to the existing game with a player waiting
    else:
        games[gameId].ready = True
        player = 1
    #Start the game thread
    start_new_thread(threadedClient, (connection, player, gameId))
