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

### How to run it
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
0) Stock Abbreviation 
    ex. goog
1) Number of business days out that you want to forecast 
    ex. 20
2) Forecasting Model Abbreviation
-Options include
  - randwalk: random walk
  - driftrandwalk: drifting random walk
  - georandwalk: geometric random walk
  - savg: Simple 1 step ahead average
  - ses: simple 1 step ahead exponential smoothing
  - dses: Brown's Linear Exponential Smoothing / Double exponential smoothing
  - hles: Holt's Linear Exponential Smoothing
3) Variable \(Optional\)
-Options include
  - Open
  - High
  - Low
  - Close
  - Adj_Close
  - Volume

