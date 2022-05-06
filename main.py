from datetime import datetime, timedelta

import pytz
import requests

URL_POSITION_API = 'http://api.open-notify.org/iss-now.json'
URL_SUNSET_API = 'https://api.sunrise-sunset.org/json'


# returns latitude, longitude, timestamp
def get_iss_position():
    iss_position_response = requests.get(URL_POSITION_API)
    if iss_position_response.status_code != 200:
        print(f'Error occurred on iss position request - status code: {iss_position_response.status_code}')
        return None, None, None
    else:
        data = iss_position_response.json()
        latitude = data['iss_position']['latitude']
        longitude = data['iss_position']['longitude']
        timestamp = data['timestamp']
        return latitude, longitude, timestamp


# returns sunrise, sunset
def get_sun_info(latitude, longitude, date, date_current):
    url = URL_SUNSET_API + f'?lat={latitude}&lng={longitude}&date={date.strftime("%Y-%m-%d")}&formatted=0'
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Error occurred on sun info request - status code: {response.status_code}')
        return None, None
    else:
        data = response.json()['results']
        sunrise = datetime.fromisoformat(data['sunrise'])
        sunset = datetime.fromisoformat(data['sunset'])

        if sunrise < date_current and sunset < date_current:
            return get_sun_info(latitude, longitude, date + timedelta(days=1), date_current)
        else:
            return sunrise, sunset


def get_is_illuminated_side(sunrise, sunset, current_date):
    return sunrise <= current_date <= sunset


def get_are_ideal_conditions(sunrise, sunset, current_date):
    ideal_sunrise_minus_two_h = sunrise - timedelta(hours=2)
    ideal_sunrise_minus_one_h = sunrise - timedelta(hours=1)
    ideal_sunset_plus_one_h = sunset + timedelta(hours=1)
    ideal_sunset_plus_two_h = sunset + timedelta(hours=2)

    if ideal_sunrise_minus_two_h <= current_date <= ideal_sunrise_minus_one_h:
        # ideal conditions for observation (1-2 hours before sunrise)
        return True

    if ideal_sunset_plus_one_h <= current_date <= ideal_sunset_plus_two_h:
        # ideal conditions for observation (1-2 hours after sunset)
        return True

    return False


def show_results(latitude, longitude, sunrise, sunset, current_date, is_illuminated, ideal_conditions):
    print(f"ISS position: latitude={latitude}, longitude={longitude}")
    print(f"Sunrise (UTC): {sunrise}, sunset (UTC)={sunset}")
    print(f"Current date (UTC): {current_date}")

    if is_illuminated:
        print("ISS is on the illuminated side of the Earth")
    else:
        print("ISS is on the NOT illuminated side of the Earth")

    if ideal_conditions:
        print("There are ideal conditions for observing the ISS from the Earth")
    else:
        print("There are NOT ideal conditions for observing the ISS from the Earth")


def main():
    lat, long, timestamp = get_iss_position()
    utc_date_timestamp = datetime.fromtimestamp(timestamp).astimezone(pytz.utc)
    sunrise, sunset = get_sun_info(lat, long, utc_date_timestamp, utc_date_timestamp)

    is_illuminated = get_is_illuminated_side(sunrise, sunset, utc_date_timestamp)
    are_ideal_conditions = get_are_ideal_conditions(sunrise, sunset, utc_date_timestamp)

    show_results(lat, long, sunrise, sunset, utc_date_timestamp, is_illuminated, are_ideal_conditions)


if __name__ == '__main__':
    main()
