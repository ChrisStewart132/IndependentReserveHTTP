'''
crypto trading program using services provided by:
    https://www.independentreserve.com/nz/products/api#public-methods
'''

import time
import urllib, urllib.request, urllib.parse

url = "https://api.independentreserve.com"


public = url+"/Public/"


get_crypto_codes = public + "GetValidPrimaryCurrencyCodes"
get_cash_codes = public + "GetValidSecondaryCurrencyCodes"


get_valid_limit_order_types = public + "GetValidLimitOrderTypes"
get_valid_market_order_types = public + "GetValidMarketOrderTypes"
get_valid_order_types = public + "GetValidOrderTypes"
get_valid_transaction_types = public + "GetValidTransactionTypes"


'''takes a crypto_code and cash_code as input, returns info on price'''
get_market_summary = public + "GetMarketSummary"


'''takes a crypto_code and cash_code as input, returns orders for this instance'''
get_order_book = public + "GetOrderBook"
'''takes a crypto_code and cash_code as input'''
get_all_orders = public + "GetAllOrders"


'''takes a crypto_code, cash_code, and hours in past as input'''
get_trade_history_summary = public + "GetTradeHistorySummary"
'''takes a crypto_code, cash_code, and no. of trades as input'''
get_recent_trades = public + "GetRecentTrades"


'''returns data on cash conversion rates'''
get_Fx_rates = public + "GetFxRates"


'''returns minimum quantity/volume for all crypto_codes'''
get_order_minimum_volume = public + "GetOrderMinimumVolumes"


'''returns cash deposit schemes to avoid fees'''
get_cash_deposit_fees = public + "GetDepositFees"


'''returns cash withdrawl schemes to avoid fees'''
get_cash_withdrawl_fees = public + "GetFiatWithdrawalFees"


'''returns crypto withdrawl schemes to avoid fees'''
get_crypto_withdrawl_fees = public + "GetCryptoWithdrawalFees"


'''
private = url+"Private/"
key = 'api_key'
secret = 'api_secret'
nonce = int(time.time())
'''

class IndependentReserve:
    headers = None
    crypto_codes = None
    cash_codes = None
    cash_index = 2#only using index 2 from cash_codes (Nzd)
    market_summary_dict = {}
    
    def __init__(self):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0"
        self.headers = {'User-Agent': user_agent}
        self.get_crypto_codes()       
        self.get_cash_codes()
        for code in self.crypto_codes:
            self.get_market_summary(code, self.cash_codes[self.cash_index])

        '''
        self.get_valid_limit_order_types()
        self.get_valid_market_order_types()
        self.get_valid_order_types()
        self.get_valid_transaction_types()
        '''

    def timeout(self):
        time.sleep(1)#called after every api call (e.g. 1 call per second)
        
    def get_crypto_codes(self):
        post = urllib.request.Request(get_crypto_codes, None, self.headers)
        with urllib.request.urlopen(post) as response:
            the_page = response.read()
            text = the_page.decode()
            #print(text)
        data = text[1:-1].replace('"','')
        data = data.split(',')
        self.crypto_codes = data
        print(self.crypto_codes)
        self.timeout()

    def get_cash_codes(self):
        post = urllib.request.Request(get_cash_codes, None, self.headers)
        text = urllib.request.urlopen(post).read().decode()
        #print(text)
        data = text[1:-1].replace('"','')
        data = data.split(',')
        self.cash_codes = data
        print(self.cash_codes)
        self.timeout()

    def get_valid_limit_order_types(self):
        post = urllib.request.Request(get_valid_limit_order_types, None, self.headers)
        text = urllib.request.urlopen(post).read().decode()
        print(text)
        self.timeout()
    def get_valid_market_order_types(self):
        post = urllib.request.Request(get_valid_market_order_types, None, self.headers)
        text = urllib.request.urlopen(post).read().decode()
        print(text)
        self.timeout()
    def get_valid_order_types(self):
        post = urllib.request.Request(get_valid_order_types, None, self.headers)
        text = urllib.request.urlopen(post).read().decode()
        print(text)
        self.timeout()
    def get_valid_transaction_types(self):
        post = urllib.request.Request(get_valid_transaction_types, None, self.headers)
        text = urllib.request.urlopen(post).read().decode()
        print(text)
        self.timeout()

    def get_market_summary(self, crypto_code, cash_code):
        '''post is not allowed for public methods?
        values = {
            "primaryCurrencyCode": crypto_code,
            "secondaryCurrencyCode": cash_code
        }
        data = urllib.parse.urlencode(values).encode()
        post = urllib.request.Request(get_market_summary, data, self.headers)
        text = urllib.request.urlopen(post).read().decode()
        '''
        values = f"?primaryCurrencyCode={crypto_code}&secondaryCurrencyCode={cash_code}"
        post = urllib.request.Request(get_market_summary + values, None, self.headers)
        text = urllib.request.urlopen(post).read().decode()
        data = text[1:-1].replace('"','')
        data = data.split(',')
        data_dict = {}
        for pair in data:
            key = pair.split(':')[0]
            value = pair.split(':')[1]
            data_dict[key] = value
        self.market_summary_dict[crypto_code+cash_code] = data_dict
        self.print_market_summary(crypto_code, cash_code)
        self.timeout()

    def print_market_summary(self, crypto_code, cash_code):
        print('-'*40)
        print(f'{crypto_code}:', cash_code)
        for key in self.market_summary_dict[crypto_code+cash_code].keys():
            print(f'{key}:', self.market_summary_dict[crypto_code+cash_code][key])
        print('-'*40)

'''
values = {
    "name": "morpheus",
    "job": "leader"
}
data = urllib.parse.urlencode(values).encode()
post = urllib.request.Request(url, data, headers)
'''

def main():
    I = IndependentReserve()

main()
