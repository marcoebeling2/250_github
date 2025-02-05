import requests

def get_weather():
    url = f'https://official-joke-api.appspot.com/random_joke'
    r = requests.get(url, auth=('user', 'pass'))
    status = r.status_code
    
    if r.status_code == 200:
        data = r.json()
        type = data['type']
        setup = data['setup']
        punchline = data['punchline']

        print(f"Your {type} joke is: {setup}...\n{punchline}")


    else:
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
    joke = input("Do you want a joke?")
    if joke.lower() == "no":
        print("Goodbye")
        exit()
    get_weather()
    pass

