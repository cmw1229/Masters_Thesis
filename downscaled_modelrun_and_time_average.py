#Chrissy Rogers
#Thesis
#Create ensemble plots and time average plots for CMIP5 data
#---------------------------------------------------------------------
import numpy as n
import pandas as pd
import matplotlib.pyplot as p
from scipy import stats
#import vertex as v

#filepath='C:\Users\cmw1229\Google Drive\Thesis Work\Pickled Files'
#outfile='C:\Users\cmw1229\Google Drive\Thesis Work\Weekly Thesis Meeting\images'

filepath="/home/cwilliams/thesis/npz_files"
outfile="/home/cwilliams/thesis/images"
cells="/home/cwilliams/thesis/region_cells.csv"

Run_Names=n.array(['bcc-csm1_run1',
'canesm2_run1','canesm2_run2','canesm2_run3','canesm2_run4','canesm2_run5',
'ccsm4_run1','ccsm4_run2',
'gfdl-esm2g_run1',
'gfdl-esm2m_run2',
'ipsl-cm5a-lr_run1','ipsl-cm5a-lr_run2','ipsl-cm5a-lr_run3','ipsl-cm5a-lr_run4', 
'ipsl-cm5a-mr_run1', #14
'miroc-esm_run1', #15
'miroc-esm-chem_run1', #16
'miroc5_run1','miroc5_run2','miroc5_run3',
'mpi-esm-lr_run1','mpi-esm-lr_run2','mpi-esm-lr_run3',
'mpi-esm-mr_run1', #23
'mri-cgcm3_run1', #24
'noresm1-m_run1', #25
'csiro_mk3_run1','csiro_mk3_run2', 
'csiro_mk3_run3','csiro_mk3_run4','csiro_mk3_run5','csiro_mk3_run6',
'csiro_mk3_run7','csiro_mk3_run8','csiro_mk3_run9','csiro_mk3_run10'])

Model_Names=['bcc-csm1','canesm2','ccsm4',
'gfdl-esm2g','ipsl-cm5a-lr','ipsl-cm5a-mr','miroc-esm',
'miroc-esm-chem','miroc5','mpi-esm-lr','mpi-esm-mr', 
'mri-cgcm3','noresm1-m','csiro_mk3']
#=========================================================
# read in lat and lon from dataset
#=========================================================
misc=n.load(filepath+'/misc_info_all_files.npz')
lat=misc['lat']
lon=misc['lon']

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Read in Lat/Lon values for each cell in the region, generated
# from ArcGIS
# find where (index) they occur and save a n-D array to index with
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
ocean_lat=n.array([[list(n.ravel(n.where(lat==y)))[0] for y in n.genfromtxt(cells,usecols=0,delimiter=',',skip_header=1)[:92]]])
ocean_lon=n.array([[list(n.ravel(n.where(lon==x)))[0] for x in n.genfromtxt(cells,usecols=1,delimiter=',',skip_header=1)[:92]]])

coast_lat=n.array([[list(n.ravel(n.where(lat==y)))[0] for y in n.genfromtxt(cells,usecols=2,delimiter=',',skip_header=1)[:52]]])
coast_lon=n.array([[list(n.ravel(n.where(lon==x)))[0] for x in n.genfromtxt(cells,usecols=3,delimiter=',',skip_header=1)[:52]]])

diablo_lat=n.array([[list(n.ravel(n.where(lat==y)))[0] for y in n.genfromtxt(cells,usecols=4,delimiter=',',skip_header=1)[:68]]])
diablo_lon=n.array([[list(n.ravel(n.where(lon==x)))[0] for x in n.genfromtxt(cells,usecols=5,delimiter=',',skip_header=1)[:68]]])

valley_lat=n.array([[list(n.ravel(n.where(lat==y)))[0] for y in n.genfromtxt(cells,usecols=6,delimiter=',',skip_header=1)]])
valley_lon=n.array([[list(n.ravel(n.where(lon==x)))[0] for x in n.genfromtxt(cells,usecols=7,delimiter=',',skip_header=1)]])


print 'start reading files'
#misc_data=n.load(filepath+'\misc_info_all_files.npz')
datamax45=n.load(filepath+'/Tmax45.npz')
print 'read file 1'
datamin45=n.load(filepath+'/Tmin45.npz')
print 'read file 2'
datamax85=n.load(filepath+'/Tmax85.npz')
print 'read file 3'
datamin85=n.load(filepath+'/Tmin85.npz')
print 'read file 4'


dates=[]
for i in range(1950,2100):
    start=str(i)+'-06-01'
    end=str(i)+'-08-31'
    dates.append(pd.date_range(start,end,freq='D'))
dates=[item for sublist in dates for item in sublist]

Tmax45=datamax45['Tmax45']*9./5+32
Tmin45=datamin45['Tmin45']*9./5+32
Tmax85=datamax85['Tmax85']*9./5+32
Tmin85=datamin85['Tmin85']*9./5+32

Diff45=Tmax45-Tmin45
Diff85=Tmax85-Tmin85

#model index positions
cansm2=[1,2,3,4,5]
ccsm4=[6,7]
gfdl=[8,9]
ipsl=[10,11,12,13]
micro5=[17,18,19]
mpi_esm=[20,21,22]
csiro=[26,27,28,29,30,31,32,33,34,35]

def Region(data,Lat,Lon,rcp,temp,Legend=False):
  '''data=dataset to process and plot
     rcp= rcp value as a string
     temp= either Max, Min, or diff as string'''
  regional_avg=pd.DataFrame(n.transpose(n.nanmean(n.nanmean(
    data[:,:,Lat,Lon],3),2)),index=dates,columns=
    Run_Names).resample('AS',how='mean').as_matrix()
  
  bcccsm1_avg=regional_avg[:,0]
  cansm2_avg=n.nanmean(regional_avg[:,cansm2],1)
  ccsm4_avg=n.nanmean(regional_avg[:,ccsm4],1)
  gfdl_avg=n.nanmean(regional_avg[:,gfdl],1)
  ipsl_avg=n.nanmean(regional_avg[:,ipsl],1)
  ipslcm5amr_avg=regional_avg[:,14]
  micro5_avg=n.nanmean(regional_avg[:,micro5],1)
  microesm_avg=regional_avg[:,15]
  microesmchem_avg=regional_avg[:,16]
  mpi_esm_avg=n.nanmean(regional_avg[:,mpi_esm],1)
  mpiesmmr_avg=regional_avg[:,23]
  mricgcm3_avg=regional_avg[:,24]
  noresmlm_avg=regional_avg[:,25]
  csiro_avg= n.nanmean(regional_avg[:,csiro],1)
  
  model_avg=(bcccsm1_avg+cansm2_avg+ccsm4_avg+gfdl_avg+
  ipsl_avg+ipslcm5amr_avg+micro5_avg+microesm_avg+
  microesmchem_avg+mpi_esm_avg+mpiesmmr_avg+mricgcm3_avg+
  noresmlm_avg+csiro_avg)/14.

  month=n.arange(len(regional_avg))+1950 # ***
         # *** really the year. didn't change variable name
  
  p.set_cmap('spring')
  p.plot(month,bcccsm1_avg,label='bcc-csm1 (1 Run)',color='firebrick',alpha=.8)
  p.plot(month,cansm2_avg,label='cansm2 (5 Runs)',color='red',alpha=.8)
  p.plot(month,ccsm4_avg,label='ccsm4 (2 Runs)',color='peru',alpha=.8)
  p.plot(month,csiro_avg,label='csiro-mk3 (10 Runs)',color='goldenrod',alpha=.8)
  p.plot(month,gfdl_avg,label='gfdl-esm2g (2 Runs)',color='gold',alpha=.8)
  p.plot(month,ipsl_avg,label='ipsl=cm5a-lr (4 Runs)',color='DarkGreen',alpha=.8)
  p.plot(month,ipslcm5amr_avg,label='ipsl-cm5a-mr (1 Run)',color='seagreen',alpha=.8)
  p.plot(month,micro5_avg,label='micro5 (3 Runs)',color='lightgreen',alpha=.8)
  p.plot(month,microesm_avg,label='micro-esm (1 Run)',color='cyan',alpha=.8)
  p.plot(month,microesmchem_avg,label='micro-esm-chem (1 Run)',color='teal',alpha=.8)
  p.plot(month,mpi_esm_avg,label='mpi-esm-lr (3 Runs)',color='steelblue',alpha=.8)
  p.plot(month,mpiesmmr_avg,label='mpi-esm-mr (1 Run)',color='blue',alpha=.8)
  p.plot(month,mricgcm3_avg,label='mri-cgcm3 (1 Run)',color='purple',alpha=.8)
  p.plot(month,noresmlm_avg,label='noresml-m (1 Run)',color='palevioletred',alpha=.8)
  p.plot(month,model_avg,linestyle='--',color='k',
         linewidth=5,label='Multi-Model Mean')
  p.xlim(1950,2099)
  if temp=='Max':
    p.ylim(60,100)
  elif temp=='Min':
    p.ylim(45,65)
  else:
    p.ylim(10,40)
  if temp=='diff':
    p.suptitle('Summer Average Diurnal Temperature Difference Over Study Area (RCP '+rcp+')',fontsize=14)
  else:
    p.suptitle(temp+'imum Summer Average Temperatures Over Study Area (RCP '+rcp+')',
    fontsize=18)

  p.subplots_adjust(left=.05,right=.8,top=.9,bottom=.07,wspace=.1)
  if Legend==True: 
    legand=p.legend(loc='best',title=r'Models $Ensemble Average$',
          frameon=False,fontsize=12,bbox_to_anchor=(1,0.8))
    for label in legand.get_lines():
      label.set_linewidth(2)
    return legand
    
  

def plot_time(data,rcp,temp):
  '''data=dataset to process and plot
     rcp= rcp value as a string
     temp= either Max, Min, or diff as string'''
 
  p.figure(temp+' '+rcp,figsize=(14.4,9),dpi=100)
  

  p.subplot(221)
  p.title('Ocean Region')
  p.ylabel(r'Temperature $^\circ{F}$',fontsize=16) 
  Region(data,ocean_lat,ocean_lon,rcp,temp)

  p.subplot(222)
  p.title('Coastal Region') 
  Region(data,coast_lat,coast_lon,rcp,temp,Legend=True)

  p.subplot(223)
  p.title('Diablo Range Region')
  p.ylabel(r'Temperature $^\circ{F}$',fontsize=16)
  p.xlabel('Date (Years)',fontsize=16) 
  Region(data,diablo_lat,diablo_lon,rcp,temp)

  p.subplot(224)
  p.title('Central Valley Region') 
  p.xlabel('Date (Years)',fontsize=16)
  Region(data,valley_lat,valley_lon,rcp,temp)
  p.savefig(outfile+'/'+temp+rcp+'.png',orientation='landscape',dpi=300)
  

plot_time(Tmax45,'4.5','Max')
print 'plot 1.1'
plot_time(Tmin45,'4.5','Min')
print 'plot 1.2'
plot_time(Tmax85,'8.5','Max')
print 'plot 1.3'
plot_time(Tmin85,'8.5','Min')
print 'plot 1.4'
plot_time(Diff45,'4.5','diff')
print 'plot 1.5'
plot_time(Diff85,'8.5','diff')
print 'plot 1.6'





#====================================================================
#Decadal Average and Return NPZ
#==================================================================== 

def Region10(data,var,Lat,Lon,rcp,color1,color2,color3,Legend=False):

  regional_avg=pd.DataFrame(n.transpose(n.nanmean(n.nanmean(data[:,:,Lat,Lon],3),
         2)),index=dates,columns=Run_Names).resample('10AS',
          how='mean').as_matrix()

  bcccsm1_avg=regional_avg[:,0]
  cansm2_avg=n.nanmean(regional_avg[:,cansm2],1)
  ccsm4_avg=n.nanmean(regional_avg[:,ccsm4],1)
  gfdl_avg=n.nanmean(regional_avg[:,gfdl],1)
  ipsl_avg=n.nanmean(regional_avg[:,ipsl],1)
  ipslcm5amr_avg=regional_avg[:,14]
  micro5_avg=n.nanmean(regional_avg[:,micro5],1)
  microesm_avg=regional_avg[:,15]
  microesmchem_avg=regional_avg[:,16]
  mpi_esm_avg=n.nanmean(regional_avg[:,mpi_esm],1)
  mpiesmmr_avg=regional_avg[:,23]
  mricgcm3_avg=regional_avg[:,24]
  noresmlm_avg=regional_avg[:,25]
  csiro_avg= n.nanmean(regional_avg[:,csiro],1)
  
  model_avg=(bcccsm1_avg+cansm2_avg+ccsm4_avg+gfdl_avg+
  ipsl_avg+ipslcm5amr_avg+micro5_avg+microesm_avg+
  microesmchem_avg+mpi_esm_avg+mpiesmmr_avg+mricgcm3_avg+
  noresmlm_avg+csiro_avg)/14.
  
  decade=n.arange(1950,2091,10)

  slope,inter,r,p_val,stderr=stats.linregress(decade,model_avg)
  deviation=regional_avg.std(axis=1)
  trend=slope*decade+inter
  p.plot(decade,model_avg,color=color1)
  p.plot(decade,trend,color=color2,linewidth=2)
  p.text(decade[1],trend[1]+10,var+r' Trend ($2\sigma$) %.3f $\pm$ %.3f'\
     r'$\frac{^\circ{F}}{Decade}$' %(slope*10,stderr*1.98*10),
     fontsize=8,bbox={'facecolor':color2,'alpha':.4})#,'pad':10})
  p.fill_between(decade,trend+(deviation+stderr*1.98),
    trend-(deviation+stderr*1.98),facecolor=color3,
    label=var+r' $\pm$ $1$ Standard Deviation',alpha=.1)

  p.suptitle('Multi-Model Decadal Mean '+rcp,fontsize=18)
  p.subplots_adjust(left=.05,right=.99,top=.9,bottom=.07,wspace=.1)
  p.ylim(20,110)
  p.xlim(1950,2090)
 
 
     




def plot_time10(data,rcp,temp,color1,color2,color3):
  '''data=dataset to process and plot
     rcp= rcp value as a string
     temp= either Max, Min, or diff as string'''
  if rcp=='4.5': 
    p.figure('Decade 4.5',figsize=(14.4,9),dpi=100)
  else:
    p.figure('Decade 8.5',figsize=(14.4,9),dpi=100)
      
  if temp=='Max': var='Maximum Temperatures'
  elif temp=='Min':var='Minimum Temperatures'
  else: var='Diurnal Temperature Difference'

  p.subplot(221)
  p.title('Ocean Region',fontsize=12)
  p.ylabel(r'Temperature $^\circ{F}$',fontsize=12) 
  Region10(data,var,ocean_lat,ocean_lon,rcp,color1,color2,color3)

  p.subplot(222)
  p.title('Coastal Region',fontsize=12) 
  Region10(data,var,coast_lat,coast_lon,rcp,color1,color2,color3,Legend=True)

  p.subplot(223)
  p.title('Diablo Range Region',fontsize=12)
  p.ylabel(r'Temperature $^\circ{F}$',fontsize=12
  )
  p.xlabel('Date (Years)',fontsize=12) 
  Region10(data,var,diablo_lat,diablo_lon,rcp,color1,color2,color3)

  p.subplot(224)
  p.title('Central Valley Region',fontsize=12) 
  p.xlabel('Date (Years)',fontsize=12)
  Region10(data,var,valley_lat,valley_lon,rcp,color1,color2,color3)
  p.savefig(outfile+'/decade'+rcp+'.png',orientation='landscape',dpi=300)
  
plot_time10(Tmax45,'4.5','Max','DarkRed','r','r')
plot_time10(Tmin45,'4.5','Min','DarkBlue','b','b')
plot_time10(Diff45,'4.5','Diff','DarkGreen','g','g')
print 'plot 2.1'

plot_time10(Tmax85,'8.5','Max','DarkRed','r','r')
plot_time10(Tmin85,'8.5','Min','DarkBlue','b','b')
plot_time10(Diff85,'8.5','Diff','DarkGreen','g','g')


def Coast10(data,var,Lat,Lon,rcp,color1,color2,color3,Legend=False):
  regional_avg=pd.DataFrame(n.transpose(n.nanmean(n.nanmean(data[:,:,Lat,Lon],3),
         2)),index=dates,columns=Run_Names).resample('10AS',
          how='mean').as_matrix()

  bcccsm1_avg=regional_avg[:,0]
  cansm2_avg=n.nanmean(regional_avg[:,cansm2],1)
  ccsm4_avg=n.nanmean(regional_avg[:,ccsm4],1)
  gfdl_avg=n.nanmean(regional_avg[:,gfdl],1)
  ipsl_avg=n.nanmean(regional_avg[:,ipsl],1)
  ipslcm5amr_avg=regional_avg[:,14]
  micro5_avg=n.nanmean(regional_avg[:,micro5],1)
  microesm_avg=regional_avg[:,15]
  microesmchem_avg=regional_avg[:,16]
  mpi_esm_avg=n.nanmean(regional_avg[:,mpi_esm],1)
  mpiesmmr_avg=regional_avg[:,23]
  mricgcm3_avg=regional_avg[:,24]
  noresmlm_avg=regional_avg[:,25]
  csiro_avg= n.nanmean(regional_avg[:,csiro],1)
  
  model_avg=(bcccsm1_avg+cansm2_avg+ccsm4_avg+gfdl_avg+
  ipsl_avg+ipslcm5amr_avg+micro5_avg+microesm_avg+
  microesmchem_avg+mpi_esm_avg+mpiesmmr_avg+mricgcm3_avg+
  noresmlm_avg+csiro_avg)/14.
  
  decade=n.arange(1950,2091,10)

  slope,inter,r,p_val,stderr=stats.linregress(decade,model_avg)
  deviation=regional_avg.std(axis=1)
  trend=slope*decade+inter
  p.plot(decade,model_avg,color=color1,linewidth=2,
         label=rcp+r' Average Decadal Temperatures')
  p.plot(decade,trend,color=color2,linewidth=2,linestyle='--',
     label=var+r' Trend ($2\sigma$) %.3f $\pm$ %.3f'\
     r'$\frac{^\circ{F}}{Decade}$' %(slope*10,stderr*1.98*10))
  
  p.fill_between(decade,trend+(deviation+stderr*1.98),
    trend-(deviation+stderr*1.98),facecolor=color3,
    label=var+r' $\pm$ $1$ Standard Deviation',alpha=.1)

  p.suptitle('Multi-Model Decadal Mean Coastal Region',fontsize=18)
  p.subplots_adjust(left=.06,right=.99,top=.9,bottom=.07)
  p.xlim(1950,2090)
  p.ylabel(r'Temperatures $(^\circ{F})$')
  
  legand=p.legend(ncol=2,loc='upper left',frameon=False,fontsize=10)
  for label in legand.get_lines():
      label.set_linewidth(2)
  print slope,stderr
 
 
fig= p.figure('Decade coast',figsize=(14.4,9),dpi=100)
a=fig.add_subplot(311)
Coast10(Tmax45,'RCP 4.5',coast_lat,coast_lon,'4.5','r','firebrick','r')
Coast10(Tmax85,'RCP 8.5',coast_lat,coast_lon,'8.5','chocolate',
         'indianred','chocolate')
p.ylim(70,85)
p.title('Maximum Temperatures',fontsize=12)
p.setp(a.get_xticklabels(),visible=False)

a2=fig.add_subplot(312,sharex=a)
Coast10(Tmin45,'RCP 4.5',coast_lat,coast_lon,'4.5','b','DarkBlue','b')
Coast10(Tmin85,'RCP 8.5',coast_lat,coast_lon,'8.5','deepskyblue',
         'darkcyan','deepskyblue')
p.ylim(50,65)
p.title('Minimum Temperatures',fontsize=12)
print 'plot 2.2'
p.setp(a2.get_xticklabels(),visible=False)

a3=fig.add_subplot(313,sharex=a)
Coast10(Diff45,'RCP 4.5',coast_lat,coast_lon,'4.5','forestgreen',
         'seagreen','forestgreen')
Coast10(Diff85,'RCP 8.5',coast_lat,coast_lon,'8.5','m',
         'blueviolet','m')
p.ylim(21,24)
p.title('Diurnal Temperature Difference',fontsize=12)
print 'plot 2.3'
p.xlabel('Date (Years)',fontsize=12)

p.setp(a3.get_xticklabels(),visible=True)

a.tick_params(axis='both', which='major', labelsize=12)
p.savefig(outfile+'/decade_coast.png',orientation='landscape',dpi=300)
#p.show()