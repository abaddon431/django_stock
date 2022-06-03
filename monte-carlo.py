##################################################################
# Author: Bryan Tabares
# Description : Monte Carlo Simulation of PSEI Stock Prices using Random Walk theory
# this code assumes that the returns of the stock portfolio follows a normal distribution, this code also
# assumes that the volatility risk of the stock will not change and will remain constant
##################################################################


import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

start_time = time.time()

# change this to change the data source of stock from yahoo finance
SOURCE = 'PSEI.PS'
stock_company = 'Philippine Stock Market Index'
# stock_ticker = yf.Ticker(SOURCE)
# stock_company = stock_ticker.info['shortName']

# read csv file of Philippine Stock Exchange Index since December 1st 2011
stock_data = pd.read_csv('PSEI.PS.csv', skipinitialspace=True, usecols=['Adj Close'])

# we get stock returns by comparing the percent change of current day price to the previous day price of..
# .. adjusted close prices on the set of data
stock_returns = stock_data['Adj Close'].pct_change()
# standard deviation of the stock returns
daily_volatility = stock_returns.std()

# setting of initial variables needed
trading_days = 365
last_prices = []  # last price array
last_price = stock_data['Adj Close'].iloc[-1]  # set initial value of the last price by getting the last entry on the csv file

TOTAL_SIMULATIONS = 1000
temp_frames = []
for x in range(TOTAL_SIMULATIONS):
    counter = 0
    prices = []
    price = last_price  # set the point of origin of every graph as the latest stock value
    # price = last_price * (1 + np.random.normal(0, daily_volatility))
    prices.append(price)

    for y in range(trading_days):
        if counter > trading_days - 1:
            break
        # we get the simulated price by drawing random samples from a normal distribution using numpy where..
        # .. mean =0 , standard deviation = daily_volatility, ..
        # .. and multiplying the sample with the prices array.
        price = prices[counter] * (1 + np.random.normal(0, daily_volatility))
        prices.append(price)
        counter += 1

    # code to optimize data frame fragmentation from previous code version
    last_prices.append(prices[-1])
    temp_frame = pd.DataFrame()
    temp_frame[x] = prices
    temp_frames.append(temp_frame)
df = pd.concat(temp_frames, axis=1)

# code to get the latest stock prices
ticker_yahoo = yf.Ticker('PSEI.PS')
data = ticker_yahoo.history()
last_quote = data['Close'].iloc[-1]

plt.style.use('ggplot')  # styling
title = str(TOTAL_SIMULATIONS) + " Monte Carlo simulations of :\n" + str(stock_company) + " for " + str(trading_days) + " days"  #title
# object-oriented matplotlib charting
fig1, ax1 = plt.subplots()
ax1.plot(df)
ax1.set_title(title)
ax1.set_ylabel("Price")
ax1.set_xlabel("Days")
filename = str(TOTAL_SIMULATIONS) + "-" + str(trading_days) + ".png"
plt.axhline(y=last_quote, color='black', linestyle='-')
plt.savefig(filename, dpi=300)  # save figure with filename

expected_price = np.mean(last_prices)  # expected price of stock based on the simulation calculated using their mean(u)
quantile_five = np.percentile(last_prices, 5)  # 5% of low
quantile_ninetyfive = np.percentile(last_prices, 95)  # 5% of high



print("Current price: ", last_quote)
print("Expected price: ", expected_price)
print("Quantile (5%): ", quantile_five)
print("Quantile (95%): ", quantile_ninetyfive)

# charting of normal distribution chart
fig2, ax2 = plt.subplots()
ax2.hist(last_prices, bins=100, color='#6397ff')
ax2.set_title("Distribution")
ax2.set_ylabel("Frequency")
ax2.set_xlabel("Stock Price")
plt.axvline(quantile_five, color='r', linestyle='dashed', linewidth=2)
plt.axvline(quantile_ninetyfive, color='r', linestyle='dashed', linewidth=2)
plt.savefig("hist.png", dpi=300)
plt.show()

print("--- %s seconds ---" % (time.time() - start_time))
