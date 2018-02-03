#!/usr/bin/env python3
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib as style
import overlay
import forecast
import f_base
import plottin
import error

#plt.style.use('ggplot')

df = pd.read_csv('ea.csv', index_col=0, parse_dates=True)
#x = overlay.ema_overlay(df, 88, 'Open')
#x = forecast.sma(df, 3,'Open')


x = forecast.lin_reg(df, 5, 'Adj Close')

print(x)










    #end
