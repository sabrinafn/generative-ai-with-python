import sys
import requests # requests allows you to send HTTP requests

# This function validates the arguments received from the command line
def city_to_search():

    # exit from program if argument is empty or not argument was provided
    if len(sys.argv) != 2 or sys.argv[1] == "":
        print('Incorrect usage!\nUsage: python3 weather.py "valid city name"')
        return sys.exit(1)
    
    # returns the argument at pos 1, which should be the city provided
    return sys.argv[1]


# This function returns a valid response from the api request
def get_city_response(city: str):

    response = requests.get(f'https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1')

    # if there's not 'result' dict inside, it means it did not find a city with this name
    if "results" not in response.json():
        print(f'City "{city}" not found'),
        return sys.exit(1)
    
    # returns the response with the list that only contains the data needed
    return response.json()["results"][0]


# This function returns all data necessary inside a dictionary
def weather_forecast_data(city: str):

    city_response = get_city_response(city)

    try:
        data = dict(
            city = city_response["name"],
            country = city_response["country"],
            lat = city_response["latitude"],
            lon = city_response["longitude"]
            )
    except:
        print(f'City "{city}" returned incomplete data')
        return sys.exit(1)

    forecast_response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={data["lat"]}&longitude={data["lon"]}&current=temperature_2m')

    data["unit"] = forecast_response.json()["current_units"]["temperature_2m"]
    data["temp"] = forecast_response.json()["current"]["temperature_2m"]

    return data


# This function prints the weather forecast with the data received as argument
def print_weather_forecast(data: dict):
    print(f'Current temperature in {data["city"]}, {data["country"]} is {data["temp"]} {data["unit"]}')


# Main function
def main():
    city = city_to_search()
    
    data = weather_forecast_data(city)
    
    print_weather_forecast(data)

if __name__ == "__main__":
    main()