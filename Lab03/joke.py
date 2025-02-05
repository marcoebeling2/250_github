import requests

# WeatherAPI key

def get_weather():
    # TODO: Build the API request URL using the base API endpoint, the API key, and the city name provided by the user.
    url = f'https://official-joke-api.appspot.com/random_joke'
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
        data = r.json()
        type = data['type']
        setup = data['setup']
        punchline = data['punchline']

        print(f"Your {type} joke is: {setup}...\n {punchline}")


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
    joke = input("Do you want a joke?")
    if joke.lower() == "no":
        print("Goodbye")
        exit()
    # TODO: Call the 'get_weather' function with the city name provided by the user.
    get_weather()
    pass

