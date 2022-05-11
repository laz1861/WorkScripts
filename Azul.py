#! /usr/env/python3

#This is an azul simulator

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#this will be an object-oriented attempt to simulate the game of azul

import random
#########################################################################
class pool_gen:
    #this is a class that contains the construct for the draw pool
    #the tiles in this case will be represented as numbers, 1 through 5
    def __init__(self):
        self.tiles = list()
        for i in range(20):
            self.tiles.append("A")
            self.tiles.append("B")
            self.tiles.append("C")
            self.tiles.append("D")
            self.tiles.append("E")

    def output(self):
        #simple output for debugging
        print("Current Pool:\n", self.tiles)

    def shuffle(self):
        #a function to shuffle the pool
        random.shuffle(self.tiles)

    def draw(self):
        random.shuffle(self.tiles)
        drawn_tile=self.tiles.pop()
        return drawn_tile

        

#########################################################################
   

#########################################################################
class player:
    #create an object to hold information about players
    def __init__(self,player_name):
        #hold a name for a player
        self.name=player_name
        #this is the tile placement board for a player, and is used to score
        self.wall=[['a','b','c','d','e'],
                   ['e','a','b','c','d'],
                   ['d','e','a','b','c'],
                   ['c','d','e','a','b'],
                   ['b','c','d','e','a'],]
        #this is the tile loader board for the player.  The player moves tiles 
        #from the factory to their loader during a round.
        #tiles are moved from the loader to the board at the end of the round
        self.pattern=[[0],
                      [0, 0],
                      [0,0,0],
                      [0,0,0,0],
                      [0,0,0,0,0]]
        #this is the overflow.  This is where the penalty tile and unused tiles go
        self.floor=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        #this is the score for the player
        self.score=0
        
    def status(self):
        #this is an output function to display the player status
        print("\n" + self.name + "'s game board looks like this:")
        print("        " + str(self.pattern[0][0])+ "   " + self.wall[0][0] + " "+ self.wall[0][1] + " "+ self.wall[0][2] + " "+ self.wall[0][3] + " "+ self.wall[0][4])
        print("      " + str(self.pattern[1][0]) + " " + str(self.pattern[1][1])+ "   " + self.wall[1][0] + " "+ self.wall[1][1] + " "+ self.wall[1][2] + " "+ self.wall[1][3] + " "+ self.wall[1][4])
        print("    " + str(self.pattern[2][0]) + " " + str(self.pattern[2][1]) + " " + str(self.pattern[2][2])+ "   " + self.wall[2][0] + " "+ self.wall[2][1] + " "+ self.wall[2][2] + " "+ self.wall[2][3] + " "+ self.wall[2][4])
        print("  " + str(self.pattern[3][0]) + " " + str(self.pattern[3][1]) + " " + str(self.pattern[3][2]) + " " + str(self.pattern[3][3])+ "   " + self.wall[3][0] + " "+ self.wall[3][1] + " "+ self.wall[3][2] + " "+ self.wall[3][3] + " "+ self.wall[3][4])
        print(str(self.pattern[4][0]) + " " + str(self.pattern[4][1]) + " " + str(self.pattern[4][2]) + " " + str(self.pattern[4][3]) + " " + str(self.pattern[4][4])+ "   " + self.wall[4][0] + " "+ self.wall[4][1] + " "+ self.wall[4][2] + " "+ self.wall[4][3] + " "+ self.wall[4][4])
        

        print("\n" + self.name + "'s floor tiles are: ")
        print(self.floor)
        
#########################################################################
class game:
    #create an object to hold information about the game state outside the playres
    def __init__(self,num_players):
        self.players=num_players
        #set the number of factories based on the number if players
        if num_players==2:
            self.factory_count=5
        elif num_players==3:
            self.factory_count=7
        elif num_players==4:
            self.factory_count=9
        else:
            print("Error, incorrect number of players")
            
        #create a list of player objects
        self.players=list()
        for i in range(num_players):
            if i == 0:
                self.players.append(player("Alice"))
            elif i == 1:
                self.players.append(player("Bob"))
            elif i == 2:
                self.players.append(player("Charles"))
            elif i ==3:
                self.players.append(player("Dee"))
                
        #initialize an activeplayer value to zero, so first playre will start
        #initialize starting player to increment between rounds
        self.startingplayer=0
        self.activeplayer= 0
            
        #create a blank factory collection
        self.factories=list()
        
        #add an empty factory for the count
        for i in range(self.factory_count):
            self.factories.append([0,0,0,0])    
        
        #this is a place to collect the used tiles
        self.usedtiles=list()
        #this is the place to collect the tiles in the center after removal from the factories
        self.centertiles=list()
        #use this to track if the center -1 tile is in the center for the round
        #if true, if a player draws from the center they get a penalty
        #if false, no penalty is applied for taking from the center
        self.penalty=True
        #set this to true.  once false, the game is over and scores are final
        self.active=True
        #create the set of tiles for the game
        self.pool=pool_gen()
        
    def round_start(self):
        #this function is used to set the board up for a round
        #it starts by loading the factories
        
        #load the center with the penalty tile
        self.centertiles.append(-1)
        
        #shuffe the pool
        random.shuffle(self.pool.tiles)
        
        #load all the factories with tiles from the pool
        for i in range(self.factory_count):
            for j in range(4):
                #if the pool is empty, return the used tiles to the pool and shuffle
                if len(self.pool.tiles)==0:
                    self.pool.tiles=self.usedtiles
                    self.usedtiles=list()
                    random.shuffle(self.pool)
                
                self.factories[i][j]=self.pool.tiles.pop(0)
            self.factories[i].sort()
        
        self.startingplayer+=1
        if self.startingplayer>len(self.players):
            self.startingplayer=1
            
        self.activeplayer=self.startingplayer
            
        
        
    def player_action(self):
        #this is a method that defines a players action on their turn
        #the steps are for the active player:
            #selects which factory (or center) to pull from
            #selects which tile type to pull from the selected source
            #selects a row (or rows) on their pattern board to place the tiles
            #puts any extra tiles in the floor
            #if selected from factory, move excess tiles to center
            #increment active player
            
            #first, display the game status
            self.game_status()
            self.players[self.activeplayer-1].status()
            
    
    def game_status(self):
        #this is a methode to output the relevant game status
        
        #output the factory status
        for i in range(self.factory_count):
            print("Factory " + str(i+1) + " contains: " , self.factories[i])
            
        #output the center tiles
        print("\nThe center contains the following tiles: ", self.centertiles)
            
        
        
#########################################################################
mygame=game(3)
def window():
    app=QApplication(sys.argv)
    w = QWidget()
    b = QLabel(w)
    b.setText("Hello World!")
    w.setGeometry(100, 100, 1600, 900)
    b.move(50,20)
    w.setWindowTitle("Azul Simulator")
    w.show()
    sys.exit(app.exec_())
    
    

#if __name__ == '__main__':
#    window()