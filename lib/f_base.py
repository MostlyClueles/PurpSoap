#!/usr/bin/env python3
import numpy as np
import pandas as pd
import datetime as dt


#This is a compilation of all of the forecast basics. These are functions
#   that will commonly be used in forecast models. They are here because
#   I had all of my forecasts here and it got too big.

#df = data frame of stock inputed
#f_len = # of days inputed
#var = relevant column inputed, Ex: 'Adj Close', 'Open', ect...

'''
Pre-processing operations:
    Operations which take the raw data frame and modify it in such a
    way that it is more convient to use for data analysis. Alpha and
    Beta are both very simple and could be lambda functions. However,
    I put them here. This is so that the values scale for all forecasts.
    Possibly making the code more flexible for user input for alpha and
    beta.
'''
def hist_data(df, var):
    #gives a single column of the historical dataframe by input variable

    df = df[[var]]
    #retruns single column dataframe

    df= df.rename(columns = {var : 'Hist_Data'})
    #renames only column to Hist_Data

    return df

def randwalk(df, f_len, var):
    #Only moves the dates up f_len business days

    df = df[[var]]
    #retruns single column dataframe

    df = df.rename(columns={var : 'Forecast'})
    #this is generally the first step of a forecast so rename column

    df.index = df.index + pd.tseries.offsets.BDay(f_len)
    #shifts new dataframe dates foward the exact period of forecasting
    #   inputed by the user. B for business day doesn't include
    #   holidays.

    return df


def lag(df, f_len, var):
    #Calculates the difference or lag with respect to the users
    #   input. Ex: user put in 5 for business week. Takes this
    #   weeks data and subtracts last weeks data to normalize.
    #   Also known as taking the difference

    df1 = df[[var]]
    #double [] keeps it a dataframe and limits the data frame to variable

    df1= df1.rename(columns = {var : 'Forecast'})
    #rename only column to Forecast

    df2 = df1[['Forecast']]
    #replicate df1 and call it df2

    df2= df2.rename(columns = {'Forecast': 'F2'})
    #rename df2 column for future reference

    df2.index = df2.index + pd.tseries.offsets.BDay(f_len)
    #lags number you put in so if you enter 1 you get a lag-1

    df1 = pd.concat([df1, df2], axis=1).bfill()
    #put together both data frames by date and fill in holidays

    df1['Forecast'] = df1['Forecast'] - df1['F2']
    #Take difference between both columns and store in Forecast

    del df1['F2']
    #delete the F2 column

    df1 = df1[f_len:-1*f_len]
    #trim off the top and bottom since the top consists of dates
    #   after today and the bottom has a number + NaN and
    #   not the difference we are looking for.

    return df1 #gives you single column named 'Forecast'

def alpha(f_len):
    #this gives the alpha value for a forecast based on pandas ewm
    #   documentation with respect to span

    alpha = 2 / (f_len + 1)

    return alpha


def beta(f_len):
    #this gives you beta

    beta = 1 / (f_len*2)
    #beta is an estimate of trend, so this is taking 4 times the values
    #   over f_len and using them to get a trend.
    #Ex: f_len = 10, trend of the forecast = average trend over the last
    #   40 periods
    #Multiply the denominator by a constant to scale accordingly

    return beta


def full_period(df, f_len, var):
    #calculated 5 points and puts them in a list
    # 0 = day before validation period
    # 1 = first day of validation
    # 2 = last day of validation and day before first forecast day
    # 3 = first day of forecast
    # 4 = last day of forecast

    df = df[[var]]

    today = df.index.max() #2
    #if you set today to dt.date.today() it will bug out at weird times

    df.index = df.index + pd.tseries.offsets.BDay(f_len)
    #offset so dates match up

    last = df.index.max() # 4

    pretomorrow = len(df.loc[today:last, var])

    tomorrow = df.index[-pretomorrow+1] # 3
    #index one above today

    v_begin = df.index[-2*pretomorrow] # 1

    first = df.index[-2*pretomorrow-1] # 0

    full_list = [first, v_begin, today, tomorrow, last]

    return full_list


'''
Post-processing Operations:
    Operations which occur after forecasting operations. They take into
    account the columns [0] = Hist_Data, [1] = Forecast, [2] = Valid
    and that the data was pulled from today. The data must have been
    pulled from today because otherwise bussiness days work in a super
    wonky fashion and break the code. These are 'prerequsites'
    for all post-processing operations. Processes only affect the first
    3 columns.
'''

def centralize(df, periodtwo):
    #takes the forecast and sets the forecast price of today to the
    #   stock price of today. Does the same operation with validation
    #   period except gets it centralized with respect to
    #   (today - number of business days the user put in) = start of
    #   validation period.
    #   MUST use full_period[2] otherwise the program breaks on
    #   weekends.

    f_len = len(df.loc[periodtwo:, 'Forecast'])
    #because weekends we don't actucally know how many forecast days
    #   there are so this just takes the length and holidays don't help

    df.iloc[:-1*f_len, 1] =  None
    #remove all data before today in forecast

    df.iloc[0:-2*f_len, 2] =  None
    #remove data before validation period, but not after

    df.iloc[:, 1:] = df.iloc[:, 1:].ffill()
    #fill holidays on forecast and validation and future columns

    df.iloc[:, 0] = df.iloc[:, 0].bfill()
    #back fill because it seems simpler

    center = df.iat[-1*f_len,1] - df.iat[-1*f_len,0]
    #center = todays value Forecast - todays value Hist Data

    df.iloc[-1*f_len-1:, 1] = df.iloc[-1*f_len-1:, 1] - center
    #sets Forecast so that the forecast of today == todays
    #   actucal stock price

    #do same to validation column
    center2 = df.iat[-2*f_len,2] - df.iat[-2*f_len,0]
    df.iloc[-2*f_len-1:, 2] = df.iloc[-2*f_len-1:, 2] - center2

    return df
