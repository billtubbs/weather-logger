#!/usr/bin/env bash
# Run weather forecast data retrieval jobs

dir=~/pi/code/weather-logger/
cd $dir

# Vancouver forecast
python weather_logger.py

# Sechelt, BC forecast
python weather_logger.py -p BC -i 317

# Collins Bay, SK forecast
python weather_logger.py -p SK -i 369

cd ~
