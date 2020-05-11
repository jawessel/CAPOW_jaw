# -*- coding: utf-8 -*-
"""
Created on Mon May  4 01:01:54 2020

@author: jkern
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pyDOE import *
from random import randint

# bring in data
sets = ['s1','s2','s3','s4']

for s in sets:
    
    s_index = sets.index(s)
    
    if s_index < 1:
                
        filename = s + '/synthetic_discharge_Hoover.csv'
        df_Hoov = pd.read_csv(filename,header=None)
        df_Hoov_combined = df_Hoov
        
        filename = s + '/synthetic_irradiance_data.csv'
        df_irr = pd.read_csv(filename,header=0,index_col=0)
        df_irr_combined = df_irr
        
        filename = s + '/synthetic_streamflows_CA.csv'
        df_streamflow_CA = pd.read_csv(filename,header=0,index_col=0)
        df_streamflow_CA_combined = df_streamflow_CA
        
        filename = s + '/synthetic_streamflows_FCRPS.csv'
        df_streamflow_FCRPS = pd.read_csv(filename,header=None)
        df_streamflow_FCRPS_combined = df_streamflow_FCRPS
        
        filename = s + '/synthetic_streamflows_TDA.csv'
        df_TDA = pd.read_csv(filename,header=None,index_col=0)
        df_TDA_combined = df_TDA
        
        filename = s + '/synthetic_streamflows_Willamette.csv'
        df_Willamette = pd.read_csv(filename,header=0,index_col=0)
        df_Willamette_combined = df_Willamette
        
        filename = s + '/synthetic_weather_data.csv'
        df_weather = pd.read_csv(filename,header=0,index_col=0)
        df_weather_combined = df_weather
        
    else:
        
        filename = s + '/synthetic_discharge_Hoover.csv'
        df_Hoov = pd.read_csv(filename,header=None)
        df_Hoov_combined = pd.concat([df_Hoov_combined,df_Hoov],axis=0)
        
        filename = s + '/synthetic_irradiance_data.csv'
        df_irr = pd.read_csv(filename,header=0,index_col=0)
        df_irr_combined = pd.concat([df_irr_combined,df_irr],axis=0)
        
        
        filename = s + '/synthetic_streamflows_CA.csv'
        df_streamflow_CA = pd.read_csv(filename,header=0,index_col=0)
        df_streamflow_CA_combined = pd.concat([df_streamflow_CA_combined,df_streamflow_CA],axis=0)
        
        
        filename = s + '/synthetic_streamflows_FCRPS.csv'
        df_streamflow_FCRPS = pd.read_csv(filename,header=None)
        df_streamflow_FCRPS_combined = pd.concat([df_streamflow_FCRPS_combined,df_streamflow_FCRPS],axis=0,sort=False)
        
        
        filename = s + '/synthetic_streamflows_TDA.csv'
        df_TDA = pd.read_csv(filename,header=None)
        df_TDA_combined = pd.concat([df_TDA_combined,df_TDA],axis=0)
        
        
        filename = s + '/synthetic_streamflows_Willamette.csv'
        df_Willamette = pd.read_csv(filename,header=0,index_col=0)
        df_Willamette_combined = pd.concat([df_Willamette_combined,df_Willamette],axis=0)
        
        
        filename = s + '/synthetic_weather_data.csv'
        df_weather = pd.read_csv(filename,header=0,index_col=0)
        df_weather_combined = pd.concat([df_weather_combined,df_weather],axis=0)
          
df_irr_combined = df_irr_combined.reset_index(drop=True)
df_streamflow_CA_combined = df_streamflow_CA_combined.reset_index(drop=True)
df_streamflow_FCRPS_combined = df_streamflow_FCRPS_combined.reset_index(drop=True)
df_Willamette_combined = df_Willamette_combined.reset_index(drop=True)
df_weather_combined = df_weather_combined.reset_index(drop=True)
df_TDA_combined = df_TDA_combined.reset_index(drop=True)
df_Hoov_combined = df_Hoov_combined.reset_index(drop=True)


# convert to smaller dimensions, annual values
years = int(len(df_weather_combined)/365)
annual_irr_NW = np.zeros((years,1))
annual_temp_NW = np.zeros((years,1))
annual_wind_NW = np.zeros((years,1))
annual_streamflow_NW = np.zeros((years,1))
annual_irr_CA = np.zeros((years,1))
annual_temp_CA = np.zeros((years,1))
annual_wind_CA = np.zeros((years,1))
annual_streamflow_CA = np.zeros((years,1))

NW_irr = df_irr_combined[['Site8','Site9','Site10']]
CA_irr = df_irr_combined[['Site1','Site2','Site3','Site4','Site5','Site6','Site7']]
NW_wind = df_weather_combined[['SALEM_W','EUGENE_W','SEATTLE_W','BOISE_W','PORTLAND_W','SPOKANE_W','PASCO_W']]
CA_wind = df_weather_combined[['FRESNO_W','LOS ANGELES_W','SAN DIEGO_W','SACRAMENTO_W','SAN JOSE_W','SAN FRANCISCO_W','TUCSON_W','PHOENIX_W','LAS VEGAS_W','OAKLAND_W']]
NW_temp = df_weather_combined[['SALEM_T','EUGENE_T','SEATTLE_T','BOISE_T','PORTLAND_T','SPOKANE_T','PASCO_T']]
CA_temp = df_weather_combined[['FRESNO_T','LOS ANGELES_T','SAN DIEGO_T','SACRAMENTO_T','SAN JOSE_T','SAN FRANCISCO_T','TUCSON_T','PHOENIX_T','LAS VEGAS_T','OAKLAND_T']]


for i in range(0,years):
    
    annual_irr_NW[i] = NW_irr.loc[i*365:i*365+365,:].values.sum()
    annual_temp_NW[i] = NW_temp.loc[i*365:i*365+365,:].values.sum()
    annual_wind_NW[i] = NW_wind.loc[i*365:i*365+365,:].values.sum()
    annual_streamflow_NW[i] = df_streamflow_FCRPS_combined.loc[i*365:i*365+365,:].values.sum()
    annual_irr_CA[i] = CA_irr.loc[i*365:i*365+365,:].values.sum()
    annual_temp_CA[i] = CA_temp.loc[i*365:i*365+365,:].values.sum()
    annual_wind_CA[i] = CA_wind.loc[i*365:i*365+365,:].values.sum()
    annual_streamflow_CA[i] = df_streamflow_CA_combined.loc[i*365:i*365+365,:].values.sum()
    

a = np.column_stack((annual_irr_NW,annual_irr_CA,annual_temp_NW,annual_temp_CA,annual_wind_NW,annual_wind_CA,annual_streamflow_NW,annual_streamflow_CA))

df_combined = pd.DataFrame(a)
columns = ['Irr_NW','Irr_CA','Temp_NW','Temp_CA','Wind_NW','Wind_CA','Streamflow_NW','Streamflow_CA']
df_combined.columns = columns
df_combined.to_csv('annual.csv')

# convert to cdfs
df_sorting = df_combined.copy(deep=True)
df_sorting['Year'] = pd.Series(range(0,1012))

#pull representative years
years=[]

for c in columns:
    df_sorting.sort_values(c,inplace=True,ascending=True)
    df_sorting[c] = np.linspace(0,1,1012)
    df_sorting = df_sorting.reset_index(drop=True)
    min_year = df_sorting.loc[0,'Year']
    max_year = df_sorting.loc[1011,'Year']
    year_95 = df_sorting.loc[962,'Year']
    year_5 = df_sorting.loc[50,'Year']

    if min_year in years:
        pass
    else:
        years.append(int(min_year))

    if max_year in years:
        pass
    else:
        years.append(int(max_year))
    if year_95 in years:
        pass
    else:
        years.append(int(year_95))
    if year_5 in years:
        pass
    else:
        years.append(int(year_5))
    
df_sorting.sort_values('Year',inplace=True,ascending=True)
df_sorting = df_sorting.reset_index(drop=True)
syn_mat = df_sorting.loc[:,:'Streamflow_CA'].values

# Latin hyper cube sample with 
sample_size = int(100 - len(years))
sample = lhs(len(columns),sample_size,criterion='maximin')

for i in range(0,sample_size):
    
    sample_year = sample[i,:]
    sample_mat = sample_year*np.ones((len(df_sorting),len(columns)))
    difference = np.abs(sample_mat - syn_mat)
    sum_difference = np.sum(difference,axis=1)
    yr_attached = np.column_stack((sum_difference,range(0,len(df_sorting))))
    df_yrs = pd.DataFrame(yr_attached,columns=['value','year'])
    sorted_yrs = df_yrs.sort_values('value',inplace=False,ascending=True)
    sorted_yrs = sorted_yrs.reset_index(drop=True)
    
    switch = 0
    count = 0
    
    while switch < 1:
        
        match_year = sorted_yrs.loc[count,'year']
        
        if match_year in years:
            
            count = count + 1
            
        else:
            years.append(int(match_year))
            switch = switch + 1
        
unique = np.unique(years)
print(len(unique)/len(years))
        
selected = df_combined.loc[years,:]
#
## compare to random selection
years2 = []

for i in range(0,100):
    a = randint(0,1011)
    years2 = np.append(years2,a)
    
selected2 = df_combined.loc[years2,:]

# get new cdfs for comparison

# convert to cdfs
df_sorting_selected= selected.copy(deep=True)
df_sorting_selected2= selected2.copy(deep=True)
df_syn = df_combined.copy(deep=True)
#
#
plt.figure()

for c in columns:
    
    c_index = columns.index(c) + 1
    
    df_sorting_selected.sort_values(c,inplace=True,ascending=True)
    sample_values = df_sorting_selected[c].values

    df_sorting_selected2.sort_values(c,inplace=True,ascending=True)
    random_values = df_sorting_selected2[c].values

    df_syn.sort_values(c,inplace=True,ascending=True)
    syn_values = df_syn[c].values
    
    sample_x = np.linspace(0,1,len(selected))
    syn_x = np.linspace(0,1,len(df_sorting))

    plt.subplot(3,3,c_index)
    plt.scatter(syn_x,syn_values,s=12)
    plt.scatter(sample_x,sample_values,s=2)
    plt.scatter(sample_x,random_values,s=2)
    plt.title(c)
#    plt.legend(['Full','LHS','Random'])    
    plt.subplots_adjust(hspace=0.6,wspace=0.5)
#
plt.savefig("cdfs.png", dpi=1000)
#
## covariance plots
df_syn.insert(0,'Test','Full')
df_sorting_selected.insert(0,'Test','LHS')
df_sorting_selected2.insert(0,'Test','Random')

df_C = pd.concat([df_syn,df_sorting_selected,df_sorting_selected2],axis=0)
sns.pairplot(df_C,hue='Test')
#
plt.savefig("pairplot.png", dpi=1000)
#
#
#    