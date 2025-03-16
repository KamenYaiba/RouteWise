import json

import requests


def clean_url(raw_url):
    url = requests.get(raw_url, allow_redirects=True).url
    url = url.split("data")[0] if "data" in url else url
    if "?hl=en" not in url:
        url = url + "?hl=en"
    return url


def time_to_gmt(time_frame: str, offset):
    time_frame = time_frame.strip().split('-')
    first_hour = (int(time_frame[0]) - offset) % 24
    second_hour = (int(time_frame[1]) - offset) % 24
    return [first_hour, second_hour]


def eta_to_mins(eta: str):
    if "min" in eta:
        return int(eta.split()[0])
    h, m = eta.split()

    h = int(h.replace('h', ''))
    m = int(m.replace('m', ''))

    return 60 * h + m


def add_route_to_json(hour, route):
    file_path = f'jobs_JSON/jobs{hour:02d}.json'
    try:
        with open(file_path, "r") as f:
            routes_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        routes_data = []

    routes_data.append(route.to_dict())

    with open(file_path, "w") as f:
        json.dump(routes_data, f, indent=4)


