from coordinates import get_coordinates, Coordinates
from weather_api_service import get_weather
from weather_formatter import format_weather

from expections import CantGetCoordinates, ApiServiceError

def main():
    try:
        coordinates: Coordinates = get_coordinates()
    except CantGetCoordinates:
        print('Не удалось получить координаты')
        exit(1)
    try:
        weather = get_weather(coordinates)
    except ApiServiceError:
        print("Не удалось получить погоду по текущим координатам")
        exit(1)
    print(format_weather(weather))


if __name__ == '__main__':
    main()
