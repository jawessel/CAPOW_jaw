# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 20:59:27 2019

@author: YSu
"""

import pandas as pd
import numpy as np
from sklearn import linear_model
from statsmodels.tsa.arima_model import ARMA
from datetime import datetime
from datetime import timedelta
import scenario_chooser

def solar_sim(sim_years):

    sim_years=sim_years+3
    df_CAISO = pd.read_excel('Synthetic_wind_power/renewables_2011_2017.xlsx',sheet_name='CAISO',header=0)
    df_BPA = pd.read_excel('Synthetic_wind_power/renewables_2011_2017.xlsx',sheet_name='BPA',header=0)
    df_cap = pd.read_excel('Synthetic_wind_power/cap_by_month.xlsx',sheet_name = 'solar',header=0)
    
    years = range(2011,2018)
    
    ## first standardize solar by installed capacity, yielding hourly capacity factors
    hours = len(df_CAISO)
    num_years = int(len(years))
    st_solar = np.zeros((hours,2))
    
    
    for i in years:
        
        year_index = years.index(i)
    
        for j in range(0,31):
            for k in range(0,24):
                
                st_solar[year_index*8760 +j*24+k,0] = df_CAISO.loc[year_index*8760 + j*24+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==1),'CAISO']
                st_solar[year_index*8760 +j*24+1416+k,0] = df_CAISO.loc[year_index*8760 + j*24+1416+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==3),'CAISO']
                st_solar[year_index*8760 +j*24+2880+k,0] = df_CAISO.loc[year_index*8760 + j*24+2880+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==5),'CAISO']
                st_solar[year_index*8760 +j*24+4344+k,0] = df_CAISO.loc[year_index*8760 + j*24+4344+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==7),'CAISO']
                st_solar[year_index*8760 +j*24+5088+k,0] = df_CAISO.loc[year_index*8760 + j*24+5088+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==8),'CAISO']
                st_solar[year_index*8760 +j*24+6552+k,0] = df_CAISO.loc[year_index*8760 + j*24+6552+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==10),'CAISO']
                st_solar[year_index*8760 +j*24+8016+k,0] = df_CAISO.loc[year_index*8760 + j*24+8016+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==12),'CAISO']
    
                st_solar[year_index*8760 +j*24+k,1] = df_BPA.loc[year_index*8760 + j*24+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==1),'BPA']
                st_solar[year_index*8760 +j*24+1416+k,1] = df_BPA.loc[year_index*8760 + j*24+1416+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==3),'BPA']
                st_solar[year_index*8760 +j*24+2880+k,1] = df_BPA.loc[year_index*8760 + j*24+2880+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==5),'BPA']
                st_solar[year_index*8760 +j*24+4344+k,1] = df_BPA.loc[year_index*8760 + j*24+4344+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==7),'BPA']
                st_solar[year_index*8760 +j*24+5088+k,1] = df_BPA.loc[year_index*8760 + j*24+5088+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==8),'BPA']
                st_solar[year_index*8760 +j*24+6552+k,1] = df_BPA.loc[year_index*8760 + j*24+6552+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==10),'BPA']
                st_solar[year_index*8760 +j*24+8016+k,1] = df_BPA.loc[year_index*8760 + j*24+8016+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==12),'BPA']
    
        for j in range(0,30):
            for k in range(0,24):
    
                st_solar[year_index*8760 +j*24+2160+k,0] = df_CAISO.loc[year_index*8760 + j*24+2160+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==4),'CAISO']
                st_solar[year_index*8760 +j*24+3624+k,0] = df_CAISO.loc[year_index*8760 + j*24+3624+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==6),'CAISO']
                st_solar[year_index*8760 +j*24+5832+k,0] = df_CAISO.loc[year_index*8760 + j*24+5832+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==9),'CAISO']
                st_solar[year_index*8760 +j*24+7296+k,0] = df_CAISO.loc[year_index*8760 + j*24+7296+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==11),'CAISO']
    
                st_solar[year_index*8760 +j*24+2160+k,1] = df_BPA.loc[year_index*8760 + j*24+2160+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==4),'BPA']
                st_solar[year_index*8760 +j*24+3624+k,1] = df_BPA.loc[year_index*8760 + j*24+3624+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==6),'BPA']
                st_solar[year_index*8760 +j*24+5832+k,1] = df_BPA.loc[year_index*8760 + j*24+5832+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==9),'BPA']
                st_solar[year_index*8760 +j*24+7296+k,1] = df_BPA.loc[year_index*8760 + j*24+7296+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==11),'BPA']
                
        for j in range(0,28):
            for k in range(0,24):
    
                st_solar[year_index*8760 +j*24+744+k,0] = df_CAISO.loc[year_index*8760 + j*24+744+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==2),'CAISO']
                st_solar[year_index*8760 +j*24+744+k,1] = df_BPA.loc[year_index*8760 + j*24+744+k,'solar']/df_cap.loc[(df_cap['Year']==i) & (df_cap['Month']==2),'BPA']
       
    st_solar=st_solar[35040:,:]
    daily_st_solar_CAISO=np.reshape(st_solar[:,0],(3*365,24))
    daily_st_solar_BPA=np.reshape(st_solar[:,1],(3*365,24))
    
    
    daily_st_solar_CAISO=np.sum(daily_st_solar_CAISO,axis=1)
    daily_st_solar_BPA = np.sum(daily_st_solar_BPA,axis=1)
    irrediance=pd.read_csv('Synthetic_solar_power/Solar_data_GHI_regress.csv',header=0)
    
    #CAISO simulation
    
    Normal_Starting=datetime(1900,1,1)
    
    datelist=pd.date_range(Normal_Starting,periods=365)
    count=0
    m=np.zeros(len(daily_st_solar_CAISO))
    for i in range(0,len(daily_st_solar_CAISO)):
        m[i]=int(datelist[count].month)
        count= count +1
        if count >364:
            count=0
    
    X=pd.DataFrame()
       
    X['Month']=m
    X['y']=daily_st_solar_CAISO
    X['1']=np.sum(np.reshape(irrediance['Site1'].values[35040:],(3*365,24)),axis=1)
    X['2']=np.sum(np.reshape(irrediance['Site2'].values[35040:],(3*365,24)),axis=1)
    X['3']=np.sum(np.reshape(irrediance['Site3'].values[35040:],(3*365,24)),axis=1)
    X['4']=np.sum(np.reshape(irrediance['Site4'].values[35040:],(3*365,24)),axis=1)
    X['5']=np.sum(np.reshape(irrediance['Site5'].values[35040:],(3*365,24)),axis=1)
    X['6']=np.sum(np.reshape(irrediance['Site6'].values[35040:],(3*365,24)),axis=1)
    X['7']=np.sum(np.reshape(irrediance['Site7'].values[35040:],(3*365,24)),axis=1)
    X['8']=np.sum(np.reshape(irrediance['Site8'].values[35040:],(3*365,24)),axis=1)
    X['9']=np.sum(np.reshape(irrediance['Site9'].values[35040:],(3*365,24)),axis=1)
    X['10']=np.sum(np.reshape(irrediance['Site10'].values[35040:],(3*365,24)),axis=1)
       
           
    
    for i in range(1,13):
        name='reg_' + str(i)
        data=X.loc[X['Month']==i]
        y=data['y']
        x=data.loc[:,'1':]
    #    y=np.log(y+1)
    #    x=np.log(x+1)
        locals()[name]=linear_model.LinearRegression(fit_intercept=False)
        locals()[name].fit(x,y)
    #        print(locals()[name].score(x,y))
        
    Syn_irr=pd.read_csv('Synthetic_weather/synthetic_irradiance_data.csv',header=0,index_col=0)
    Syn_irr = Syn_irr.loc[0:365*sim_years-1,:]
    
    Normal_Starting=datetime(1900,1,1)
    
    datelist=pd.date_range(Normal_Starting,periods=365)
    count=0
    m=np.zeros(len(Syn_irr))
    for i in range(0,len(Syn_irr)):
        m[i]=int(datelist[count].month)
        count= count +1
        if count >364:
            count=0
    d_sim=np.column_stack((Syn_irr.values,m))   
    #
    ##Test the fit
    predicted = np.zeros(len(X))
    
    for i in range(0,len(X)):
        data=X.loc[i,:]
        Month=int(data['Month'])
        x_values=data['1':].values
        x_values = np.reshape(x_values,(1,10))
        reg_name='reg_' + str(Month)
        p=locals()[reg_name].predict(x_values)
        predicted[i]=p
    residules= predicted - X['y'].values
    
    
    predicted_sim=np.zeros(len(Syn_irr))
    for i in range(0,len(Syn_irr)):
        data=d_sim[i,:]
        Month=int(data[10])
        x_values=data[:10]
        x_values = np.reshape(x_values,(1,10))
        reg_name='reg_' + str(Month)
        p=locals()[reg_name].predict(x_values)
        predicted_sim[i]=p
    
    
    
    Model=ARMA(residules,order=(7,0))
    arma_fit1 = Model.fit()
    #ARMA_residuals = arma_fit1.resid
    
    
    y_seeds=residules[-7:]
    e=np.random.normal(np.mean(residules),np.std(residules),len(Syn_irr))
    
    
    
    p=arma_fit1.params
    
    res_sim=np.zeros(len(Syn_irr)+7)
    res_sim[0:7]=y_seeds
    for i in range(0,len(Syn_irr)):
        y=p[0]+p[1]*y_seeds[6]+ p[2]*y_seeds[5] + p[3]*y_seeds[4] + p[4]*y_seeds[3] +p[5]*y_seeds[2] + p[6]*y_seeds[1] + p[7]*y_seeds[0]+e[i]
        res_sim[i+7]=y
        y_seeds=res_sim[i:i+7]
        
        
        
    Solar=predicted_sim -e
    
    Solar[Solar<np.min(daily_st_solar_CAISO)]=np.min(daily_st_solar_CAISO)
    NT=int(sim_years*365)
    # scalable sythetic daily solar
    sim_solar = np.zeros((NT,1))
    
    sim_solar=Solar
    #impose historical minimum    
    
        
    #sample hourly loss patterns from historical record based on calender day
    sim_hourly_CAISO = np.zeros((NT*24,1))
    
    daily = np.reshape(daily_st_solar_CAISO,(3,365))
    daily = np.transpose(daily)
    
    #tolerance
    t = 0.01
    
    days = np.zeros((365,int(sim_years)))
    years = np.zeros((365,int(sim_years)))
    
    #match daily sum with hourly profile of historical day with similar date/production
    for i in range(0,int(sim_years)):
        for j in range(0,365):
            target = sim_solar[i*365+j]
            s = 0
            tol = 100
            
            while (tol > t and s < 10):
                
                if j + s > 364:
                    up = j + s - 365
                else:
                    up = j + s
                
                if j - s < 0:
                    down = j - s + 365
                else:
                    down = j - s
                
                for k in range(0,3):
                    if np.abs(sim_solar[i*365+j] - daily[up,k]) < tol:
                        tol = np.abs(sim_solar[i*365+j] - daily[up,k])
                        day = up
                        year = k
                
                for k in range(0,3):
                    if np.abs(sim_solar[i*365+j] - daily[down,k]) < tol:
                        tol = np.abs(sim_solar[i*365+j] - daily[down,k])
                        day = down
                        year = k                    
                        
                s = s + 1
                
                days[j,i] = day
                years[j,i] = year
            
            a = st_solar[year*8760+day*24:year*8760+day*24+24,0]*(sim_solar[i*365+j]/daily[day,year])
            a = np.reshape(a,(24,1))
            sim_hourly_CAISO[i*8760+j*24:i*8760+j*24+24] = a
            
    #impose maximum constraint
    for i in range(0,len(sim_hourly_CAISO)):
       if sim_hourly_CAISO[i] > 1:
           sim_hourly_CAISO[i] = 1
    
    
     #BPA simulation
    
    Normal_Starting=datetime(1900,1,1)
    
    datelist=pd.date_range(Normal_Starting,periods=365)
    count=0
    m=np.zeros(len(daily_st_solar_BPA))
    for i in range(0,len(daily_st_solar_BPA)):
        m[i]=int(datelist[count].month)
        count= count +1
        if count >364:
            count=0
    
    X=pd.DataFrame()
       
    X['Month']=m
    X['y']=daily_st_solar_BPA
    X['1']=np.sum(np.reshape(irrediance['Site1'].values[35040:],(3*365,24)),axis=1)
    X['2']=np.sum(np.reshape(irrediance['Site2'].values[35040:],(3*365,24)),axis=1)
    X['3']=np.sum(np.reshape(irrediance['Site3'].values[35040:],(3*365,24)),axis=1)
    X['4']=np.sum(np.reshape(irrediance['Site4'].values[35040:],(3*365,24)),axis=1)
    X['5']=np.sum(np.reshape(irrediance['Site5'].values[35040:],(3*365,24)),axis=1)
    X['6']=np.sum(np.reshape(irrediance['Site6'].values[35040:],(3*365,24)),axis=1)
    X['7']=np.sum(np.reshape(irrediance['Site7'].values[35040:],(3*365,24)),axis=1)
    X['8']=np.sum(np.reshape(irrediance['Site8'].values[35040:],(3*365,24)),axis=1)
    X['9']=np.sum(np.reshape(irrediance['Site9'].values[35040:],(3*365,24)),axis=1)
    X['10']=np.sum(np.reshape(irrediance['Site10'].values[35040:],(3*365,24)),axis=1)
       
           
    
    for i in range(1,13):
        name='reg_' + str(i)
        data=X.loc[X['Month']==i]
        y=data['y']
        x=data.loc[:,'1':]
    #    y=np.log(y+1)
    #    x=np.log(x+1)
        locals()[name]=linear_model.LinearRegression(fit_intercept=False)
        locals()[name].fit(x,y)
    #        print(locals()[name].score(x,y))
        
    Syn_irr=pd.read_csv('Synthetic_weather/synthetic_irradiance_data.csv',header=0,index_col=0)
    Syn_irr = Syn_irr.loc[0:365*sim_years-1,:]
    
    Normal_Starting=datetime(1900,1,1)
    
    datelist=pd.date_range(Normal_Starting,periods=365)
    count=0
    m=np.zeros(len(Syn_irr))
    for i in range(0,len(Syn_irr)):
        m[i]=int(datelist[count].month)
        count= count +1
        if count >364:
            count=0
    d_sim=np.column_stack((Syn_irr.values,m))   
    #
    ##Test the fit
    predicted = np.zeros(len(X))
    
    for i in range(0,len(X)):
        data=X.loc[i,:]
        Month=int(data['Month'])
        x_values=data['1':].values
        x_values = np.reshape(x_values,(1,10))
        reg_name='reg_' + str(Month)
        p=locals()[reg_name].predict(x_values)
        predicted[i]=p
    residules= predicted - X['y'].values
    
    
    predicted_sim=np.zeros(len(Syn_irr))
    for i in range(0,len(Syn_irr)):
        data=d_sim[i,:]
        Month=int(data[10])
        x_values=data[:10]
        x_values = np.reshape(x_values,(1,10))
        reg_name='reg_' + str(Month)
        p=locals()[reg_name].predict(x_values)
        predicted_sim[i]=p
    
    
    
    Model=ARMA(residules,order=(7,0))
    arma_fit1 = Model.fit()
    #ARMA_residuals = arma_fit1.resid
    
    
    y_seeds=residules[-7:]
    e=np.random.normal(np.mean(residules),np.std(residules),len(Syn_irr))
    
    
    
    p=arma_fit1.params
    
    res_sim=np.zeros(len(Syn_irr)+7)
    res_sim[0:7]=y_seeds
    for i in range(0,len(Syn_irr)):
        y=p[0]+p[1]*y_seeds[6]+ p[2]*y_seeds[5] + p[3]*y_seeds[4] + p[4]*y_seeds[3] +p[5]*y_seeds[2] + p[6]*y_seeds[1] + p[7]*y_seeds[0]+e[i]
        res_sim[i+7]=y
        y_seeds=res_sim[i:i+7]
        
        
        
    Solar=predicted_sim -e
    
    Solar[Solar<np.min(daily_st_solar_BPA)]=np.min(daily_st_solar_BPA)
    NT=int(sim_years*365)
    # scalable sythetic daily solar
    sim_solar = np.zeros((NT,1))
    
    sim_solar=Solar
    #impose historical minimum    
    
        
    #sample hourly loss patterns from historical record based on calender day
    sim_hourly_BPA = np.zeros((NT*24,1))
    
    daily = np.reshape(daily_st_solar_BPA,(3,365))
    daily = np.transpose(daily)
    
    #tolerance
    t = 0.01
    
    days = np.zeros((365,int(sim_years)))
    years = np.zeros((365,int(sim_years)))
    
    #match daily sum with hourly profile of historical day with similar date/production
    for i in range(0,int(sim_years)):
        for j in range(0,365):
            target = sim_solar[i*365+j]
            s = 0
            tol = 100
            
            while (tol > t and s < 10):
                
                if j + s > 364:
                    up = j + s - 365
                else:
                    up = j + s
                
                if j - s < 0:
                    down = j - s + 365
                else:
                    down = j - s
                
                for k in range(0,3):
                    if np.abs(sim_solar[i*365+j] - daily[up,k]) < tol:
                        tol = np.abs(sim_solar[i*365+j] - daily[up,k])
                        day = up
                        year = k
                
                for k in range(0,3):
                    if np.abs(sim_solar[i*365+j] - daily[down,k]) < tol:
                        tol = np.abs(sim_solar[i*365+j] - daily[down,k])
                        day = down
                        year = k                    
                        
                s = s + 1
                
                days[j,i] = day
                years[j,i] = year
            
            a = st_solar[year*8760+day*24:year*8760+day*24+24,1]*(sim_solar[i*365+j]/daily[day,year])
            a = np.reshape(a,(24,1))
            sim_hourly_BPA[i*8760+j*24:i*8760+j*24+24] = a
    
    
    #impose maximum constraint
    for i in range(0,len(sim_hourly_BPA)):
       if sim_hourly_BPA[i] > 1:
           sim_hourly_BPA[i] = 1
           
    #iterate through each scenario
    #Scenarios: 'MID' = Mid-Case (S1), 'EV' = High EV Adoption (S2), 'BAT' = Low Battery Storage Cost (S3)
    #'LOWRECOST' = Low RE Cost / High Gas Price (S4), 'HIGHRECOST' = High RE Cost / Low Gas Price (S5)
    
    df_S = pd.DataFrame()
    pathways = ['MID','EV','BAT','LOWRECOST','HIGHRECOST']
    
    for pathway in pathways:
    
        p_index = pathways.index(pathway)
    
        #iterate through each year (every 5 years from 2020-2050)
        yrs = [2020,2025,2030,2035,2040,2045,2050]
    
        for year in yrs:
        
            #define all specific parameters using scenario chooser (only need wind capacities here)
            [CAISO_wind_cap,CAISO_solar_cap,CAISO_bat_cap,PNW_wind_cap,PNW_solar_cap,PNW_bat_cap,bat_RoC_coeff,bat_RoD_coeff,bat_eff,ev_df,identifier] = scenario_chooser.choose(pathway,year)
    
           
            #multiply by installed capacity (CAISO)
            solar_sim_CAISO = sim_hourly_CAISO*CAISO_solar_cap
    
            h = int(len(solar_sim_CAISO))
            solar_sim_CAISO = solar_sim_CAISO[8760:h-2*8760,:]
            df_S[pathway + "_" + str(year) + "_CAISO"] = solar_sim_CAISO[:,0]
                   
            #multiply by installed capacity (BPA)
            solar_sim_BPA = sim_hourly_BPA*PNW_solar_cap
            
            h = int(len(solar_sim_BPA))
            solar_sim_BPA = solar_sim_BPA[8760:h-2*8760,:]
            df_S[pathway + "_" + str(year) + "_BPA"] = solar_sim_BPA[:,0]
                  
    df_S.to_csv('Synthetic_solar_power/solar_power_sim.csv', index = None, header = True)
    
    return None