#!/usr/bin/env python3
from datetime import datetime, timedelta
import pandas_datareader.data as web
import pandas as pd
import datetime as dt
import sys

'''
The point of this is to take the users input and
modify it in order to get a data frame which is will
be put through whatever Forecast Model the user specifies
these will be in the forecast_m.py document
'''

def time_stock(raw_usr_input):

    if raw_usr_input == 'help':
        welcome_message = open('help_message.txt', 'r').read()
        print(welcome_message)
        sys.exit()
        #this is the only time that the program won't work and will just
        #   give you a help menu instead

    else:
        mod_usr_info = raw_usr_input.replace(' ', '').title()
        #strips all of the spaces in the users input
        #capitalizes all letters

        all_usr_info = mod_usr_info.split(',') + [None]
        #all_usr_info is a list with elements seperated by commas.
        #Tack on 2 empty slots for defaults if user did not enter data

        all_usr_info[1] = int(all_usr_info[1])
        #sets number of busisness days to a number rather than a string


        if all_usr_info[3] is None:
            all_usr_info[3] = 'Adj Close'
        else:
            all_usr_info[3] = all_usr_info[3].replace('_', ' ').title()

        #if statements make defaults so user must only enter
        #   the first 2 csv's. Still works if user only
        #   enters a total of 3 csv's


    return all_usr_info


def time_frame(days_usr_input, base):

    last_date = dt.date.today()
    #gets todays date

    time_diff = pd.tseries.offsets.BDay(int(days_usr_input)*base)
    #24 because if you forecast a month everything beyond 2 years old
    #   seems irrelevant. It just seemed like a good average

    first_date = last_date - time_diff
    #gets (today - # of days user inputed * 24)


    time_endpoints = [first_date, last_date]

    return time_endpoints


def get_df(stock, first_date, last_date):

    try:
        data = web.get_data_yahoo(stock, first_date, last_date)
        #gives the stock data within time_endpoints

    except:
        sys.exit('Could not get data from Yahoo.')
    #this means that either you couldn't access yahoo or the stock doesn't
    #   exist


    raw_df = pd.DataFrame(data)
    #gives a data frame which is easy to work with in pandas

    return raw_df
    #if uncommented will make a CSV file
    #makes data into CSV and puts it in the PurpBrass directory


def min_time(df, days_usr_input, base):
    today = dt.date.today()
    minimum = pd.tseries.offsets.BDay(int(days_usr_input)*base)
    hyp_smallest = today - minimum
    #minimum length of time required to get a reliable forecast
    #   is 4 times the size of the forecast length

    smallest = df.index.min()
    #smallest index value

    if hyp_smallest < smallest:
        x = True
        #if you can't get more than 4 times the length of the
        #   forecast period for data analysis DO NOT RUN
    else:
        x = False

    return x
