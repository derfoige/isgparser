
# -*- coding: utf-8 -*-

from urllib.request import urlopen
import urllib.parse, json
from .urlret import retry



WINDDIRMAP = {
    "s": [0, 22.4],
    "sw": [22.5, 77.4],
    "w": [77.5, 112.4],
    "nw": [112.5, 157.4],
    "n": [157.5, 202.4],
    "ne": [202.5, 247.4],
    "e": [247.5, 292.4],
    "se": [292.5, 337.4],
    "x": [337.5, 360],
}
INTERESTING_ITEMS = ("solarRadiation", "uv", "humidity")
METRIC_ITEMS = "metric"
WINDDIR_NUMBER = ["winddir"]


def get_winddir_char(d):
    """
     Converts Numeric Wind Direction to N, S, E etc.
    """
    x = {k: v for k, v in sorted(WINDDIRMAP.items(), key=lambda item: item[1])}
    for a in x.keys():
        for b in x[a]:
            if b < d:
                c = a
                break
    return(c)

@retry(urllib.error.URLError, tries=1, delay=10)
def get_weather(url, apikey, stationid):
    """
     Get current Weatherdata from WU 
    """
    metrics = {}
    ret = {}
    response = urlopen(f"http://{url}?apiKey={apikey}&stationId={stationid}&format=json&numericPrecision=decimal&units=m")
    data = json.loads(response.read())
    data2 = data["observations"][0]
    for key in INTERESTING_ITEMS:
        value = data2[key]
        metrics[key] = value

    for key in data2[METRIC_ITEMS].keys():
        value = data2[METRIC_ITEMS][key]
        metrics[key] = value

    for key in WINDDIR_NUMBER:
        value = data2[key]
        metrics[key] = value
    ret["Wetterdaten"] = metrics
    return ret
