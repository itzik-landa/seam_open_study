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




output=pd.read_csv(r'D:\Logs\Research\D14 seam open\D14 1.9-1.11 ready behavior\sorted\B4bSS\output.csv')

output.columns

DancerPosition=pd.DataFrame();
BlanketTention=pd.DataFrame();


for ind in output.index:
    tmp=list(map(float, output['DancerPositionActual_All'][ind].split('@')))
    DancerPosition=pd.concat([DancerPosition,pd.Series(tmp)],axis=1).rename(columns={0:output['timestamp'][ind]})
    tmp=list(map(float, output['BlanketTension_All'][ind].split('@')))
    BlanketTention=pd.concat([BlanketTention,pd.Series(tmp)],axis=1).rename(columns={0:output['timestamp'][ind]})

DancerPosition = DancerPosition.loc[:,~DancerPosition.columns.duplicated()].copy()
BlanketTention = BlanketTention.loc[:,~BlanketTention.columns.duplicated()].copy()





# col=list(BlanketTention.columns)

# a=BlanketTention[col[0]].rolling(5).mean()
#################################################################
#################################################################
#################################################################

figDancerPosition = go.Figure()
#


for col in DancerPosition.columns:
    if len(np.where(DancerPosition[col].isnull() == True)[0]):
        if np.where(DancerPosition[col].isnull() == True)[0][0]<300:
            continue
    figDancerPosition.add_trace(go.Scatter(y=list(DancerPosition[col]),
                name=col))


            

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


for col in BlanketTention.columns:
    if len(np.where(BlanketTention[col].isnull() == True)[0]):
        if np.where(BlanketTention[col].isnull() == True)[0][0]<300:
            continue;
    figBlanketTention.add_trace(go.Scatter(y=list(BlanketTention[col]),
                    name=col))


            

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
#figBlanketTention.show()

#################################################################
#################################################################
#################################################################

winsowSize= 30
movingAVRBlanketTention=BlanketTention.rolling(winsowSize).mean()



figBlanketTentionAVR = go.Figure()
#


for col in movingAVRBlanketTention.columns:

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

