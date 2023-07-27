import json
import urllib.error
from urllib.request import urlopen
from typing import NamedTuple
from expections import CantGetCoordinates
from config import IPINFO_JSON_URL


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


def get_coordinates() -> Coordinates:
    """Returns current coordinates based on user's IP address"""
    data = _get_data_json()
    lat, lon = _parse_latitude_and_longitude(data)
    return _build_coordinates(lat, lon)

def _get_data_json() -> str:
    try:
        response = _get_data_response(IPINFO_JSON_URL)
        return json.load(response)['loc']
    except urllib.error.HTTPError:
        raise CantGetCoordinates

def _get_data_response(url: str) -> str:
    response = urlopen(url)
    return response

def _parse_latitude_and_longitude(data: str) -> tuple[float, float]:
    try:
        latitude = float(data.split(',')[0])
        longitude = float(data.split(',')[1])
        return latitude, longitude
    except ValueError:
        raise CantGetCoordinates
    except AttributeError:
        raise CantGetCoordinates

def _build_coordinates(latitude: float, longitude: float) -> Coordinates:
    return Coordinates(
        latitude=latitude,
        longitude=longitude
    )
