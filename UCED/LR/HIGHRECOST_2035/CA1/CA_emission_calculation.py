# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 11:08:22 2018

@author: YSu
"""

from __future__ import division
import pandas as pd
import numpy as np

#==============================================================================
 
df_mwh1 = pd.read_csv('mwh_1.csv',header=0)
df_mwh2 = pd.read_csv('mwh_2.csv',header=0)
df_mwh3 = pd.read_csv('mwh_3.csv',header=0)
df_gen = pd.read_csv('generators.csv',header=0)
emission_rate=pd.read_csv('CA_emissions_generator.csv',header=0)

Result=[]
for i in range(0,len(df_mwh1)):
    name=df_mwh1.loc[i]['Generator']
    zone=df_mwh1.loc[i]['Zones']
    time=df_mwh1.loc[i]['Time']
    gen_1=df_mwh1.loc[i]['Value']
    gen_2=df_mwh2.loc[i]['Value']
    gen_3=df_mwh3.loc[i]['Value']
    
    total_gen= gen_1+ gen_2+ gen_3
    emission_gen=emission_rate.loc[emission_rate['name']==name]
    
    NOX=total_gen *emission_gen['NOX lb/MWh']
    SO2=total_gen *emission_gen['SO2 lb/MWh']
    CO2=total_gen *emission_gen['CO2 lb/MWh']
    N2O=total_gen *emission_gen['N2O lb/MWh']
    CO2_e=total_gen *emission_gen['CO2 equivalent lb/MWh']
    Result.append((name,zone,time,NOX.values[0],SO2.values[0],CO2.values[0],N2O.values[0],CO2_e.values[0]))
    
    
Results=pd.DataFrame(Result,columns=('Generator','Zone','Time','NOX lb','SO2 lb','CO2 lb','N2O lb','CO2_equivelent lb'))
Results.to_csv('Emission_calculation.csv')
###################################################
#Using below to calculate the monthly emission
S=Results.loc[Results['Time'] >=1]
S=S.loc[S['Time'] <=24]
##################################################
#Annual emission
Total_NOX= np.sum(Results.loc[:]['NOX lb'].values)
Total_SO2= np.sum(Results.loc[:]['SO2 lb'].values)
Total_CO2= np.sum(Results.loc[:]['CO2 lb'].values)
Total_N2O= np.sum(Results.loc[:]['N2O lb'].values)
Total_CO2_e= np.sum(Results.loc[:]['CO2_equivelent lb'].values)

Annual_total=pd.DataFrame()
Annual_total['Total NOX lb']=Total_NOX
Annual_total['Total N2O lb']=Total_N2O
Annual_total['Total CO2 lb']=Total_CO2
Annual_total['Total CO2 equivelent lb'] = Total_CO2_e
Annual_total['Total SO2 lb']=Total_SO2

np.savetxt('TotalCO2.txt',[1,Total_CO2_e])