################################################
# Python script to retrieve a weather forecast #
# and print it to an e-Paper Driver hat for    #
# Raspberry Pi.                                #
# Written by Joseph Oaks                       #
# 24 Nov 2023                                  #
# Version 0.9                                  #
################################################
import requests
import json
import os
import sys
from datetime import datetime
import time
from PIL import Image, ImageDraw, ImageFont

# Replace with your actual API, Location (Zip, Long/Lat, City Name, auot:ip, etc)
# http://api.weatherapi.com/v1/forecast.json?key='API_KEY'&q='LOCATION'&days='DAYS'&aqi='AQI'&alerts='ALERTS'
BASE_URL = 'http://api.weatherapi.com/v1/forecast.json?'
API_KEY = 'INSERT YOUR API'
LOCATION = 'SET YOUR LOCATION'
DAYS = '4'
AQI = 'no'
ALERTS = 'no'
URL = BASE_URL + '&key=' + API_KEY + '&q=' + LOCATION + '&days=' + DAYS + '&aqi=' + AQI + '&alerts=' + ALERTS

# Directory and font setup
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
image_path = os.path.join(picdir, 'template.png')
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'font')
font20 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 20)
font30 = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 30)
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

        forecast_data = data['forecast']['forecastday']

        # Current weather data
        date_str = data['current']['last_updated']
        date_obj = datetime.strptime(date_str.split()[0], '%Y-%m-%d')
        formatted_date = date_obj.strftime('%A, %d-%b-%Y')
        draw.text((163, 20), f"{formatted_date}", fill=white, font=font20)
        draw.text((146, 55), f"{data['current']['temp_f']} F", fill=white, font=font90)
        draw.text((163, 170), f"Feels like {data['current']['feelslike_f']} F", fill=white, font=font30)
        draw.text((556, 20), f"{data['current']['condition']['text']}", fill=white, font=font30)
        draw.text((556, 55), f"Precip: {data['current']['precip_in']}", fill=white, font=font30)
        draw.text((556, 90), f"Wind: {data['current']['wind_mph']} MPH", fill=white, font=font30)
        draw.text((556, 125), f"Wind: {data['current']['wind_dir']}", fill=white, font=font30)

        # 3-day forecast weather data
        y_position = 250
        date_str = forecast_data[1]['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%A, %d-%b-%Y')
        draw.text((36, y_position), f"{formatted_date}", fill=white, font=font20)
        y_position += 35
        draw.text((36, y_position), f"H: {forecast_data[1]['day']['maxtemp_f']}", fill=white, font=font20)
        y_position += 35
        draw.text((36, y_position), f"L: {forecast_data[1]['day']['mintemp_f']}", fill=white, font=font20)
        y_position += 35
        draw.text((36, y_position), f"Condition: {forecast_data[1]['day']['condition']['text']}", fill=white, font=font20)
        y_position += 35
        if forecast_data[1]['day']['daily_chance_of_snow'] != 0:
          precip_type = "Snow"
          precip_value = forecast_data[1]['day']['daily_chance_of_snow']
        else:
          precip_type = "Rain"
          precip_value = forecast_data[1]['day']['daily_chance_of_rain']
        draw.text((36, y_position), f"{precip_type}: {precip_value}%", fill=white, font=font20)
        y_position += 35
        draw.text((36, y_position), f"Wind: {forecast_data[1]['day']['maxwind_mph']}", fill=white, font=font20)

        y_position = 250
        date_str = forecast_data[2]['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%A, %d-%b-%Y')
        draw.text((301, y_position), f"{formatted_date}", fill=white, font=font20)
        y_position += 35
        draw.text((301, y_position), f"H: {forecast_data[2]['day']['maxtemp_f']}", fill=white, font=font20)
        y_position += 35
        draw.text((301, y_position), f"L: {forecast_data[2]['day']['mintemp_f']}", fill=white, font=font20)
        y_position += 35
        draw.text((301, y_position), f"Condition: {forecast_data[2]['day']['condition']['text']}", fill=white, font=font20)
        y_position += 35
        if forecast_data[2]['day']['daily_chance_of_snow'] != 0:
          precip_type = "Snow"
          precip_value = forecast_data[2]['day']['daily_chance_of_snow']
        else:
          precip_type = "Rain"
          precip_value = forecast_data[2]['day']['daily_chance_of_rain']
        draw.text((301, y_position), f"{precip_type}: {precip_value}%", fill=white, font=font20)
        y_position += 35
        draw.text((301, y_position), f"Wind: {forecast_data[1]['day']['maxwind_mph']}", fill=white, font=font20)

        y_position = 250
        date_str = forecast_data[3]['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%A, %d-%b-%Y')
        draw.text((566, y_position), f"{formatted_date}", fill=white, font=font20)
        y_position += 35
        draw.text((566, y_position), f"H: {forecast_data[3]['day']['maxtemp_f']}", fill=white, font=font20)
        y_position += 35
        draw.text((566, y_position), f"L: {forecast_data[3]['day']['mintemp_f']}", fill=white, font=font20)
        y_position += 35
        draw.text((566, y_position), f"Condition: {forecast_data[3]['day']['condition']['text']}", fill=white, font=font20)
        y_position += 35
        if forecast_data[3]['day']['daily_chance_of_snow'] != 0:
          precip_type = "Snow"
          precip_value = forecast_data[3]['day']['daily_chance_of_snow']
        else:
          precip_type = "Rain"
          precip_value = forecast_data[3]['day']['daily_chance_of_rain']
        draw.text((566, y_position), f"{precip_type}: {precip_value}%", fill=white, font=font20)
        y_position += 35
        draw.text((566, y_position), f"Wind: {forecast_data[1]['day']['maxwind_mph']}", fill=white, font=font20)

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
  time.sleep(14400)
