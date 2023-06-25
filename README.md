# weather-logger
Pythons script to log Environment Canada weather forecast data to file every hour.

Run the script [weather_logger.py](weather_logger.py) from the command line as follows:

```bash
python weather_logger.py -p BC -i 317
```

If no arguments are passed, it will log data for Vancouver, BC.

This will create a csv file in a sub-directory called 'data' with the current hourly forecast (24 hours ahead) for BC weather station 317 (Sechelt).

If you run this every hour, it will append new data to the csv file.

The csv file contains the following information.
```
Date,Hour,Time,Current actual,Start hour,End hour,F00,F01,F02,F03,F04,F05,F06,F07,F08,F09,F10,F11,F12,F13,F14,F15,F16,F17,F18,F19,F20,F21,F22,F23
2023-06-24,19,19:17,17.3,20,19,20,18,17,15,14,14,13,13,12,12,13,15,16,17,18,19,20,21,22,23,24,25,24,24
```
