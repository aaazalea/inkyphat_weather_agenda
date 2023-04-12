import requests
import local_secrets

LOCATION = local_secrets.location #put your longitude and latittude here in decimal degrees
APIKEY = local_secrets.climacell_apikey

timelines_url = "https://api.tomorrow.io/v4/timelines"
realtime_url = "https://api.tomorrow.io/v4/weather/realtime"
def get_timelines():
    querystring = {
        "location": f"{LOCATION[0]}, {LOCATION[1]}",
        "fields":["temperature", "precipitationProbability"],
        "units":"imperial",
        "timesteps":"1h",
        "startTime": "now",
        "endTime": "nowPlus15h",
        "apikey":APIKEY
    }
    response = requests.request("GET", timelines_url, params=querystring)
    # if "data" not in response.json():
        # print(response.json())
    if response.status_code != 200:
        print(response.json())
        raise Exception("can't get weather")
    return (response.json()['data']['timelines'][0]['intervals'])

def get_realtime():
    querystring = {
        "location": f"{LOCATION[0]}, {LOCATION[1]}",
        "fields":["temperature", "temperatureApparent", "weatherCode"],
        "units":"imperial",
        "apikey":APIKEY
    }
    response = requests.request("GET", realtime_url, params=querystring)
    # if "data" not in response.json():
        # print(response.json())
    return (response.json()['data']['values'])

def icon_convert(weathercode):
    conversions = {
        '1000': 'clear-day', #TODO: night
        '1100': 'partly-clear-day',
        '1101': 'partly-cloudy-day',
        '1102': 'cloudy', # mostly cloudy
        '1001': 'cloudy',
        '2100': 'fog', #light fog
        '2000': 'fog',

        '4000': 'rain', # drizzle
        '4200': 'rain', # light rain
        '4001': 'rain', # rain
        '4201': 'rain', # heavy rain
        '8000': 'rain', # t-storm TODO

        '5001': 'snow', # flurries
        '5100': 'snow', # light snow
        '5000': 'snow', # snow
        '5101': 'snow', # heavy snow
        '7102': 'snow', # light hail TODO
        '7000': 'snow', # hail TODO
        '7102': 'snow', # heavy hail TODO

        '6001': 'sleet', # freezing drizzle
        '6200': 'sleet', # light freezing drizzle
        '6001': 'sleet', # freezing rain
        '6201': 'sleet', # heavy freezing rain    
    }
    return conversions.get(str(weathercode), f'unknown-{weathercode}')