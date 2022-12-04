# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 14:26:02 2022

@author: Ireneg
"""
import os


import numpy as np
from matplotlib import pyplot as plt
import scipy.io
from datetime import datetime
import glob
from zipfile import ZipFile 
from pathlib import Path
from collections import OrderedDict
from scipy.signal import savgol_filter

# Load the Pandas libraries with alias 'pd' 
import pandas as pd 
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot
from plotly.subplots import make_subplots
import math

def plot_fig(data, title, mach):


    fig = go.Figure()
    columnsDF= list(dictdict[dictitem].columns)
    columnsDF.sort()
    for col in columnsDF:
        if len(np.where(dictdict[dictitem][col].isnull() == True)[0]):
            if np.where(dictdict[dictitem][col].isnull() == True)[0][0]<300:
                continue
        fig.add_trace(go.Scatter(y=list(dictdict[dictitem][col]-dictdict[dictitem][col][0]),
                    name=str(col)))



    fig.update_layout(title=title)

    fig.update_layout(
        hoverlabel=dict(
            namelength=-1
        )
    )

    # datetime object containing current date and time

    # dd/mm/YY H:M:S
    dt_string = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    plot(fig,auto_play=True,filename=f"{mach}_{dt_string}.html")   

def plot_rolling(data, type, winsowSize, mach):
    fig = go.Figure()
    #
    movingAVRBlanketTention=BlanketTention.rolling(winsowSize).mean()
    columnsDF = movingAVRBlanketTention.columns
    for col in columnsDF:

        res = list(filter(lambda item: not math.isnan(item), list(movingAVRBlanketTention[col])))
        if len(res)>300:
            fig.add_trace(go.Scatter(y=res,
                            name=col))



    fig.update_layout(title=f"{mach}_{type} moving AVR window size={winsowSize}")


    fig.update_layout(
        hoverlabel=dict(
            namelength=-1
        )
    )

    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    plot(fig,auto_play=True,filename="Scale_FRONT_AQM_"+ dt_string +".html")  
    #plot(fig_back,filename="AQM-Back.html")  





dirdir = "D:\Logs\Research\D14 seam open\D14 15.9_15.10 ready with loadCellDiff\sorted\B4bSS"
output=pd.read_csv(f'{dirdir}\output.csv')
os.chdir(dirdir)
mach="D14"

#output.columns

dictdict = {}
for col in output.columns:
    if col!="mach" and col!="path" and col!="timestamp" and col not in dictdict:
        dictdict[col] = pd.DataFrame()


for ind, row in output.iterrows():
    for dictitem in dictdict:
        tmp=list(map(float, output[dictitem][ind].split('@')))
        dictdict[dictitem]=pd.concat([dictdict[dictitem],pd.Series(tmp)],axis=1).rename(columns={0:output['timestamp'][ind]})

n = 100
for dictitem in dictdict:
    dictdict[dictitem] = dictdict[dictitem].loc[:,~dictdict[dictitem].columns.duplicated()].copy()
    #dictdict[dictitem].columns.sort_values()
    dictdict[dictitem].drop(index=dictdict[dictitem].index[:n],inplace=True)
    dictdict[dictitem]=dictdict[dictitem].reset_index(drop=True)




#################################################################
#################################################################
#################################################################


#for dictitem in dictdict:
#    plot_fig(dictdict[dictitem], dictitem, mach)
    



########################################################################
########################################################################
########################################################################
########################################################################
########################################################################

PosTen=pd.DataFrame()
PosTenCumSum=pd.DataFrame()

DancerPosition = dictdict["DancerPositionActual_All"]
BlanketTention = dictdict["BlanketTension_All"]

for col in DancerPosition.columns:
    if len(np.where(DancerPosition[col].isnull() == True)[0]):
        if np.where(DancerPosition[col].isnull() == True)[0][0]<100:
            continue
    else:
        continue;
    y=[]
    for i in range(len(DancerPosition[col])):
        y.append((DancerPosition[col][i]-DancerPosition[col][0])*(BlanketTention[col][i]-BlanketTention[col][0]))
    
    arr1 = np.cumsum(y);
    
    PosTen=pd.concat([PosTen,pd.Series(y)],axis=1).rename(columns={0:col})
    PosTenCumSum=pd.concat([PosTenCumSum,pd.Series(arr1)],axis=1).rename(columns={0:col})







columnsDF = pd.to_datetime(PosTenCumSum.columns,dayfirst=False)

colDic={}

for i,col in enumerate(PosTenCumSum.columns):
    # print(col + ' vs '+ str(columnsDF[i]))
    colDic[col]= (columnsDF[i])

PosTenCumSum=PosTenCumSum.rename(columns=colDic)
PosTen=PosTen.rename(columns=colDic)

cols=list(columnsDF)

cols.sort()

figPosTen = go.Figure()
#


for col in cols:
    if len(np.where(PosTenCumSum[col].isnull() == True)[0]):
        if np.where(PosTenCumSum[col].isnull() == True)[0][0]<100:
            continue
    
    figPosTen.add_trace(go.Scatter(y=list(PosTenCumSum[col]),
                    name=str(col)))


            



# fig.update_layout(title='ImagePlacement_Right')
# fig.update_layout(title='ImagePlacement_Left')

figPosTen.update_layout(title='Pos * Ten')


figPosTen.update_layout(
    hoverlabel=dict(
        namelength=-1
    )
)

# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
plot(figPosTen,auto_play=True,filename="PosTenD8_"+ dt_string +".html")  
#plot(fig_back,filename="AQM-Back.html")  

#################################################################
#################################################################
#################################################################
SlopData=pd.DataFrame(columns=['Date Of Min Slop','Slop'])
SlopDay=pd.DataFrame()
minDaySlop=0
MinSlopDate=cols[0]
dateEvents=[]
DayList=[]
dateEvents.append(cols[0].date())
for col in cols:
    inx=(PosTenCumSum[col].reindex(index=PosTenCumSum[col].index[::-1])).first_valid_index()
    z=np.polyfit(list(PosTenCumSum[col][:inx].index),list(PosTenCumSum[col][:inx]),1)[0]
    if col.date() in dateEvents:
        DayList.append(z)
        if z<minDaySlop:
            minDaySlop=z
            MinSlopDate=col
    else:
       SlopDay=pd.concat([SlopDay,pd.Series(DayList)],axis=1).rename(columns={0:col.date()}) 
       DayList=[]
       dateEvents.append(col.date()) 
       SlopData=pd.concat([SlopData,pd.DataFrame([[str(MinSlopDate),minDaySlop]], columns=['Date Of Min Slop','Slop'])],axis=0)
       minDaySlop=z;
       MinSlopDate=col
    

SlopData=SlopData.reset_index(drop=True)
###### PLOT 

figSlop = go.Figure()

figSlop.add_trace(go.Scatter(y=list(SlopData['Slop']),
                name='Min Slop Per Day'))
for i in range(len(SlopData['Date Of Min Slop'])):
     figSlop.add_trace(go.Scatter(x=[i], y=[SlopData['Slop'][i]],
                             marker=dict(color="green", size=6),
                             mode="markers",
                             text="{0:.3f}".format(SlopData['Slop'][i])+'  '+SlopData['Date Of Min Slop'][i],
                             # font_size=18,
                             hoverinfo='text'))
     figSlop.data[len(figSlop.data)-1].showlegend = False

now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
plot(figSlop,auto_play=True,filename="MinSlop_"+ dt_string +".html")  
#plot(fig_back,filename="AQM-Back.html")  

#################################################################
#################################################################
#################################################################

AllSlope=pd.DataFrame(columns=['Date Time','Slop'])

for col in cols:
   inx=(PosTenCumSum[col].reindex(index=PosTenCumSum[col].index[::-1])).first_valid_index()
   z=np.polyfit(list(PosTenCumSum[col][:inx].index),list(PosTenCumSum[col][:inx]),1)[0] 
   AllSlope=pd.concat([AllSlope,pd.DataFrame([[str(col),z]], columns=['Date Time','Slop'])],axis=0)

AllSlope=AllSlope.reset_index(drop=True)



###### PLOT 

figSlopAll = go.Figure()

figSlopAll.add_trace(go.Scatter(y=list(AllSlope['Slop']),
                name='Slop Per Ready'))
for i in range(len(AllSlope['Date Time'])):
     figSlopAll.add_trace(go.Scatter(x=[i], y=[AllSlope['Slop'][i]],
                             marker=dict(color="green", size=6),
                             mode="markers",
                             text="{0:.3f}".format(AllSlope['Slop'][i])+'  '+AllSlope['Date Time'][i],
                             # font_size=18,
                             hoverinfo='text'))
     figSlopAll.data[len(figSlopAll.data)-1].showlegend = False

now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
plot(figSlopAll,auto_play=True,filename="SlopForReady_"+ dt_string +".html")  
#plot(fig_back,filename="AQM-Back.html")  

# plt.figure()
# plt.plot(SlopData['Slop'])


#################################################################
#################################################################
#################################################################






winsowSize= 30
key = 'BlanketTension_All'
plot_rolling(dictdict[key], key, winsowSize, mach)



#################################################################
#################################################################
#################################################################





