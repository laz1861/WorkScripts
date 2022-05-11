#!/usr/bin/env python
# -*- coding: cp1252 -*-
#This program should merge available data from the source weather file
#and overwite the matching data in the target weather file

import os


infilepath =os.path.abspath("NOA Weather.txt")
outfilepath =os.path.abspath("MergedOutput.txt")
tarfilepath = os.path.abspath("WEATHER.FMT")

#=========Debugger==============
dbg = True


#=========Functions=============

def P_sat(T_db):
    Tc = FtoC(T_db)
    #constants accurate from -20C to 50C
    A = 6.116441 #constant
    m = 7.591386 #constant
    Tn = 240.7263 #constant
    return A* 10**((m*Tc)/(Tc+Tn)) #returns saturation pressure in hPa


def FtoC(Tf):
    Tc = (Tf-32)*5/9
    return Tc #return in degrees celcius

def CtoF(Tc):
    Tf = Tc*9/5+32
    return Tf #return in degrees farenheit 

def P_wat(P_sat,P_atm,T_wb,T_db):
    Tc_wb = FtoC(T_wb)
    Tc_db = FtoC(T_db)
    K = 0.000662 #1/°C, Constant
    Pw = P_sat*Tc_wb-P_atm*K*(Tc_db-Tc_wb)
    return Pw #returns partial pressure of water in hPa

def Humid_Ratio(P_wat,P_atm):
    B = 621.9907 #g/kg, Constant for water in air
    X = B*P_wat/(P_atm-P_wat)
    return X #returns humidity ratio in g/kg

def enthalpy(T_db,X):
    Tc_db = FtoC(T_db)
    h = Tc_db *(1.01+.00189*X)+2.5*X
    return h #returns enthalpy in kJ/kg

def air_density(P_wat,P_atm,T_db):
    Rwat = 461.4964 #ideal gas constant for water
    Rair = 287.0531 #ideal gas constant for air
    P_dry = P_atm-P_wat
    Tc_db = FtoC(T_db)
    rho = (P_dry/(Rair*(Tc_db+273.15)))+(P_wat/(Rwat*(Tc_db+273.15)))
    return rho #return density in kg/m^3

def mbartoinHg(P_in):
    P_inHg = P_in/33.8637526
    return P_inHg

def inHgtombar(P_in):
    P_mbar = P_in*33.8637526
    return P_mbar

#Input file format codes
#Input files are actual weather data observations
#they may have more than 1 reading for a given hour

#1 = Local Climatological Data (LCD) Data file

inp_format = 1

#variables and formats for different input file types
if inp_format ==1:
    inp_month_start = 107
    inp_month_end = 109
    inp_day_start = 110
    inp_day_end = 112
    inp_hour_start = 113
    inp_hour_end = 115
    inp_db_start = 263
    inp_db_end = 265
    inp_wb_start = 335
    inp_wb_end = 337
    inp_baro_start = 623
    inp_baro_end = 628
    inp_type_start =119
    inp_type_end = 121
    start_line = 3
    


#Output File Format Codes
#Output files are intended for feeding to eQUEST
#they will have exactly 1 hourly value for every hour of the year

#1 = Text2Bin format to create eQUEST data files

out_format = 1

#variables and formats for different file types
if out_format == 1:
    month_start = 0
    month_end = 2
    day_start = 2
    day_end = 4
    hour_start = 4
    hour_end = 6
    wb_start = 7
    wb_end = 11
    db_start = 12
    db_end = 16
    baro_start = 18
    baro_end = 22
    hr_start = 38
    hr_end = 45
    density_start = 45
    density_end = 50
    enthalpy_start = 52
    enthalpy_end = 56
    
#establish starting point of input file
if inp_format == 1:
    curr_line = start_line

#open the target file first, grab any headers
with open(tarfilepath,'rt') as tarfile:
    if dbg: print "Opening Target File"
    outline = ""
    with open(outfilepath, 'w') as outfile:
        if dbg: print "Opening Output File"
        if out_format == 1:
            #get the first three lines as header lines
            outfile.write(tarfile.readline())
            outfile.write(tarfile.readline())
            outfile.write(tarfile.readline())
            testline = tarfile.readline()
            while len(testline)>0:
                month = int(testline[month_start:month_end])
                day = int(testline[day_start:day_end])
                hour = int(testline[hour_start:hour_end])
                T_wb = float(testline[wb_start:wb_end])
                T_db = float(testline[db_start:db_end])
                Baro = float(testline[baro_start:baro_end])
                if dbg: print("Looking for: ", month, day, hour, T_wb, T_db, Baro)
                if inp_format == 1:
                   with open(infilepath,'rt') as infile:
                       for i, line in enumerate(infile):
                           if i == curr_line:                           
                               getline = line
                               curr_line = curr_line + 1                           
                               gooddata = True
                               data_count = 0
                               out_T_db = 0
                               out_T_wb = 0
                               out_baro = 0
                               
                               if getline[inp_type_start:inp_type_end] == "FM":

                                   try:
                                       inp_month = int(getline[inp_month_start:inp_month_end])
                                   except:
                                       gooddata=False

                                   try:
                                       inp_day = int(getline[inp_day_start:inp_day_end])
                                   except:
                                       gooddata=False

                                   try:
                                       inp_hour = int(getline[inp_hour_start:inp_hour_end])
                                   except:
                                       gooddata=False
                                   try:
                                       inp_T_wb = float(getline[inp_wb_start:inp_wb_end])
                                   except:
                                       gooddata= False
                                   try:
                                       inp_T_db = float(getline[inp_db_start:inp_db_end])
                                   except:
                                       gooddata= False
                                   try:
                                       inp_baro = float(getline[inp_baro_start:inp_baro_end])
                                   except:
                                       gooddata = False

                                   if gooddata:
                                       if dbg: print(inp_month,inp_day,inp_hour,inp_T_wb,inp_T_db,inp_baro)
                                       if month == inp_month and day == inp_day and hour == inp_hour +1:
                                           #if the dates match up
                                           #add this data into the new data and average it out
                                           data_count = data_count + 1
                                           out_T_db = out_T_db + inp_T_db
                                           out_T_wb = out_T_wb + inp_T_wb
                                           out_baro = out_baro + inp_baro
                                       if month<inp_month or (month == inp_month and day<inp_day):
                                           if dbg: print "Breaking"
                                           break
                                
                               
                               

                testline = tarfile.readline()
            
    
    
