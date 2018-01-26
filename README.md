# PurpSoap

### What's the point?

This was built to get stock data and pump it through forecasting models based on how far out you would like to forecast it. You don't set up parameters. These can be easily changed in the source code and I'm hoping to make that easier in the future. There is no UI, because it will run faster and defnitely not because I don't know how to program UI's. 

### Prerequsites
It's all built in python 3, so that along with the python libraries:
  * Numpy
  * Pandas
  * Datetime
  * Matplotlib
  
I included the \#!/usr/bin/env python3 as a header for everyone using linux, so make sure to pip3 those libraries instead of just using the normal pip

### How to run it /(Using only python\)

in terminal

```
cd ~/PurpSoap/lib
python3 main.py
```

When given the screen
```
Stock Data:
```

Give comma spaced values
1) Stock Abbreviation 
    - ex. goog
2) Number of business days out that you want to forecast 
    - ex. 20
3) Forecasting Model Abbreviation
    - randwalk: random walk
    - driftrandwalk: drifting random walk
    - georandwalk: geometric random walk
    - savg: Simple 1 step ahead average
    - ses: simple 1 step ahead exponential smoothing
    - dses: Brown's Linear Exponential Smoothing / Double exponential smoothing
    - hles: Holt's Linear Exponential Smoothing
4) Variable \(Optional\)
    - Open
    - High
    - Low
    - Close
    - Adj_Close = Default
    - Volume
    
Example
```
Stock Data: amzn, 260, dles
```
This returns amazons stock forecasted about 1 year ahead using Brown's Model

or type help for a help list

### Run for windows
I haven't tested this out, but I ran pyinstaller and it didn't throw an error. So its probably great!

Just open windows folder, then dist, then run main.exe and then just input with respect to the list above.
