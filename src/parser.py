import json
import requests
from datetime import date

API_KEY = "NONE"


def get_marginal_forecast():
    """
    Get the marginal forecast carbon intensity hourly for the next day
    :return: array of predicted hourly values for the next 24 hours
    """
    response = requests.get("https://api.electricitymap.org/v3/marginal-carbon-intensity/forecast?zone='NL'",
                            headers={'Authorization': f'auth-token {API_KEY}'})
    print(f'Response received from the API: {response}')

    forecasted_marginal_carbon_intensity = None

    if response.status_code == 200:
        forecasted_marginal_carbon_intensity = response.json()['Response']
    else:
        # Currently, we use data in the file since we don't have the API key
        f = open('dummy_data/forecasted_marginal.json')

        forecasted_marginal_carbon_intensity = json.load(f)

    results_data = [x["marginalCarbonIntensity"] for x in forecasted_marginal_carbon_intensity['forecast']]

    return results_data


def get_past_carbon_intensity_history():
    """
    Get range of past carbon intensity around last year on the same exact day as the time of execution of this program
    :return: Past carbon intensity history range
    """

    today = date.today()
    # calculate range based on today - at most 10 days range limit by API
    start_date = "2019-05-21T21:00:00Z"
    end_date = "2019-05-22T00:00:00Z"

    response = requests.get(
        f"https://api.electricitymap.org/v3/carbon-intensity/past-range?zone=NL&start={start_date}&end={end_date}",
        headers={'Authorization': f'auth-token {API_KEY}'})
    print(f'Response received from the API: {response}')

    past_carbon_intensity_history = None

    if response.status_code == 200:
        past_carbon_intensity_history = response.json()['Response']
    else:
        # Currently, we use data in the file since we don't have the API key
        f = open('dummy_data/past_carbon_history.json')

        past_carbon_intensity_history = json.load(f)

    results_data = [x["carbonIntensity"] for x in past_carbon_intensity_history['data']]

    return results_data


print(f'Forecasted marginal intensities for the next 24 hours\n {get_marginal_forecast()}')
print(f'Last year carbon intensity around today\n {get_past_carbon_intensity_history()}')
