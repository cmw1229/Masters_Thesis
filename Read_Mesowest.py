# Chrissy Rogers
# Thesis Work
#
# This file reads in excel files and outputs Pandas DataFrames and Panels.
# It averages the data hourly using scipy.stats.nanmean
# Data is output in various slices including Temp, RH, WS, WD, and All Combined
# Output files also include Location data with Station, Lat, Lon, Network
#==============================================================================

import glob
import chrissy
import pandas as pd
import numpy as n

#===============================================================================

#MainPath='C:\Users\cmw1229\Google Drive\Thesis Work'
#       Defined so shorten the width of code

MainPath='C:\Users\cmw1229\Google Drive\Thesis Work'
#*******************************************************************************

stations=[]
paneldict={}

#*******************************************************************************

#-------------------------------------------------------------------------------
#  Groups together all files with wildcard and sorts Alphabetically
#-------------------------------------------------------------------------------
filelist=glob.glob(MainPath+'\MesoWest Data\*.xls')
filelist.sort()

#-------------------------------------------------------------------------------
#Creates Namelist by striping parts off of the filename to assure same order
# as filelist for later use
#-------------------------------------------------------------------------------
for files in filelist:
    name=files.replace(MainPath+'\MesoWest Data\\','')
    stations.append(name.replace('.xls',''))

#-------------------------------------------------------------------------------
# Reads in Excel Data using Custom Function and creates a pandas dataframe then 
# appends the dataframe into a dictionary with the station name as key
#------------------------------------------------------------------------------- 
for i in range(len(filelist)):
    print i, stations[i] #print command for run tracking only
    dataf=chrissy.station_data(filelist[i])
    paneldict[str(stations[i])]=dataf

#-------------------------------------------------------------------------------
# Reads in RAWS (.dat) file using custom Function as Dataframe and appends to
# dictonary.
#-------------------------------------------------------------------------------
print '83','Skylark' #print command for run tracking only

paneldict['Skylark']=chrissy.Raws(MainPath+"\Chrissy.dat")

#-------------------------------------------------------------------------------
# Creates Pandas Panel
#-------------------------------------------------------------------------------
Data=pd.Panel(paneldict)

#-------------------------------------------------------------------------------
# Reads in locations Excel File as a DataFrame
#-------------------------------------------------------------------------------
Location=pd.io.excel.read_excel(
     MainPath+"\Station_Data_Location.xlsx",
       header=0,index_col=0,parse_cols=3)
       
       
#*******************************************************************************

#-------------------------------------------------------------------------------
# Create DataFrame slices from Panel for each variable with stations as
# column headers and date and row indexes.
#-------------------------------------------------------------------------------       
Temp=Data.xs('Temp','minor')
WS=Data.xs('Wind Speed','minor')
WD=Data.xs('Wind Direction','minor')
RH=Data.xs('RH','minor')



#-------------------------------------------------------------------------------
# Saves Pandas data as pickled file to be read in with (read_pickle) in 
# another script.
#-------------------------------------------------------------------------------

#Data.to_pickle(MainPath+'\Pickled Files\All_Data.pkl')
#Temp.to_pickle(MainPath+'\Pickled Files\Temp.pkl')
#WS.to_pickle(MainPath+'\Pickled Files\Wind_Speed.pkl')
#WD.to_pickle(MainPath+'\Pickled Files\Wind_Dir.pkl')
#RH.to_pickle(MainPath+'\Pickled Files\RH.pkl')
#Location.to_pickle(MainPath+'\Pickled Files\Location.pkl')

#===============================================================================
# End File
#===============================================================================
