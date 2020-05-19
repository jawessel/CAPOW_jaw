# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 21:26:30 2019

@author: jawessel
"""

##################################################################################
#GIVES SOLAR AND WIND CAPACITIES FOR CA AND PNW BASED ON CHOSEN SCENARIO AND YEAR#
##################################################################################

#from pandas import ExcelWriter
import pandas as pd
import numpy as np

#MUST SPECIFY VALID SCENARIO AND YEAR
#Scenarios: 'MID' = Mid-Case (S1), 'EV' = High EV Adoption (S2), 'BAT' = Low Battery Storage Cost (S3)
#   'LOWRECOST' = Low RE Cost / High Gas Price (S4), 'HIGHRECOST' = High RE Cost / Low Gas Price (S5)
#Years: 2020 - 2050
#scenario = 'MID'
#year = 2020

def choose(pathway, year):

#scenario = 'EV'
#year=2045
    scenario = pathway

    #identifier for outputting scenario parameters to excel file to be read elsewhere
    identifier = pd.DataFrame([scenario, str(year)])
    
    #Specify battery rate of charge, rate of discharge, and efficiency (hard coded here)
    bat_RoC_coeff = 0.2 #fraction of capacity (multiplied by capacities in setup file)
    bat_RoD_coeff = 0.8 #fraction of capacity (multiplied by capacities in setup file)
    bat_eff = 0.85
    
    #Specify total average annual load for CA and PNW, in order to calculate additional load due to EVs as a fraction of total load (MW)
    CA_hist_load = 25865.58304
    PNW_hist_load = 16994.26555
    
    #Read csv of ReEDS output data into a dataframe indexed by scenario, state, year, and plant type
    #Includes only outputs of wind, solar, and storage capacity (in case storage capacity is needed later)
    data = pd.read_csv('cap_wind_solar.csv', index_col = ['Scenario','State','Type','Year'])
    
    #Read csv's of ReEDS total capacities and generation into dataframes, in order to calculate fractions of renewables penetration
    #cap_totals = pd.read_csv('reeds_cap_totals.csv', index_col = ['Scenario','State','Year'])
    gen_totals = pd.read_csv('reeds_gen_totals.csv', index_col = ['Scenario','State','Year'])
    
    #Read csv's of generator data to get total modeled capacity
    #caiso_generators = pd.read_csv('CA_data_file/generators.csv')
    #caiso_must_run = pd.read_csv('CA_data_file/must_run_final.csv')
    #pnw_generators = pd.read_csv('PNW_data_file/generators.csv')
    #pnw_must_run = pd.read_csv('PNW_data_file/must_run.csv')
    #conv_types = ['ngcc','ngct','ngst','oil','coal','psh','hydro']
    #caiso_conv_cap = caiso_generators[caiso_generators['typ'].isin(conv_types)]['netcap'].sum() + caiso_must_run.values.sum()
    #pnw_conv_cap = pnw_generators[pnw_generators['typ'].isin(conv_types)]['netcap '].sum() + pnw_must_run.values.sum()
    
    #Aggregate land-based wind and offshore wind to single WIND capacity
    #Aggregate CSP, Utility PV, and Rooftop PV to single SOLAR capacity
    sums = data.groupby(['Scenario','State','Type','Year']).sum()
    
    #Read computed fractions of state wind and solar used in CAPOW
    frac = pd.read_csv('fractions.csv', index_col = ['State','Type'])
    
    #Read CSV of 24 hour EV charging profile
    EV_prof = pd.read_csv('ev_prof.csv', index_col = ['Scenario','Year','Region'])
    MW_per_vehicle_hourly = pd.read_csv('mwpervehicle.csv')
    EV_frac = np.zeros((24,2))
    
    #Retrieve capacity fractions directly from sums dataframe if year is even
    if(year % 2 == 0):
        CAISO_wind_frac = (sums.loc[(scenario, 'CA', 'WIND', year), 'Capacity']*1000*frac.loc[('CA','WIND'), 'Fraction'] / gen_totals.loc[(scenario,'CA',year), 'Demand (MW)']) + \
            (sums.loc[(scenario, 'NV', 'WIND', year), 'Capacity']*1000*frac.loc[('NV','WIND'), 'Fraction'] / gen_totals.loc[(scenario,'NV',year), 'Demand (MW)'])
        
        CAISO_solar_frac = (sums.loc[(scenario, 'CA', 'SOLAR', year), 'Capacity']*1000*frac.loc[('CA','SOLAR'), 'Fraction'] / gen_totals.loc[(scenario,'CA',year), 'Demand (MW)']) + \
            (sums.loc[(scenario, 'NV', 'SOLAR', year), 'Capacity']*1000*frac.loc[('NV','SOLAR'), 'Fraction'] / gen_totals.loc[(scenario,'NV',year), 'Demand (MW)'])
        
        CAISO_bat_frac = sums.loc[(scenario, 'CA', 'BATT', year), 'Capacity']*1000 / gen_totals.loc[(scenario,'CA',year), 'Demand (MW)']
        
        PNW_solar_frac = (sums.loc[(scenario, 'WA', 'SOLAR', year), 'Capacity']*1000*frac.loc[('WA','SOLAR'), 'Fraction'] / gen_totals.loc[(scenario,'WA',year), 'Demand (MW)']) + \
            (sums.loc[(scenario, 'OR', 'SOLAR', year), 'Capacity']*1000*frac.loc[('OR','SOLAR'), 'Fraction'] / gen_totals.loc[(scenario,'OR',year), 'Demand (MW)']) + \
            (sums.loc[(scenario, 'ID', 'SOLAR', year), 'Capacity']*1000*frac.loc[('ID','SOLAR'), 'Fraction'] / gen_totals.loc[(scenario,'ID',year), 'Demand (MW)'])
        
        PNW_wind_frac = (sums.loc[(scenario, 'WA', 'WIND', year), 'Capacity']*1000*frac.loc[('WA','WIND'), 'Fraction'] / gen_totals.loc[(scenario,'WA',year), 'Demand (MW)']) + \
        (sums.loc[(scenario, 'OR', 'WIND', year), 'Capacity']*1000*frac.loc[('OR','WIND'), 'Fraction'] / gen_totals.loc[(scenario,'OR',year), 'Demand (MW)']) + \
        (sums.loc[(scenario, 'ID', 'WIND', year), 'Capacity']*1000*frac.loc[('ID','WIND'), 'Fraction'] / gen_totals.loc[(scenario,'ID',year), 'Demand (MW)'])
        
        PNW_bat_frac = (sums.loc[(scenario, 'WA', 'BATT', year), 'Capacity']*1000 / gen_totals.loc[(scenario,'WA',year), 'Demand (MW)']) + \
        (sums.loc[(scenario, 'OR', 'BATT', year), 'Capacity']*1000 / gen_totals.loc[(scenario,'OR',year), 'Demand (MW)'])
        
        #Create 24x2 matrix of added demand due to EV adoption (0 for CAISO, 1 for PNW)
        for i in range(0,24):
            EV_frac[i,0] = (EV_prof.loc[(scenario,year,'CA'), 'Number of Vehicles']*MW_per_vehicle_hourly.loc[i, 'MW/Vehicle']*0.90823665)/gen_totals.loc[(scenario,'CA',year),'Demand (MW)'] #0.908 is the proportion of CA EV's which are in CAPOW
            EV_frac[i,1] = (((EV_prof.loc[(scenario,year,'OR'), 'Number of Vehicles']*0.607928)/gen_totals.loc[(scenario,'OR',year),'Demand (MW)']) + \
               ((EV_prof.loc[(scenario,year,'WA'), 'Number of Vehicles']*0.906621704)/gen_totals.loc[(scenario,'WA',year),'Demand (MW)']) + \
               ((EV_prof.loc[(scenario,year,'ID'), 'Number of Vehicles']*0.0591133)/gen_totals.loc[(scenario,'ID',year),'Demand (MW)']))*MW_per_vehicle_hourly.loc[i, 'MW/Vehicle']
            #scale factors show proportion of EVs in each state which are captured by CAPOW
    
    #Capacity fractions must be computed if year is odd, because ReEDS outputs are every two years
    #Capacity fractions are computed as the average of the previous year and the next year
    elif(year % 2 != 0):
        CAISO_wind_frac = (sums.loc[(scenario, 'CA', 'WIND', year+1), 'Capacity']*1000*frac.loc[('CA','WIND'), 'Fraction'] + \
                            sums.loc[(scenario, 'CA', 'WIND', year-1), 'Capacity']*1000*frac.loc[('CA','WIND'), 'Fraction'])/(gen_totals.loc[(scenario,'CA',year+1), 'Demand (MW)']+gen_totals.loc[(scenario,'CA',year-1), 'Demand (MW)']) + \
                            (sums.loc[(scenario, 'NV', 'WIND', year+1), 'Capacity']*1000*frac.loc[('NV','WIND'), 'Fraction'] + \
                            sums.loc[(scenario, 'NV', 'WIND', year-1), 'Capacity']*1000*frac.loc[('NV','WIND'), 'Fraction'])/(gen_totals.loc[(scenario,'NV',year+1), 'Demand (MW)']+gen_totals.loc[(scenario,'NV',year-1), 'Demand (MW)'])
        
        CAISO_solar_frac = (sums.loc[(scenario, 'CA', 'SOLAR', year+1), 'Capacity']*1000*frac.loc[('CA','SOLAR'), 'Fraction'] + \
                            sums.loc[(scenario, 'CA', 'SOLAR', year-1), 'Capacity']*1000*frac.loc[('CA','SOLAR'), 'Fraction'])/(gen_totals.loc[(scenario,'CA',year+1), 'Demand (MW)']+gen_totals.loc[(scenario,'CA',year-1), 'Demand (MW)']) + \
                            (sums.loc[(scenario, 'NV', 'SOLAR', year+1), 'Capacity']*1000*frac.loc[('NV','SOLAR'), 'Fraction'] + \
                            sums.loc[(scenario, 'NV', 'SOLAR', year-1), 'Capacity']*1000*frac.loc[('NV','SOLAR'), 'Fraction'])/(gen_totals.loc[(scenario,'NV',year+1), 'Demand (MW)']+gen_totals.loc[(scenario,'NV',year-1), 'Demand (MW)'])
        
        CAISO_bat_frac = (sums.loc[(scenario, 'CA', 'BATT', year+1), 'Capacity']*1000 + sums.loc[(scenario, 'CA', 'BATT', year-1), 'Capacity']*1000)/(gen_totals.loc[(scenario,'CA',year+1), 'Demand (MW)']+gen_totals.loc[(scenario,'CA',year-1), 'Demand (MW)'])
        
        PNW_solar_frac = (sums.loc[(scenario, 'WA', 'SOLAR', year+1), 'Capacity']*1000*frac.loc[('WA','SOLAR'), 'Fraction'] + \
                            sums.loc[(scenario, 'WA', 'SOLAR', year-1), 'Capacity']*1000*frac.loc[('WA','SOLAR'), 'Fraction'])/(gen_totals.loc[(scenario,'WA',year+1), 'Demand (MW)']+gen_totals.loc[(scenario,'WA',year-1), 'Demand (MW)']) + \
                            (sums.loc[(scenario, 'OR', 'SOLAR', year+1), 'Capacity']*1000*frac.loc[('OR','SOLAR'), 'Fraction'] + \
                            sums.loc[(scenario, 'OR', 'SOLAR', year-1), 'Capacity']*1000*frac.loc[('OR','SOLAR'), 'Fraction'])/(gen_totals.loc[(scenario,'OR',year+1), 'Demand (MW)']+gen_totals.loc[(scenario,'OR',year-1), 'Demand (MW)']) + \
                            (sums.loc[(scenario, 'ID', 'SOLAR', year+1), 'Capacity']*1000*frac.loc[('ID','SOLAR'), 'Fraction'] + \
                            sums.loc[(scenario, 'ID', 'SOLAR', year-1), 'Capacity']*1000*frac.loc[('ID','SOLAR'), 'Fraction'])/(gen_totals.loc[(scenario,'ID',year+1), 'Demand (MW)']+gen_totals.loc[(scenario,'ID',year-1), 'Demand (MW)'])
        
        PNW_wind_frac = (sums.loc[(scenario, 'WA', 'WIND', year+1), 'Capacity']*1000*frac.loc[('WA','WIND'), 'Fraction'] + \
                            sums.loc[(scenario, 'WA', 'WIND', year-1), 'Capacity']*1000*frac.loc[('WA','WIND'), 'Fraction'])/(gen_totals.loc[(scenario,'WA',year+1), 'Demand (MW)']+gen_totals.loc[(scenario,'WA',year-1), 'Demand (MW)']) + \
                            (sums.loc[(scenario, 'OR', 'WIND', year+1), 'Capacity']*1000*frac.loc[('OR','WIND'), 'Fraction'] + \
                            sums.loc[(scenario, 'OR', 'WIND', year-1), 'Capacity']*1000*frac.loc[('OR','WIND'), 'Fraction'])/(gen_totals.loc[(scenario,'OR',year+1), 'Demand (MW)']+gen_totals.loc[(scenario,'OR',year-1), 'Demand (MW)']) + \
                            (sums.loc[(scenario, 'ID', 'WIND', year+1), 'Capacity']*1000*frac.loc[('ID','WIND'), 'Fraction'] + \
                            sums.loc[(scenario, 'ID', 'WIND', year-1), 'Capacity']*1000*frac.loc[('ID','WIND'), 'Fraction'])/(gen_totals.loc[(scenario,'ID',year+1), 'Demand (MW)']+gen_totals.loc[(scenario,'ID',year-1), 'Demand (MW)'])
        
        PNW_bat_frac = (sums.loc[(scenario, 'WA', 'BATT', year+1), 'Capacity']*1000 + sums.loc[(scenario, 'WA', 'BATT', year-1), 'Capacity']*1000)/(gen_totals.loc[(scenario,'WA',year+1), 'Demand (MW)']+gen_totals.loc[(scenario,'WA',year-1), 'Demand (MW)']) + \
                            (sums.loc[(scenario, 'OR', 'BATT', year+1), 'Capacity']*1000 + sums.loc[(scenario, 'OR', 'BATT', year-1), 'Capacity']*1000)/(gen_totals.loc[(scenario,'OR',year+1), 'Demand (MW)']+gen_totals.loc[(scenario,'OR',year-1), 'Demand (MW)'])
    
            #Create 24x2 matrix of added demand due to EV adoption (0 for CAISO, 1 for PNW)
        for i in range(0,24):
            EV_frac[i,0] = (EV_prof.loc[(scenario,year,'CA'), 'Number of Vehicles']*MW_per_vehicle_hourly.loc[i, 'MW/Vehicle']*0.90823665)/ \
                ((gen_totals.loc[(scenario,'CA',year+1),'Demand (MW)'] + gen_totals.loc[(scenario,'CA',year-1),'Demand (MW)'])/2) #0.908 is the proportion of CA EV's which are in CAPOW
                
            EV_frac[i,1] = (((EV_prof.loc[(scenario,year,'OR'), 'Number of Vehicles']*0.607928)/((gen_totals.loc[(scenario,'OR',year+1),'Demand (MW)'] + gen_totals.loc[(scenario,'OR',year-1),'Demand (MW)'])/2)) + \
                ((EV_prof.loc[(scenario,year,'WA'), 'Number of Vehicles']*0.906621704)/((gen_totals.loc[(scenario,'WA',year+1),'Demand (MW)'] + gen_totals.loc[(scenario,'WA',year-1),'Demand (MW)'])/2)) + \
                ((EV_prof.loc[(scenario,year,'ID'), 'Number of Vehicles']*0.0591133)/((gen_totals.loc[(scenario,'ID',year+1),'Demand (MW)'] + gen_totals.loc[(scenario,'ID',year-1),'Demand (MW)'])/2)))*MW_per_vehicle_hourly.loc[i, 'MW/Vehicle']
            #scale factors show proportion of EVs in each state which are captured by CAPOW
    
    #Calculate real capacities based on the computed fractions and the total capacity in the model
    #Since the addition of these resources adds to the total capacity, algebra was used to correct: capacity = (fraction * conventional capacity) / (1 - fraction)
            
    CAISO_wind_cap = CAISO_wind_frac * CA_hist_load
    CAISO_solar_cap = CAISO_solar_frac * CA_hist_load
    CAISO_bat_cap = CAISO_bat_frac * CA_hist_load
    PNW_wind_cap = PNW_wind_frac * PNW_hist_load
    PNW_solar_cap = PNW_solar_frac * PNW_hist_load
    PNW_bat_cap = PNW_bat_frac * PNW_hist_load     
            
    #Old method of calculating based on not adding to total demand
    #CAISO_wind_cap = (CAISO_wind_frac * CA_hist_load) / (1 - CAISO_wind_frac)
    #CAISO_solar_cap = (CAISO_solar_frac * CA_hist_load) / (1 - CAISO_solar_frac)
    #CAISO_bat_cap = (CAISO_bat_frac * CA_hist_load) / (1 - CAISO_bat_frac)
    #PNW_wind_cap = (PNW_wind_frac * PNW_hist_load) / (1 - PNW_wind_frac)
    #PNW_solar_cap = (PNW_solar_frac * PNW_hist_load) / (1 - PNW_solar_frac)
    #PNW_bat_cap = (PNW_bat_frac * PNW_hist_load) / (1 - PNW_bat_frac)
    
    #Zero out batteries for testing
    #CAISO_bat_cap = 0
    #PNW_bat_cap = 0
    
    #collects values in a DataFrame to write to csv file
    #scenario_parameters = pd.DataFrame([CAISO_wind_cap,CAISO_solar_cap,CAISO_bat_cap,PNW_wind_cap,PNW_solar_cap,PNW_bat_cap,bat_RoC_coeff,bat_RoD_coeff,bat_eff], \
    #    index=['CAISO_wind_cap','CAISO_solar_cap','CAISO_bat_cap','PNW_wind_cap','PNW_solar_cap','PNW_bat_cap','bat_RoC_coeff','bat_RoD_coeff','bat_eff'], columns = ['Value (MW)'])
    ev_df = pd.DataFrame(EV_frac,index=['Hour ' + str(x) for x in range(1,25)], columns = ['CAISO 24H EV Load','PNW 24H EV Load'])
    ev_df['CAISO 24H EV Load'] = (ev_df['CAISO 24H EV Load'] * CA_hist_load) / (1 - ev_df['CAISO 24H EV Load'])
    ev_df['PNW 24H EV Load'] = (ev_df['PNW 24H EV Load'] * PNW_hist_load) / (1 - ev_df['PNW 24H EV Load'])
    
    #with ExcelWriter('scenario_parameters.xlsx') as writer:
        #scenario_parameters.to_excel(writer, sheet_name='Capacities')
        #ev_df.to_excel(writer, sheet_name='EV Load Profiles')
        #identifier.to_excel(writer, sheet_name='Scenario and Year')
    
    return [CAISO_wind_cap,CAISO_solar_cap,CAISO_bat_cap,PNW_wind_cap,PNW_solar_cap,PNW_bat_cap,bat_RoC_coeff,bat_RoD_coeff,bat_eff,ev_df,identifier];