#! /usr/bin/env python

#This is a folder cleaning script for cleaning up equest output.
#It targets one specific destination folder.
#It will scrub that folder, and every folder in that directory,
#leaving only necessary eQUEST files.


import os




CleanerFolder = "C:/Users/dlaney/Desktop/Cleaner/"


for root, dirs, files in os.walk(CleanerFolder):
    for f in files:
        #print os.path.join(root,f)
        #preserve only .cvs, .sim, .inp, and .pd2 files
        if ".SIM" not in f:
            if ".csv" not in f:
                if ".inp" not in f:
                    if ".PD2" not in f:
                        if ".prd" not in f:
                            if ".pd2" not in f:
                                print("Removing: ", os.path.join(root,f))
                                os.remove(os.path.join(root,f))
