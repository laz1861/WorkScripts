#!/usr/bin/env python3

#This is a simulation for strategic modeling
#we will model the following strategies

#random
#a100 - always pick A
#b100 - always pick B
#Greedy - always pick what has the best return
#Generous - always pick what is best for opponent
#Minimax - I still need to look this one up
#TitForTat - pick whatever opponent picked last round
#BeatLast - pick whatever would have been better the last round

from random import randint

######################################################################
def score_output(score,players,opponents):
    #this is a function to define how the score is output
    #we need to start spacing out a table, then display the names, then post the scores
    starter_spacing = 0
    for name in players:
        if len(name)>starter_spacing:
            starter_spacing=len(name)
            
    starter_spacing = starter_spacing+1
    
    for row in range(len(score)+1):
        #print("Row =",row)
        output_text = ""
        total=0
        for col in range(len(score[0])+2):
            #print("Col=",col)
            if row==0:
                if col == 0:
                    output_text=output_text+"         "
                elif col<=len(score[row]):
                    for i in range(starter_spacing-len(str(opponents[col-1]))-1):
                        output_text=output_text+chr(32)
                    output_text=output_text+opponents[col-1]
                    output_text=output_text+chr(32)
                else:
                    output_text=output_text+"      Total"
                        
                
            else:
                if col ==0:
                    for i in range(starter_spacing-len(players[row-1])-1):
                        output_text=output_text+chr(32)
                    output_text=output_text+players[row-1]
                    output_text=output_text+":"
                elif col<=len(score[row-1]):
                    for i in range(starter_spacing-len(str(score[row-1][col-1]))-2):
                        output_text = output_text + chr(32)
                    output_text = output_text + str(score[row-1][col-1]) + chr(32)+chr(32)
                    total=total+score[row-1][col-1]
                else:
                    for i in range(starter_spacing-len(str(total))):
                        output_text = output_text +chr(32)
                    output_text = output_text+str(total)
                

        print(output_text)
                    
######################################################################

def contest(player,opponent,v1,v2,v3,v4):
    

    #define a constant that will set the number of games between opponents for each contest
    gamecount = 20
    for game in range(gamecount):
        #initialized player_last and opponent_last as zero
        player_last=0
        opponent_last=0
        
        if player == 0:
            player_choice = rand_choice(v1,v2,v3,v4,player_last,opponent_last)
        elif player ==1:
            player_choice = A100_choice(v1,v2,v3,v4,player_last,opponent_last)
        elif player ==2:
            player_choice = B100_choice(v1,v2,v3,v4,player_last,opponent_last)
        elif player == 3:
            player_choice = Greedy_choice(v1,v2,v3,v4,player_last,opponent_last)
        elif player == 4:
            player_choice = Generous_choice(v1,v2,v3,v4,player_last,opponent_last)
        elif player == 5:
            player_choice = MM_choice(v1,v2,v3,v4,player_last,opponent_last)
        elif player == 6:
            player_choice = T4T_choice(v1,v2,v3,v4,player_last,opponent_last)
        elif player == 7:
            player_choice = BL_choice(v1,v2,v3,v4,player_last,opponent_last)

            
        #use the same logic for the opponent choice, but swap v2 and v3, and opponent for player choice
        if opponent == 0:
            opponent_choice = rand_choice(v1,v3,v2,v4,opponent_last,player_last)
        elif opponent ==1:
            opponent_choice = A100_choice(v1,v3,v2,v4,opponent_last,player_last)
        elif opponent == 2:
            opponent_choice = B100_choice(v1,v3,v2,v4,opponent_last,player_last)
        elif opponent == 3:
            opponent_choice = Greedy_choice(v1,v3,v2,v4,opponent_last,player_last)
        elif opponent == 4:
            opponent_choice = Generous_choice(v1,v3,v2,v4,opponent_last,player_last)
        elif opponent == 5:
            opponent_choice = MM_choice(v1,v3,v2,v4,opponent_last,player_last)
        elif opponent == 6:
            opponent_choice = T4T_choice(v1,v3,v2,v4,opponent_last,player_last)
        elif opponent == 7:
            opponent_choice = BL_choice(v1,v3,v2,v4,opponent_last,player_last)
            
        player_last=player_choice
        opponent_last=opponent_choice
        score[player][opponent]+=eval_choice(player_choice,opponent_choice,v1,v2,v3,v4)
            
######################################################################

def eval_choice(player_choice,opponent_choice,v1,v2,v3,v4):
    if player_choice == 0:
        if opponent_choice == 0:
            return v1
        else:
            return v2
    else:
        if opponent_choice ==0:
            return v3
        else:
            return v4

######################################################################
def rand_choice(v1,v2,v3,v4,player_last,opponent_last):
    #random is not influenced by choices at all
    return randint(0,1)

######################################################################
def A100_choice(v1,v2,v3,v4,player_last,opponent_last):
    #always pick option a, represented by 0
    return 0

######################################################################
def B100_choice(v1,v2,v3,v4,player_last,opponent_last):
    #always pick option b, represented by 1
    return 1

######################################################################
def Generous_choice(v1,v2,v3,v4,player_last,opponent_last):
    #always pick whichever option has the highest possible outcome for opponent
    selection = 0
    #highlight all of the cases that we'd pick selection 1 over selection 0
    if v2>v1 and v2>v3:
        selection=1
    if v4>v1 and v4>v3:
        selection=1
    if v2==v3 and v4>v1:
        selection=1
    if v1==v4 and v2>v3:
        selection=1
    
    return selection

######################################################################
def Greedy_choice(v1,v2,v3,v4,player_last,opponent_last):
    #always pick whichever option has the highest possible outcome  
    selection = 0
    #highlight all of the cases that we'd pick selection 1 over selection 0
    if v3>v1 and v3>v2:
        selection=1
    if v4>v1 and v4>v2:
        selection=1
    if v2==v3 and v4>v1:
        selection=1
    if v1==v4 and v3>v2:
        selection=1
    
    return selection

######################################################################   
def T4T_choice(v1,v2,v3,v4,player_last,opponent_last):
    #always pick whichever the opponent chose last turn  
    return opponent_last

######################################################################
def BL_choice(v1,v2,v3,v4,player_last,opponent_last):
    #always pick what would have beaten the opponents last choice
    selection=0
    #highlight all of the cases that we'd pick selection 1 over selection 0
    if opponent_last == 0:
        if v3>=v1:
            selection=1
    else:
        if v4>=v2:
            seletion=1
    return selection

######################################################################
def MM_choice(v1,v2,v3,v4,player_last,opponent_last):
    #always pick what make the minimum possible score as high as possible
    selection=0
    #highlight all of the cases that we'd pick selection 1 over selection 0
    if v1<v3 and v1<v4:
        selection=1
    if v2<v3 and v2<v4:
        selection=1
    if v2==v3 and v4>v1:
        selection=1
    if v1==v4 and v2>v3:
        selection=1
    
    return selection

######################################################################
def win_counter(score):
    #import a score matrix, add up each row, and return the index of the highest point value
    #we will assume no ties here, and only count the number of times that a strategy bests all
    best=0
    #we will use 999 as a flag to show that there was a tie and no clear winner
    best_position = 999
    for row in range(len(score)):
        total=0
        for col in range(len(score[row])):
            total=total+score[row][col]
        #print(total)
        if total>best:
            #print("Better",total,row)
            best=total
            best_position=row
        elif total== best:
            #print("Tie",total,row)
            best_position=998
    return best_position
            
######################################################################
def yomi_calc(score):
    #import a score matrix, add up each row, and figure out how many strategies were beat
    #calulate a yomi based on the score and strategies beat
    yomi = [0 for i in range(len(score))]
    totals = [0 for i in range(len(score))]

    #calculate the total for each strategy and store the result
    for row in range(len(score)):
        total=0
        for col in range(len(score[row])):
            total=total+score[row][col]

        totals[row]=total

    #iterate through the totals for each strategy and count the number of strategies beaten
    for i in range(len(totals)):
        for j in range(len(totals)):
            if totals[j]<totals[i]:
                yomi[i]+=1

    #print("Beats=",yomi)
    #now yomi contains a count of how many strategies each strategy was beat
    #we need to replace any zeros with ones, and then multiply the totals by the beat count

    for i in range(len(yomi)):
        if yomi[i]==0:
            yomi[i]=totals[i]
        else:
            yomi[i]=yomi[i]*totals[i]
    return yomi
            
######################################################################

#create lists of Players
players = ["RN","A100","B100","Greedy","Generous","Minimax","TitForTat","BeatLast"]
opponents = players

win_count=[0 for x in range(8)]
tie_count=[0 for x in range(8)]
yomi=[0 for x in range(8)]

for i in range(10000):

    score = [[0 for col in range(8)] for row in range(8)]
    

    player_pool = 8#len(players)
    opponent_pool = 8#len(opponents)

    v1 = randint(1,10)
    v2 = randint(1,10)
    v3 = randint(1,10)
    v4 = randint(1,10)
    #print(v1,v2,v3,v4)
    for i in range(player_pool):
        for j in range(opponent_pool):
            contest(i,j,v1,v2,v3,v4)

    #score_output(score,players,opponents)
    win_position=win_counter(score)
    if win_position<900:
        win_count[win_position]+=1

    new_yomi=yomi_calc(score)

    yomi=[e1+e2 for e1,e2 in zip(yomi,new_yomi)]
    
print("Total wins: ",win_count)
print(yomi)
        
                    
