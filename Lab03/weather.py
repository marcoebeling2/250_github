import requests

# WeatherAPI key
WEATHER_API_KEY = 'your_api_key_here'  # TODO: Replace with your own WeatherAPI key

def get_weather(city):
    # TODO: Build the API request URL using the base API endpoint, the API key, and the city name provided by the user.
    
    # TODO: Make the HTTP request to fetch weather data using the 'requests' library.
    
    # TODO: Handle HTTP status codes:
    # - Check if the status code is 200 (OK), meaning the request was successful.
    # - If not 200, handle common errors like 400 (Bad Request), 401 (Unauthorized), 404 (Not Found), and any other relevant codes.
    
    if response.status_code == 200:
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

        # TODO: Display the extracted weather information in a well-formatted manner.
        print(f"Weather data for {city}...")
    else:
        # TODO: Implement error handling for common status codes. Provide meaningful error messages based on the status code.
        print(f"Error: {response.status_code}. Something went wrong.")

if __name__ == '__main__':
    # TODO: Prompt the user to input a city name.
    
    # TODO: Call the 'get_weather' function with the city name provided by the user.
    pass
