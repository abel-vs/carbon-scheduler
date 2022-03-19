import json

import requests


def get_data(country="NL"):
    api_key = open("key.txt").read()  # API Key should be stored in src/key.txt file
    params = {'countryCode': country}
    headers = {"auth-token": api_key}
    response = requests.get("https://api.co2signal.com/v1/latest", params=params, headers=headers)
    if response.ok:
        return json.loads(response.content.decode('utf-8'))["data"]
    else:
        return "Something went wrong."


def get_current_carbon_intensity(country="NL"):
    data: dict = get_data(country=country)
    if "carbonIntensity" in data:
        return data["carbonIntensity"]
    else:
        return Exception("No carbon intensity available.")


if __name__ == '__main__':
    carbon = get_current_carbon_intensity()
    print(carbon)
