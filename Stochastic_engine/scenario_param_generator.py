# -*- coding: utf-8 -*-
"""
Created on Tue May 19 12:20:06 2020

@author: jawessel
"""

###########################################################################################################
# LOOPS THROUGH SCENARIO CHOOSER FOR ALL SCENARIO/YEAR COMBINATIONS AND OUTPUTS ALL PARAMETERS TO ONE CSV #
###########################################################################################################

import scenario_chooser
import pandas as pd

#initialize empty DataFrame to populate with list of row names
row_names = ['CAISO_wind_cap','CAISO_solar_cap','CAISO_bat_cap','PNW_wind_cap','PNW_solar_cap','PNW_bat_cap','bat_RoC_coeff','bat_RoD_coeff','bat_eff']
param_output = pd.DataFrame(index=row_names)
ev_output = pd.DataFrame()

#loop through each pathway and year
pathways = ['MID','EV','BAT','LOWRECOST','HIGHRECOST']

for pathway in pathways:

    #iterate through each year (every 5 years from 2020-2050)
    yrs = [2020,2025,2030,2035,2040,2045,2050]

    for year in yrs:
    
        #define all specific parameters using scenario chooser
        [CAISO_wind_cap,CAISO_solar_cap,CAISO_bat_cap,PNW_wind_cap,PNW_solar_cap,PNW_bat_cap,bat_RoC_coeff,bat_RoD_coeff,bat_eff,ev_df,identifier] = scenario_chooser.choose(pathway,year)

        #write parameters into param_output DataFrame under new column
        param_list = [CAISO_wind_cap,CAISO_solar_cap,CAISO_bat_cap,PNW_wind_cap,PNW_solar_cap,PNW_bat_cap,bat_RoC_coeff,bat_RoD_coeff,bat_eff]
        new_column = pathway + '_' + str(year)
        param_output[new_column] = param_list
        
        #write EV load profile into ev_output DataFrame under new column
        ev_columns = [pathway + '_' + str(year) + '_' + 'CAISO',pathway + '_' + str(year) + '_' + 'BPA']
        ev_output[ev_columns[0]] = ev_df['CAISO 24H EV Load'].values
        ev_output[ev_columns[1]] = ev_df['PNW 24H EV Load'].values

ev_full_year = ev_output        
for i in range(0,364):
    ev_full_year = ev_full_year.append(ev_output)
        
#write csv files for parameters and EV load        
param_output.to_csv('scenario_parameters.csv')
ev_full_year.to_csv('EV_load.csv',index=False)