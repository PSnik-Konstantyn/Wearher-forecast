import unittest
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import os

class TestModel(unittest.TestCase):
    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        root_dir = os.path.dirname(dir_path)
        file_path = os.path.join(root_dir, 'csv/from1940Weather.csv')
        df = pd.read_csv(file_path)


        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['year'] = df['timestamp'].dt.year
        df['month'] = df['timestamp'].dt.month
        df['day'] = df['timestamp'].dt.day

        X = df[['year', 'month', 'day']]
        y = df[['MaxTemp', 'MinTemp', 'AverageTemp', 'CloudCoverTotal']]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    def test_model(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        root_dir = os.path.dirname(dir_path)
        file_path = os.path.join(root_dir, 'random_forest_model.pkl')
        rf_model = joblib.load(file_path)

        y_pred = rf_model.predict(self.X_test)

        mse = mean_squared_error(self.y_test, y_pred)
        print("Mean Squared Error on test set:", mse)
        self.assertLess(mse, 140)

if __name__ == '__main__':
    unittest.main()