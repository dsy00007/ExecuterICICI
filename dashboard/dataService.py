import json
import pandas as pd
from datetime import datetime, timedelta
from breeze_connect import BreezeConnect


class HistoricalDataCollector:

    def __init__(self,
                 stock_code,
                 exchange_code,
                 product_type,
                 session_token,
                 right=None,
                 strike_price=None):
        self.stock_code = stock_code
        self.exchange_code = exchange_code
        self.product_type = product_type
        self.right = right
        self.strike_price = strike_price
        self.session_token = session_token
        self.breeze = self.login()

    def login(self):
        # Initialize SDK
        breeze = BreezeConnect(api_key="aT33RE8gb1)62510bO585#8B71E7774g")

        # Obtain your session key from https://api.icicidirect.com/apiuser/login?api_key=YOUR_API_KEYaT33RE8gb1)62510bO585#8B71E7774g
        # Incase your api-key has special characters(like +,=,!) then encode the api key before using in the url as shown below.
        import urllib
        print("https://api.icicidirect.com/apiuser/login?api_key=" +
              urllib.parse.quote_plus("aT33RE8gb1)62510bO585#8B71E7774g"))

        # Generate Session
        breeze.generate_session(api_secret="0512c9lH4)98^75M205CI61qV(23)460",
                                session_token=self.session_token)
        print('logged in')
        return breeze

    def _get_default_dates(self, current_date):
        # Set the time to 8 AM
        start_date = datetime(current_date.year, current_date.month,
                              current_date.day, 9, 0, 0)
        # Set the time to 4 PM
        end_date = datetime(current_date.year, current_date.month,
                            current_date.day, 16, 0, 0)

        # Find the upcoming Thursday
        expiry_date = self._get_expiry_date(start_date)
        return start_date, end_date, expiry_date

    def _get_expiry_date(self, current_date):
        # Calculate the upcoming Thursday or use the current date if it's Thursday
        days_until_thursday = (3 - current_date.weekday() + 7) % 7
        expiry_date = current_date + timedelta(days=days_until_thursday)
        return expiry_date

    def _format_date(self, date):
        return date.strftime('%Y-%m-%dT%H:%M:%S.000Z')

    def collect_historical_data(self,
                                from_date,
                                to_date,
                                expiry_date,
                                interval="1minute"):
        historical_data = []
        #current_date = datetime.now()

        #for _ in range(num_weeks):
        #start_date, expiry_date = self._get_default_dates(current_date)
        #end_date = start_date + timedelta(days=7)  # Saturday of the same week
        print(from_date)
        print(expiry_date)
        print(to_date)

        historical_data.extend(
            self.breeze.get_historical_data_v2(
                interval=interval,
                from_date=self._format_date(from_date),
                to_date=self._format_date(to_date),
                stock_code=self.stock_code,
                exchange_code=self.exchange_code,
                product_type=self.product_type,
                expiry_date=self._format_date(expiry_date),
                right=self.right,
                strike_price=self.strike_price).get('Success', []))
        # Move to the previous week
        #current_date -= timedelta(weeks=1)
        return historical_data

    def _round_to_nearest_50(self, value):
        return 50 * round(value / 50)

    def download_historical_data_from_csv(self, csv_file_path):
        df = pd.read_csv(csv_file_path)
        date_column = pd.to_datetime(df['Date'], format='%d-%m-%Y')
        #pd.to_datetime(df['Date'], format='%Y-%m-%d')

        historical_data_list = []

        for i, date in enumerate(date_column):
            # Calculate the strike_price based on the Open column value
            raw_strike_price = df.at[i, 'Open']
            strike_price = self._round_to_nearest_50(raw_strike_price)

            # Set the calculated strike_price
            self.strike_price = strike_price

            from_date, to_date, expiry_date = self._get_default_dates(date)
            historical_data = self.collect_historical_data(
                from_date, to_date, expiry_date)
            historical_data_list.append({str(date): historical_data})
        return historical_data_list

    def collect_historical_data_for_futures(self,
                                            interval="1minute",
                                            num_weeks=3):
        # Customize parameters for Futures
        self.product_type = "futures"
        #return self.collect_historical_data(interval, num_weeks)

    def collect_historical_data_for_equity(self,
                                           interval="1minute",
                                           num_weeks=3):
        # Customize parameters for Equity
        self.product_type = "cash"
        #return self.collect_historical_data(interval, num_weeks)

    def collect_historical_data_for_options(self,
                                            interval="1minute",
                                            num_weeks=3):
        # Customize parameters for Options
        self.product_type = "options"
        #return self.collect_historical_data(interval, num_weeks)


class DataFileHandler:

    @staticmethod
    def save_to_file(data, file_path):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
        print(f"Data saved to {file_path}")

    @staticmethod
    def read_file_and_load_dataframe(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Extract last nodes with datetime as index
            last_nodes = []
            for item in data:
                timestamp, values = list(item.items())[0]
                #print(timestamp, values)
                if values:
                    for value in values:
                        value["timestamp"] = pd.to_datetime(value["datetime"])
                        last_nodes.append(value)

            # Convert to DataFrame with datetime index
            return pd.DataFrame(last_nodes).set_index('timestamp')
