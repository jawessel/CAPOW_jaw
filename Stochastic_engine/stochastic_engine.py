# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 09:59:48 2018

@author: YSu
"""

import pandas as pd
import scenario_chooser

#############################################################################
## HISTORICAL WEATHER AND STREAMFLOW ANALYSIS
#
## Perform statistical analysis of historical meteorological data
## Note: this script ('calculatte_cov') only needs to be performed once; after
## that stochastic input generation can occur as many times as desired.
#import time
#starttime = time.time()
##import calculate_cov
#
#############################################################################
## STOCHASTIC WEATHER AND STREAMFLOW GENERATION
#
## Specify a number of synthetic weather years to be simulated. Then
## edit the /cord/data/input/base_inflows.json file, specifying the start and end 
## dates of the forecast_exp scenario flow files. Start date must be 1/1/1901.
## End dates must be stoch_years + 3 after start date. 
#
#stoch_years=1000
#
## Generate synthetic weather (wind speed and temperature) records. 
#import synthetic_temp_wind_v3
#synthetic_temp_wind_v3.synthetic(stoch_years)
#print('synth weather')
#
## Generate synthetic streamflow records 
#import synthetic_streamflow_v2
#print('streamflows')
#
###############################################################################
###
##############################################################################
## DAILY HYDROPOWER SIMULATION
#
# Now specify a smaller subset of stochastic data to run (must be <= stoch years)
sim_years = 100

# Run ORCA to get California storage dam releases
import main
main.sim(sim_years)
print('ORCA')
#
# California Hydropower model
import CA_hydropower
CA_hydropower.hydro(sim_years)
print('CA hydropower')

#Willamette operational model
import Willamette_launch
Willamette_launch.launch(sim_years)
print('Willamette')


# Federal Columbia River Power System Model (mass balance in Python)
import ICF_calc_new
ICF_calc_new.calc(sim_years)
import FCRPS_New
FCRPS_New.simulate(sim_years)
print('FCRPS')

#############################################################################
#
#############################################################################
## HOURLY WIND AND SOLAR POWER PRODUCTION

#iterate through each scenario
#Scenarios: 'MID' = Mid-Case (S1), 'EV' = High EV Adoption (S2), 'BAT' = Low Battery Storage Cost (S3)
#   'LOWRECOST' = Low RE Cost / High Gas Price (S4), 'HIGHRECOST' = High RE Cost / Low Gas Price (S5)

pathways = ['MID','EV','BAT','LOWRECOST','HIGHRECOST']

for pathway in pathways:
    
    p_index = pathways.index(pathway)

    #iterate through each year (every 5 years from 2020-2050)
    yrs = [2020,2025,2030,2035,2040,2045,2050]
    
    for year in yrs:
        
        #define all specific parameters using scenario chooser
        [CAISO_wind_cap,CAISO_solar_cap,CAISO_bat_cap,PNW_wind_cap,PNW_solar_cap,PNW_bat_cap,bat_RoC_coeff,bat_RoD_coeff,bat_eff,ev_df,identifier] = scenario_chooser.choose(pathway,year)
        
        #write EV Load profiles to csv to be used elsewhere
        ev_df.to_csv('EV_load.csv')        
        
    # Generate synthetic hourly wind power production time series for the BPA and
    # CAISO zones for the entire simulation period
import wind_speed2_wind_power
wind_speed2_wind_power.wind_sim(sim_years,PNW_wind_cap,CAISO_wind_cap)
print('wind')

# Generate synthetic hourly solar power production time series for 
# the CAISO zone for the entire simulation period
import solar_production_simulation2
solar_production_simulation2.solar_sim(sim_years, PNW_solar_cap, CAISO_solar_cap)
print('solar')
##############################################################################
#
##############################################################################
# ELECTRICITY DEMAND AND TRANSMISSION PATH FLOWS

# Calculate daily peak and hourly electricity demand for each zone and daily 
# flows of electricity along each WECC path that exchanges electricity between
# core UC/ED model (CAISO, Mid-C markets) and other WECC zones

import demand_pathflows
print('paths')
##############################################################################
#
##############################################################################
# NATURAL GAS PRICES

# NOTE: NEED SCRIPT HERE TO SIMULATE STOCHASTIC NATURAL GAS PRICES 
# *OR*
# ESTIMATE STATIC GAS PRICES FOR EACH ZONE

import numpy as np
ng = np.ones((sim_years*365,5))
ng[:,0] = ng[:,0]*4.47
ng[:,1] = ng[:,1]*4.47
ng[:,2] = ng[:,2]*4.66
ng[:,3] = ng[:,3]*4.66
ng[:,4] = ng[:,4]*5.13

import pandas as pd
NG = pd.DataFrame(ng)
NG.columns = ['SCE','SDGE','PGE_valley','PGE_bay','PNW']
NG.to_excel('Gas_prices/NG.xlsx')

#open .csv file with scenario parameters

#for i in range(1,6):
#
#    #iterate through each year (every 5 years from 2020-2050)
#    yrs = [2020,2025,2030,2035,2040,2045,2050]
#    for j in yrs:
#        
#        #############################################################################
#        #
#        #############################################################################
#        #MODEL SETUP (UCED_setup file converted to function to iterate through each scenario/year combination)
#        import UCED_setup
#        UCED_setup.model_setup(CAISO_wind_cap,CAISO_solar_cap,CAISO_bat_cap,PNW_wind_cap,PNW_solar_cap,PNW_bat_cap,bat_RoC_coeff,bat_RoD_coeff,bat_eff,ev_df,i,j,identifier)
#


elapsed = time.time() - starttime
print(elapsed)