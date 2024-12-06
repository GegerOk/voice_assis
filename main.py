import pyttsx3
import speech_recognition as sr
import sounddevice as sd
import requests
from tkinter import *
from tkinter import ttk
import subprocess
import threading



engine = pyttsx3.init()

recognizer = sr.Recognizer()

def speak(text):
    engine.say(text)
    engine.runAndWait()

#Отдача команд ассистенту
def listen():
    with sr.Microphone() as source:
        label["text"] = "Скажите что-то..."
        label.update()
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language='ru-RU')
            label["text"] = f"Вы сказали: {command}"
            return command
        except sr.UnknownValueError:
            label["text"] = "Не удалось распознать речь"
            return None
        except sr.RequestError:
            label["text"] = "Ошибка соединения с сервисом распознавания"
            return None

#Функция записи звука в .wav файл
def record_audio(filename='output.wav', duration=5):
    print(f"Запись звука в {filename}...")
    fs = 44100  # Частота дискретизации
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
    sd.wait()  # Ожидание окончания записи
    # Сохранение записанных данных в файл
    from scipy.io.wavfile import write
    write(filename, fs, audio_data)
    print(f"Запись завершена. Файл сохранен как {filename}.")

# Цикл обработки команд
def v_a(name):
    while True:
        x = 0
        x += 1
        if x == 1:
            speak(f"Доброго дня{name}")
        command = listen()
        if command:
            response = ""  # Накопление ответа
            if "погода" in command:
                command = command.replace('погода', '')
                speak('В каком городе?')
                city = listen()  # Запрос города
                if city:
                    url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
                    weather_data = requests.get(url).json()
                    if weather_data.get('cod') != 200:
                        response = "Не удалось получить данные о погоде. Проверьте название города."
                    else:
                        # В случае успеха, говорит фактическую температуру и по ощущениям 
                        temperature = round(weather_data['main']['temp'])
                        temperature_feels = round(weather_data['main']['feels_like'])
                        response = f"Погода сейчас: {temperature} градусов, по ощущению: {temperature_feels}."
                        speak(response)
                        label['text'] = f"{city}: {response}"
                        label.update()
                else:
                    response = "Не удалось распознать город. Пожалуйста, повторите."
            elif "записать звук" in command:
                command = command.replace('записать звук', '')
                response = "Запись звука на 5 секунд."
                record_audio(duration=5)  # Запись звука на 5 секунд
            elif "включить музыку" in command:
                command = command.replace('включить музыку', '')
                response = "Включаю вашу любимую музыку."
                speak(response)
                # Запуск приложения для воспроизведения музыки
                try:
                    subprocess.Popen(["C:/Users/"])  # Укажите путь к вашему приложению
                except Exception as e:
                    label["text"] = f"Не удалось открыть приложение: {e}"
                    print ({e})
            elif "выход" in command:
                response = f"До свидания {name}!"
                speak(response)
                root.destroy()
                break
            else:
                response = "Извините, я не понял команду."

            if response:
                pass

#Запуск отдельного потока для основного цикла 
def start_voice_assistant():
    name = name_entry.get()
    threading.Thread(target=v_a, args=(name,)).start()


if __name__ == '__main__':
    root = Tk()
    root.title("Voice Assistant")
    root.geometry("300x250")

    label = ttk.Label(root, text="")
    label.pack(pady=20)

    name_entry = ttk.Entry(root)
    name_entry.pack(pady=10)

    btn = ttk.Button(root, text="Начать", command=start_voice_assistant)
    btn.pack(pady=10)

    root.mainloop()