#Chrissy Rogers
#Thesis

import numpy as n
import pandas as pd


filepath='C:\Users\cmw1229\Google Drive\Thesis Work\Pickled Files'
cells='C:\Users\cmw1229\Google Drive\Thesis Work\Region_cells.csv'

#filepath="/home/cwilliams/thesis/npz_files"
#cells="/home/cwilliams/thesis/region_cells.csv"

# read in lat and lon from dataset
#=========================================================
misc=n.load(filepath+'\misc_info_all_files.npz')
lat=misc['lat']
lon=misc['lon']

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Read in Lat/Lon values for each cell in the region, generated
# from ArcGIS
# find where (index) they occur and save a n-D array to index with
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
ocean_lat=n.array([[list(n.ravel(n.where(lat==y)))[0] for y in
          n.genfromtxt(cells,usecols=0,delimiter=',',
          skip_header=1)[:92]]])
ocean_lon=n.array([[list(n.ravel(n.where(lon==x)))[0] for x in
          n.genfromtxt(cells,usecols=1,delimiter=',',
          skip_header=1)[:92]]])

coast_lat=n.array([[list(n.ravel(n.where(lat==y)))[0] for y in
          n.genfromtxt(cells,usecols=2,delimiter=',',
          skip_header=1)[:52]]])
coast_lon=n.array([[list(n.ravel(n.where(lon==x)))[0] for x in
          n.genfromtxt(cells,usecols=3,delimiter=',',
          skip_header=1)[:52]]])

diablo_lat=n.array([[list(n.ravel(n.where(lat==y)))[0] for y 
           in n.genfromtxt(cells,usecols=4,delimiter=',',
           skip_header=1)[:68]]])
diablo_lon=n.array([[list(n.ravel(n.where(lon==x)))[0] for x 
           in n.genfromtxt(cells,usecols=5,delimiter=',',
           skip_header=1)[:68]]])

valley_lat=n.array([[list(n.ravel(n.where(lat==y)))[0] for y 
           in n.genfromtxt(cells,usecols=6,delimiter=',',
           skip_header=1)]])
valley_lon=n.array([[list(n.ravel(n.where(lon==x)))[0] for x 
           in n.genfromtxt(cells,usecols=7,delimiter=',',
           skip_header=1)]])

#=========================================================
# Read in Temp files
#=========================================================
print 'start reading files'
datamax45=n.load(filepath+'\Tmax45.npz')
print 'read file 1'
datamin45=n.load(filepath+'\Tmin45.npz')
print 'read file 2'
datamax85=n.load(filepath+'\Tmax85.npz')
print 'read file 3'
datamin85=n.load(filepath+'\Tmin85.npz')
print 'read file 4'
#----------------------------------------------------------------

#=========================================================
# Model Runs
#=========================================================
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
#----------------------------------------------------------------

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
#----------------------------------------------------------------

#model index positions
cansm2=[1,2,3,4,5]
ccsm4=[6,7]
gfdl=[8,9]
ipsl=[10,11,12,13]
micro5=[17,18,19]
mpi_esm=[20,21,22]
csiro=[26,27,28,29,30,31,32,33,34,35]
#----------------------------------------------------------------
def decade_avg(data):
    
  bcccsm1_avg=Tmax45[0,:,:,:]
  cansm2_avg=n.nanmean(Tmax45[cansm2,:,:,:],0)
  ccsm4_avg=n.nanmean(Tmax45[ccsm4,:,:,:],0)
  gfdl_avg=n.nanmean(Tmax45[gfdl,:,:,:],0)
  ipsl_avg=n.nanmean(Tmax45[ipsl,:,:,:],0)
  ipslcm5amr_avg=Tmax45[14,:,:,:]
  micro5_avg=n.nanmean(Tmax45[micro5,:,:,:],0)
  microesm_avg=Tmax45[15,:,:,:]
  microesmchem_avg=Tmax45[16,:,:,:]
  mpi_esm_avg=n.nanmean(Tmax45[mpi_esm,:,:,:],0)
  mpiesmmr_avg=Tmax45[23,:,:,:]
  mricgcm3_avg=Tmax45[24,:,:,:]
  noresmlm_avg=Tmax45[25,:,:,:]
  csiro_avg= n.nanmean(Tmax45[csiro,:,:,:],0)
  
  model_avg=(bcccsm1_avg+cansm2_avg+ccsm4_avg+gfdl_avg+
  ipsl_avg+ipslcm5amr_avg+micro5_avg+microesm_avg+
  microesmchem_avg+mpi_esm_avg+mpiesmmr_avg+mricgcm3_avg+
  noresmlm_avg+csiro_avg)/14.
  #
  return pd.Panel(model_avg,items=dates,
     major_axis=lat,minor_axis=lon).resample('10AS',how='mean'
     ).as_matrix()
#--------------------------------------------------------------------

decade=n.arange(1950,2091,10)

Max45=decade_avg(Tmax45)
Min45=decade_avg(Tmin45)
Max85=decade_avg(Tmax85)
Min85=decade_avg(Tmin85)
Diff45_10=decade_avg(Diff45)
Diff85_10=decade_avg(Diff85)

n.savez_compressed(filepath+'/decade_avg.npz',Tmax4=Max45,
  Min45=Tmin45,Tmax85=Max85,Tmin85=Min85,Diff45=Diff45_10,
  Diff85=Diff85_10)