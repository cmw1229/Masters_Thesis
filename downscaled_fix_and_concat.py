#Chrissy Rogers
#Thesis
#Fix bad data and concatenate into one array


import numpy as n

#=====================================================================
#          Read files
#=====================================================================
filepath='C:\Users\cmw1229\Google Drive\Thesis Work\Pickled Files'

data1=n.load(filepath+'\summer_dailytasmax45.npz')
data2=n.load(filepath+'\summer_dailytasmin45.npz')#

data3=n.load(filepath+'\summer_dailytasmax85.npz')
data4=n.load(filepath+'\summer_dailytasmin85.npz')

data5=n.load(filepath+'\summer_csirotasmax45.npz')
data6=n.load(filepath+'\summer_csirotasmin45.npz')

data7=n.load(filepath+'\summer_csirotasmax85.npz')#
data8=n.load(filepath+'\summer_csirotasmin85.npz')

#data sets had different lat and lons selected the smallest extent
# of both lat and lon and adjusted rest to match.
lat=data1['lat']
lon=data2['lon']

days=data1['days']
days_in_month=data1['days_in_month']
num_days_in_summer=data1['num_days_summer']
year=data1['year']

print 'Data read in! \n'
#*********************************************************************
#fix spacial and projections so datasets match
# and concatanate arrays
#*********************************************************************
fixlon1=n.array([0,1,2,3,4,23,24,25,26,27,28,29])
fixlon7=n.array([18,19,20,21,22,23,24,25])

fixlat2=n.array([0,1,2,23,24,25])

fixproj1=n.array([24,25])
fixproj2=n.array([8,9,10,11,12,13,14,15,16,17,34,35])


Tdata1=n.delete(n.delete(data1['dailytemp'],fixlon1,3),fixproj1,0)
print 'data1 fixed'
Tdata2=n.delete(n.delete(data2['dailytemp'],fixlat2,2),fixproj2,0)
print 'data2 fixed'
#Tdata3=n.delete(data3['dailytemp'],fixlon1,3)
#print 'data3 fixed'
#Tdata4=n.delete(data4['dailytemp'],fixlon1,3)
#print 'data4 fixed'
Tdata5=n.delete(data5['dailytemp'],fixlon1,3)
print 'data5 fixed'
Tdata6=n.delete(data6['dailytemp'],fixlon1,3)
print 'data6 fixed'
#Tdata7=n.delete(data7['dailytemp'],fixlon7,3)
#print 'data7 fixed'
#Tdata8=n.delete(data8['dailytemp'],fixlon1,3)
#print 'data8 fixed'

print ''

Tmax45=n.append(Tdata1,Tdata5,0)
print 'Concat Tmax45 Done'
Tmin45=n.append(Tdata2,Tdata6,0)
print 'Concat Tmin45 Done'
Tmax85=n.append(Tdata3,Tdata7,0)
print 'Concat Tmax85 Done'
Tmin85=n.append(Tdata4,Tdata8,0)
print 'Concat Tmin85 Done\n'

print 'Storing as .npz file'

n.savez(filepath+'\misc_info_all_files.npz'
       ,lat=lat,lon=lon, days_in_month=days_in_month, days=days,
       num_days_in_summer=num_days_in_summer,year=year)
print 'misc saved'

n.savez(filepath+'\Tmax45',Tmax45=Tmax45)
print 'max45 saved'

n.savez(filepath+'\Tmax85',Tmax85=Tmax85)
print 'max85 saved'

n.savez(filepath+'\Tmin45',Tmin45=Tmin45)
print 'min45 saved'

n.savez(filepath+'\Tmin85',Tmin85=Tmin85)
print 'min85 saved'

print 'closing file.  DONE!'