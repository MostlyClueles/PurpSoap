#!/usr/bin/env python3
import numpy as np
import pandas as pd

'''
ALL error calculations use the validation period dataframe.
This is obtained through using the val_period function.
'''

def val_period(df, today):
    #limits the dataframe to the Validation Period which in this
    #    case is as long as the forecasting length

    f_len = len(df.loc[today:, 'Forecast'])

    err_df = df.iloc[-2*int(f_len) : -1*int(f_len), :]
    #returns viable intersection of Validation and Hist_Data

    del err_df['Forecast']
    #delete forecast column

    return err_df

def mae(df):
    #Mean Absolute Error (I tried to use standard textbook notation)

    v = len(df)
    #v stands for validation period

    e_t = df.loc[:, 'Hist_Data'] - df.loc[:, 'Valid']
    #make a data frame because making a new column breaks pandas

    x = sum(abs(e_t))
    #x == take the absolute value of all data points and then add
    #   them together

    error = x/v
    #MAE error is not a percentage, so it will be in dollars

    return error


def avg_err(df):
    #Average Error
    #same as MAE, but don't take the absolute value of difference

    v = len(df)

    e_t = df.loc[:, 'Hist_Data'] - df.loc[:, 'Valid']

    x = sum(e_t)

    error = x/v

    return error


def mape(df):
    #Mean Absolute Percentage Error

    v = len(df)

    e_t = df.loc[:, 'Hist_Data'] - df.loc[:, 'Valid']

    e_t = e_t / df.loc[:, 'Hist_Data']
    # divide difference by validation

    x = sum(abs(e_t))

    error = x/v

    percent_error = error * 100

    return percent_error


def rmse(df):
    #Root Mean Squared Error

    v = len(df)

    e_t = df.loc[:, 'Hist_Data'] - df.loc[:, 'Valid']

    e_t = np.square(e_t)
    #square the data
    #   np.square(df) is faster look up pd refrence

    x = sum(e_t)

    error = np.sqrt(x/v)
    #take the square root since you squared e_t

    return error
