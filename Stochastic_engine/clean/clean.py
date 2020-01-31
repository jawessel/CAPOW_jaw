# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 16:09:38 2019

@author: YSu
"""

import pandas as pd
import numpy as np

#For sites 8, 9, and 10
#eastoregon is 198250 (site 10), salem is 209205 (site 8), southoregon is 174608 (site 9)
Site_ID=['198250_44.05_-117.34_','209205_44.97_-123.02_','174608_42.13_-121.78_']
year=range(1998,2018)

y=[]
m=[]
d=[]
h=[]
m=[]
DNI_all=[]
DNI_clear=[]
count=0

j=Site_ID[0]
for i in year:
    name=j+str(int(i))+'.csv'
    file=pd.read_csv(name,header=2)
    year=file['Year'].values
    hour=file['Hour'].values
    month=file['Month'].values
    day=file['Day'].values
    DNI=file['GHI'].values
    DNI_c=file['Clearsky GHI'].values
    
    
    year=np.average(np.reshape(year,(8760,2)),axis=1)
    hour=np.average(np.reshape(hour,(8760,2)),axis=1)
    month=np.average(np.reshape(month,(8760,2)),axis=1)
    day=np.average(np.reshape(day,(8760,2)),axis=1)
    DNI=np.average(np.reshape(DNI,(8760,2)),axis=1)
    DNI_c=np.average(np.reshape(DNI_c,(8760,2)),axis=1)
    
    y.append(year)
    m.append(month)
    d.append(day)
    h.append(hour)
    DNI_all.append(DNI)
    DNI_clear.append(DNI_c)
    

y1=np.vstack(y)
y1=np.reshape(y1,(8760*20))

m1=np.vstack(m)
m1=np.reshape(m1,(8760*20))

d1=np.vstack(d)
d1=np.reshape(d1,(8760*20))

h1=np.vstack(h)
h1=np.reshape(h1,(8760*20))

DNI1=np.vstack(DNI_all)
DNI1=np.reshape(DNI1,(8760*20))

DNI_CL=np.vstack(DNI_clear)
DNI_CL=np.reshape(DNI_CL,(8760*20))


K=pd.DataFrame()
K['Year']=y1
K['Month']=m1
K['Day']=d1
K['Hour']=h1

K['Site1']=DNI1
K['Site1 clearsky']=DNI_CL

K['Site2']=DNI1
K['Site2 clearsky']=DNI_CL

K['Site3']=DNI1
K['Site3 clearsky']=DNI_CL

K['Site4']=DNI1
K['Site4 clearsky']=DNI_CL

K['Site5']=DNI1
K['Site5 clearsky']=DNI_CL

K['Site6']=DNI1
K['Site6 clearsky']=DNI_CL

K['Site7']=DNI1
K['Site7 clearsky']=DNI_CL

K['Site8']=DNI1
K['Site8 clearsky']=DNI_CL

K['Site9']=DNI1
K['Site9 clearsky']=DNI_CL

K['Site10']=DNI1
K['Site10 clearsky']=DNI_CL

K.to_csv('Solar_data_GHI.csv')
