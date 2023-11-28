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
    draw = ImageDraw.Draw(image)

    # Set variables to clean up the draw.text section
    forecast_data = data['forecast']['forecastday']

    # current day variables
    current = data['current']
    date_str0 = current['last_updated']
    date_obj0 = datetime.strptime(date_str0.split()[0], '%Y-%m-%d')
    f_date0 = date_obj0.strftime('%A, %d-%b-%Y')
    temp0_f = str(current['temp_f']) + u'\N{DEGREE SIGN}F'
    feelslike = 'Feels: ' + str(current['feelslike_f']) + 'F'
    cond0 = current['condition']['text']
    precip0 = 'Precip: ' + str(current['precip_in'])
    wind0 = 'Wind: ' + str(current['wind_mph']) + ' mph'
    windd0 = 'Wind: ' + str(current['wind_dir'])

    # day 1 variables
    day1 = forecast_data[1]['day']
    date_str1 = forecast_data[1]['date']
    date_obj1 = datetime.strptime(date_str1, '%Y-%m-%d')
    f_date1 = date_obj1.strftime('%A, %d-%b-%Y')
    maxtemp1 = 'H: ' + str(day1['maxtemp_f']) + u'\N{DEGREE SIGN} F'
    mintemp1 = 'L: ' + str(day1['mintemp_f']) + u'\N{DEGREE SIGN} F'
    cond1 =  day1['condition']['text']
    wind1 = 'Wind: ' + str(day1['maxwind_mph']) + ' mph'
    if day1['daily_chance_of_snow'] != 0:
      precip_t1 = "Snow: "
      precip_v1 = day1['daily_chance_of_snow']
    else:
      precip_t1 = "Rain: "
      precip_v1 = day1['daily_chance_of_rain']
    precip1 = precip_t1 + str(precip_v1)

    # day 2 variables
    day2 = forecast_data[2]['day']
    date_str2 = forecast_data[2]['date']
    date_obj2 = datetime.strptime(date_str2, '%Y-%m-%d')
    f_date2 = date_obj2.strftime('%A, %d-%b-%Y')
    maxtemp2 = 'H: ' + str(day2['maxtemp_f']) + u'\N{DEGREE SIGN} F'
    mintemp2 = 'L: ' + str(day2['mintemp_f']) + u'\N{DEGREE SIGN} F'
    cond2 =  day2['condition']['text']
    wind2 = 'Wind: ' + str(day2['maxwind_mph']) + ' mph'
    if day2['daily_chance_of_snow'] != 0:
      precip_t2 = "Snow: "
      precip_v2 = day2['daily_chance_of_snow']
    else:
      precip_t2 = "Rain: "
      precip_v2 = day2['daily_chance_of_rain']
    precip2 = precip_t2 + str(precip_v2)

    # day 3 variables
    day3 = forecast_data[3]['day']
    date_str3 = forecast_data[3]['date']
    date_obj3 = datetime.strptime(date_str3, '%Y-%m-%d')
    f_date3 = date_obj3.strftime('%A, %d-%b-%Y')
    maxtemp3 = 'H: ' + str(day3['maxtemp_f']) + u'\N{DEGREE SIGN} F'
    mintemp3 = 'L: ' + str(day3['mintemp_f']) + u'\N{DEGREE SIGN} F'
    cond3 =  day3['condition']['text']
    wind3 = 'Wind: ' + str(day3['maxwind_mph']) + ' mph'
    if day3['daily_chance_of_snow'] != 0:
      precip_t3 = "Snow: "
      precip_v3 = day3['daily_chance_of_snow']
    else:
      precip_t3 = "Rain: "
      precip_v3 = day3['daily_chance_of_rain']
    precip3 = precip_t3 + str(precip_v3)

    # Draw section to print the data to the screen
    # Current weather data
    draw.text((163, 20), f_date0, fill=white, font=font20)
    draw.text((146, 55), temp0_f, fill=white, font=font90)
    draw.text((163, 170), feelslike, fill=white, font=font30)
    draw.text((556, 20), cond0, fill=white, font=font30)
    draw.text((556, 55), precip0, fill=white, font=font30)
    draw.text((556, 90), wind0, fill=white, font=font30)
    draw.text((556, 125), windd0, fill=white, font=font30)

    # day 1
    draw.text((36, 250), f_date1, fill=white, font=font20)
    draw.text((36, 285), maxtemp1, fill=white, font=font20)
    draw.text((36, 320), mintemp1, fill=white, font=font20)
    draw.text((36, 355), cond1, fill=white, font=font20)
    draw.text((36, 390), precip1, fill=white, font=font20)
    draw.text((36, 425), wind1, fill=white, font=font20)

    # day 2
    draw.text((301, 250), f_date2, fill=white, font=font20)
    draw.text((301, 285), maxtemp2, fill=white, font=font20)
    draw.text((301, 320), mintemp2, fill=white, font=font20)
    draw.text((301, 355), cond2, fill=white, font=font20)
    draw.text((301, 390), precip2, fill=white, font=font20)
    draw.text((301, 425), wind2, fill=white, font=font20)

    # day 3
    draw.text((566, 250), f_date3, fill=white, font=font20)
    draw.text((566, 285), maxtemp3, fill=white, font=font20)
    draw.text((566, 320), mintemp3, fill=white, font=font20)
    draw.text((566, 355), cond3, fill=white, font=font20)
    draw.text((566, 390), precip3, fill=white, font=font20)
    draw.text((566, 425), wind3, fill=white, font=font20)

    epd.display(epd.getbuffer(image))
    epd.sleep()
  except IOError as e:
    print(e)
  except KeyboardInterrupt:
    epd7in5_V2.epdconfig.module_exit()
    exit()

# Making the API call and displaying the data
while True:
  try:
    response = requests.get(URL)
    if response.status_code == 200:
      data = response.json()
      display_weather_data(epd, image_path, font20, data)
    else:
      print("Failed to retrieve data:", response.status_code)
  except requests.exceiptions.RequestException as e:
    print("Connection error:", e)

  time.sleep(14400)
