import requests

# WeatherAPI key
WEATHER_API_KEY = '10666b511f7a43fcb0d00529250502'  # TODO: Replace with your own WeatherAPI key

def get_weather(city):
    # TODO: Build the API request URL using the base API endpoint, the API key, and the city name provided by the user.
    url = f'https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}'
    # TODO: Make the HTTP request to fetch weather data using the 'requests' library.
    r = requests.get(url, auth=('user', 'pass'))
    # TODO: Handle HTTP status codes:
    # - Check if the status code is 200 (OK), meaning the request was successful.
    status = r.status_code
    # - If not 200, handle common errors like 400 (Bad Request), 401 (Unauthorized), 404 (Not Found), and any other relevant codes.
    
    if r.status_code == 200:
        # TODO: Parse the JSON data returned by the API. Extract and process the following information:
        # - Current temperature in Fahrenheit
        # - The "feels like" temperature
        # - Weather condition (e.g., sunny, cloudy, rainy)
        # - Humidity percentage
        # - Wind speed and direction
        # - Atmospheric pressure in mb
        # - UV Index value
        # - Cloud cover percentage
        # - Visibility in miles

        # print the json
        print(r.json())

        weather_data = r.json()
        temperature = weather_data['current']['temp_f']
        feels_like = weather_data['current']['feelslike_f']
        condition = weather_data['current']['condition']['text']
        humidity = weather_data['current']['humidity']
        wind_speed = weather_data['current']['wind_mph']
        wind_dir = weather_data['current']['wind_dir']
        atm = weather_data['current']['pressure_mb']
        uv = weather_data['current']['uv']
        cloud = weather_data['current']['cloud']
        visibility = weather_data['current']['vis_miles']


        # TODO: Display the extracted weather information in a well-formatted manner.
        print(f"Weather data for {city}...")
        print(f"Temperature: {temperature} F")
        print(f"Feels like: {feels_like} F")
        print(f"Condition: {condition}")
        print(f"Humidity: {humidity}%")
        print(f"Wind: {wind_speed} mph, {wind_dir}")
        print(f"Atmospheric Pressure: {atm} mb")
        print(f"UV Index: {uv}")
        print(f"Cloud Cover: {cloud}%")
        print(f"Visibility: {visibility} miles")

    else:
        # TODO: Implement error handling for common status codes. Provide meaningful error messages based on the status code.
        print(f"Error: {r.status_code}. Something went wrong.")
        if status == 400:
            print("Bad Request")
        elif status == 401:
            print("Unauthorized")
        elif status == 404:
            print("Not Found")
        else:
            print("Unknown Error")
if __name__ == '__main__':
    # TODO: Prompt the user to input a city name.
    city = input("Enter the city name: ")
    # TODO: Call the 'get_weather' function with the city name provided by the user.
    get_weather(city)
    pass
