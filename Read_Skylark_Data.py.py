#Chrissy Rogers
#Thesis Data Logger Dataset
#
#Reads in .dat file output from CR1000 datalogger.
#Plots raw data
#--------------------------------------------------------------------

#====================================================================
#Import Libraries
#=====================================================================
import numpy as n
import matplotlib.pyplot as p
import matplotlib.dates as md
import datetime as dt
import matplotlib.ticker as tic
#--------------------------------------------------------------------
#define variables
#====================================================================
filename="C:\Users\cmw1229\Google Drive\Thesis Work\Chrissy.dat"
delimiter=','
usecol=2,3,4,5
usecoltime=[0]
skip_rows=6

#--------------------------------------------------------------------
# Read data and create arrays
#====================================================================
data=n.loadtxt(filename, delimiter=delimiter, usecols=usecol,skiprows=skip_rows)

time=n.loadtxt(filename, delimiter=delimiter, usecols=usecoltime,skiprows=skip_rows,dtype=str)

WS=data[:,2]

WD=data[:,3]

Temp=data[:,0]

RH=data[:,1]

Date=[dt.datetime.strptime(x,'"%Y-%m-%d %H:%M:%S"') for x in time]
#--------------------------------------------------------------------
# Plot Raw Data
#====================================================================
p.figure(1)
p.suptitle('Chrissy Rogers\nThesis RAWS')

p.subplot(211)
p.title('Temperature')
ax=p.gca()
major_locator=md.DayLocator()
ax.xaxis.set_major_locator(major_locator )
ax.xaxis.set_major_formatter(md.DateFormatter('%m/%d/%Y'))
p.plot(Date,Temp,'magenta')
p.ylabel('Temperature (C)')
p.gcf().autofmt_xdate()

p.subplot(212)
p.title('Relative Humidity')
ax=p.gca()
major_locator=md.DayLocator()
ax.xaxis.set_major_locator(major_locator )
ax.xaxis.set_major_formatter(md.DateFormatter('%m/%d/%Y'))
p.plot(Date,RH,'b')
p.ylabel('Relative Humidity (%)')
p.gcf().autofmt_xdate(rotation=90)

p.figure(2)
p.suptitle('Chrissy Rogers\nThesis RAWS')
p.subplot(211)
p.title('Wind Speed')
ax=p.gca()
major_locator=md.DayLocator()
ax.xaxis.set_major_locator(major_locator )
ax.xaxis.set_major_formatter(md.DateFormatter('%m/%d/%Y'))
p.plot(Date,WS)
p.ylabel('m/s')
p.xlabel('Time (PDT)')
p.gcf().autofmt_xdate()

p.subplot(212)
p.title('Wind Direction')
ax=p.gca()
major_locator=md.DayLocator()
ax.xaxis.set_major_locator(major_locator )
ax.xaxis.set_major_formatter(md.DateFormatter('%m/%d/%Y'))
p.plot(Date,WD,'ko--')
p.ylabel('deg')
p.xlabel('Time (PDT)')
p.gcf().autofmt_xdate(rotation=90)

p.show()
