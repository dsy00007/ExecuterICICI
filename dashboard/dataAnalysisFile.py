import json
import pandas as pd
from datetime import datetime, timedelta
from dataService import *
from sklearn.ensemble import VotingRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from dataAnalysisFile import *
import logging


class DataAnalyzer:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.df = self.getDataFromFile()

    def getDataFromFile(self):
        print('loading historical data')
        file_path = "historicalData/historical_data.json"
        file_handler = DataFileHandler()
        historical_df = file_handler.read_file_and_load_dataframe(file_path)
        print('loading historical data done...')
        return historical_df

    def analyze_data_by_weeks(self, dataframe, num_weeks):
        # Convert 'datetime' column to datetime objects
        dataframe['datetime'] = pd.to_datetime(dataframe['datetime'])
        end_date = datetime.now()
        start_date = end_date - timedelta(weeks=num_weeks)

        filtered_df = dataframe[(dataframe['datetime'] >= start_date)
                                & (dataframe['datetime'] <= end_date)]
        # Perform your analysis on the filtered data here
        return filtered_df

    def preprocess_data(self, last_configurable_data=5):
        # Drop unnecessary columns and handle missing values
        self.df = self.df[[
            'close', 'datetime', 'high', 'low', 'open', 'volume'
        ]]
        self.df['datetime'] = pd.to_datetime(self.df['datetime'])
        self.df = self.df.set_index('datetime')
        self.df = self.df.dropna()

        # Include the last configurable data along with the 'close' column
        for i in range(1, last_configurable_data + 1):
            self.df[f'close_{i}'] = self.df['close'].shift(i)

        self.df = self.df.dropna()

    def filter_data_by_day(self, day_of_week):
        # Filter data based on the provided day of the week
        filtered_data = self.df[self.df.index.dayofweek == day_of_week]
        return filtered_data

    def split_data(self, last_configurable_data=5, future_steps=5):
        # Group data by day
        daily_data = self.df.groupby(pd.Grouper(key='datetime', freq='D'))

        # Shift the 'close' column within each daily group
        shifted_y = daily_data['close'].shift(-future_steps)

        # Concatenate the shifted target variable back to the original dataframe
        self.df['future_close'] = shifted_y.reset_index(drop=True)

        # Drop rows with NaN values (introduced by shifting)
        self.df.dropna(inplace=True)

        # Features and target variables
        feature_cols = [
            'open', 'open_interest', 'volume'
        ]
        X = self.df[feature_cols]
        y = self.df[
            'future_close']  # Future close value shifted by future_steps

        # Split the data into training and testing sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)

    def train_models(self):
        self.logger.info("Training models started...")

        # Initialize individual regressors
        rf_regressor = RandomForestRegressor(n_estimators=50, random_state=42)
        gb_regressor = GradientBoostingRegressor(n_estimators=50,
                                                 random_state=42)
        lr_regressor = LinearRegression()

        # Train the regressors
        self.logger.debug("Training RandomForestRegressor with parameters: %s",
                          rf_regressor.get_params())
        rf_regressor.fit(self.X_train, self.y_train)
        self.logger.debug("RandomForestRegressor training score: %f",
                          rf_regressor.score(self.X_train, self.y_train))

        self.logger.debug(
            "Training GradientBoostingRegressor with parameters: %s",
            gb_regressor.get_params())
        gb_regressor.fit(self.X_train, self.y_train)
        self.logger.debug("GradientBoostingRegressor training score: %f",
                          gb_regressor.score(self.X_train, self.y_train))

        self.logger.debug("Training LinearRegression...")
        lr_regressor.fit(self.X_train, self.y_train)
        self.logger.debug("LinearRegression training score: %f",
                          lr_regressor.score(self.X_train, self.y_train))

        # Create an ensemble model with a voting system
        self.logger.debug("Creating ensemble model with VotingRegressor...")
        self.ensemble_model = VotingRegressor(
            estimators=[('rf',
                         rf_regressor), ('gb',
                                         gb_regressor), ('lr', lr_regressor)])

        # Train the ensemble model
        self.logger.debug("Training ensemble model...")
        self.ensemble_model.fit(self.X_train, self.y_train)
        self.logger.debug(
            "Ensemble model training score: %f",
            self.ensemble_model.score(self.X_train, self.y_train))

        self.logger.info("Training models completed.")

    def evaluate_model(self):
        # Make predictions on the test set
        y_pred = self.ensemble_model.predict(self.X_test)

        # Evaluate the model
        mse = mean_squared_error(self.y_test, y_pred)
        print(f'Mean Squared Error: {mse}')

    def predict_future_close_range(self, features):
        # Make predictions for the future close range
        future_close_range = self.ensemble_model.predict(features)
        return future_close_range
