import time
from datetime import datetime, timedelta
import pytz
import requests
from timezonefinder import TimezoneFinder
from colorama import Fore, Back, Style

start = time.time()
def kelvin_to_cels(kelvin):
    cels = kelvin - 273
    return int(cels)


def sun_times(sun_time, timezones):
    # Convert Unix timestamp to datetime
    utc_sun_datetime = datetime.utcfromtimestamp(sun_time)
    # Apply the timezone offset
    sun_datetime = utc_sun_datetime + timedelta(seconds=timezones)
    # Format the datetime as a string
    return sun_datetime.strftime("%I:%M %p")


def weather_entry(w_data):
    time = w_data['dt_txt']  # Extracting the time part
    date_obj = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    time_formatted = date_obj.strftime("%I:%M %p")
    temp = w_data['main']['temp']
    feels_like = w_data['main']['feels_like']
    description = w_data['weather'][0]['description']
    pressure = w_data['main']['pressure']
    humidity = w_data['main']['humidity']
    wind = w_data['wind']['speed']

    return {
        'time_formatted': time_formatted,
        'temp': kelvin_to_cels(temp),
        'feels_like': kelvin_to_cels(feels_like),
        'description': description,
        'pressure': pressure,
        'humidity': humidity,
        'wind': wind
    }


def display_weather_data(data1, data2):
    city_timezone = data1['city']["timezone"]
    city_name = data1['city']["name"]

    obj = TimezoneFinder()
    current_time = obj.timezone_at(lng=longitude, lat=latitude)
    timestamp = datetime.now(pytz.timezone(f'{current_time}'))
    current_time = timestamp.strftime("%I:%M %p")

    sunset_time = sun_times(data1['city']["sunset"], city_timezone)
    sunrise_time = sun_times(data1['city']["sunrise"], city_timezone)

    weather_description = data2["weather"][0]["description"]
    C_temperature = data2["main"]["temp"]
    C_temp_feel = data2['main']['feels_like']
    C_humidity = data2['main']['humidity']
    C_pressure = data2['main']['pressure']
    C_wind = data2['wind']['speed']
    print(Fore.RED + f"{city_name:-^35}" + Style.RESET_ALL)
    print(Fore.LIGHTCYAN_EX + f'Current time in {city_name} : {current_time}')
    print("Sunrise Time: ", sunrise_time)
    print(f"Sunset Time: ", sunset_time)
    print(Fore.LIGHTYELLOW_EX + "Current Weather Condition:" + Style.RESET_ALL)
    print(Fore.LIGHTCYAN_EX + f"Temperature: {kelvin_to_cels(C_temperature)}°C")
    print(f"Feel Temperature: {kelvin_to_cels(C_temp_feel)}°C")
    print(f"Humidity: {C_humidity}%")
    print(f"Pressure: {C_pressure}hPa")
    print(f"Weather Condition: {weather_description}")
    print(f"Wind Speed: {C_wind}m/s" + Style.RESET_ALL)


def after_5day_data(data3):
    Current_date = None

    for entry in data3['list']:
        date = entry['dt_txt'].split()[0]

        if date != Current_date:
            if Current_date is not None:
                print()
            print(Fore.LIGHTGREEN_EX + f"Date: {date}" + Style.RESET_ALL)
            Current_date = date

        weather_data = weather_entry(entry)
        print(
            f"Time: {weather_data['time_formatted']} : Temp: {weather_data['temp']}°C : Feel Temp: {weather_data['feels_like']}°C : Wind Speed: {weather_data['wind']:.2f}m/s : Humidity: {weather_data['humidity']}% : Pressure: {weather_data['pressure']}hPa : description: {weather_data['description']}")


print(Fore.RED + "_" * 35 + "Weather Forecast Application" + "_" * 35 + Style.RESET_ALL)
City_name = input("Enter City Name (" + Style.BRIGHT + "New York" + Style.RESET_ALL + "): ")
# City_name = 'karachi'
country_code = input("Enter Country Code (" + Style.BRIGHT + "US" + Style.RESET_ALL + ") OR Name: ")
# country_code = 'pk'

api_key = "aa73e86ed7565d95c864ff8041401bbb"

try:
    C_url = f"https://api.openweathermap.org/data/2.5/weather?q={City_name},{country_code}&appid={api_key}"
    data = requests.get(C_url).json()

    if 'coord' in data:
        C_city = data['name']
        if C_city.lower() == City_name.lower():
            longitude = data['coord']['lon']
            latitude = data['coord']['lat']
            C_city = data['name']

            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={api_key}"
            weather = requests.get(url).json()
            display_weather_data(weather, data)

            current_date = None
            print()
            print(Fore.RED + "_" * 35 + "After 5 Days Weather Forecast Data" + "_" * 25 + Style.RESET_ALL)
            print()
            after_5day_data(weather)
        else:
            print("City Not Found")
    else:
        print("Invalid response")

except requests.exceptions.RequestException as e:
    print(f"Error connecting to API: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print(time.time() - start)