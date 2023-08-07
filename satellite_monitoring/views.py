import requests
from datetime import datetime, timedelta
from django.http import JsonResponse

SAT_API_URL = 'https://api.cfast.dev/satellite/'


# Store the last 5 minutes of altitude data
altitude_data = []

def get_satellite_stats(request):
    try:
        global altitude_data

        # Fetch real-time data from the satellite API
        response = requests.get(SAT_API_URL)
        response.raise_for_status()  # Check if the request was successful (status code 2xx)
        data = response.json()

        # Check if 'altitude' key is present in the data
        if 'altitude' not in data:
            return JsonResponse({'error': 'Satellite data is missing the altitude field'}, status=500)

        # Ensure the 'altitude' value is a list
        if isinstance(data['altitude'], float):
            # Wrap the single altitude data point in a list
            data['altitude'] = [{'timestamp': data['last_updated'], 'altitude': data['altitude']}]

        # Append the new altitude data points to the altitude_data list
        altitude_data.extend(data['altitude'])

        # Remove old altitude data points that are outside the last 5 minutes
        five_minutes_ago = (datetime.now() - timedelta(minutes=5)).isoformat()
        altitude_data = [d for d in altitude_data if d['timestamp'] >= five_minutes_ago]

        if altitude_data:
            altitudes = [d['altitude'] for d in altitude_data]
            min_altitude = min(altitudes)
            max_altitude = max(altitudes)
            avg_altitude = sum(altitudes) / len(altitudes)
            response_data = {
                'min_altitude': min_altitude,
                'max_altitude': max_altitude,
                'avg_altitude': avg_altitude,
            }
        else:
            response_data = {
                'min_altitude': None,
                'max_altitude': None,
                'avg_altitude': None,
            }

        return JsonResponse(response_data)

    except requests.exceptions.RequestException as e:
        # Handle any request-related exceptions (e.g., connection error)
        return JsonResponse({'error': f'Failed to fetch data from the satellite API: {e}'}, status=500)

    except ValueError as e:
        # Handle JSON decoding error (invalid JSON format)
        return JsonResponse({'error': 'Failed to parse JSON response from the satellite API'}, status=500)

def get_satellite_health(request):
    try:
        # Fetch real-time data from the satellite API
        response = requests.get(SAT_API_URL)
        response.raise_for_status()  # Check if the request was successful (status code 2xx)
        data = response.json()
        
        

        # Check if 'altitude' key is present in the data
        if 'altitude' not in data:
            return JsonResponse({'error': 'Satellite data is missing the altitude field'}, status=500)

        # Ensure the 'altitude' value is a list
        if isinstance(data['altitude'], float):
            # Wrap the single altitude data point in a list
            data['altitude'] = [{'timestamp': data['last_updated'], 'altitude': data['altitude']}]

        # Get the average altitude over the last minute
        one_minute_ago = (datetime.now() - timedelta(minutes=1)).isoformat()
        recent_data = [d for d in data['altitude'] if d['timestamp'] >= one_minute_ago]
        if not recent_data:
            return JsonResponse({'message': 'No recent altitude data available'}, status=200)

        avg_altitude = sum(d['altitude'] for d in recent_data) / len(recent_data)

        # Check the health status based on the average altitude
        if avg_altitude < 160:
            return JsonResponse({'message': 'WARNING: RAPID ORBITAL DECAY IMMINENT'}, status=200)
        elif avg_altitude >= 160 and avg_altitude < 172:
            return JsonResponse({'message': 'Sustained Low Earth Orbit Resumed'}, status=200)
        else:
            return JsonResponse({'message': 'Altitude is A-OK'}, status=200)

    except requests.exceptions.RequestException as e:
        # Handle any request-related exceptions (e.g., connection error)
        return JsonResponse({'error': f'Failed to fetch data from the satellite API: {e}'}, status=500)

    except ValueError as e:
        # Handle JSON decoding error (invalid JSON format)
        return JsonResponse({'error': 'Failed to parse JSON response from the satellite API'}, status=500)