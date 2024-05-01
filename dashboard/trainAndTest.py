# Example usage:
# Assuming df is your DataFrame
from dataService import *
from dataAnalysisFile import *

last_configurable_data = 5
ensemble_model = DataAnalyzer()
ensemble_model.preprocess_data(last_configurable_data)

# Filter data for a specific day (e.g., Monday - day_of_week=0)
filtered_data_monday = ensemble_model.filter_data_by_day(day_of_week=0)
print(f'Data for Monday:\n{filtered_data_monday}')

ensemble_model.split_data()
ensemble_model.train_models()
ensemble_model.evaluate_model()

# Assuming 'features' is a DataFrame containing features for prediction
# Adjust 'features' based on your actual feature data
#predicted_future_close_range = ensemble_model.predict_future_close_range(features)
#print(f'Predicted Future Close Range: {predicted_future_close_range}')