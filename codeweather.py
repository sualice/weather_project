import requests

def translate_weather_description(description):
  translations = {
    "clear sky": "ясно",
    "few clouds": "частичная облачность",
    "scattered clouds": "облачно",
    "broken clouds": "облачно",
    "overcast clouds": "пасмурно",
    "drizzle": "мелкий дождь",
    "drizzle": "морось",
    "haze": "легкий туман",
    "rain": "дождь",
    "shower rain": "ливневый дождь",
    "thunderstorm": "гроза",
    "snow": "снег",
    "mist": "туман"
  }
  return translations.get(description, description)

def get_weather(city, api_key):
  url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
  try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    weather = translate_weather_description(data['weather'][0]['description'])
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    visibility = data['visibility'] / 1000 # переводим в километры

    print(f"Погода в {city}: {weather}, температура: {temperature}°C")
    print(f"Влажность: {humidity}%, скорость ветра: {wind_speed} м/с, видимость: {visibility} км")
  except requests.exceptions.Timeout:
    print("Время ожидания истекло. Попробовать снова? (да/нет)")
    answer = input()
    if answer.lower() == "да":
      get_weather(city, api_key)
    else:
      print("До свидания!")
  except requests.exceptions.RequestException as e:
    print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
  city = input("Введите название города: ")
  api_key = "a041a61deb2966764e5c913c10270375" 
  get_weather(city, api_key)