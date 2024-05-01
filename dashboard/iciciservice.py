from breeze_connect import BreezeConnect
import urllib
import requests
import urllib.parse
from datetime import datetime, timezone, timedelta
import pytz  # You may need to install this package using pip install pytz

class iciciServiceClass:
    def __init__(self,sessionToken):
        #self.apiKey = "aT33RE8gb1)62510bO585#8B71E7774g"
        self.api_key = "aT33RE8gb1)62510bO585#8B71E7774g"
        self.api_secret = "0512c9lH4)98^75M205CI61qV(23)460"
        self.breeze = None
        self.userName = None
        self.session_token = sessionToken
        self.todayDate = None
        self.expiryDate=None
        self.tradeStrikePrice = 0
        self.callOrPutTxt = None #call put
        self.connectBreezeAPI()
        self.getCustomerDetails()
        self.placedOrder = None
        self.squaredOffOrder = None
        self.totalProfit = 0
    
    def setExpiryDate(self):
        # Get today's date
        today = datetime.utcnow()

        # Add one day to today's date
        expiry_date = today + timedelta(days=1)

        # Format the expiry date as "YYYY-MM-DDTHH:MM:SS.000Z"
        self.todayDate = today.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        self.expiryDate = expiry_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        print("Today's Date: "+self.todayDate)
        print("Expiry Date (after one day):"+ self.expiryDate)
    
    def getDataFromApi(self):
        
        self.totalProfit = self.totalProfit + self.calculate_pnl()
        return { 
                'userName' : self.userName,
                'totalProfit' : self.totalProfit,
                'currentOrder' : self.placedOrder
                }
    def connectBreezeAPI(self):
        #self.breeze = BreezeConnect(api_key=self.apiKey)
        print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus("aT33RE8gb1)62510bO585#8B71E7774g"))
        # Step 1: Get a temporary token
        #temporary_token = self.get_temporary_token()

        # Step 2: Generate a session using the temporary token
        #self.generate_session(temporary_token)
        self.breeze = BreezeConnect(api_key=self.api_key)
        self.breeze.generate_session(api_secret=self.api_secret,
                        session_token=self.session_token)
        print("session generated")
    def placeOrder(self):
        placedOrder = self.breeze.place_order(stock_code="NIFTY",
                    exchange_code="NFO",
                    product="options",
                    action="buy",
                    order_type="market",
                    stoploss="",
                    quantity="50",
                    price="",
                    validity="day",
                    validity_date= self.todayDate,#"2022-08-30T06:00:00.000Z",
                    disclosed_quantity="0",
                    expiry_date= self.expiryDate, #"2022-09-29T06:00:00.000Z",
                    right=self.callOrPutTxt,
                    strike_price=self.tradeStrikePrice)
        self.placedOrder = placedOrder
        #print(placedOrder)
    
    def squareoff(self):
            self.totalProfit = self.totalProfit + self.calculate_pnl()
            response = self.breeze.square_off(exchange_code="NFO",
                                product="options",
                                stock_code="NIFTY",
                                expiry_date="2023-07-20T06:00:00.000Z",
                                right=self.callOrPutTxt,
                                strike_price= self.tradeStrikePrice,
                                action="sell",
                                order_type="market",
                                validity="day",
                                stoploss="0",
                                quantity="50",
                                price="0",
                                validity_date=self.expiryDate,
                                trade_password="",
                                disclosed_quantity="0")
            self.squaredOffOrder = response
            
            #print(response)   
    def calculate_pnl(self):    
        pnl = 1
        response = self.breeze.get_portfolio_positions()
        if response['Status'] == 200:
            response = response['Success']
            if(response):
                for item in response:
                    ltp = float(item['ltp'])
                    cost = float(item['average_price'])
                    qty = int(item['quantity'])
                    # print((item['ltp'],item['average_price']))
                    pnl += round((ltp - cost)*qty, 2)     

        #print("P&L : "+pnl)
        return pnl
    def getCustomerDetails(self):
        details = self.breeze.get_customer_details(api_session=self.session_token)
        self.userName = details['Success']['idirect_user_name']
    def getDematHolding(self):
        self.breeze.get_demat_holdings()
