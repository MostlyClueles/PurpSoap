#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib as style
import datetime as dt



def b_plot(df, f_len, var, stock, f_abb, today):
    #basic plot
    del df['Valid'] #remove this after you make code pretty

    plt.style.use('ggplot')
    #ggplot mimics the plotting in R. Other options can be found with
    #   the command: print(plt.style.available)

    plt.plot(df)

    #add titles and labels before plt.show()
    plt.xlabel('Dates')
    plt.ylabel(var + ' ($)')

    plt.title(stock + '\'s ' + f_abb + ' forecast over ' + str(f_len) +\
        ' business days' + '\n' + str(today))
    #Ex: GOOG's ARIMA forecast over 18 business days
    #                 Year-Month-Date

    #Must have plt.show() after using this function

#maybe change to just a function later if it works better?
