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




output=pd.read_csv(r'D:\Research\D8_ready\sorted\B4bSS\output.csv')
os.chdir(r'D:\Research\D8_ready\sorted\B4bSS')

output.columns

DancerPosition=pd.DataFrame();
BlanketTention=pd.DataFrame();


for ind in output.index:
    # tmp=list(map(float, output['dancer all'][ind].split('@')))
    # DancerPosition=pd.concat([DancerPosition,pd.Series(tmp)],axis=1).rename(columns={0:output['timestamp'][ind]})
    # tmp=list(map(float, output[' blanket all'][ind].split('@')))
    # BlanketTention=pd.concat([BlanketTention,pd.Series(tmp)],axis=1).rename(columns={0:output['timestamp'][ind]})
    tmp=list(map(float, output['DancerPositionActual_All'][ind].split('@')))
    DancerPosition=pd.concat([DancerPosition,pd.Series(tmp)],axis=1).rename(columns={0:output['timestamp'][ind]})
    tmp=list(map(float, output['BlanketTension_All'][ind].split('@')))
    BlanketTention=pd.concat([BlanketTention,pd.Series(tmp)],axis=1).rename(columns={0:output['timestamp'][ind]})

DancerPosition = DancerPosition.loc[:,~DancerPosition.columns.duplicated()].copy()
BlanketTention = BlanketTention.loc[:,~BlanketTention.columns.duplicated()].copy()


n = 100
DancerPosition.drop(index=DancerPosition.index[:n],inplace=True)

BlanketTention.drop(index=BlanketTention.index[:n],inplace=True)


DancerPosition=DancerPosition.reset_index(drop=True)

BlanketTention=BlanketTention.reset_index(drop=True)


columnsDF= list(BlanketTention.columns)

columnsDF.sort()
# col=list(BlanketTention.columns)

# a=BlanketTention[col[0]].rolling(5).mean()
#################################################################
#################################################################
#################################################################

figDancerPosition = go.Figure()
#


for col in columnsDF:
    if len(np.where(DancerPosition[col].isnull() == True)[0]):
        if np.where(DancerPosition[col].isnull() == True)[0][0]<300:
            continue
    figDancerPosition.add_trace(go.Scatter(y=list(DancerPosition[col]-DancerPosition[col][0]),
                name=str(col)))


            

# fig.update_layout(title='ImagePlacement_Right')
# fig.update_layout(title='ImagePlacement_Left')

figDancerPosition.update_layout(title='DancerPosition')


figDancerPosition.update_layout(
    hoverlabel=dict(
        namelength=-1
    )
)

# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
plot(figDancerPosition,auto_play=True,filename="Scale_FRONT_AQM_"+ dt_string +".html")  
#plot(fig_back,filename="AQM-Back.html")  
figDancerPosition.show()


#################################################################
#################################################################
#################################################################

figBlanketTention = go.Figure()
#


for col in columnsDF:
    if len(np.where(BlanketTention[col].isnull() == True)[0]):
        if np.where(BlanketTention[col].isnull() == True)[0][0]<300:
            continue;
    figBlanketTention.add_trace(go.Scatter(y=list(BlanketTention[col]-BlanketTention[col][0]),
                    name=str(col)))


            

# fig.update_layout(title='ImagePlacement_Right')
# fig.update_layout(title='ImagePlacement_Left')

figBlanketTention.update_layout(title='BlanketTention')


figBlanketTention.update_layout(
    hoverlabel=dict(
        namelength=-1
    )
)

# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
plot(figBlanketTention,auto_play=True,filename="Scale_FRONT_AQM_"+ dt_string +".html")  
#plot(fig_back,filename="AQM-Back.html")  
figBlanketTention.show()

########################################################################
########################################################################
########################################################################
########################################################################
########################################################################

PosTen=pd.DataFrame();
PosTenCumSum=pd.DataFrame();

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
figPosTen.show()

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
figSlop.show()

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
figSlopAll.show()

# plt.figure()
# plt.plot(SlopData['Slop'])


#################################################################
#################################################################
#################################################################











#################################################################
#################################################################
#################################################################

winsowSize= 30
movingAVRBlanketTention=BlanketTention.rolling(winsowSize).mean()



figBlanketTentionAVR = go.Figure()
#


for col in columnsDF:

    res = list(filter(lambda item: not math.isnan(item), list(movingAVRBlanketTention[col])))
    if len(res)>300:
        figBlanketTentionAVR.add_trace(go.Scatter(y=res,
                        name=col))


            

# fig.update_layout(title='ImagePlacement_Right')
# fig.update_layout(title='ImagePlacement_Left')

figBlanketTentionAVR.update_layout(title='BlanketTention moving AVR window size='+str(winsowSize))


figBlanketTentionAVR.update_layout(
    hoverlabel=dict(
        namelength=-1
    )
)

# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
plot(figBlanketTentionAVR,auto_play=True,filename="Scale_FRONT_AQM_"+ dt_string +".html")  
#plot(fig_back,filename="AQM-Back.html")  
figBlanketTentionAVR.show()

