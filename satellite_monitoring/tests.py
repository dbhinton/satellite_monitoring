# tests.py

import json
from django.test import TestCase
from django.urls import reverse

class SatelliteHealthTests(TestCase):
    def test_no_recent_data(self):
        # No recent altitude data available
        response = self.client.get(reverse('satellite-health'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'No recent altitude data available'})

    def test_rapid_orbital_decay_imminent(self):
        # Rapid orbital decay imminent
        data = {'altitude': [{'timestamp': '2023-08-06T20:45:00', 'altitude': 150}]}
        response = self.client.get(reverse('satellite-health'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'WARNING: RAPID ORBITAL DECAY IMMINENT'})

    def test_sustained_low_earth_orbit(self):
        # Sustained low earth orbit
        data = {'altitude': [{'timestamp': '2023-08-06T20:45:00', 'altitude': 170}]}
        response = self.client.get(reverse('satellite-health'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Sustained Low Earth Orbit Resumed'})

    def test_altitude_ok(self):
        # Altitude is A-OK
        data = {'altitude': [{'timestamp': '2023-08-06T20:45:00', 'altitude': 175}]}
        response = self.client.get(reverse('satellite-health'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Altitude is A-OK'})
