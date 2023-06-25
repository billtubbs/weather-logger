#!/usr/bin/env bash
# Script to Run weather forecast data retrieval jobs
#
# Instructions
#  1. Remember to make this file executable by executing:
#
#   chmod +x log_weather_data_rpi.bash
#
# 2. Then add it as a job to the crontab:
#
#   crontab -e
#

dir=/home/pi/code/weather-logger/
cd $dir

# Vancouver forecast
python weather_logger.py

# Sechelt, BC forecast
python weather_logger.py -p BC -i 317

# Collins Bay, SK forecast
python weather_logger.py -p SK -i 369

cd ~
