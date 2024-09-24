import requests
from bs4 import BeautifulSoup
import pandas as pd
from geopy.geocoders import Nominatim
import time

# scrapes a list of "100 places to visit before you die" as the list of places to get sunrise/sunset information about
def scrapeHeader():
    response = requests.get("https://www.wanderluststorytellers.com/100-places-to-visit-before-you-die/")
    if response.status_code != 200:
        print(f'Failed to get the webpage: {response.status_code}')
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    header_list = soup.find_all('p')
    headers = [strong.getText() for p in header_list for strong in p.find_all('strong')]
    for header in headers:
        if header == "Further Reading:":
            headers.remove(header)
    return headers

# using the Nominatim library to convert place name to latitude/longitude. found a post on StackOverflow for this one
def getCoordinates(location):
    try:
        loc = Nominatim(user_agent="Geopy Library")
        getCoords = loc.geocode(location)
        coords = [getCoords.latitude, getCoords.longitude]
        return coords
    except Exception as e:
        print(f"Error getting coordinates for {location}: {e}")
    return []

# get the data from the sunrise/sunset API for sunrise time, sunset time, and day length
def sunsetTimes(lat, long):
    URL = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={long}"
    response = requests.get(URL)
    data = response.json()
    if data['status']=="OK":
        return[data['results']['sunrise'], data['results']['sunset'], data['results']['day_length']]
    else:
        print(f"Error: {data['status']}")
        return[]

# main function -- establishes lists to hold data being assembled row by row, populates those lists, and then creates and cleans the dataframe
def main():
    placeList = scrapeHeader()
    latList = []
    longList = []
    sunriseList = []
    sunsetList = []
    dayLengthList = []

    # run through coordinate and sunrise/sunset time process for each place
    for place in placeList:
        place = place.rstrip(':') # removes the colon at the end of each place name from the list
        if '/' in place: # checks for instances of locations with two countries, which otherwise have errors
            place = place.split('/')[0].strip()
        if ' and ' in place: # checks for instances of multiple locations being included in one entry
            place = place.split(' and ')[1].strip()
        coord = getCoordinates(place)
        if coord:
            lat, long = coord
            latList.append(lat)
            longList.append(long)
            times = sunsetTimes(coord[0],coord[1])
            if times:
                sunrise, sunset, day_length = times
                sunriseList.append(sunrise)
                sunsetList.append(sunset)
                durationPieces = day_length.split(':')
                durationSeconds = (int(durationPieces[0]) * 3600) + (int(durationPieces[1]) * 60) + int(durationPieces[2])
                durationHours = durationSeconds/3600
                dayLengthList.append(durationHours)
                if(len(dayLengthList) % 10 == 0):
                    print("10 items completed!") # indicates the program making progress
            else: 
                sunriseList.append(None)
                sunsetList.append(None)
                dayLengthList.append(None)
        else:
            latList.append(None)
            longList.append(None)
            sunriseList.append(None)
            sunsetList.append(None)
            dayLengthList.append(None)
        time.sleep(1)
    
    # create the dataframe holding everything
    df = pd.DataFrame({
        'Place Name': placeList,
        'Latitude': latList,
        'Longitude': longList,
        'Sunrise Time (UTC)': sunriseList,
        'Sunset Time (UTC)': sunsetList,
        'Day Length (Hours)': dayLengthList
    })
    df = df.dropna(subset=['Latitude','Longitude','Day Length (Hours)']) # get rid of rows where data has not successfully been found
    df['Latitude'] = df['Latitude'].astype(float).round(7) # round latitude to 7 digits
    df['Longitude'] = df['Longitude'].astype(float).round(7) # round longitude to 7 digits
    df['Day Length (Hours)'] = df['Day Length (Hours)'].astype(float).round(2) # round hours to 2 digits
    df = df.sort_values('Day Length (Hours)', ascending=False) # sort by the longest days (for the SAD sufferers)
    print("Here are the locations with the longest days!")
    print(df.head())

    df.to_csv('destinations.csv', index=False)


if __name__ == "__main__":
    main()