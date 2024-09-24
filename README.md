# week3-getOuttaTown

A Python program fighting SAD by informing users of the sunrise/sunset times and day lengths of must-see destinations worldwide.

# Overview

As someone living in New York City at this time of year, it's hard not to start thinking about escaping the hustle and bustle. Not only is the temperature getting cooler, but the days are getting shorter, and it's quite evident. This program seeks to help people knock destinations off of their bucket lists which might provide refuge from the shrinking daylight of East Coast USA.

It first scrapes a travel blog listing "100 Places to Go Before You Die" to provide a baseline set of places to search. Then, it converts the place names from the article to coordinates and uses those coordinates to call a Sunrise/Sunset API. Finally, it assembles a dataframe with place names, lat/long coordinates, and times/durations of days.

# APIs Used

The program uses the Sunrise/Sunset API, which can be found at https://sunrise-sunset.org/api. This API does not require a key or any form of authentication.

# Setup Instructions

First, set up a Python virtual environment by first running "python -m venv .venv" then running

".venv\Scripts\activate" on Windows
"source .venv/bin/activate" on Mac
Verify that the terminal prefix is (.venv) to demonstrate that you have successfully set up the virtual environment. Then, install the necessary packages listed in requirements.txt with "pip install -r requirements.txt".

Finally, run the program using the command "python3 main.py"

# Usage

When the program is run, it will generate a CSV file with the destinations and their respective datapoints, along with printing out a head showing the five locations with the longest days.

# Prerequisites

Installation of the required libraries and Python 3.9 or above.

# Notes

All of the times are returned in UTC by default, which I found strange. In future iterations, I would likely seek to standardize these times based on the local timezones of the locations being searched for slightly more useful information to be available.
