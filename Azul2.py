# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 14:43:25 2022

@author: dlaney
"""

class player:
    #create an object to hold information about players
    def __init__(self,player_name):
        self.name=player_name
        self.board=[[0]*5]*5
        self.loader=[[0],[0, 0],[0,0,0],[0,0,0,0],[0,0,0,0,0]]
        self.overflow=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

class game:
    #create an object to hold information about the game state outside the playres
    def __init__(self,num_players):
        self.players=num_players
        self.usedtiles=[[]]
        self.centertiles=[[]]
        self.active=True
        