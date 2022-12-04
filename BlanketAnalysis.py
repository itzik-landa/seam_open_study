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

    for col in data.columns:
        if len(np.where(data[col].isnull() == True)[0]):
            if np.where(data[col].isnull() == True)[0][0]<120:
                continue
        fig.add_trace(go.Scatter(y=list(data[col]),
                    name=col))


    fig.update_layout(title=title)

    fig.update_layout(
        hoverlabel=dict(
            namelength=-1
        )
    )


    plot(fig,auto_play=True,filename=f"{mach}_dt_string.html")   
    #fig.show()

def plot_rolling(data, type, winsowSize, mach):
    fig = go.Figure()
    
    movingAVRBlanketTention=data.rolling(winsowSize).mean()
    for col in movingAVRBlanketTention.columns:

        res = list(filter(lambda item: not math.isnan(item), list(movingAVRBlanketTention[col])))
        if len(res)>120:
            fig.add_trace(go.Scatter(y=res,
                            name=col))


    fig.update_layout(title=f"{mach}_{type} moving AVR window size=str({winsowSize})")

    fig.update_layout(
        hoverlabel=dict(
            namelength=-1
        )
    )

    dt_string = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    plot(fig,auto_play=True,filename="Scale_FRONT_AQM_"+ dt_string +".html")  
    return movingAVRBlanketTention


def clean_me(movingAVRBlanketTention):
    cleaned_df = {}
    for col in movingAVRBlanketTention.columns:
        res = list(filter(lambda item: not math.isnan(item), list(movingAVRBlanketTention[col])))
        if len(res)>300:
            cleaned_df[col] = res
            
    lendict = len(cleaned_df)
    avgd = []

    idx = 0

    broke = False

    while 1:
        total = 0
        for item in cleaned_df:
            if idx == len(cleaned_df[item])-1:
                broke = True
                break
            total += cleaned_df[item][idx]
        if broke:
            break
        avgd.append(total/lendict)
        idx+=1


    norms_dict = {}



    for item in cleaned_df:
        vec = cleaned_df[item][:idx]
        subd = np.subtract(vec, avgd)
        norms_dict[item] = np.linalg.norm(subd)


    return {k: v for k, v in sorted(norms_dict.items(), key=lambda item: item[1])}

 




#output=pd.read_csv(r'D:\Logs\Research\D14 seam open\D14 1.9-1.11 ready behavior\sorted\B4bSS\output.csv')
#mach="D14"

output=pd.read_csv(r'D:\Logs\Research\D14 seam open\D14 15.9_15.10 ready with loadCellDiff\sorted\B4bSS\output.csv')
mach="D14"


#output=pd.read_csv(r'D:\Logs\Research\D6 seam open\blanket ready\sorted\B4bSS\output.csv')
#mach="D6"

dictdict = {}
for col in output.columns:
    if col!="mach" and col!="path" and col!="timestamp" and col not in dictdict:
        dictdict[col] = pd.DataFrame()

for ind, row in output.iterrows():

    for dictitem in dictdict:
        tmp=list(map(float, output[dictitem][ind].split('@')))
        dictdict[dictitem]=pd.concat([dictdict[dictitem],pd.Series(tmp)],axis=1).rename(columns={0:output['timestamp'][ind]})



for dictitem in dictdict:
    dictdict[dictitem] = dictdict[dictitem].loc[:,~dictdict[dictitem].columns.duplicated()].copy()
    dictdict[dictitem].columns.sort_values()





#for key in dictdict:
#    plot_fig(dictdict[key], key, mach)



dict_avgd = {}

for dictitem in dictdict:
    if dictitem=="BCD-BTD [TorqueNm]_All":
        w = 10
    else:
        w = 30
    ans = plot_rolling(dictdict[dictitem], dictitem, w, mach)
    dict_avgd[dictitem] = ans




ans = clean_me(dict_avgd["BCD-BTD [TorqueNm]_All"])




#################################################################
#################################################################
#################################################################





