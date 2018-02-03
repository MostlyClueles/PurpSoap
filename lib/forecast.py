#!/usr/bin/env python3
import numpy as np
import pandas as pd
import datetime as dt
import f_base
import overlay

#This is a compilation of all of the forecast models. Error should
#   be calculated properly for all forecasting models

#df = data frame of stock inputed
#f_len = # of days inputed
#var = relevant column inputed, Ex: 'Adj Close', 'Open', ect...


def randwalk(df, f_len, var):
    #random walk

    #all f_base transformations
    period = f_base.full_period(df, f_len, var)
    df1 = f_base.hist_data(df, var)
    df2 = f_base.randwalk(df, f_len, var)

    df2.loc[:, 'Valid'] = df2.loc[:, 'Forecast']
    #make new column called Valid which is the same as forecast

    df = pd.concat([df1,df2], axis=1)
    #combinde dataframes by Date, so there will be NaN values
    #   after today in the historica data value section

    df = f_base.centralize(df, period[2])

    return df


def randwalk_drift(df, f_len, var):
    #random walk with drift

    #all f_base transformations
    period = f_base.full_period(df, f_len, var)
    df1 = f_base.hist_data(df, var)
    df2 = f_base.randwalk(df, f_len, var)

    slope = (df2.iat[-1,0] + df2.iat[-1*f_len, 0]) / (f_len - 1)
    #calculates the slope of the line with respect to the points at
    #   final and initial business day

    df2.loc[:, 'Forecast'] = df2.loc[:, 'Forecast'] + (f_len * slope)
    #add slope times length to each element

    df2.loc[:, 'Valid'] = df2.loc[:, 'Forecast']
    #make new column called Valid which is the same as forecast

    df = pd.concat([df1,df2], axis=1)
    #combinde dataframes by Date, so there will be NaN values
    #   after today in the historica data value section

    df = f_base.centralize(df, period[2])

    return df


def randwalk_geo(df, f_len, var):
    #geometric random walk

    #all f_base transformations
    period = f_base.full_period(df, f_len, var)
    df1 = f_base.hist_data(df, var)
    df2 = f_base.randwalk(df, f_len, var)
    alpha = f_base.alpha(f_len)

    df2.loc[:, 'Forecast'] = df2.loc[:, 'Forecast'] * np.exp(alpha)
    #each value in the forecast is multiplied by e^(alpha)

    df2.loc[:, 'Valid'] = df2.loc[:, 'Forecast']
    #make new column called Valid which is the same as forecast

    df = pd.concat([df1,df2], axis=1)
    #combinde dataframes by Date, so there will be NaN values
    #   after today in the historica data value section

    df = f_base.centralize(df, period[2])

    return df


def savg(df, f_len, var):
    #seasonal average (1-step)

    #all f_base transformations
    period = f_base.full_period(df, f_len, var)
    df1 = f_base.hist_data(df, var)
    df2 = f_base.lag(df, f_len, var)

    df2.index = df2.index + pd.tseries.offsets.BDay(f_len)
    #move forecast into the future so you don't have to make new columns

    df3 = df2
    #remember that they're both moved into the forecast future

    df3= df3.rename(columns = {'Forecast': 'Valid'})
    #create last dataframe for validation period

    savg = df2.loc[period[3] : period[4],'Forecast'].mean()
    #calculate the mean of today back f_len business days
    #doesn't seem right but the data was moved up, so it works

    savg_v = df3.loc[period[1] : period[2],'Valid'].mean()
    #do same for validation

    df2.loc[period[3] : period[4], 'Forecast'] = savg

    df3.loc[period[1] : period[2], 'Valid'] = savg_v
    #do same for validation period

    df = pd.concat([df1, df2, df3], axis=1)
    #put together all of the columns

    df = f_base.centralize(df, period[2])

    return df


def ses(df, f_len, var):
    #Brown's Simple Exponential Smoothing (1-step)

    #all f_base transformations
    period = f_base.full_period(df, f_len, var)
    df1 = f_base.hist_data(df, var)
    df2 = f_base.lag(df, f_len, var)

    df2 = overlay.ses_overlay(df2, f_len, 'Forecast')
    #gives you the ses and the last value is equal to the forecast

    df2 = df2.rename(columns = {'Overlay' : 'Forecast'})
    #rename the only column to forecast

    df2.index = df2.index + pd.tseries.offsets.BDay(f_len)
    #move up the data to forecast period

    df3 = df2
    #make validation column

    df3 = df3.rename(columns = {'Forecast' : 'Valid'})

    forecast = df2.iat[-1,0]
    #gives you the forecast value

    preforecast = df2.iat[-2,0]
    #day before forecast

    df2.loc[period[3] : period[4],'Forecast'] = forecast
    #make tomorrow till end = forecast value

    df2.loc[period[2],'Forecast'] = preforecast
    #make today the preforecast value

    #same for validatijon
    valid = df3.at[period[3], 'Valid']
    prevalid = df3.at[period[2], 'Valid']
    df3.loc[period[1] : period[2],'Valid'] = valid
    df3.at[period[0],'Valid'] = prevalid

    df = pd.concat([df1, df2, df3], axis=1)
    #put together all of the columns

    df = f_base.centralize(df, period[2])

    return df


def dses(df, f_len, var):
    #Brown's Linear Exponential Smoothing/ Double exponential smoothing
    #Trend is NOT removed

    #all f_base transformations
    period = f_base.full_period(df, f_len, var)
    df1 = f_base.hist_data(df, var)
    alpha = f_base.alpha(f_len)

    smooth = overlay.ses_overlay(df, 1, var)
    #smooths the dataframe

    dsmooth = overlay.ses_overlay(smooth, 1, 'Overlay')
    #double smoothed dataframe

    dsmooth.index = dsmooth.index - pd.tseries.offsets.BDay(1)
    #double smooth series is used after a single time period is removed

    level = 2*smooth - 1*dsmooth

    trend = smooth - 1*dsmooth

    df2 = level + (f_len * (alpha / (1 - alpha)) * trend)

    period = f_base.full_period(df2, f_len, 'Overlay')
    #take the period now because otherwise dates might not line up

    df2 = df2.rename(columns = {'Overlay' :  'Forecast'})
    #Rename becasue it's not an overlay anymore

    df2.index = df2.index + pd.tseries.offsets.BDay(f_len)
    #put it up to forecast because that's what the equation says

    df3 = df2
    #no need to move them because it's a continuous forecast#

    df3 = df3.rename(columns = {'Forecast' : 'Valid'})

    df = pd.concat([df1, df2, df3], axis=1)
    #put together all of the columns

    df = f_base.centralize(df, period[2])

    return df


def hles(df, f_len, var):
    #Holts linear exponential smoothing
    #Trend is NOT removed

    #all f_base transfromations
    period = f_base.full_period(df, f_len, var)
    df1 = f_base.hist_data(df, var)
    alpha = f_base.alpha(f_len)
    beta = f_base.beta(f_len)

    smooth = overlay.ses_overlay(df, 1, var)
    #smooths the dataframe

    dsmooth = overlay.ses_overlay(smooth, 1, 'Overlay')
    #double smoothed dataframe

    dsmooth.index = dsmooth.index - pd.tseries.offsets.BDay(1)
    #double smooth series is used after a single time period is removed

    #basic levels and trends
    level = 2*smooth - 1*dsmooth
    trend = smooth - 1*dsmooth

    #Make new data frames for the t-1 series
    lesslevel = level
    lesstrend = trend

    #gives the level and trend at t - 1
    lesslevel.index = lesslevel.index - pd.tseries.offsets.BDay(1)
    lesstrend.index = lesstrend.index - pd.tseries.offsets.BDay(1)

    #set original data to new dataframe with column named overlay
    #   so you can manipulate it with the others
    original = df1
    original = original.rename(columns = {'Hist_Data' : 'Overlay'})

    #gives level and trend with respect to holts model
    newlevel = alpha*original + (1 - alpha)*(lesslevel + lesstrend)
    newtrend = beta*(level - lesslevel) + (1 - beta)*lesstrend

    #there are a few gaps from holidays so fill those, but don't fill
    #   any possible future forecasts
    newlevel = newlevel.bfill()
    newtrend = newtrend.bfill()

    forecast = newlevel + f_len*newtrend
    #this is Holts final equation using the new trend and level

    forecast = forecast.rename(columns = {'Overlay' : 'Forecast'})

    forecast.index = forecast.index + pd.tseries.offsets.BDay(f_len)

    validation = forecast
    #validation column is the same as the forecast

    validation = validation.rename(columns = {'Forecast' : 'Valid'})
    #rename for error calculations

    df = pd.concat([df1, forecast, validation], axis=1)

    df = f_base.centralize(df, period[2])

    return df

def lin_reg(df, f_len, var):
    #linear regression
    '''
    THIS DOES NOT WORK YET
    '''

    #all f_base transfromations
    period = f_base.full_period(df, f_len, var)
    df1 = f_base.hist_data(df, var)

    df2 = overlay.ses_overlay(df, 1, var)
    df2 = df2.rename(columns={'Overlay' : 'Forecast'})

    x = len(df2)

    df2 = df2.loc[:, 'Forecast'].between(1,x+1)

    return df2






# the end
