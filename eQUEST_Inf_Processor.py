#! /usr/bin/env python

#This script will process on eQUEST input file
#and it will change infiltration from the default pre-processed infiltration flow
#which is specified in CFM/ft^2
#To Air changes per hour

import os
import Tkinter, tkFileDialog
import shutil


infperim = .90
infplenum = 0.01
infcore = 0.25

dbg = True

root = Tkinter.Tk()
root.withdraw()

filepath = tkFileDialog.askopenfilename()
outfilepath = os.path.abspath("test.out")

with open(filepath,'rt') as sourcefile:
    if dbg: print "Opening Source File"
    with open(outfilepath,'w') as outfile:
        if dbg: print "Opening Output File"
        for testline in sourcefile:
            if testline.find(" = SPACE  ") <> -1:
                  if testline.find(" Perim Spc") <> -1:
                      perimeter = True
                  else:
                      perimeter = False

                  if testline.find(" Plnm") <> -1:
                      plenum = True
                  else:
                      plenum = False
                
            if testline.find("INF-FLOW/AREA")<>-1:
                if plenum :
                    outfile.write("   AIR-CHANGES/HR   = " +str(infplenum) + "     \n")
                else:
                    if perimeter:
                        outfile.write("   AIR-CHANGES/HR   = " +str(infperim) + "     \n")  
                    else:
                        outfile.write("   AIR-CHANGES/HR   = " +str(infcore) + "     \n")
            elif testline.find("AIR-CHANGES/HR") <> -1:
                if plenum :
                    outfile.write("   AIR-CHANGES/HR   = " +str(infplenum) + "     \n")
                else:
                    if perimeter:
                        outfile.write("   AIR-CHANGES/HR   = " +str(infperim) + "     \n")  
                    else:
                        outfile.write("   AIR-CHANGES/HR   = " +str(infcore) + "     \n")
                
            else: outfile.write(testline)
if dbg: print "Replacing Files"
shutil.copy(outfilepath,filepath)
if dbg: print "Deleting File"
os.remove(outfilepath)

if dbg: print "Mission Accomplished"
