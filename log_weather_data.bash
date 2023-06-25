#!/usr/bin/env bash
# Run weather forecast data retrieval jobs

source /Users/billtubbs/opt/anaconda3/bin/activate
conda activate torch

dir=/Users/billtubbs/weather-logger/
cd $dir

# Vancouver forecast
python weather_logger.py

# Sechelt, BC forecast
python weather_logger.py -p BC -i 317

# Collins Bay, SK forecast
python weather_logger.py -p SK -i 369

cd ~
conda deactivate
