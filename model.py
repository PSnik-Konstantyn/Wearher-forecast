import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import mean_squared_error
import joblib

df = pd.read_csv('csv/from1940Weather.csv')

df['timestamp'] = pd.to_datetime(df['timestamp'])

df['year'] = df['timestamp'].dt.year
df['month'] = df['timestamp'].dt.month
df['day'] = df['timestamp'].dt.day

X = df[['year', 'month', 'day']]
y = df[['MaxTemp', 'MinTemp', 'AverageTemp', 'CloudCoverTotal']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

try:
    rf_model = joblib.load('random_forest_model.pkl')
    print("Модель успішно завантажена з файлу")

except FileNotFoundError:
    param_grid = {
        'n_estimators': [100, 200, 300, 400],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10]
    }

    rf_model = RandomForestRegressor(random_state=42)
    grid_search = GridSearchCV(rf_model, param_grid, cv=5, scoring='neg_mean_squared_error')
    grid_search.fit(X_train, y_train)

    rf_model = grid_search.best_estimator_
    joblib.dump(rf_model, 'random_forest_model.pkl')
    print("Модель успішно збережена в файл")

cv_scores = cross_val_score(rf_model, X, y, cv=5, scoring='neg_mean_squared_error')

cv_rmse_scores = np.sqrt(-cv_scores)

print("Результати крос-валідації:")
print("Середнє RMSE:", cv_rmse_scores.mean())
print("Стандартне відхилення RMSE:", cv_rmse_scores.std())

y_pred = rf_model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
print("Середньоквадратична помилка на тестовому наборі:", mse)