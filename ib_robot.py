
import os
import numpy as np
import pandas as pd
from credentials.config import USERNAME, PASSWORD
from ibw.client import IBClient

from ib.cp.client import


class IBTradingRobot():

     """
        The Trading Robot Class object, this object will initalize a session with Interactive Broker,
        make any requests with the API, handle indicator calculation, and provide signals for trading.

        ATTRIBUTES:
            RSI_BUY_THRESHOLD: The RSI level needed to signal a buy.
            RSI_SELL_THRESHOLD: The RSI level needed to signal a signal.
            RSI_DAYS: The number of days the RSI looks back on.

            EMA_LONG: The period for the long run EMA.
            EMA_SHORT: The period for the short run EMA.
            EMA_MACD: The period for the MACD short run EMA.

    """


    def __init__(self, username = None, password = None, symbols = None):

        # define the RSI constants
        self.RSI_BUY_THRESHOLD = 30
        self.RSI_SELL_THRESHOLD = 60
        self.RSI_DAYS = 14

        # define the EMA constants
        self.EMA_LONG = 26
        self.EMA_SHORT = 12
        self.EMA_MACD = 9

        # Store components for authentication
        self.USERNAME = username
        self.PASSWORD = password

        # Store the symbols to be traded
        self.symbols = symbols

        # define a place holder for our current TD session
        self.session = self._create_session()

        # define the directory where will save files and load data from
        self.directory = os.path.join(os.getcwd(), 'ibw')


        self.ALPHA_URL = r'https://www.alphavantage.co/query'
        self.ALPHA_VANTAGE_APIKEY = None


    def _create_session(self):
        '''
            Creates a new session with Interactive Broker using the credentials
            passed through when the Robot was initalized.
            
            NAME: account_number
            DESC: The user's account number they use to login with the TD API.
            TYPE: String

            NAME: account_password
            DESC: The user's account password they use to login with the TD API.
            TYPE: String

            NAME: consumer_id
            DESC: The consumer ID created when a new app is registered with the TD Ameritrade API.
            TYPE: String

            NAME: redirect_uri
            DESC: The redirect URL the user specified during app registration.
            TYPE: String
        '''

        # Initalize the web client
        ib_client = IBWebClient(username = self.USERNAME, password = self.PASSWORD)
        
        # connect
        ib_client.connect()

        # check if authenticated.
        if ib_client.is_authenticated():
            self.session = ib_client
        else:
            print('Session is connected but not authenticated, requests will be limited.')
            self.session = ib_client


    def _grab_accounts(self):
        pass

    def _update_account(self):
        pass

    def _grab_portfolio_positions(self):
        pass


    def _historical_prices(self, api = 'interactive_broker'):
        '''
            Grabs the historical prices for each symbol, if possible, in the `symbols` list. The user
            can also specify which service they want to recieve quotes from, either Interactive Broker
            or Alpha Vantage.

            NAME: api
            DESC: Specifies which API service to pull historical data from.
                  Possible options are 'interactive-broker' or 'alpha-vantage'
            TYPE: String

        '''

        if api == 'interactive-broker':
                        
            # make a request for the data.
            price_data = self._ib_historical

        elif api == 'alpha-vantage'

            # make a request for the data.
            symbol = 'MSFT'
            function = 'TIME_SERIES_INTRADAY'
            price_data = self._alpha_historical(interval = '1min', symbol = symbol, function = function)

        else:
            RaiseValueError('The API Service you selected is incorrect please choose either `interactive-broker` or `alpha-vantage`')


    def _alpha_historical(self, interval = None, symbol = None, function = None):
        '''
            Makes a request to the ALPHA VANTAGE API for historical price data.
        '''

        # define the parameters of the request
        params = {'function':function,
                  'symbol':symbol,
                  'interval':interval,
                  'outputsize':'full',
                  'output':'json',
                  'apikey':ALPHA_VANTAGE_APIKEY}

        # make the request.
        response = requests.get(url = self.ALPHA_URL, params = params, verify = True)

        # if everything is good, then return the JSON content.
        if response.status_code == 200:
            return response.json()
        else:
            raise requests.RequestException
            print('There was an issue with the ALPHA VANTAGE API during the request.')

    def _ib_historical(self, symbol = symbol, period = period, bar = bar):
        price_data = self.session.market_data_history(conid = symbol, period = period, bar = bar)
        return price_data


    def _create_price_df(self, price_data = None):
        
        # initalize list to store all candle data
        all_prices = []

        # grab just the candles, and add them to the list.
        for candle in price_data['candles']:
            candle['symbol'] = price_history['symbol']
            all_prices.append(candle)
        
        # store all the prices
        self.prices_df = pd.DataFrame(all_prices)

        # sort the dataframe
        self.prices_df.sort_values(by = ['symbol','datetime'], inplace = True)

    def change_in_price(self):
        # calculate the change in price
        self.prices_df['change_in_price'] = self.prices_df.groupby('symbol')['close'].transform(lambda x: x.diff())

    def macd(self):
        self.prices_df['ema_26'] = self.prices_df.groupby('symbol')['close'].transform(lambda x: x.ewm(span=self.EMA_26).mean())
        self.prices_df['ema_12'] = self.prices_df.groupby('symbol')['close'].transform(lambda x: x.ewm(span=self.EMA_12).mean())
        self.prices_df['macd'] = self.prices_df['ema_12'] - self.prices_df['ema_26']

         self.prices_df['macd_ema'] = self.prices_df['macd'].ewm(span = self.EMA_MACD).mean()
    
    def rsi(self):

        # first calculate the change in price
        self.change_in_price()

        # For up days, if the change is less than 0 set to 0.
        self.prices_df['up_day'] = self.prices_df.loc[(self.prices_df['change_in_price'] < 0), 'change_in_price'] = 0

        # For down days, if the change is greater than 0 set to 0.
        self.prices_df['down_day'] = down_df.loc[(down_df['change_in_price'] > 0), 'change_in_price'] = 0

        # We need change in price to be absolute.
        self.prices_df['down_day'] = self.prices_df['down_day'].abs()

        # calculate the EMA of the UP days and EMA of the DOWN days.
        ewma_up = self.prices_df.groupby('symbol')['up_day'].transform(lambda x: x.ewm(span=self.RSI_DAYS).mean())
        ewma_down = self.prices_df.groupby('symbol')['down_day'].transform(lambda x: x.ewm(span=self.RSI_DAYS).mean())

        # calculate the relative strength column
        self.prices_df['relative_strength'] = ewma_up / ewma_down

        # finally calculatet the Relative Strength Index.
        self.prices_df['rsi'] = 100.0 - (100.0 / (1.0 + self.prices_df['relative_strength']))

    def _add_signal_flags(self):

        rsi_sell_mask = self.prices_df['rsi'] >= self.RSI_SELL_THRESHOLD
        rsi_buy_mask = self.prices_df['rsi'] <= self.RSI_BUY_THRESHOLD

        self.prices_df['macd_signal'] = self.prices_df['macd_signal'] > self.prices_df['macd']
        self.prices_df['rsi_signal'] = np.where(rsi_sell_mask, 'rsi_sell', 
                                       np.where(rsi_buy_mask, 'rsi_buy', 
                                       'rsi_no_signal'))
        
        self.prices_df['in_portfolio'] = True
        self.prices_df['is_profitable'] = True

    def determine_signal(self):

        # grab the last row for each symbol
        symbol_groups = self.prices_df.groupby('symbol').tail(1)

        # store them in a new dataframe
        last_row_df = pd.concat(last_value)

        # define sell conditions
        flag_profit_sell = last_row_df['is_profitable'] == True
        flag_rsi_sell = last_row_df['rsi_signal'] == 'rsi_sell'
        flag_macd_sell= last_row_df['macd_signal'] == False
        flag_portfolio_sell = last_row_df['in_portfolio'] == True

        # define buy conditions
        flag_profit_buy = last_row_df['is_profitable'] == False
        flag_rsi_buy = last_row_df['rsi_signal'] == 'rsi_buy'
        flag_macd_buy = last_row_df['macd_signal'] == True
        flag_portfolio_buy = last_row_df['in_portfolio'] == False

        # build the flags
        sell_flag = (flag_profit_sell & flag_rsi_sell & flag_macd_sell & flag_portfolio_sell)
        buy_flag = (flag_profit_buy & flag_rsi_buy & flag_macd_buy & flag_portfolio_buy)

        # specify the conditions and options
        conditions = [sell_flag, buy_flag]
        options = ['SELL','BUY']

        # build the signal row
        last_row_df['signal'] = np.select(condlist = conditions, choicelist = options, default = 'NO SIGNAL')

    def place_orders(self, signals_df = None):

        buy_orders = signals_df['BUY'] == True
        sell_orders = signals_df['SELL'] == True

        for buy_order in buy_orders:
            pass

        for sell_order in sell_orders:
            pass


        orders_payload = {"acctId": "string",
                          "conid": conid,
                          "secType": conid + ':' + secType,
                          "cOID": order_id_generated,
                          "parentId": "string",
                          "orderType": "LMT",
                          "listingExchange": "SMART",
                          "outsideRTH":True,
                          "price":price,
                          "side":"BUY",
                          "referrer":"IB_ROBOT",
                          "ticker":symbol,
                          "tif":"GTC",
                          "quantity":quantity,
                          "useAdaptive":True}


    def grab_current_price(self, symbol = None):
        '''
            Use's the Get Quotes endpoint to return the current quote for a given symbol.

            NAME: symbol
            DESC: A list of ticker symbols that you wish to recieve quotes for.
            TYPE: List<Strings>

            bid, ask, last, change, change pct, close, listing exchange

            RTYPE: Dict            
        '''

        # initalize list of prices
        price_list = []

        # make the request
        quote_data = self.session.get_quotes(instruments = symbol)

        # grab current prices
        current_prices = [[key, quote_data[key]['lastPrice'], quote_data[key]['quoteTimeInLong'], 
                           quote_data[key]['bidPrice'], quote_data[key]['askPrice']] for key in quote_data.keys()]
        
        # create a new data frame that will house the new quotes.
        new_prices_df = pd.DataFrame(data = current_prices)

        # add the new rows and then sort again.
        self.prices_df.append(new_prices_df).sort_values(by = ['symbol','datetime'], inplace = True)    

        return current_prices
       

    def _is_market_open(self):
        '''
            Converts the Local time zone into UTC time so that way everything is consistent, regardless of where you live.
            Then determines if market is opened and returns the necessary information to active the script.
        '''

        # define the different timezones and market hour info.
        self.local_timezone = tz.tzlocal()
        self.local_timezone_markets = tz.tzutc()
        self.market_daysISO_open = [1, 2, 3, 4, 5]
        self.market_daysISO_close = [6, 7]
        self. market_open_time = time(hour = 14, minute = 30, second = 0, tzinfo = timezone.utc)
        self. market_close_time = time(hour = 21, minute = 00, second = 0, tzinfo = timezone.utc)

        # get the current datetime
        now = datetime.now().astimezone(timezone.utc)

        # grab today's date
        today = now.date()

        # grab the current time
        current_time = now.timetz()

        # determine if the market is open.
        if today.isoweekday() not in self.market_daysISO_close and (current_time > self.market_open_time and current_time < self.market_close_time):
            market_is_open = True
        else:
            market_is_open = False

        # if we aren't in testing mode, then send the real flag back
        if extended_hours == False:
            return market_is_open, self.market_close_time, now
        else:
            return True, self.market_close_time.replace(hour = 23), now






    def get_symbols(self):
        '''
            Loads all the information necessary to stream quotes, calculate order sizes, and determine signals.
            Stores it in a list.

            RTYPE: List<Tuple(String, Integer, Integer, Float)>
        '''

        # define the file location
        file_path = os.path.join(self.directory, 'symbols_list.csv')

        # open the CSV file and read the data, skip the header, and append to list.
        with open(file_path, newline = '') as symbol_file:
            
            # define the reader, and skip the header.
            symbol_reader = csv.reader(symbol_file, delimiter=',')            
            next(symbol_reader, None)

            # store the data in a list.
            symbols_data = list(symbol_reader)

        return symbols_data


    def parse_candle_data(self, candle_data = None):
        '''
            Takes the Dictionary object returned by the get price history endpoint,
            and keeps on selected values.

            NAME: candle_price_data
            DESC: A dictionary of price data over a specified range of time.
            TYPE: Dictionary

            RTYPE: List<List<String, Integer, Float>>

        '''

        # parse the candle if they arent empty
        if candle_data['Time Series (1min)']:
            closing_prices = [((candle_data['Meta Data']['2. Symbol']), 
                              int(datetime.fromisoformat(date_time).timestamp()), 
                              float(candle_data['Time Series (1min)'][date_time]['4. close'])) for date_time in candle_data['Time Series (1min)']]

        # we will convert it to a numpy array, specify the data types.
        dt = np.dtype('object, i8, f4')

        # convert it into an array
        closing_prices = np.array(closing_prices, dtype=dt)

        # specify the fields.
        closing_prices.dtype.names = ['symbol', 'datetime', 'close']

        return closing_prices


    def dump_price_data(self, price_data = None):
        '''
            Dumps the parsed data into a CSV file for further processing.

            NAME: historical_price_data
            DESC: A list of lists that contains three elements a Ticker Symbol, a timestamp, and the closing price
            TYPE: List<List<String, Integer, Float>>
        '''

        # define the list of hold symbols, and grab the current directory.
        file_path = os.path.join(self.directory, 'price_data.csv')

        # open the CSV file and read the data, skip the header, and append to list.
        with open(file_path, mode = 'a', newline = '') as price_file:
            price_writer = csv.writer(price_file, quoting=csv.QUOTE_ALL)
            price_writer.writerows(price_data)           



    def grab_historical_prices(self, ticker_symbol = None):
        '''
            Use's the Alpha Vantage API to get historical Intrday prices before the market opens,
            and anytime the script is started during market hours.

            NAME: ticker_symbol
            DESC: A single ticker symbols that you wish to recieve historical price data for.
            TYPE: Strings

        '''

        # define the URL
        url = r'https://www.alphavantage.co/query?'

        # define the parameters of the request
        params = {'function':'TIME_SERIES_INTRADAY',
                  'symbol':ticker_symbol,
                  'interval':'1min',
                  'outputsize':'full',
                  'output':'json',
                  'apikey':ALPHA_VANTAGE_APIKEY}

        # grab the response
        response = requests.get(url, params = params, verify = True)

        # if everything is good, then return the JSON content.
        if response.status_code == 200:
            return response.json()
        else:
            raise requests.RequestException



    def instrument_check(self, ticker_symbol = None):
        '''
            Determines if a given financial instrument exists in any of the individuals accounts.

            NAME: symbol
            DESC: A single symbol to search for.
            TYPE: String

            RTYPE: Boolean            
        '''

        # grab all the account data.
        accounts = self.session.get_accounts(account = 'all', fields = 'positions')

        position_exists = False
        purchase_price = 0

        # see if the instrument is a position in any of our accounts.
        for account in accounts:

            if 'positions' in account['securitiesAccount'].keys():
                for position in account['securitiesAccount']['positions']:

                    if ticker_symbol == position['instrument']['symbol']:
                        position_exists = True
                        purchase_price = position['averagePrice']


        # return the results of the search
        return position_exists, purchase_price


    def determine_signal_flag(self, ticker_symbol = None, prices = None, instrument_flag = None,  
                              macds = None, previous_ema_26 = None, previous_ema_12 = None, previous_avg_down = None,
                              previous_avg_up = None, profit_margin = None, purchase_price = None, bid_price = None):
        '''
            Using the RSI & MACD indicator, determines if the instrument signals a BUY or SELL flag.
            The RSI checks for a signal and the MACD indicator confirms the RSI signal. An additional
            condition is applied that requires either the position to exisit in the portfolio (SELL) or
            the position to not exist in the portfolio (BUY).

            NAME: symbol
            DESC: The symbol to check for in any of the accounts.
            TYPE: String

            NAME: prices
            DESC: The current trading price of the instrument.
            TYPE: Float

            NAME: instrument_flag
            DESC: The flag that specifies whether the instrument is in the portfolio (True) or
                  not in the portfolio (False)
            TYPE: Boolean

            NAME: macds
            DESC: List of historical MACDS.
            TYPE: List<Floats>

            NAME: previous_ema_26, pervious_ema_12
            DESC: The previous EMA's calculated for the both 12 and 26 periods.
            TYPE: Float

            NAME: profit_margin
            DESC: Required profit percentage to sell the stock.
            TYPE: Float

            NAME: purchase_price
            DESC: The price the instrument was purchased at.
            TYPE: Float

            RTYPE: Tuple            
        '''

        # define current price
        current_price = prices[-1]
        previous_price = prices[-2]

        # calculate the RSI, using the weights
        current_rsi, average_up, average_down = self.calculate_rsi(previous_rsi = True, average_down = previous_avg_down, average_up = previous_avg_up, 
                                                                   current_price = current_price, previous_price = previous_price)

        # calculate the specified indicators
        macd_parts = self.calculate_macd(price_data = prices, previous_ema_26 = previous_ema_26, previous_ema_12 = previous_ema_12)

        # grab the parts for storage in the main script        
        current_ema_26 = macd_parts[0]
        current_ema_12 = macd_parts[1]
        current_macd = macd_parts[2]

        current_macd_ema = self.calculate_ema(np.append(macds, current_macd), n = self.EMA_MACD)
        
        # determine if the RSI is Signaling a buy or sell
        if current_rsi <= self.RSI_BUY_THRESHOLD:
            rsi_signal = True
        elif current_rsi >= self.RSI_SELL_THRESHOLD:
            rsi_signal = False
        else:
            rsi_signal = None

        # determine if the MACD is confirming a buy or sell
        if current_macd_ema > current_macd:
            macd_signal = True
        elif current_macd_ema < current_macd:
            macd_signal = False

        # if a purchase price was provided, is means we need to check for a sell signal by calculating the profit.
        if purchase_price != 0:
            
            # calculate the current profit margin
            current_profit_margin = current_price / purchase_price

            # profit margin to confirm sell
            if profit_margin < current_profit_margin:
                profit_signal = True

        # For testing
        if TESTING_FLAG == True:
            profit_signal = True
        
        # add the cost signal
        if bid_price >= purchase_price:
            cost_signal = True
        else:
            cost_signal = False

        # if the RSI signals a buy, the MACD confirms it, and we don't own the instrument then provide a BUY signal.
        if rsi_signal == True and macd_signal == True and instrument_flag == False:
            return {'signal':'BUY', 'ticker':ticker_symbol, 'current_RSI':current_rsi, 
                    'current_MACD':current_macd, 'current_MACD_EMA_9':current_macd_ema, 'current_EMA_26':current_ema_26,
                    'current_EMA_12':current_ema_12, 'current_avg_up': average_up, 'current_avg_down':average_down}

        # if the RSI signals a SELL, the MACD confirms it, and we do own the instrument then provide a SELL signal.
        elif rsi_signal == False and macd_signal == False and instrument_flag == True and cost_signal == True and profit_signal == True:
            return {'signal':'SELL', 'ticker':ticker_symbol, 'current_RSI':current_rsi, 
                    'current_MACD':current_macd, 'current_MACD_EMA_9':current_macd_ema, 'current_EMA_26':current_ema_26,
                    'current_EMA_12':current_ema_12, 'current_avg_up': average_up, 'current_avg_down':average_down}
        
        else:# if the RSI provides no signal, then no flag needs to be provided.
            return {'signal':'NO SIGNAL', 'ticker':ticker_symbol, 'current_RSI':current_rsi, 
                    'current_MACD':current_macd, 'current_MACD_EMA_9':current_macd_ema, 'current_EMA_26':current_ema_26,
                    'current_EMA_12':current_ema_12, 'current_avg_up': average_up, 'current_avg_down':average_down}

    def place_order(self, ticker_symbol = None, price = None, quantity = None, total_capital = None, purchase_type = None):
        '''
            Places an order if a buy or sell signal was given. The order will be a limit order that will be active
            till canceled and will go into extended market hours. Defaults to quantity.

            NAME: symbol
            DESC: The symbol that will be purchased or sold.
            TYPE: String

            NAME: price
            DESC: The price at which to buy or sell the security. For purchases, the price will be the latest
                bid price. For sales, the price will be the latest ask price.
            TYPE: Float

            NAME: quantity
            DESC: The number of shares to purchase.
            TYPE: Integer

            NAME: total_capital
            DESC: The amount of capital allowed to be used to purchase the stock. It will be used to calculate
                the quantity purchased.
            TYPE: Float 

            NAME: purchase_type
            DESC: Specifies whether the order is a sell or buy order.
            TYPE: Float              
        '''

        # define duration of the order
        DURATION_TYPE = 'GOOD_TILL_CANCEL'

        # define the session, in this case keep it open after hours.
        SESSION_TYPE = 'SEAMLESS'

        # define order type
        ORDER_TYPE = 'LIMIT'

        # if quantity is provided default to that, otherwise calculate the quantity to purchase.
        if purchase_type == 'buy':

            # build the order request
            order = {"orderType": ORDER_TYPE,
                    "session": SESSION_TYPE,
                    "duration":  DURATION_TYPE,
                    "orderStrategyType": "SINGLE",
                    "price": price,
                    "orderLegCollection": [{
                        "instruction": "BUY",
                        "quantity": quantity,
                        "instrument": {
                            "symbol": ticker_symbol,
                            "assetType": "EQUITY"
                    }}]}

        elif purchase_type == 'sell':

            # build the order request
            order = {"orderType": ORDER_TYPE,
                    "session": SESSION_TYPE,
                    "duration":  DURATION_TYPE,
                    "orderStrategyType": "SINGLE",
                    "price": price,
                    "orderLegCollection": [{
                        "instruction": "SELL",
                        "quantity": quantity,
                        "instrument": {
                            "symbol": ticker_symbol,
                            "assetType": "EQUITY"
                    }}]}

        #place the order
        if TESTING_FLAG == True:
            print('ORDER GENERATED')
            pprint.pprint(order)
        else:
            print('ORDER GENERATED:')
            pprint.pprint(order)
            print(self.session.place_order(account = ACCOUNT_NUMBER, order = order))


if __name__ == '__main__':
    
    # delete the old historical data before running the script.
    if os.path.exists(r'td_robot\price_data.csv'):
        os.remove(r'td_robot\price_data.csv')

    if os.path.exists(r'td_robot\signals.csv'):
        os.remove(r'td_robot\signals.csv')

    # create a new instance of the robot.
    trading_rob = TradingRobot()

    # create a session
    trading_rob.create_td_session()

    # get the symbols
    trading_data = trading_rob.get_symbols()

    # define portfolio dict
    indicator_dict = {}

    # get the file path
    file_path_signal = os.path.join(trading_rob.directory, 'signals.csv')

    # grab the ticker symnbols and capital amounts
    for row in trading_data:

        # grab the components
        ticker_symbol, capital, quantity, profit_margin = row[0], float(row[1]), int(row[2]), float(row[3])

        # grab the historical data
        price_data_hist = trading_rob.grab_historical_prices(ticker_symbol = ticker_symbol)

        # check if a particular symbol exists in any of the portfolios, and add it to indicator dictionary
        position_flag, purchase_price = trading_rob.instrument_check(ticker_symbol = ticker_symbol)

        # parse the candles and sort them
        parsed_prices = trading_rob.parse_candle_data(price_data_hist)
        parsed_prices.sort(order = 'datetime')

        # grab prices only
        all_price = parsed_prices['close']
     
        # calcualte the EMA
        indicator_dict[ticker_symbol] = {}

        # initalize a list to store all the historical MACDs
        historical_macd = []

        # determine the size of the list
        price_size = len(all_price)

        # we need to calculate historical indicators, so specify how many periods we need to look back.
        day_start_26 = 26 * 2
        price_data_temp = all_price[-day_start_26:]

        # calculate the indicators, they'll be used for additional indicators.
        pre_ema_12 = trading_rob.calculate_ema(price_data = price_data_temp, n = trading_rob.EMA_SHORT)
        pre_ema_26 = trading_rob.calculate_ema(price_data = price_data_temp, n = trading_rob.EMA_LONG)
        pre_macd = pre_ema_12 - pre_ema_26
        historical_macd = np.array(pre_macd)

        # we need historical MACD indicators to calculate the EMA of the MACD.
        for i in all_price[-26:]:
            pre_ema_12 = trading_rob.calculate_ema(price_data = [i], n = trading_rob.EMA_SHORT, previous_ema=pre_ema_12)
            pre_ema_26 = trading_rob.calculate_ema(price_data = [i], n = trading_rob.EMA_LONG, previous_ema=pre_ema_26)
            pre_macd = pre_ema_12 - pre_ema_26
            historical_macd = np.append(historical_macd, pre_macd)

        # store all calculated values
        indicator_dict[ticker_symbol]['historical_prices'] = all_price
        indicator_dict[ticker_symbol]['intraday_prices'] = []

        current_rsi, current_avg_up, current_avg_down = trading_rob.calculate_rsi(price_data = all_price[-trading_rob.RSI_DAYS:])
        indicator_dict[ticker_symbol]['previous_rsi'] = current_rsi
        indicator_dict[ticker_symbol]['previous_avg_up'] = current_avg_up
        indicator_dict[ticker_symbol]['previous_avg_down'] = current_avg_down

        indicator_dict[ticker_symbol]['previous_ema_26'] = trading_rob.calculate_ema(price_data = all_price, n = trading_rob.EMA_LONG)
        indicator_dict[ticker_symbol]['previous_ema_12'] = trading_rob.calculate_ema(price_data = all_price, n = trading_rob.EMA_SHORT)
        indicator_dict[ticker_symbol]['previous_macd'] =  indicator_dict[ticker_symbol]['previous_ema_12'] - indicator_dict[ticker_symbol]['previous_ema_26'] 
        indicator_dict[ticker_symbol]['previous_ema_macd'] = trading_rob.calculate_ema(price_data = historical_macd, n = trading_rob.EMA_MACD)
        indicator_dict[ticker_symbol]['historical_macd'] = historical_macd

        indicator_dict[ticker_symbol]['in_portfolio'] = position_flag
        indicator_dict[ticker_symbol]['purchase_price'] = purchase_price
        indicator_dict[ticker_symbol]['quantity_to_purchase'] = quantity
        indicator_dict[ticker_symbol]['capital'] = capital
        indicator_dict[ticker_symbol]['profit_margin'] = profit_margin

        # dump the data
        trading_rob.dump_price_data(parsed_prices)  

    # grab components for market operation hours
    market_open_flag, market_closing_time, right_now = trading_rob.handle_timezones(extended_hours = True)

    i = 1

    # keep going as long as the markets aren't close
    while market_open_flag == True and (market_closing_time > right_now.timetz()):

        # situations arise where a request was unsuccessful, but the data still has to be collected.
        # create a loop that will keep trying every 10 seconds until data is collected.
        current_prices = None
        while current_prices is None:
            try:
                current_prices = trading_rob.grab_current_price(ticker_symbol=list(indicator_dict.keys()))
            except:
                print('Failed Request, pausing 10 seconds then trying again.')
                t.sleep(10)
                pass

        # loop through each quote
        for price in current_prices:
            
            # grab the quote info
            ticker_symbol = price[0]
            current_price = price[1]
            quote_time = price[2]
            bid_price = price[3]
            ask_price = price[4]

            # grab the historical info
            prices = indicator_dict[ticker_symbol]['historical_prices']
            macds = indicator_dict[ticker_symbol]['historical_macd']
            instrument_flag = indicator_dict[ticker_symbol]['in_portfolio']
            previous_ema_12 = indicator_dict[ticker_symbol]['previous_ema_12']
            previous_ema_26 = indicator_dict[ticker_symbol]['previous_ema_26']

            profit_margin = indicator_dict[ticker_symbol]['profit_margin']
            purchase_price = indicator_dict[ticker_symbol]['purchase_price']
            quantity = indicator_dict[ticker_symbol]['quantity_to_purchase']

            previous_avg_up = indicator_dict[ticker_symbol]['previous_avg_up']
            previous_avg_down = indicator_dict[ticker_symbol]['previous_avg_down']
                 
            # check for a signal
            signal_flag = trading_rob.determine_signal_flag(ticker_symbol = ticker_symbol,
                                                            prices = np.append(prices, current_price), 
                                                            instrument_flag = instrument_flag,
                                                            macds = macds,
                                                            previous_avg_down = previous_avg_down,
                                                            previous_avg_up = previous_avg_up,
                                                            previous_ema_12= previous_ema_12,
                                                            previous_ema_26= previous_ema_26,
                                                            purchase_price=purchase_price,
                                                            profit_margin=profit_margin,
                                                            bid_price=bid_price)

            # add the current price, bid price, ask price, and timestamp
            signal_flag['current_price'] = current_price
            signal_flag['bid_price'] = bid_price
            signal_flag['ask_price'] = ask_price
            signal_flag['timestamp'] = quote_time            

            # grab the signal parts
            current_signal = signal_flag['signal']

            current_rsi = signal_flag['current_RSI']
            current_avg_up = signal_flag['current_avg_up']
            current_avg_down = signal_flag['current_avg_down']

            current_macd = signal_flag['current_MACD']
            current_macd_ema = signal_flag['current_MACD_EMA_9']
            current_ema_26 = signal_flag['current_EMA_26']
            current_ema_12 = signal_flag['current_EMA_12']

            quantity = indicator_dict[ticker_symbol]['quantity_to_purchase']
            profit_margin = indicator_dict[ticker_symbol]['profit_margin']
            capital = indicator_dict[ticker_symbol]['capital']

            # based on the signal make a trade
            if current_signal == 'BUY':
                
                # place the order
                trading_rob.place_order(ticker_symbol = ticker_symbol, price = ask_price, quantity = quantity, purchase_type = 'buy')

                # if a trade was made it is now in the portfolio.
                indicator_dict[ticker_symbol]['in_portfolio'] = True

                # it also has a purchase price equal to the ASK price.
                indicator_dict[ticker_symbol]['purchase_price'] = ask_price

                print('Purchased {}'.format(ticker_symbol))

            elif current_signal == 'SELL':

                # place the order
                trading_rob.place_order(ticker_symbol = ticker_symbol, price = bid_price, quantity = quantity, purchase_type = 'sell')

                # if a trade was made, then it's no longer in the portfolio.
                indicator_dict[ticker_symbol]['in_portfolio'] = False

                # it also will reset it's purchase price to 0
                indicator_dict[ticker_symbol]['purchase_price'] = 0

                print('Sold {}'.format(ticker_symbol))

            # Add the purchase price and portfolio Flag
            signal_flag['purchase_price'] = indicator_dict[ticker_symbol]['purchase_price']
            signal_flag['portfolio_status'] = indicator_dict[ticker_symbol]['in_portfolio']

            # open the CSV file and read the data, skip the header, and append to list.
            with open(file_path_signal, mode = 'a', newline = '') as signal_file:
                signal_writer = csv.DictWriter(signal_file, fieldnames = list(signal_flag.keys()))

                # first loop write header
                if i == 1:
                    signal_writer.writeheader()
                    i = 2

                signal_writer.writerow(signal_flag)

            # Update the previous values so they are the current values.
            indicator_dict[ticker_symbol]['historical_prices'] = np.append(indicator_dict[ticker_symbol]['historical_prices'][1:], current_price)
            indicator_dict[ticker_symbol]['historical_macd'] = np.append(indicator_dict[ticker_symbol]['historical_macd'][1:], current_macd)  
            indicator_dict[ticker_symbol]['previous_ema_12'] = current_ema_12
            indicator_dict[ticker_symbol]['previous_ema_26'] = current_ema_26
            indicator_dict[ticker_symbol]['previous_ema_macd'] = current_macd_ema
            indicator_dict[ticker_symbol]['previous_rsi'] = current_rsi
            indicator_dict[ticker_symbol]['previous_avg_up'] = current_avg_up
            indicator_dict[ticker_symbol]['previous_avg_down'] = current_avg_down

            # display info to User
            print('DATA FOR {}:'.format(ticker_symbol))
            print('-'*20)
            print('\tCURRENT PRICE: {}\n\tBID PRICE: {}\n\tASK PRICE: {}'.format(current_price, bid_price, ask_price))
            print('\tSIGNAL: {}'.format(signal_flag['signal']))
            print('\tIN PORTFOLIO: {}'.format(indicator_dict[ticker_symbol]['in_portfolio']))
            print('\tPURCHASE PRICE: {}'.format(indicator_dict[ticker_symbol]['purchase_price']))
            print('\tRSI: {0:.2f}'.format(current_rsi))
            print('\tEMA 26: {0:.2f}'.format(current_ema_26))
            print('\tEMA 12: {0:.2f}'.format(current_ema_12))
            print('\tMACD: {0:.4f}'.format(current_macd))
            print('\tMACD EMA 9: {0:.4f}'.format(current_macd_ema))
            print('\n')

        # pause till the next request
        t.sleep(60)

        # update the time
        right_now = datetime.now().astimezone(timezone.utc)


