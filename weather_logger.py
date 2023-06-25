# Python script to download EC weather forecast and actuals

import os
from time import sleep
import datetime
import asyncio
import argparse
import pandas as pd
from env_canada import ECWeather

import logging

parser = argparse.ArgumentParser(
    description="Log weather forecast data from Environment Canada"
)
parser.add_argument('-p', '--prov', default='BC', help="Province code, default: 'BC'.")
parser.add_argument('-i', '--stn', type=int, default=141, help="Station ID number, default: 141 (Vancouver).")
args = parser.parse_args()

logging.basicConfig(
    filename='weather_logger.log', 
    filemode='w', 
    format='%(name)s - %(levelname)s - %(message)s'
)

# Station id used by EC, e.g. 
station_id = f"{args.prov:s}/s{args.stn:07d}"

# For list of stations see this link:
# https://dd.weather.gc.ca/citypage_weather/docs/site_list_towns_en.csv

# Set up directory where files are stored
data_dir = "data"
if not os.path.exists(data_dir):
    os.mkdir(data_dir)

now = datetime.datetime.now()
date = now.date()
date_string = date.strftime('%Y-%m-%d')
time_now_string = now.time().strftime("%H:%M")

# Note: a new file is started each day (so they don't get too big)
filenames = {
    s: f"{s}_{args.prov:s}_{args.stn:07d}_{date_string:s}.csv"
    for s in ['temp_fcast', 'precip_fcast', 'conds_fcast']
}
# TODO: Implement logging of precipitation and conditions forecast

# Initialize API for accessing Env. Canada data
ec = ECWeather(station_id=station_id)
logging.info("Logging data for station_id: %s", station_id)

while True:
    filename = filenames['temp_fcast']
    filepath = os.path.join(data_dir, filename)

    if os.path.exists(filepath):
        existing_data = pd.read_csv(filepath, index_col=0)
        if now.hour in existing_data['Hour'].values:
            # Data already saved
            break
        kwargs = dict(mode='a', index=False, header=False)
    else:
        existing_data = None
        kwargs = dict(mode='w', index=False)

    # Get latest data
    asyncio.run(ec.update())

    # Prepare new row of data for CSV
    new_data = {
        'Date': date_string,
        'Hour': now.hour,
        'Time': time_now_string
    }

    # Add current temperature
    current_conditions = pd.Series(ec.conditions)
    new_data['Current actual'] = current_conditions.temperature['value']

    for _ in range(5):  # Make up to 5 attempts to get forecast data

        hourly_forecasts = pd.DataFrame(ec.hourly_forecasts).set_index('period')
        hourly_forecasts.index = hourly_forecasts.index.tz_convert(now.astimezone().tzinfo)

        # Save temperature forecast
        new_data['Start hour'] = hourly_forecasts.index.hour[0]
        new_data['End hour'] = hourly_forecasts.index.hour[-1]

        # Check that forecast is new (sometimes it is delayed)
        if new_data['Start hour'] == new_data['Hour'] + 1:
            break
        sleep(60)
        asyncio.run(ec.update())

    else:
        logging.warning('New temp. forecast not found after 5 attempts')
        hourly_forecasts[:] = None

    columns = [f"F{i:02d}" for i in range(24)]
    for name, value in zip(columns, hourly_forecasts.temperature):
        new_data[name] = value

    # Save to CSV
    new_data = pd.DataFrame(new_data, index=[0])
    new_data.to_csv(filepath, **kwargs)

    break
