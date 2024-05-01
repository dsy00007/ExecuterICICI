from dataService import *
from dataAnalysisFile import *


class downloadAndPrepareDataClass:

    def __init__(self, session_token):
        self.session_token = session_token
        self.file_path_call = "historicalData/call_historical_data.json"
        self.file_path_put = "historicalData/put_historical_data.json"

    def get_Option_CallData(self):
        collector = HistoricalDataCollector(stock_code="NIFTY",
                                            exchange_code="NFO",
                                            product_type="options",
                                            session_token=self.session_token,
                                            right="call",
                                            strike_price=21750)
        csv_file_path = "cnse.csv"  # Update with the actual CSV file path
        historical_data_list = collector.download_historical_data_from_csv(
            csv_file_path)
        file_handler = DataFileHandler()
        file_handler.save_to_file(historical_data_list, self.file_path_call)

    def get_Option_PutData(self):
        collector = HistoricalDataCollector(stock_code="NIFTY",
                                            exchange_code="NFO",
                                            product_type="options",
                                            session_token=self.session_token,
                                            right="put",
                                            strike_price=21750)
        csv_file_path = "cnse.csv"  # Update with the actual CSV file path
        historical_data_list = collector.download_historical_data_from_csv(
            csv_file_path)
        file_handler = DataFileHandler()
        file_handler.save_to_file(historical_data_list, self.file_path_put)

    #callable function- First step to be called to collect and save data for option call and put for nifty
    def collectOptionsData(self):
        print('collecting Data for call option')
        self.get_Option_CallData()
        print('done collecting for call option')
        print('collecting Data for put option')
        self.get_Option_PutData()
        print('done collecting for call option')
