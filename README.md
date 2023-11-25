# e-Paper Forecaster

This project is intended to display the current weather and 3 day forecast.

For this project I choose to use <https://www.weatherapi.com>

## Instructions

1. Create an account at <https://www.weatherapi.com>
2. Copy your API Key and insert it into `forecast.py`.
3. Set your interval for refresh, currently set to every 4 hours, change it as you see fit.
     this setting is the `time.sleep(14400)`
4. The days are set to 4, this gives the current day + 3 days of forecast.
5. Run `python forecast.py` or to put in the background `nohup python forecast.py &`.
