from django.shortcuts import render, redirect
from django.contrib import messages
# imports for stocks forecasting and graph plotting
import yfinance as yf
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


# Create your views here.

# this is for the home view
def home(request):
    # request.session.flush()
    # this function is responsible for current prices
    ticker_yahoo = yf.Ticker('PSEI.PS')
    data = ticker_yahoo.history()
    last_quote = data['Close'].iloc[-1]
    prev_lastquote = data['Close'].iloc[-2]
    degree = "(" + str(round(((last_quote - prev_lastquote) / abs(last_quote)) * 100, 2)) + "%)"
    change_val = round(last_quote - prev_lastquote, 2)
    change_pct = str(round(last_quote - prev_lastquote, 2)) + degree
    context = {
        'current_price': round(last_quote, 3),
        'change_pct': change_pct,
        'change_val': change_val
    }

    return render(request, 'stockApp/home.html', context)


def update_stock(request):
    request.session.flush()
    # this accepts the form fields
    simulation_days = int(request.POST['simulation_days'])
    simulation_number = int(request.POST['simulation_number'])
    initial_investment = int(request.POST['initial_investment'])
    # initial_investment = 10000
    if simulation_days == 0 or simulation_number == 0:
        messages.error(request, f'Invalid number of Days or number of Simulation')
        return redirect('stockApp:home')
    else:
        # change this to change the data source of stock from yahoo finance
        SOURCE = 'PSEI.PS'
        stock_ticker = yf.Ticker('PSEI.PS')
        stock_company = stock_ticker.info['shortName']

        # code to get the data from yahoo finance using yfinance API, supplying the stock name, start date, and end date
        # datetime(year,month,day)
        start = dt.datetime(2021, 5, 19)
        end = dt.datetime(2022, 5, 19)
        stock_data = yf.download(SOURCE, start, end)

        # we get stock returns by comparing the percent change of current day price to the previous day price of..
        # .. adjusted close prices
        stock_returns = stock_data['Adj Close'].pct_change()
        # standard deviation of the stock returns
        daily_volatility = stock_returns.std()

        # setting of initial variables needed
        trading_days = simulation_days
        last_prices = []  # last price array
        last_price = stock_data['Adj Close'][-1]  # set initial value of the last price

        TOTAL_SIMULATIONS = simulation_number
        # df = pd.DataFrame()
        temp_frames = []
        for x in range(TOTAL_SIMULATIONS):
            counter = 0
            prices = []
            # we get the simulated price by drawing random samples from a normal distribution using numpy where..
            # .. mean =0 , standard deviation = daily_volatility, ..
            # .. and multiplying the sample with the last price on the list.
            # price = last_price * (1 + np.random.normal(0, daily_volatility))
            price = last_price
            prices.append(price)

            for y in range(trading_days):
                if counter > trading_days - 1:
                    break
                # this code also gets the simulated price using the same method but multiplies the random normal
                # distribution sample with the elements on the prices array
                price = prices[counter] * (1 + np.random.normal(0, daily_volatility))
                prices.append(price)
                counter += 1

            # df[x] = prices
            temp_frame = pd.DataFrame()
            temp_frame[x] = prices
            temp_frames.append(temp_frame)
            last_prices.append(prices[-1])
        df = pd.concat(temp_frames, axis=1)
        # this is used for setting the plot
        plt.style.use('ggplot')
        title = str(TOTAL_SIMULATIONS) + " Monte Carlo simulations of :\n" + str(stock_company) + " for " + str(
            trading_days) + " days"
        fig1, ax1 = plt.subplots()
        ax1.plot(df)
        ax1.set_title(title)
        ax1.set_ylabel("Price")
        ax1.set_xlabel("Days")

        tickers = [SOURCE]
        for ticker in tickers:
            ticker_yahoo = yf.Ticker(ticker)
            data = ticker_yahoo.history()
            last_quote = data['Close'].iloc[-1]

        current_directory = "./static/images/graph"
        filename = "forecast_graph.png"
        plt.savefig(os.path.join(current_directory, filename), dpi=300)
        # plt.show()

        investment_in_stocks = initial_investment / last_quote
        expected_price = np.mean(last_prices)
        quantile_five = np.percentile(last_prices, 5)
        quantile_ninetyfive = np.percentile(last_prices, 95)
        low_expected_returns = investment_in_stocks * quantile_five
        high_expected_returns = investment_in_stocks * quantile_ninetyfive
        expected_returns = investment_in_stocks * expected_price
        low_gains_losses = low_expected_returns - initial_investment
        high_gains_losses = high_expected_returns - initial_investment
        return_of_investment = expected_returns - initial_investment

        # this is to plot the second graph (histogram)

        fig2, ax2 = plt.subplots()
        ax2.hist(last_prices, bins=100, color='#6397ff')
        ax2.set_title("Normal Distribution Graph")
        ax2.set_ylabel("Frequency")
        ax2.set_xlabel("Price")
        plt.axvline(np.percentile(last_prices, 5), color='r', linestyle='dashed', linewidth=2)
        plt.axvline(np.percentile(last_prices, 95), color='r', linestyle='dashed', linewidth=2)
        filename = "histogram.png"
        plt.savefig(os.path.join(current_directory, filename), dpi=150)

        request.session['expected_price'] = round(expected_price, 2)
        request.session['quantile_five'] = round(quantile_five, 2)
        request.session['quantile_ninetyfive'] = round(quantile_ninetyfive, 2)
        request.session['initial_investment'] = initial_investment
        request.session['expected_returns'] = round(expected_returns, 2)
        request.session['return_of_investment'] = round(return_of_investment, 2)
        request.session['low_expected_returns'] = abs(round(low_expected_returns, 2))
        request.session['high_expected_returns'] = round(high_expected_returns, 2)
        request.session['low_gains_losses'] = abs(round(low_gains_losses, 2))
        request.session['high_gains_losses'] = round(high_gains_losses, 2)
        request.session['investment_in_stocks'] = round(investment_in_stocks, 4)
        request.session['last_qoute'] = round(last_quote, 2)
        # in this return, redirect the users to the home template
        return redirect('stockApp:home')
