#! /usr/bin/env python
#building a sudoku solver

class sudoku:
    #create a sudoku matrix
    #it is made up of 9 grids
    #each grid is numbered:
    # 0|1|2
    # 3|4|5
    # 6|7|8
    #each grid is made of a sub-grid with the same coordinates
    def __init__(self):
        #this function initialized an object
        #the grid property is the actual puzzle board
        #by default, it is filled with blanks
        #the possibles list is a list of all possible numbers
        #that can be in that spot
        #by default, it is filled with 1 through 9
        self.grid = list()
        self.possibles=list()
        for i in range( 0, 9):
            for j in range(0,9):
                self.grid.append(" ")
                placeholder=list()
                for k in range(0,9):
                    placeholder.append(str(k+1))
                self.possibles.append(placeholder)
        #create a boolean that will indicate if the solution has moved forward
        self.changed = True
        
                
    def load_value(self, value, coord):
        #this is a method that should load a value into the array
        #print(coord)
        self.grid[int(9*coord[0])+coord[1]]=value
        self.remove_possibles_grid(value, coord)
        self.remove_possibles_row(value, coord)
        self.remove_possibles_column(value,coord)
        self.possibles[int(coord[0]*9)+coord[1]]=list()
        
    def remove_possibility(self,value,index):
        pos_list = self.possibles[int(index)]
        #create an iterator
        possible_index=0
        for possible in pos_list:
            if possible == str(value):
                #print("Removing value: ",value)
                #print("from index: ",index)
                self.possibles[int(index)].pop(possible_index)
            possible_index+=1

    def remove_possibles_grid(self, value, coord):
        #this function will remove the value from being possible
        #for ever other space in the current grid
        for j in range(0,9):
            #print "in grid " + str(coord[0]) + " in spot " + str(j)
            self.remove_possibility(value,coord[0]*9+j)

    def remove_possibles_row(self, value, coord):
        #this function will remove the value from being possible
        #for every other space in the current row
        #start by taking the coordinate and translating to an index
        index = int(9*coord[0]+coord[1])
        #using the same i,j,k,l iterators, we can extract out values
        l=int(index/27)
        index=index%27
        k=int(index/9)
        index=index%9
        j=int(index/3)
        index=index%3
        i=int(index)
        #to pull out the index for every element in a given row
        #we hold l and j constant, then interate over i and k
        
        for k in range(0,3):
            for i in range(0,3):
                self.remove_possibility(value,27*l+9*k+3*j+i)

    def remove_possibles_column(self, value, coord):
        #this function will remove the value from being possible
        #for every other space in the current column
        #start by taking the coordinate and translating to an index
        index = int(9*coord[0]+coord[1])
        #using the same i,j,k,l iterators, we can extract out values
        l=int(index/27)
        index=index%27
        k=int(index/9)
        index=index%9
        j=int(index/3)
        index=index%3
        i=int(index)
        #to pull out the index for every element in a given row
        #we hold i and k constant, then interate over j and l
        
        for l in range(0,3):
            for j in range(0,3):
                self.remove_possibility(value,27*l+9*k+3*j+i)

    def solver(self):
        #this is the solver for the puzzle
        #it will call the individual solving functions

        #test 1
        #the simplest test is to see if any spots on the puzzle
        #have exactly one possibility on the grid
        self.solve_single_possibility()

        #test 2
        #the next test is to see if in a given sub-grid
        #if there is only one possible location for a given value
        self.solve_single_possible_grid()

        #test 3
        #test to see if there is only one option for a given value on a row
        self.solve_single_possible_row()

        #test 4
        #test to see if there is only one option for a given value on a column
        self.solve_single_possible_column()

    def solve_single_possibility(self):
        #this solver will search through the entire list of possibilities
        #if any of them are of length 1, then load that value
        index = 0
        for pos_list in self.possibles:
            if len(pos_list) == 1:
                self.load_value(pos_list[0],(int(index/9),index%9))
                self.changed = True
                print("Singe Possibility at index ", index)
                printgrid(self)
            index+=1

    def solve_single_possible_grid(self):
        #this solver will search through each number
        #it will iterate over every sub-grid
        #if there is only one possible for that grid, it will load that value
        for subgrid in range(0,9):
            for value in range (1,10):
                #create an empty list of the positions we find a match
                index = list()
                for position in range(0,9):
                    pos_list = self.possibles[subgrid*9+position]
                    for possible in pos_list:
                        
                        if str(value) == possible:
                            #in the event of a match, add the index to the list
                            index.append(subgrid*9+position)
                #if after searching each position the index only has 
                #one item, then it's the only possible for that subgrid
                #load that value into the index position
                if len(index)==1:
                    self.load_value(value,(int(index[0]/9),index[0]%9))
                    self.changed = True
                    print("Single Grid Possible at index ", index)
                    printgrid(self)

    def solve_single_possible_row(self):
        #this solver will search through each row
        #if there is only one possible location for a given value in a row, then add that one
        for l in range(0,3):
            for j in range(0,3):
                #this iterate give us each row, so check each value in each row
                for value in range(1,10):
                    #create an empty list of the positions in which we find a match for value
                    matches=list()
                    for k in range(0,3):
                        for i in range(0,3):
                            for possible in self.possibles[i+3*j+9*k+27*l]:
                                if str(value) == possible:
                                    matches.append(i+3*j+9*k+27*l)
                    #if after searching through each row for a match
                    #if there is only one, then we have found a result
                    #print("row matches = ", matches)
                    if len(matches)==1:
                        self.load_value(value,(int(matches[0]/9),int(matches[0]%9)))
                        self.changed = True
                        print("Single Row Possible at index ",matches[0])
                        printgrid(self)
                        
                                
                    
    def solve_single_possible_column(self):
        #this solver will search through each row
        #if there is only one possible for that row, it will load that value
        for k in range(0,3):
            for i in range(0,3):
                #this iterate give us each column, so check each value in each row
                for value in range(1,10):
                    #create an empty list of the positions in which we find a match for value
                    matches=list()
                    for l in range(0,3):
                        for j in range(0,3):
                            for possible in self.possibles[i+3*j+9*k+27*l]:
                                if str(value) == possible:
                                    matches.append(i+3*j+9*k+27*l)
                    #if after searching through each row for a match
                    #if there is only one, then we have found a result
                    if len(matches)==1:
                        self.load_value(value,(int(matches[0]/9),int(matches[0]%9)))
                        self.changed = True
                        print("Single Column Possible at index ",matches[0])
                        printgrid(self)
                    
def printgrid(puzzle):
    #this method should format and print the existing grid
    print("Grid Output\n")
    for l in range(0,3):
        for j in range(0,3):
            outstring = ""
            for k in range(0,3):
                for i in range(0,3):
                    outstring+=str(puzzle.grid[i+3*j+9*k+27*l])
                    if i <3:
                        outstring+=" "
                if k < 2:
                    outstring+="|"
            print(outstring)
        if l<2:
            print("--------------------")
            
            
def printpossibles(puzzle):
    #this function should print the possibles for each grid index
    #one per row
    for possibles in puzzle.possibles:
        print(possibles)

#====================
#create object
puzzle = sudoku()

###Easy Puzzle, solves in one simple test
###load object with given values
##puzzle.load_value(4,(1,1))
##puzzle.load_value(2,(1,2))
##puzzle.load_value(9,(2,0))
##puzzle.load_value(1,(2,1))
##puzzle.load_value(9,(0,3))
##puzzle.load_value(2,(0,4))
##puzzle.load_value(8,(1,5))
##puzzle.load_value(7,(2,4))
##puzzle.load_value(4,(0,8))
##puzzle.load_value(1,(1,7))
##puzzle.load_value(5,(2,7))
##puzzle.load_value(6,(3,2))
##puzzle.load_value(5,(4,1))
##puzzle.load_value(2,(5,0))
##puzzle.load_value(9,(5,2))
##puzzle.load_value(7,(4,3))
##puzzle.load_value(9,(4,5))
##puzzle.load_value(2,(3,6))
##puzzle.load_value(5,(3,8))
##puzzle.load_value(8,(4,7))
##puzzle.load_value(3,(5,6))
##puzzle.load_value(4,(6,1))
##puzzle.load_value(7,(7,1))
##puzzle.load_value(5,(8,0))
##puzzle.load_value(5,(6,4))
##puzzle.load_value(8,(7,3))
##puzzle.load_value(9,(8,4))
##puzzle.load_value(1,(8,5))
##puzzle.load_value(7,(6,7))
##puzzle.load_value(3,(6,8))
##puzzle.load_value(6,(7,6))
##puzzle.load_value(9,(7,7))

###hard puzzle
##puzzle.load_value(6,(0,1))
##
##puzzle.load_value(1,(1,3))
##puzzle.load_value(4,(1,5))
##puzzle.load_value(8,(1,6))
##puzzle.load_value(5,(1,7))
##
##puzzle.load_value(1,(2,1))
##puzzle.load_value(9,(2,6))
##puzzle.load_value(6,(2,8))
##
##puzzle.load_value(3,(3,1))
##puzzle.load_value(4,(3,2))
##puzzle.load_value(2,(3,3))
##
##puzzle.load_value(7,(4,1))
##puzzle.load_value(3,(4,7))
##
##puzzle.load_value(5,(5,6))
##puzzle.load_value(8,(5,7))
##
##puzzle.load_value(5,(6,0))
##puzzle.load_value(3,(6,2))
##puzzle.load_value(2,(6,5))
##
##puzzle.load_value(1,(7,1))
##puzzle.load_value(5,(7,3))
##puzzle.load_value(3,(7,5))
##
##puzzle.load_value(7,(8,0))
##puzzle.load_value(2,(8,7))

puzzle.load_value(1,(0,3))

puzzle.load_value(2,(1,0))
puzzle.load_value(9,(1,2))
puzzle.load_value(8,(1,4))
puzzle.load_value(7,(1,8))

puzzle.load_value(7,(2,0))
puzzle.load_value(8,(2,1))
puzzle.load_value(6,(2,2))
puzzle.load_value(3,(2,5))
puzzle.load_value(5,(2,8))

puzzle.load_value(9,(3,0))
puzzle.load_value(5,(3,4))
puzzle.load_value(8,(3,5))
puzzle.load_value(2,(3,7))

puzzle.load_value(2,(4,1))

puzzle.load_value(1,(5,3))
puzzle.load_value(5,(5,6))
puzzle.load_value(7,(5,7))
puzzle.load_value(8,(5,8))

puzzle.load_value(3,(6,6))
puzzle.load_value(5,(6,8))

puzzle.load_value(4,(7,1))
puzzle.load_value(2,(7,2))
puzzle.load_value(7,(7,6))

puzzle.load_value(6,(8,0))
puzzle.load_value(9,(8,3))

printgrid(puzzle)

#now loop through solutions
#the puzzle should continue through the solve function
iterations = 0
while puzzle.changed:
    iterations+=1
    print("\nITERATIONS: ", iterations)
    #immediately set the changed stat to false
    #the loop will only repeat if the solver has progressed towards a solution
    puzzle.changed = False
    puzzle.solver()
    
