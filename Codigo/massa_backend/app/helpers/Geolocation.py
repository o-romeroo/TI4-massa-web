import requests as requests

import geocoder


def get_ip_location():
    url: str = 'https://checkip.amazonaws.com'
    requests.get(url)
    ip = requests.get(url).text
    return ip


def get_ip_infos():
    g = geocoder.ip(get_ip_location())
    if g.ok:
        return {
            "country": g.country,
            "city": g.city
        }
    else:
        return {"error": "Unable to retrieve location"}


