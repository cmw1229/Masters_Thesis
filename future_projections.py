#Chrissy Rogers
#Thesis Future Projection

#Create NetCDF File to analysis in GIS
#Create Line Plots of fog changes including std err and save as PNG.
#===================================================================

#--------------------------------------------------------------------
#Import needed Libraries
#--------------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as p
import numpy as n
import scipy.misc as sm
from scipy.io import netcdf
#--------------------------------------------------------------------

#Create Functions for script
#====================================================================

def gis_netcdf(data,arr,filename):
  '''creates netcdf file of projected fog hours
     data=Dataset with Lat and Lon data stored
     arr=fog dataset
     filename=Output filepath and name'''
    
  f=netcdf.netcdf_file(outfile1+filename,'w')
  #f.history='Downscaled CMIP5 data which has been averaged over all'\
  #  'models and decadaly averaged'
    
  f.createDimension('time',9)
  f.createDimension('lat',len(data['lat']))
  f.createDimension('lon',len(data['lon']))

  time=f.createVariable('time','i',('time',))
  lat=f.createVariable('lat','f4',('lat',))
  lon=f.createVariable('lon','f4',('lon',))
  fog=f.createVariable('fog','f4',('time','lat','lon',))

 
  time.units='decades since 1950' 
  lon.units='Degrees East'
  lat.units='Degrees North'
    
  fog.units='Change in Hours'
  fog.missing_value=1e20
  fog.valid_min=n.min(arr[arr<500])
  fog.valid_max=n.max(arr[arr<500])
  
  
  lat[:]=data['lat']
  lon[:]=data['lon']
  time[:]=n.arange(2010,2091,10)
  fog[:]=arr

 
  f.close

def gis_netcdf_var(data,arr,filename):
  '''creates netcdf file of the variance of projected fog hours and 
     current observations.
     data=Dataset with Lat and Lon data stored
     arr=fog dataset
     filename=Output filepath and name'''
     
  f=netcdf.netcdf_file(outfile+filename,'w')
  f.history='Difference between Model 2010 Decade on 2014 Observations'
    
  #f.createDimension('time',1)
  f.createDimension('lat',len(data['lat']))
  f.createDimension('lon',len(data['lon']))

  #time=f.createVariable('time',int,('time',))
  lat=f.createVariable('lat',float,('lat',))
  lon=f.createVariable('lon',float,('lon',))
  var=f.createVariable('var',float,('lat','lon',))

  #time[:]=2010
  #time.units='2010 Decade' 

  lat[:]=data['lat']
  lat.units='Degrees North'

  lon[:]=data['lon']
  lon.units='Degrees East'

  var[:]=arr
  var.units='Degrees F'

  f.close
#====================================================================


MainPath='C:\Users\cmw1229\Google Drive\Thesis Work'
outfile='C:\Users\cmw1229\Google Drive\Thesis Work\Images'
outfile1='C:\Users\cmw1229\Google Drive\Thesis Work\GIS\NetCDF'
filepath='C:\Users\cmw1229\Google Drive\Thesis Work\Pickled Files'


#Tdiff_all_excel.csv
T_diff=n.genfromtxt(MainPath+'\pixel_tdiff_coast_excel.csv',skip_header=1,usecols=2,missing_values='NaN',
filling_values=n.nan,delimiter=',')

Tobs=T_diff.reshape(20,18) #observed diurnal temp diff

Fog_obs=n.genfromtxt(MainPath+'\Fog_all_excel.csv',skip_header=1,usecols=2,delimiter=',')

Fog_obs=Fog_obs.reshape(20,18)/100. #fog observations from sat.

data1=n.load(filepath+'\decade_avg.npz')

# downscaled model values
m45=data1['Diff45'][6:,:,:] #6 is the decade 2010
m85=data1['Diff85'][6:,:,:]

var45=m45[0,:,:]-Tobs #variance between model and observations in 2010's
var85=m85[0,:,:]-Tobs

Tdiff45=m45-var45 #variance adjusted model values
Tdiff85=m85-var85


#**********************************************************************


newfog45=Fog_obs/Tobs*Tdiff45-Fog_obs
newfog85=Fog_obs/Tobs*Tdiff85-Fog_obs

#set 2010 Fog diff to 0. all values are +/-10^-15 or smaller
newfog45[0,newfog45[0,:,:]>-500]=0 
newfog85[0,newfog85[0,:,:]>-500]=0

newfog85[n.isnan(newfog85)==True]=1e20

dummy_fog=newfog85[0,:,:]
dummy_fog[14,1]=n.min(newfog85[newfog85<500])
dummy_fog[2,9]=n.max(newfog85[newfog85<500])



#-------------------------------------------------------------------
#Create netcdf data for spatial analysis in GIS
#-------------------------------------------------------------------

gis_netcdf(data1,newfog45,'\pixel_model_fog45.nc')
gis_netcdf(data1,newfog85,'\pixel_model_fog85.nc')

gis_netcdf(data1,dummy_fog,'\pixel_model_dummy_fog.nc')

gis_netcdf_var(data1,var45,'\pixel_model_var45.nc')
gis_netcdf_var(data1,var85,'\pixel_model_var85.nc')

#--------------------------------------------------------------------
# Define standard error(s).  Values found in another script
#--------------------------------------------------------------------

##Rate of change plus/minus standard error
x=-0.33469641745932982 #from Point_Fog_plots.py
dx=0.091923977906536378 #from Point_Fog_plots.py

#From downscaled_regional_decades.py   (On blizzard)
y45=0.00374986444201
dy45=0.000973103510306
y85=0.00212599005018
dy85=0.00120280143524
z45=x*y45
z85=x*y85
dz45=(n.abs(y45)*dx+n.abs(x)*dy45)*1.96 #z +/-dz
dz85=(n.abs(y85)*dx+n.abs(x)*dy85)*1.96

t=n.arange(2010,2100,10) #time array
value=n.arange(len(t))

#-------------------------------------------------------------------
#Plot Linear Data
#--------------------------------------------------------------------
fig=p.figure('Predicted Fog Rate of Change',figsize=(14.4,9),dpi=100)
p.plot(t,value*z45,color='darkblue',linestyle='--',linewidth=2,
label=r'$RCP\/4.5\/\approx\/-1.26*10^{-3}\/\pm\/1.31*10^{-3}\/\frac{hrs}{decade}$')
p.fill_between(t,value*z45,value*z45+dz45,facecolor='thistle',color='thistle',alpha=.5)
p.fill_between(t,value*z45,value*z45-dz45,facecolor='thistle',color='thistle',alpha=.5)

p.ylim(-.015,.005)


p.plot(t,value*z85,color='crimson',linestyle='--',linewidth=2,
label=r'$RCP\/8.5\/\approx\/-0.712*10^{-3}\/\pm\/1.17*10^{-3}\/\frac{hrs}{decade}$')
p.fill_between(t,value*z85,value*z85+dz85,facecolor='wheat',color='wheat',alpha=.5)
p.fill_between(t,value*z85,value*z85-dz85,facecolor='wheat',color='wheat',alpha=.5)

p.xlabel('Year',fontsize=20)
p.ylabel('Change in Fog Hours',fontsize=20)
p.tick_params(axis='both', which='major', labelsize=18,color='black')
p.title('Predicted Fog Rate of Change',fontsize=24)

legand2=p.legend(loc='upper right',
  frameon=True,fontsize=22)
for label in legand2.get_lines():
      label.set_linewidth(3)

fig.savefig(outfile+'/Fog_Rate.png',orientation='landscape',dpi=300)
p.show()
