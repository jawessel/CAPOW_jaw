# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 21:29:55 2018

@author: jkern
"""

############################################################################
#                               DATA SETUP

# This file selects a single year from the synthetic record and organizes the
# data in a form that is accessible to the unit commitment/economic dispatch
# (UC/ED) simulation model. This script can be interfaced with a data mining
# scheme for selecting specific years to run.
############################################################################

############################################################################
#                             HYDROPOWER SETUP
#
# This section uses historical hydropower production data and simulated hydropower
# to creat time series of minimum hydropower production and ramp rates.

# First script
# only needs to be run 1 time, and the ramp rates should be added manually to the
# generators data file.

#import min_hydro_ramping
############################################################################

############################################################################
#                         SYNTHETIC YEAR SELECTION

# Default is that a random year from the synthetic record is selected to be run
# through the UC/ED model.

import pandas as pd
import numpy as np

def model_setup(pathway,model_year):

    # Run the following lines if you want to select a random year from the synthetic record
    #to be run through the UC/ED model.
    df_sim = pd.read_excel('CA_hydropower/CA_hydro_daily.xlsx')
    sim_years = len(df_sim)/365
    # year = np.random.uniform(0,1,1)*sim_years
    # year = int(np.floor(year))
    scenario = pathway + '_' + str(model_year)
    
    import scenario_chooser
    [CAISO_wind_cap,CAISO_solar_cap,CAISO_bat_cap,PNW_wind_cap,PNW_solar_cap,PNW_bat_cap,bat_RoC_coeff,bat_RoD_coeff,bat_eff,ev_df,identifier] = scenario_chooser.choose(pathway,model_year)

    
    #for i in range(0,1):   
    for i in range(0,int(sim_years)):
        year=int(i)
    
        ############################################################################
        #                          CA TIME SERIES SETUP
    
        # Calculates "minimum flows" for zonal hydropower production and imports,
        # dispatchable imports and hydropower, and hourly export demand
    
        import CA_exchange_time_series
        CA_exchange_time_series.exchange(year,scenario)
    
        ############################################################################
        #                          PNW TIME SERIES SETUP
    
        # Note: In future versions this can be set up differently to coordinate hourly
        # Export time series (PNW-->CAISO) with records of dispatched imports from the
        # CAISO market model.
    
    
        import PNW_exchange_time_series
        PNW_exchange_time_series.exchange(year,scenario)
    
    
        ############################################################################
        #                          UC/ED Data File Setup
    
        # CALIFORNIA
        # hist = 1 if looking at historical nuclear power production; facilitates use of
        # monthly nuclear power generation data from EIA. Note that if hist = 0
        # the model assumes that nuclear power plants in California have been retired.
        
        import CA_data_setup
        CA_data_setup.setup(scenario,CAISO_bat_cap,bat_RoC_coeff,bat_RoD_coeff,bat_eff)
    
    
        # PACIFIC NORTHWEST
        import PNW_data_setup
        PNW_data_setup.setup(scenario,PNW_bat_cap,bat_RoC_coeff,bat_RoD_coeff,bat_eff)
        
        
        
        import CA_data_setup2
        CA_data_setup2.setup(scenario,CAISO_bat_cap,bat_RoC_coeff,bat_RoD_coeff,bat_eff)
    
    
        # PACIFIC NORTHWEST
        import PNW_data_setup2
        PNW_data_setup2.setup(scenario,PNW_bat_cap,bat_RoC_coeff,bat_RoD_coeff,bat_eff)
    
        print(i)
    
    return None