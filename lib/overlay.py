#!/usr/bin/env python3
import numpy as np
import pandas as pd
import datetime as dt


def sma_overlay(df, f_len, var):
    #simple moving average overlay

    f_len = int(f_len)
    #convert the length input just in case

    df1 = df[[var]]
    #limit the dataframe to just the column

    df1= df1.rename(columns = {var : 'Overlay'})
    #rename the only column to Overlay

    df1 = df1.resample("1B").sum().fillna(0).\
        rolling(window=f_len, min_periods=0).mean()
    #gives the moving average of a heading window we want trailing
    #this has been tested with smaller data sets and works
    #Ex: window = 3, and calculating at time 5 = (t_5), we get
    #   (t_3+t_4+t_5)/3 = t_5 in new column and then essentially
    #   delete the old column. You will not use the mean of t_4
    #   to calculate t_5.
    #First Rows len(f_len-1) are bogus

    return df1 #1 column dataframe which is just the overlay


def ses_overlay(df, f_len, var):
    #Simple Exponential Smoothing

    f_len = int(f_len)

    df1 = df[[var]]
    #new dataframe equal to the column of the variable inputed

    df1= df1.rename(columns = {var : 'Overlay'})

    df1.iat[f_len-1, 0] = df1.iloc[:f_len, 0].mean()
    #take the mean of the first f_len of numbers and then gives you a mean
    #   which then replaces the f_len number. It's f_len-1 because counting
    #   starts at 0

    df1 = df1.iloc[f_len-1:, :].resample("1B").asfreq()\
        .ewm(span=f_len, adjust=False).mean()
    #this takes the actucal exponential moving average every
    #   business day is the frequency. Span is supposed to be
    #   equal to the number of days you want to forecast.
    #   Adjustment is false because we're already working with
    #   a lagged dataframe.

    return df1







#the end
