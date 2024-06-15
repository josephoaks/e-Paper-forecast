#!/usr/bin/env python3

import requests
import json
import os
import sys
from datetime import datetime
import time
from PIL import Image, ImageDraw, ImageFont

# Replace with your actual API details
BASE_URL = 'https://api.openweathermap.org/data/3.0/onecall?'
API_KEY = '<api_key>'
LAT = '<lat>'
LON = '<long>'
EXCLUDE = 'minutely,alerts'
UNITS = 'imperial'
URL = f'{BASE_URL}lat={LAT}&lon={LON}&exclude={EXCLUDE}&units={UNITS}&appid={API_KEY}'

# Directory and font setup
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
image_path = os.path.join(picdir, 'template.png')
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font')
font20 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 20)
font30 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 30)
font60 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 60)
font90 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 90)
white = 'rgb(255,255,255)'

# Initialize display
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))
from waveshare_epd import epd7in5_V2
epd = epd7in5_V2.EPD()

def display_weather_data(epd, image_path, font, data):
    try:
        epd.init()
        epd.Clear()
        image = Image.open(image_path)
        epd.display(epd.getbuffer(image))
        draw = ImageDraw.Draw(image)

        ### NEW DATA SET ###
        date_str = datetime.utcfromtimestamp(data['current']['dt']).strftime('%d-%b-%Y')
        current_temp = data['current']['temp']
        wind_speed = data['current']['wind_speed']
        weather_main = data['current']['weather'][0]['description']
        min_temp = data['daily'][0]['temp']['min']
        max_temp = data['daily'][0]['temp']['max']
        ### END DATA SET ###

        # Current weather data
        draw.text((163, 20), f"Date: {date_str}", fill=white, font=font20)
        draw.text((76, 55), f"Temp: {current_temp} F", fill=white, font=font60)
        draw.text((93, 170), f"Min: {min_temp} F, Max: {max_temp} F", fill=white, font=font30)
        draw.text((556, 20), f"Weather: {weather_main}", fill=white, font=font20)
        draw.text((556, 55), f"Wind: {wind_speed} MPH", fill=white, font=font20)

        # 3-day forecast weather data
        y_position = 250
        for i in range(1, 4):
            day = data['daily'][i]
            date_str = datetime.utcfromtimestamp(day['dt']).strftime('%A, %d-%b-%Y')
            draw.text((36 + (i - 1) * 265, y_position), f"{date_str}", fill=white, font=font20)
            y_position += 35
            draw.text((36 + (i - 1) * 265, y_position), f"H: {day['temp']['max']}", fill=white, font=font20)
            y_position += 35
            draw.text((36 + (i - 1) * 265, y_position), f"L: {day['temp']['min']}", fill=white, font=font20)
            y_position += 35
            draw.text((36 + (i - 1) * 265, y_position), f"Condition: {day['weather'][0]['description']}", fill=white, font=font20)
            y_position = 250  # Reset y_position for next column

        epd.display(epd.getbuffer(image))
        epd.sleep()
    except IOError as e:
        print(e)
    except KeyboardInterrupt:
        epd7in5_V2.epdconfig.module_exit()
        exit()

# Making the API call and displaying the data
while True:
    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()
        display_weather_data(epd, image_path, font20, data)
    else:
        print("Failed to retrieve data:", response.status_code)
    time.sleep(3600)
