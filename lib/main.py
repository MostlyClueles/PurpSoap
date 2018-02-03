#!/usr/bin/env python3

import os
import sys
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
# ^(Not My Libraries)
import mod_input
import forecast
import error
import plottin
# ^(My Libraries)

#BASES these scale the data extraction and calculation and do NOT
#   change. You can change them, but they don't change when going
#   through the program.


time_frame_base = 28
#base * user_days = length of the dataframe in business days
#based on at input of 1 month = 20 BDays will give you a little
#   over 2 years of data for accurate

min_time_base = 12
#base * user_days = minimum amount of time required to make a
#   prediction

m_avg_base = 8
#moving average is calculated by (base * user_days)
'''
MAKE ERROR IF ENTER NEGATIVE NUMBER!!!!!!!!!!!
tip: just search for a negative sign in the input or abs the output
'''

raw_usr_input = input('Stock Data: ')
#raw_usr_input takes string of CSV's that user types, can type help for
#   help_message.txt

usr_input = mod_input.time_stock(raw_usr_input)
#usr_input is a list with respect to what the user entered

'''
Current format:
    usr_input[0] = Stock Abbreviation
    usr_input[1] = Forecast in days
    usr_input[2] = Forecast Model
    usr_input[3] = Variables (Open or Close or...) all option
Note: all words are titled
'''

time_scale = mod_input.time_frame(usr_input[1], time_frame_base)
# start date = time_scale[0], end date = time_scale[1]

print('\nGetting stock data...\n')

main_df = mod_input.get_df(usr_input[0], time_scale[0], time_scale[1])
#Here we just have the stock data in a data frame/matrix

print('Got stock data.\nProcessing...\n')

if mod_input.min_time(main_df, usr_input[1], min_time_base) is True:
    sys.exit('Error: Forecast too far out')
    # this exists if you enter data and it cant get more than 4 times
    #   that many days in historical data

today = main_df.index.max()
#this is for error calculations due to problems in the past calling
#   dt.date.today() sometimes broke the code


forecasts = {
#dictionary of all forecasts so you can call values to make graphs

    'Randwalk' : forecast.randwalk(main_df, usr_input[1], \
        usr_input[3]),

    'Driftrandwalk' : forecast.randwalk_drift(main_df, usr_input[1], \
        usr_input[3]),

    'Georandwalk' : forecast.randwalk_geo(main_df, usr_input[1], \
        usr_input[3]),

    'Savg' : forecast.savg(main_df, usr_input[1], usr_input[3]),

    'Ses' : forecast.ses(main_df, usr_input[1], usr_input[3]),

    'Dses' : forecast.dses(main_df, usr_input[1], usr_input[3]),

    'Hles' : forecast.hles(main_df, usr_input[1], usr_input[3])
}

f_df = forecasts[usr_input[2]]
#f_df is the forecast data frame with respect to the usr_input

v_df = error.val_period(f_df, today)
#get validation data frame from forecast data frame

#gives all error values for dataframe
mae = error.mae(v_df)
avg_err = error.avg_err(v_df)
mape = error.mape(v_df)
rmse = error.rmse(v_df)

print('MAE = ' + str(mae) + '\nAverage Error = ' + str(avg_err) +\
    '\nMAPE = ' + str(mape) + '%\nRMSE = ' + str(rmse))
#Prints error names with values

plottin.b_plot(f_df, usr_input[1], usr_input[3], usr_input[0], \
    usr_input[2], today)
#makes a basic plot but doesn't show it

plt.show()
#shows the plot which was made in plottin





#see if you can put a timer on it
