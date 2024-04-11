from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import joblib
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://crocus:pass0000@localhost/weather'
db = SQLAlchemy(app)

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)
    max_temp = db.Column(db.Float, nullable=False)
    min_temp = db.Column(db.Float, nullable=False)
    avg_temp = db.Column(db.Float, nullable=False)
    cloud_cover = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/weatherforecast/<date>')
def weather_forecast(date):
    date = datetime.strptime(date, '%Y%m%d').date()
    weather = Weather.query.filter_by(date=date).first()

    if weather is not None:
        return render_template('weather_forecast.html', weather=weather)

    else:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'random_forest_model.pkl')
        rf_model = joblib.load(file_path)
        X = pd.DataFrame({
            'year': [date.year],
            'month': [date.month],
            'day': [date.day]
        })
        prediction = rf_model.predict(X)[0]

        weather = Weather(
            date=date,
            max_temp=prediction[0],
            min_temp=prediction[1],
            avg_temp=prediction[2],
            cloud_cover=prediction[3]
        )
        db.session.add(weather)
        db.session.commit()

        return render_template('weather_forecast.html', weather=weather)

@app.template_filter('round')
def round_filter(value, precision=1):
    return round(value, precision)

if __name__ == '__main__':
    app.run(debug=True)