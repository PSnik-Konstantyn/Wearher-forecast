import unittest
from main import app, db, Weather
from datetime import datetime

class TestDatabase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://crocus:pass0000@localhost/test_db'
        app.config['TESTING'] = True
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_weather_forecast_existing_data(self):
        test_date = datetime(2028, 1, 1).date()
        test_weather = Weather(
            date=test_date,
            max_temp=10.0,
            min_temp=5.0,
            avg_temp=7.5,
            cloud_cover=50.0
        )
        with app.app_context():
            db.session.add(test_weather)
            db.session.commit()

        response = self.client.get(f'/weatherforecast/{test_date.strftime("%Y%m%d")}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'10.0', response.data)
        self.assertIn(b'5.0', response.data)
        self.assertIn(b'7.5', response.data)
        self.assertIn(b'50.0', response.data)

    def test_weather_forecast_non_existing_data(self):
        test_date = datetime(3023, 1, 1).date()

        response = self.client.get(f'/weatherforecast/{test_date.strftime("%Y%m%d")}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()