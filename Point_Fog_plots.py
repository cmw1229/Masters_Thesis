import pandas
import matplotlib.pyplot as p
import matplotlib.lines as mlines
import numpy as n
import seaborn as sns
from scipy.stats import linregress
from scipy.optimize import curve_fit
import math


MainPath='C:\Users\cmw1229\Google Drive\Thesis Work'
outfile='C:\Users\cmw1229\Google Drive\Thesis Work\Images'

import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)

coast=pandas.io.pickle.read_pickle(
    MainPath+'\Pickled Files\Fog_diff_coast.pkl').sort()
diablo=pandas.io.pickle.read_pickle(
    MainPath+'\Pickled Files\Fog_diff_diablo.pkl').sort()
valley=pandas.io.pickle.read_pickle(
    MainPath+'\Pickled Files\Fog_diff_valley.pkl').sort()
#**********************************************************************
coast['Fog']=coast['Fog']
#coast=coast.apply(n.round)

diablo['Fog']=diablo['Fog']
#diablo=diablo.apply(n.round)

valley['Fog']=valley['Fog']
#valley=valley.apply(n.round)



  #*********************************************************************
  #Curve Fitting 
  #*********************************************************************

xc=n.round(n.linspace(5,35,len(coast['Diff'])))
slope_c,inter_c,r_c,P_c,stderr_c=linregress(coast['Diff'],coast['Fog'])
c_trend=slope_c*xc+inter_c

xd=n.round(n.linspace(5,35,len(diablo['Diff'])))
slope_d,inter_d,r_d,P_d,stderr_d=linregress(diablo['Diff'],diablo['Fog'])
d_trend=slope_d*xd+inter_d

xv=n.round(n.linspace(5,35,len(valley['Diff'])))
slope_v,inter_v,r_v,P_v,stderr_v=linregress(valley['Diff'],valley['Fog'])
v_trend=slope_v*xv+inter_v

#=====================================================================
# Calculate least squares fit & correlation coefficient
#=====================================================================
N=len(coast['Diff'])
x=coast['Diff']
y=coast['Fog']


sum_x=float(n.sum(x))
sum_y=float(n.sum(y))

sum_x2=0
sum_xy=0

for i in range(len(x)):
    sum_x2+=float(x[i]**2)
    sum_xy+=float(x[i]*y[i])
        
delta=N*sum_x2-(sum_x**2)

intercept=(sum_x2*sum_y-sum_x*sum_xy)/delta # eq. ok
slope=(N*sum_xy-sum_x*sum_y)/delta # eq. ok

sum_4sigmaY=0
sum_4sigmaX=0

sum_4sigma_y_ybar=0  #for calculated r

sum_4sigmaY_plus=0
sum_4sigmaY_minus=0
sum_4sigmaY_16=0

sum_4sigma_xy=0
x_bar=sum_x/N
y_bar=sum_y/N

for i in range(len(x)):
    sum_4sigmaY+=(y[i]-intercept-slope*x[i])**2 # eq. ok
    sum_4sigmaX+=(x[i]-x_bar)**2 # eq. ok
    sum_4sigma_y_ybar=(y[i]-y_bar)**2

    
sigma_y=math.sqrt((1./(N-2))*sum_4sigmaY) #std of y      # eq. ok  #scipy uses N-8.703
sigma_x=math.sqrt((1./(N-1))*sum_4sigmaX) #std of x      # eq. ok

sigma_intercept_95=sigma_y*n.sqrt(sum_x2/delta)*1.96  #stderr of Intercept  # eq. ok
sigma_slope_95=sigma_y*n.sqrt(N/delta)*1.96 #stderr of Slope  # eq. ok

for i in range(len(x)):
    sum_4sigmaY_plus+=(y[i]-(intercept+sigma_intercept_95/1.96)-slope*x[i])**2 # eq. ok
    sum_4sigmaY_minus+=(y[i]-(intercept-sigma_intercept_95/1.96)-slope*x[i])**2 # eq. ok
    sum_4sigmaY_16+=(y[i]-(16)-slope*x[i])**2 #16 is my Chosen intercept    # eq. ok
    
    sum_4sigma_xy+=(x[i]-x_bar)*(y[i]-y_bar)

sigma_xy=sum_4sigma_xy/float(N) # eq. ok scipy.stats uses N-1
sigma_y_plus=math.sqrt((1./(N-2))*sum_4sigmaY_plus) # eq. ok
sigma_y_minus=math.sqrt((1./(N-2))*sum_4sigmaY_minus) # eq. ok
sigma_y_16=math.sqrt((1./(N-2))*sum_4sigmaY_16) # eq. ok

r=sigma_xy/(sigma_x*sigma_y)
r_plus=sigma_xy/(sigma_x*sigma_y_plus)
r_minus=sigma_xy/(sigma_x*sigma_y_minus)
r_16=sigma_xy/(sigma_x*sigma_y_16)
print r,r_plus,r_minus


line1=slope*xc+intercept+sigma_intercept_95
line2=slope*xc+intercept-sigma_intercept_95
line3=slope*xc+16
    
#====================================================================
#Plotting
#====================================================================

#*********************************************************************
fig=p.figure('Scatter Original Subplots',figsize=(14.4,9),dpi=100)

fig.add_subplot(311)
ax=p.gca()
ax.scatter(coast['Diff'],coast['Fog'],label=r'$Original\/ Data\/ (Coast)$',
  zorder=1,color='dodgerblue')


#--------------------------------------------------------------------
# For Coast Only Plot (Comment out for all plots)
#---------------------------------------------------------------------
#ax.plot(xc,c_trend,color='mediumblue',zorder=2,
    #label=r'$Coast\/ Region\/ Trend$'\
    #r' $%.3f$ $\pm$ $%.3f$ $\frac{Hours}{\Delta T}$'\
    #%(slope_c,1.96*stderr_c)+r' $\cdots \cdots \cdots \cdots \cdots$ $r=%.3f$'%(r))
#ax.plot(xc,line1,color='k',linestyle='--',
#label=r'$y=%.3fx+(%.3f$'%(slope,intercept)+' $\pm$ $%.3f)$'%(sigma_intercept_95)+
#   r' $\cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots$ $r=%.3f$'%(r_plus))
#ax.plot(xc,line2,color='k',linestyle='--')
#ax.plot(xc,line3,color='r',linestyle='-.',linewidth=2,
#   label=r'$y=%.3fx+16$'%(slope)+' $(Best\/Fit\/ for\/ Regional\/ Tdiff)$'+
#   r' $\cdots \cdots$ $r=%.3f$'%(r_16))
#---------------------------------------------------------------------

ax.plot(xc,c_trend,color='mediumblue',zorder=2,
    label=r'$Coast\/ Region\/ Trend$'\
    r' $%.3f$ $\pm$ $%.3f$ $\frac{Hours}{\Delta T}$'\
    %(slope_c,1.96*stderr_c))
ax.annotate(r'$y=%.3fx+%.3f$'%(slope_c,inter_c)+'\n'+r'$r=%.3f$'%(r),
xy=(xc[-3],c_trend[-3]),xytext=(37,12.5),arrowprops=dict(facecolor='black',width=.1,headwidth=5,alpha=.8),
            horizontalalignment='center',
            verticalalignment='bottom',fontsize=11)
p.xlim(0,40)
p.ylim(0,20)
p.locator_params(axis='y',nbins=5)
legand=ax.legend(loc='lower left',
      frameon=False,fontsize=11)
for label in legand.get_lines():
      label.set_linewidth(2)

fig.add_subplot(312)
ax1=p.gca()
ax1.scatter(diablo['Diff'],diablo['Fog'],label=r'$Original\/ Data\/ (Diablo\/ range)$',
  zorder=3,color='mediumvioletred')
ax1.plot(xd,d_trend,color='darkmagenta',zorder=4,
    label=r'$Diablo\/ Range\/ Region\/ Trend$'\
    r' $%.3f$ $ \pm$ $%.3f$ $\frac{Hours}{\Delta T}$'%(slope_d,1.96*stderr_d))
ax1.annotate(r'$y=%.2fx+%.2f$ '%(slope_d,inter_d)+'\n'+r'$r=%.3f$'%(r_d),
xy=(xd[-3],d_trend[-3]),xytext=(37,12.5),arrowprops=dict(facecolor='black',width=.1,headwidth=5,alpha=.8),
            horizontalalignment='center',
            verticalalignment='bottom',fontsize=11)
p.locator_params(axis='y',nbins=5)
p.xlim(0,40)
p.ylim(0,18)
legand1=ax1.legend(loc='upper left',
      frameon=False,fontsize=11)
for label in legand1.get_lines():
      label.set_linewidth(2) 
       
fig.add_subplot(313) 
ax2=p.gca()   
ax2.scatter(valley['Diff'],valley['Fog'],label=r'$Original\/ Data\/ (Valley)$',
  zorder=6,color='darkorange')
ax2.plot(xv,v_trend,color='orangered',zorder=6,
    label=r'$Valley\/ Region\/ Trend$'\
    r' $%.3f$ $ \pm$ $%.3f$ $\frac{Hours}{\Delta T}$'\
    %(slope_v,1.96*stderr_v))
ax2.annotate(r'$y=%.2fx+%.2f$ '%(slope_v,inter_v)+'\n'+r'$r=%.3f$'%(r_v),
xy=(xv[-3],v_trend[-3]),xytext=(37,12.5),arrowprops=dict(facecolor='black',width=.1,headwidth=5,alpha=.8),
            horizontalalignment='center',
            verticalalignment='bottom',fontsize=11)
p.locator_params(axis='y',nbins=5)
p.xlim(0,40)
p.ylim(0,18)
legand2=ax2.legend(loc='upper left',
  frameon=False,fontsize=11)
for label in legand2.get_lines():
      label.set_linewidth(2)
              
p.suptitle('Fog Hours vs. Temperature Difference',fontsize=20)
A=r'$\Delta T$ $^{\circ}F$'
B='Fog Hours' 
p.tick_params(axis='both', which='major', labelsize=14,color='black')
p.subplots_adjust(left=.05,right=.95,top=.9,bottom=.1,wspace=.1)

  
fig.text(0.5, 0.04, A, ha='center', va='center',fontsize=16,
  fontweight='bold')
fig.text(0.025, 0.5, B, ha='center', va='center', rotation='vertical',
  fontsize=16,fontweight='bold')

#handles, labels= ax.get_legend_handles_labels()
#handles1, labels1 = ax1.get_legend_handles_labels()
#handles2, labels2 = ax1.get_legend_handles_labels()
#labels_all=(labels[-1],labels[0],labels1[-1],labels1[0],labels2[-1],labels2[0])
#handles_all=(handles[-1],handles[0],handles1[-1],handles1[0],handles2[-1],handles2[0])



fig.savefig(outfile+'/Scatter_Original.png',orientation='landscape',dpi=300)
#fig.savefig(outfile+'/Coast_Scatter_Original.png',orientation='landscape',dpi=300)
#*********************************************************************
p.figure('Scatter Original All',figsize=(14.4,9),dpi=100)
ax=p.gca()
ax.scatter(coast['Diff'],coast['Fog'],label=r'$Original\/ Data\/ (Coast)$',
  zorder=1,color='dodgerblue')
ax.plot(xc,c_trend,color='mediumblue',zorder=2,
    label=r'$Coast\/ Region\/ Trend$'\
    r' $%.3f \pm{%.3f}$ $\frac{Hours}{\Delta T}$'\
    %(slope_c,1.96*stderr_c)+'\n'+r'$y=%.2fx+%.2f$'%(slope_c,inter_c))

ax.scatter(diablo['Diff'],diablo['Fog'],label=r'$Original\/ Data\/ (Diablo\/ range)$',
  zorder=3,color='mediumvioletred')
ax.plot(xd,d_trend,color='darkmagenta',zorder=4,
    label=r'$Diablo\/ Range\/ Region\/ Trend$'\
    r' $%.3f \pm{%.3f}$ $\frac{Hours}{\Delta T}$'\
    %(slope_d,1.96*stderr_d)+'\n'+r'$y=%.2fx+%.2f$'%(slope_d,inter_d))
ax.scatter(valley['Diff'],valley['Fog'],label=r'$Original\/ Data\/ (Valley)$',
  zorder=6,color='darkorange')
ax.plot(xv,v_trend,color='orangered',zorder=6,
    label=r'$Valley\/ Region\/ Trend$'\
    r' $%.3f \pm{%.3f}$ $\frac{Hours}{\Delta T}$'\
    %(slope_v,1.96*stderr_v)+'\n'+r'$y=%.2fx+%.2f$'%(slope_v,inter_v))
 
p.title('Fog Hours vs. Temperature Difference',fontsize=20)
p.xlabel(r'Temperature Difference $^{\circ}F$',fontsize=16)
p.ylabel('Fog Hours',fontsize=16)
p.xlim(0,40)
p.ylim(0,18)
handles, labels = ax.get_legend_handles_labels()
labels=(labels[-3],labels[0],labels[-2],labels[1],labels[-1],labels[2])
handles=(handles[-3],handles[0],handles[-2],handles[1],handles[-1],handles[2])

p.subplots_adjust(left=.05,right=.98,top=.94,bottom=.1)
legend=p.legend(handles=handles, labels=labels,frameon=True,fontsize=12,ncol=3,loc='upper center')
for label in legend.get_lines():
      label.set_linewidth(2)

p.tick_params(axis='both', which='major', labelsize=14,color='black')

p.savefig(outfile+'/Scatter_Original_All.png',orientation='landscape',dpi=300)

#rcParams['mathtext.default'] = 'regular'
#********************************************************************

#fig=p.figure('Box Scatter')
#
#ax1=fig.add_subplot(311)
##sns.set_style('white')
#sns.set_style('whitegrid')
#sns.set_context('talk')
#
#ax=sns.boxplot(x='Diff',y='Fog',data=coast.sort('Diff'),color='white',
#   whis=3)
#ax=sns.stripplot(x='Diff',y='Fog',data=coast.sort('Diff'),size=6,
#   jitter=True,color='purple',edgecolor='black')
#
#ax.grid(b=True,linestyle='--',linewidth=1,color='DarkGrey')
#
#median_c=mlines.Line2D ([],[],color='red',linestyle='-',
#  label='Median (Coast Region)')
#mean_c=mlines.Line2D([],[],color='red',linestyle='None',marker='s',
#  markersize=9,label='Mean (Coast Region)')
#points_c=mlines.Line2D([],[],color='purple',linestyle='None',marker='o',
#   markersize=6,label='Data Points (Coast Region)')
#p.ylim(0,15)
#p.ylabel=''
#p.xlabel=''
#p.legend(handles=[median_c,mean_c,points_c],frameon=True,fancybox=True)
#   
#ax2=fig.add_subplot(312)
#sns.set_style('whitegrid')
#sns.set_context('talk')  
#ax_d=sns.boxplot(x='Diff',y='Fog',data=diablo.sort('Diff'),color='white',
#   whis=3)
#ax_d=sns.stripplot(x='Diff',y='Fog',data=diablo.sort('Diff'),size=6,
#   jitter=True,color='green',edgecolor='black')
#
#ax_d.grid(b=True,linestyle='--',linewidth=1,color='DarkGrey')
#
#median_d=mlines.Line2D ([],[],color='red',linestyle='-',
#  label='Median (Diablo Range Region)')
#mean_d=mlines.Line2D([],[],color='red',linestyle='None',marker='s',
#  markersize=9,label='Mean (Diablo Range Region)')
#points_d=mlines.Line2D([],[],color='green',linestyle='None',marker='o',
#   markersize=6,label='Data Points (Diablo Region)')
#p.ylim(0,15)
#p.ylabel=''
#p.xlabel=''
#p.legend(handles=[median_d,mean_d,points_d],frameon=True,fancybox=True)   
#
#ax3=fig.add_subplot(313)
#sns.set_style('whitegrid')
#sns.set_context('talk')      
#ax_v=sns.boxplot(x='Diff',y='Fog',data=valley.sort('Diff'),color='white',
#   whis=3)
#ax_v=sns.stripplot(x='Diff',y='Fog',data=valley.sort('Diff'),size=6,
#   jitter=True,color='darkcyan',edgecolor='black')
#
#ax_v.grid(b=True,linestyle='--',linewidth=1,color='DarkGrey')
#
#median_v=mlines.Line2D ([],[],color='red',linestyle='-',
#  label='Median (Valley Region)')
#mean_v=mlines.Line2D([],[],color='red',linestyle='None',marker='s',
#  markersize=9,label='Mean (Valley Region)')
#points_v=mlines.Line2D([],[],color='blue',linestyle='None',marker='o',
#   markersize=6,label='Data Points (Valley Region)')
#p.ylim(0,15)
#p.xlabel=''
#p.legend(handles=[median_v,mean_v,points_v],frameon=True,fancybox=True)   
#   
#p.suptitle('Diurnal Temperature Difference vs 9yr Average Fog Hours',
#  fontsize=18,fontweight='bold')
#A=(r'Diurnal Temperature Difference $^{\circ}F$ (Summer Average)')
#B=('Daily Number of Fog Hours (9yr Mean)')
#
#   
#fig.text(0.3, 0.04, A, ha='center', va='center',fontsize=16,
#  fontweight='bold')
#fig.text(0.06, 0.5, B, ha='center', va='center', rotation='vertical',
#  fontsize=16,fontweight='bold')



#p.show()