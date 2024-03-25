# Chrissy Rogers
# Custom Functions

#=====================================================================
import pandas 
import numpy as n
import datetime as dt
from scipy.stats import nanmean
import statsmodels.api as sm
from scipy.stats import linregress
import matplotlib.pyplot as p
from scipy import stats
import scipy.io.netcdf as S

#=====================================================================

#*********************************************************************
def NaNmean(x):
  '''For use with Pandas.resample so NaN's are ignored when 
     calculating mean'''
  return nanmean(x)
#*********************************************************************

#*********************************************************************
def station_data(filepath):
    ''' Reads in Excel File into Pandas as data frame. Sorts the dates 
        in Acsending order and makes datetime pandas object. Averages
        data Hourly to create uniform time spacing between datafiles.
        Returns Pandas Data Frame.'''
    
    raw_data=pandas.io.excel.read_excel(filepath,header=0,
                                        skip_footer=3)
    raw_sort=raw_data.sort(axis=0,ascending=False)
    raw_sort.columns=['date','Temp','RH','Wind Speed',
                      'Wind Direction']
    
    raw_sort['date']=pandas.to_datetime(raw_sort['date'].map(
                     lambda x:x.rstrip('PDT')))

    data=raw_sort.set_index('date')  
    data=data.resample('H', how=NaNmean)
    
    return data
#*********************************************************************

#*********************************************************************
def Raws(filepath):
    '''Reads in .dat file from RAWS instruments as set up for Thesis
       work.Returns Pandas Data Frame matching format of Mesowest 
       station data.'''
    
    filename=filepath
    delimiter=','
    usecol=2,3,4,5
    usecoltime=[0]
    skip_rows=6

    data=n.loadtxt(filename, delimiter=delimiter,usecols=usecol,
                   skiprows=skip_rows)
    time=n.loadtxt(filename, delimiter=delimiter,usecols=usecoltime,
                   skiprows=skip_rows,dtype=str)
    Date=[dt.datetime.strptime(x,'"%Y-%m-%d %H:%M:%S"')for x in time]

    WS=data[:,2]
    WD=data[:,3]
    Temp=data[:,0]
    RH=data[:,1]
    
    Data=pandas.DataFrame({'date':pandas.to_datetime(Date),
                           'Temp':Temp,'RH':RH,
                           'Wind Speed':WS,'Wind Direction':WD})
    Data=Data.set_index('date') 
    Data=Data.resample('H', how=NaNmean)
    return Data
#*********************************************************************
def fit_line2(x, y):
    """Return slope, intercept of best fit line. For use with Pandas
    DataFrame(s)"""
    X=sm.add_constant(x)
    model = sm.OLS(y, X, missing='drop') #sm is stats model import
    print model
    #ignores entires where x or y is NaN
    fit = model.fit()
    return fit.params[1], fit.params[0],fit.bse[1]

def fit_line1(x, y):
    """Return slope, intercept of best fit line. For use with Pandas
    DataFrame(s)"""
    # Remove entries where either x or y is NaN.
    clean_data = pandas.concat([x, y], 1).dropna(0) # row-wise
    (_, x), (_, y) = clean_data.iteritems()
    slope, intercept, r, p, stderr = linregress(x, y)
    return slope, intercept, stderr # could also return stderr

  
#####################################################################
#  Plot all RCP multi model averages
#####################################################################
def avgplot(x,figurenum=None,color=None):
    '''Plots average temeratures with trend line and +/- Standard
    deviation with filled area.
    x=filename of a .npz file
    figurenum= number or name of a new figure
    color=color of lines in plots'''
    coast=[]
    land=[]
    variable=[]
    for i in range(len(x)):
      data=n.load(x[i])
      coast.append(data['coast'])
      land.append(data['land'])
      year=data['year']
      variable.append(str(data['variable']))
   
    p.figure(figurenum)
    p.subplot(2,1,2)

    slope1,inter1,r1,p1a,stderr1=stats.linregress(year,
       stats.nanmean(land[4:]))
    deviation1=n.array(land[4:]).std(axis=0)
    trend1=slope1*year+inter1
 
    slope2,inter2,r2,p1b,stderr2=stats.linregress(year,
        stats.nanmean(coast[4:]))
    deviation2=n.array(coast[4:]).std(axis=0)
    trend2=slope2*year+inter2
   
    for i in range(4):
      p.plot(year,land[i+4],label='Inland '+variable[i+4].upper(),
             color=color[i],
       linestyle='-')
      p.plot(year,coast[i+4],label='Coastal '+variable[i+4].upper(),
             color=color[i],
       linestyle='--')

    p.plot(year,trend1,'r',linewidth=2,
     label=r'trend ($2\sigma$)= %.3f $\pm$ %.3f'\
           r'$\frac{\circ C}{Decade}$' 
     %(slope1*10,stderr1*1.98*10))

    p.plot(year,trend2,'r',linewidth=2,linestyle='--',
      label=r'trend ($2\sigma$)= %.3f $\pm$ %.3f'\
            r'$\frac{\circ C}{Decade}$' 
      %(slope2*10,stderr2*1.98*10))

    p.fill_between(year,trend1+(deviation1+stderr1*1.98),
    trend1-(deviation1+stderr1*1.98),facecolor='red',alpha=.1)

    p.fill_between(year,trend2+(deviation2+stderr2*1.98),
    trend2-(deviation2+stderr2*1.98),facecolor='cyan',alpha=.1)

    p.legend(loc='upper left',title="Legend",fontsize=12,ncol=3)
    p.title('Average Minimum Temperatures for Various RCP Runs')
    p.xlim(1950,2099)
    p.ylim(0,30)
    p.xlabel('Years')
    p.ylabel(r'Temperature $\circ$C')

    p.subplot(2,1,1)

    slope1,inter1,r1,p1a,stderr1=stats.linregress(year,
       stats.nanmean(land[0:4]))
    deviation1=n.array(land[0:4]).std(axis=0)
    trend1=slope1*year+inter1
 
    slope2,inter2,r2,p1b,stderr2=stats.linregress(year,
        stats.nanmean(coast[0:4]))
    deviation2=n.array(coast[0:4]).std(axis=0)
    trend2=slope2*year+inter2
   
    for i in range(4):
      p.plot(year,land[i],label='Inland '+variable[i].upper(),
             color=color[i])
      p.plot(year,coast[i],label='Coastal '+variable[i].upper(),
             color=color[i],
       linestyle='--')

    p.plot(year,trend1,'r',linewidth=2,
     label=r'trend ($2\sigma$)= %.3f $\pm$ %.3f'\
           r'$\frac{\circ C}{Decade}$' 
     %(slope1*10,stderr1*1.98*10))

    p.plot(year,trend2,'r',linewidth=2,linestyle='--',
      label=r'trend ($2\sigma$)= %.3f $\pm$ %.3f'\
            r'$\frac{\circ C}{Decade}$' 
      %(slope2*10,stderr2*1.98*10))

    p.fill_between(year,trend1+(deviation1+stderr1*1.98),
    trend1-(deviation1+stderr1*1.98),facecolor='red',alpha=.1)

    p.fill_between(year,trend2+(deviation2+stderr2*1.98),
    trend2-(deviation2+stderr2*1.98),facecolor='cyan',alpha=.1)

    p.legend(loc='upper left',title="Legend",fontsize=12,ncol=3)
    p.title('Average Maximum Temperatures for Various RCP Runs')
    p.ylim(20,50)
    p.xlim(1950,2099)
    p.xlabel('Years')
    p.ylabel(r'Temperature $\circ$C')

    
#********************************************************************
#********************************************************************
#********************************************************************

#==============================================================
# Create plots for all enembles and multi-model mean
#==============================================================    

def modelplot(x,RCP,figurenum,variable):


   '''Finds the summer months and averages each model. Plots multi
   model mean with +/- standard error filled. Saves multimodel mean as
   a new .npz file.
   x=filename of .npz file to read
   RCP= integer or float of RCP value to be plotted
   figurenum= integer or string with figure number or name
   variable= string with variable name being plotted'''
   #===========================================================
   #          Read files
   #===========================================================
   data=n.load(x)
   lon=data['lon']
   lat=data['lat']
   dailytemp=data['dailytemp']
   days_in_month=data['days_in_month']
   num_days_summer=int(data['num_days_summer'])
   year=data['year']
   days=data['days']

   coast=n.ravel(n.where(lon<238.2))
   inland=n.ravel(n.where(lon>238.2))

   coastavg=stats.nanmean(stats.nanmean(dailytemp[:,:,:,coast],3),2)
   inlandavg=stats.nanmean(stats.nanmean(dailytemp[:,:,:,inland],3),2)

       
   summercoastavg=n.empty((len(coastavg[:,0]),
     (len(days)/num_days_summer)))
   summerinlandavg=n.empty((len(inlandavg[:,0]),
         (len(days)/num_days_summer)))
   start=0
   for i in range(len(coastavg[0,:])/num_days_summer):
      finish=start+num_days_summer-1
      summercoastavg[:,i]=stats.nanmean(coastavg[:,start:finish],1)
      summerinlandavg[:,i]=stats.nanmean(inlandavg[:,start:finish],1)
      start=finish+1
   
   
   p.figure(figurenum)
   #p.subplot(2,1,1)
   for k in range(len(summercoastavg[:,0])):
      p.plot(year,summercoastavg[k,:], alpha=.4,linewidth=.3) 
   slope,inter,r,p1,stderr=stats.linregress(year,
                           stats.nanmean(summercoastavg,0))    
   p.plot(year,stats.nanmean(summercoastavg,0),'k',linewidth=4,
   label=r'Multimodel Coastal Avg $trend=%.3f$ $\pm %.5f$'\
         r'$\frac{\circ C}{decade}$' %(slope*10,stderr*10*1.96))
   p.plot(year,slope*year+inter,'--r',linewidth=2,
          label='Coastal trend')
   deviation=summercoastavg.std(axis=0)
   p.fill_between(year,stats.nanmean(summercoastavg,0)+deviation,
    stats.nanmean(summercoastavg,0)-deviation,
    label='Standard Deviation',facecolor='tan',alpha=.4)
   #p.ylim(13,16)
   p.suptitle('Chrissy Williams') # Showing Author
   p.xlabel('Years') # x-axis label
   p.ylabel(r'Temperature ($\circ$C)') # y-axis label
   p.xlim(1950,2099)
   if variable=='tasmin':
       p.title((
   'May thru September Average Minimum Temperatures RCP'+str(RCP)))
   else:
       p.title((
    'May thru September Average Maximum Temperatures RCP'+str(RCP)))

   #p.subplot(2,1,2)
   for k in range(len(summerinlandavg[:,0])):
      p.plot(year,summerinlandavg[k,:], alpha=.4,linewidth=.3) 
   slope,inter,r,p1,stderr=stats.linregress(year,
     stats.nanmean(summerinlandavg,0))    
   p.plot(year,stats.nanmean(summerinlandavg,0),'b',linewidth=4,
   label=(r'Multimodel Inland Avg $trend=%.3f$ $\pm %.5f$'\
         r'$\frac{\circ C}{decade}$' 
    %(slope*10,stderr*10*1.96)))
   p.plot(year,slope*year+inter,'-.r',linewidth=2,
          label='Inland Trend')
   deviation=summerinlandavg.std(axis=0)
   p.fill_between(year,stats.nanmean(summerinlandavg,0)+deviation,
    stats.nanmean(summerinlandavg,0)-deviation,
    label='Standard Deviation',facecolor='tan',alpha=.4)

   p.legend(loc='best')

   p.show() # printing graph
   
   if 'max' in variable:
       print 'True'
       v='Maximum Temperatures RCP'
   else:
       v='Minimum Temperatures RCP'
   
   n.savez('/home/cwilliams/metr_174/data/average'+variable+str(RCP)+\
           '.npz',
     coast=stats.nanmean(summercoastavg,0),
     land=stats.nanmean(summerinlandavg,0),year=year,
     variable=(v+str(RCP)),slope=slope*10,stderr=stderr*10)
   
#*********************************************************************
#*********************************************************************
#*********************************************************************   

#==============================================================
#  Read in netcdf files and output summer days in .npz format
#==============================================================
   
def readdata(x,variable,rcp,in_filepath,out_filepath):
  '''Reads in NetCDFFile and outputs smallerfile as an .npz file
    x=filepath of .nc file to read
    variable= tasmin or tasmax as a string
    rcp=string e.g.('26')
    in_filepath=filepath of data to read
    out_filepath=filepath to output data to'''
  

  #==============================================================
  #          Read files
  #==============================================================


  days_in_month = n.loadtxt(
      in_filepath+"daysinmonth.txt",delimiter=',')

  datafile=S.NetCDFFile(x,mode='r')
  Tmax26=datafile.variables[variable].getValue()
  lat=datafile.variables['latitude'].getValue()
  lon=datafile.variables['longitude'].getValue()
  time=datafile.variables['time'].getValue()-.5

  #==============================================================
  #Replace NaN's
  #==============================================================

  nan=n.where(Tmax26 >100)
  Tmax26[nan]=n.nan
  temp=stats.nanmean(stats.nanmean(Tmax26,3),2)
  #==============================================================
  #       Find Summer Months
  #==============================================================
  time2=[]
  for i in range(len(days_in_month)):
      for j in range(int(days_in_month[i,1])):
        print j
        time2.append(int(days_in_month[i,0])) #month data is in
  time2=n.array(time2)
  summer=n.ravel(n.where((time2>=5)&(time2<=9))) #find summer months

  summerdays=31+30+31+31+30 #number of days in summer

  summertemp=Tmax26[:,summer,:,:]# summer tempers

  #==============================================================
  # Create readable time
  #==============================================================

  year = n.arange(len(summer)/float(summerdays))+1950
  days=n.arange(len(summer))/float(summerdays)+1950

  #==============================================================
  #save data
  #==============================================================
  n.savez(out_filepath+'summer_'+variable+rcp+'.npz'
       ,lat=lat,lon=lon, days_in_month=[31,30,31,31,30], days=days,
       num_days_summer=summerdays, dailytemp=summertemp, year=year)

def matchrcp(data,rcp):
  matchingRCP = [d for d in data if rcp in d]
  indexRCP=[]
  for m in matchingRCP:
      indexRCP.append(matchingRCP.index(m))
  return indexRCP[0]
      
def matchmodel(datanames,model):
    matchingModel=[m for m in datanames if model in m]
    indexmodel=[]
    for m in matchingModel:
      indexmodel.append(matchingModel.index(m))
    return indexmodel  
    
def modelnames(data,rcp):
  index=matchrcp(data,str(rcp))
  datanames=[]
  text_file = open(data[index], "r")
  datanames.append(text_file.readlines())
  #
  #print a
  for name in datanames:
    names=[name.replace('.rcp'+str(rcp)+'\n','') for name in name]
  for name in names: 
      names=[name.replace(".",'-run') for name in names] 
  return names
