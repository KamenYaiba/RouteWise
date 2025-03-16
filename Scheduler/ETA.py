import requests
import os


def get_eta_from_google_maps_api(origin, destination, api_key):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "departure_time": "now",
        "key": api_key,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"] == "OK":
            duration_in_seconds = data["routes"][0]["legs"][0]["duration_in_traffic"]["value"]
            duration_in_minutes = round(duration_in_seconds / 60)
            return duration_in_minutes
        else:
            print(f"Google Maps API error: {data['error_message']}")
            return None

    except requests.exceptions.RequestException as e:
        print(e)
        return None
    except (KeyError, IndexError, TypeError) as e:
        print(e)
        return None


def get_eta(origin, destination):
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        print("environment variable not set")
        return None

    eta_minutes = get_eta_from_google_maps_api(origin, destination, api_key)
    return eta_minutes

