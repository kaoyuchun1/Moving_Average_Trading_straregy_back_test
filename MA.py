# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 09:48:07 2020

@author: user

回測均線策略
"""

#%% import data 
import time
start_time = time.time()
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import datetime


#%%

with open('twse.pickle', 'rb') as file:
    df =pickle.load(file)
    
col1=['日期','收盤價']
df=df[col1]

#%% compute ma10 & ma20

df['MA10']=df['收盤價'][::-1].rolling(10).mean()
df['MA20']=df['收盤價'][::-1].rolling(20).mean()
df=df.dropna(axis=0)

#%% select date

df['日期']=pd.to_datetime(df['日期'])
df['日期']=df['日期'].dt.date

df = df[df['日期']> datetime.date(1995,12,31) ]
df = df[df['日期']< datetime.date(2020,1,1)]
df = df.reset_index(drop=True)

#%%

label=list()
label.append('H')
for i in range(len(df)-2,-1,-1):
    if (df['MA10'][i]>df['MA20'][i]) & (df['MA10'][i+1]<df['MA20'][i+1]) :
        label.append('B')
    elif (df['MA10'][i]<df['MA20'][i]) & (df['MA10'][i+1]>df['MA20'][i+1]) :
        label.append('S')
    else:
        label.append('H')
        
df['Label']=label[::-1]

#raise SystemExit(0)

#%% plot

label_B = df[df['Label']=='B']
label_S = df[df['Label']=='S']

weekday = df['日期']

fig , (ax1 , ax2) = plt.subplots(2, 1, sharex=True, figsize=(20,40))
plt.subplots_adjust(left=None, bottom=None, right=None, top=0.3, wspace=0.3, hspace=0.3)

ax1.set_title('TWSE')
ax1.plot(weekday,df['收盤價'],label="TWSE",color = 'steelblue' )
ax1.plot(label_B['日期'],label_B['收盤價'],'b+',label="Buy")
ax1.plot(label_S['日期'],label_S['收盤價'],'r+',label="Sell")
ax1.grid(ls='--')
ax1.legend()

ax2.set_title('Profit')
ax2.plot(weekday,df['收盤價'],label="TWSE",color = 'b' )
ax2.plot(weekday,df['MA10'],label="MA10",color = 'steelblue' )
ax2.plot(weekday,df['MA20'],label="MA20",color = 'g' )
ax2.plot(label_B['日期'],label_B['收盤價'],'b.',label="Buy")
ax2.plot(label_S['日期'],label_S['收盤價'],'r.',label="Sell")
ax2.grid(ls='--')
ax2.legend()

#%% 損益 

cost=[0]*(len(df['MA20'])+1)
profit=[0]*(len(df['MA20'])+1)

for i in range(len(df['MA20'])-1,-1,-1):
    
    if df['Label'][i]=='B':
        cost[i]=cost[i+1]+df['收盤價'][i]
        profit[i]=profit[i+1]
        
    elif df['Label'][i]=='S':
        if cost[i+1]>0:            
            profit[i]=profit[i+1]+df['收盤價'][i]-cost[i+1]
            cost[i]=0
        
    else :
        profit[i]=profit[i+1]
        cost[i]=cost[i+1]

cost=cost[:-1]
profit=profit[:-1]

df['Cost']=cost
df['profit']=profit

#%%

fig , (ax1,ax2,ax3) = plt.subplots(3, 1, sharex=True, figsize=(20,60))
plt.subplots_adjust(left=None, bottom=None, right=None, top=0.3, wspace=0.3, hspace=0.3)

ax1.set_title('TWSE')
ax1.plot(weekday,df['收盤價'],label="TWSE",color = 'steelblue' )
ax1.plot(label_B['日期'],label_B['收盤價'],'b+',label="Buy")
ax1.plot(label_S['日期'],label_S['收盤價'],'r+',label="Sell")
ax1.grid(ls='--')
ax1.legend()

ax2.set_title('Profit')
ax2.plot(weekday,df['收盤價'],label="TWSE",color = 'b' )
ax2.plot(weekday,df['MA10'],label="MA10",color = 'steelblue' )
ax2.plot(weekday,df['MA20'],label="MA20",color = 'g' )
ax2.plot(label_B['日期'],label_B['收盤價'],'b.',label="Buy")
ax2.plot(label_S['日期'],label_S['收盤價'],'r.',label="Sell")
ax2.grid(ls='--')
ax2.legend()

ax3.set_title('TWSE')
ax3.plot(weekday,cost,label="cost",color = 'steelblue' )
ax3.plot(weekday,profit,label="profit",color = 'r' )
ax3.grid(ls='--')
ax3.legend()

