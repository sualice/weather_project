import tkinter as tk
import requests
import threading

def translate_weather_description(description):
    translations = {
        "clear sky": "ясно",
        "few clouds": "частичная облачность",
        "scattered clouds": "облачно",
        "broken clouds": "облачно",
        "overcast clouds": "пасмурно",
        "drizzle": "мелкий дождь",
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
        if response.status_code == 200:
            data = response.json()
            weather = translate_weather_description(data['weather'][0]['description'])
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            visibility = data['visibility'] / 1000  # переводим в километры

            return (f"Погода в {city}:\n"
                    f"{weather}\n"
                    f"Температура: {temperature}°C\n"
                    f"Влажность: {humidity}%\n"
                    f"Скорость ветра: {wind_speed} м/с\n"
                    f"Видимость: {visibility} км")
        else:
            return "Город не найден или произошла ошибка."
    except requests.exceptions.ReadTimeout:
        return "Время ожидания истекло."
    except requests.exceptions.RequestException as e:
        return f"Ошибка запроса: {e}"

def fetch_weather(city, api_key):
    weather_info = get_weather(city, api_key)
    update_weather_label(weather_info)

def update_weather_label(weather_info):
    weather_label.config(text=weather_info)

def show_retry_button(city, api_key):
    retry_window = tk.Toplevel(root)
    retry_window.title("Ошибка")
    retry_window.configure(background="#FFCCCC")

    error_label = tk.Label(retry_window, text="Время ожидания истекло. Попробуйте снова.", bg="#FFCCCC")
    error_label.pack(padx=10, pady=10)

    retry_button = tk.Button(retry_window, text="Повторить", command=lambda: retry_request(city, api_key, retry_window), bg="#FFCCCC")
    retry_button.pack(padx=10, pady=10)

def retry_request(city, api_key, retry_window):
    threading.Thread(target=fetch_weather, args=(city, api_key)).start()
    retry_window.destroy()

def show_weather():
    city = city_entry.get()
    api_key = "a041a61deb2966764e5c913c10270375"
    
    if city:
        threading.Thread(target=fetch_weather, args=(city, api_key)).start()
    else:
        update_weather_label("Пожалуйста, введите название города.")

def exit_program():
    root.quit()

root = tk.Tk()
root.title("Погода")
root.configure(background="#AFEEEE")

city_label = tk.Label(root, text="Введите название города:", bg="#AFEEEE")
city_label.pack(padx=10, pady=10)

city_entry = tk.Entry(root, width=30)
city_entry.pack(padx=10, pady=10)

button = tk.Button(root, text="Посмотреть прогноз", command=show_weather, bg="#FFFFFF")
button.pack(padx=10, pady=10)

weather_label = tk.Label(root, text="", bg="#AFEEEE", wraplength=400)
weather_label.pack(padx=10, pady=10)

exit_button = tk.Button(root, text="Выход", command=exit_program, bg="#FFCCCC")
exit_button.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=10)

root.mainloop()
