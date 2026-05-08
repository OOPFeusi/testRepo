import requests
from guizero import App, Text, Combo

def get_temperature(city='London'):
    """
    Fetch current temperature using Open-Meteo API (free, no authentication required)
    """
    try:
        # Geocode the city name to get coordinates
        geo_url = f'https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json'
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()
        
        if not geo_data.get('results'):
            return f"City '{city}' not found"
        
        location = geo_data['results'][0]
        latitude = location['latitude']
        longitude = location['longitude']
        
        # Get weather data using coordinates
        weather_url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weather_code'
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        
        temp = weather_data['current']['temperature_2m']
        return temp
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

def update_temperature(city):
    """Callback function to update temperature when city selection changes"""
    temp = get_temperature(city)
    temp_text.value = f"Current temperature in {city}: {temp} °C"

cities = ["New York", "Adelaide", "Bern", "Johannesburg"]

app = App("Weather App")
Text(app, text="Select a city:")
city_dropdown = Combo(app, options=cities, command=update_temperature)
city_dropdown.value = cities[0]  # Set default to first city
temp = get_temperature(cities[0])
temp_text = Text(app, text=f"Current temperature in {cities[0]}: {temp} °C")
app.display()