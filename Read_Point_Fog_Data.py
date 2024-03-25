#Chrissy Rogers
# Reads csv file with point fog data created in ESRI ArcGIS
#---------------------------------------------------------------------

#Import Libraries
#--------------------------------------------------------------------
import pandas as pd
import numpy as n
#===============================================================================

#MainPath='C:\Users\cmw1229\Google Drive\Thesis Work'
#       Defined so shorten the width of code for printing

MainPath='C:\Users\cmw1229\Google Drive\Thesis Work'
cells=MainPath+'\Region_cells_Obs.csv'
#*******************************************************************************

coast=list(n.genfromtxt(cells,usecols=0,delimiter=',',skip_header=1,dtype=str)[:18])
diablo=list(n.genfromtxt(cells,usecols=1,delimiter=',',skip_header=1,dtype=str)[:21])
valley=list(n.genfromtxt(cells,usecols=2,delimiter=',',skip_header=1,dtype=str)[:20])

stations=[]
paneldict={}

#*******************************************************************************

#-------------------------------------------------------------------------------
#  Groups together all files with wildcard and sorts Alphabetically
#-------------------------------------------------------------------------------
filelist=MainPath+'\Pointfog.xlsx'


#-------------------------------------------------------------------------------
# Reads in Excel Data using Custom Function and creates a pandas dataframe then 
# appends the dataframe into a dictionary with the station name as key
#------------------------------------------------------------------------------- 
Data=pd.io.excel.read_excel(filelist,header=0,
       index_col=0,parse_cols=2)

Data['Fog']=Data['Fog']

DF_Coast=Data.ix[coast]
DF_Diablo=Data.ix[diablo]
DF_Valley= Data.ix[valley]   
       
#******************************************************************************


#*******************************************************************************

#-------------------------------------------------------------------------------
# Saves Pandas data as pickled file to be read in with (read_pickle) in 
# another script.
#-------------------------------------------------------------------------------

DF_Coast.to_pickle(MainPath+'\Pickled Files\Fog_diff_coast.pkl')
DF_Diablo.to_pickle(MainPath+'\Pickled Files\Fog_diff_diablo.pkl')
DF_Valley.to_pickle(MainPath+'\Pickled Files\Fog_diff_valley.pkl')
