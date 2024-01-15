# Winter Watch: Winter Hacks 2024 Hackathon 

![My Image](https://i.ibb.co/8468c3w/Screenshot-2024-01-15-at-10-39-01-AM.png)


## Purpose

Winter Watch is a website that allows your experience in the winter and snow to be pleasent and safe.

## Languages and Frameworks

Winter Watch uses HTML, CSS, and JavaScript for frontend. For the backend it uses Python and Flask. It is hosted on GitHub Pages and Version Control was done through Git.

## API Usage

Winter Watch uses Google's free Maps API, this allows for searching and display of any location dynamically.

It then fetches the desired locations data and information from OpenWeatherMap API.

Google Maps: https://developers.google.com/maps
OpenWeatherMap: https://openweathermap.org/

## Key Features 

### Standard Information

All the basic information you could ask for when making a brief search for imformation about the location. This includes:

- Location
- Temperature
- Longitude
- Latitude
- Time
- Date
- Current Weather

### Safety Information

Along with that we have our own key features that you won't see often on your average website. 

We used custom algorithms to calculate our own:

#### Safety Score Algorithm
The Safety Score is calculated based on various environmental factors obtained from the weather data. The score starts at 100 and is reduced based on adverse weather conditions. The factors involved are:

Temperature: The score is reduced more as the temperature drops below 30°C. For every degree below 30°C, the score is decreased by 2 points. This reflects the increased risk in colder temperatures.

Visibility: Lower visibility conditions reduce the score. For every 1000 meters below 10,000 meters of visibility, the score is reduced. This accounts for the risks associated with poor visibility conditions.

UV Index: The score is reduced by twice the value of the UV index. A higher UV index indicates more intense sunlight, which can be hazardous.

Weather Conditions: If the current weather is rain, snow, or thunderstorm, the score is further reduced by 20 points, considering these conditions often bring additional hazards.

#### Frostbite Indicator Algorithm
The Frostbite Indicator assesses the risk of frostbite based on the current temperature and wind speed. The conditions for the indicator are:

High Risk: If the temperature is below 0°C and the wind speed is above 20 units (km/h, mph, depending on your data source), the risk of frostbite is considered high. This is due to the combined effect of cold temperature and wind chill.

Moderate Risk: If the temperature is below 0°C but the wind speed is not above 20 units, the risk is considered moderate. The low temperature alone can lead to frostbite, especially over prolonged exposure.

Low Risk: In all other conditions, the frostbite risk is considered low.
 
As well as key safety information such as:

- UV Index
- Visibility 
- Ice Warning
- Last Snow (If snow coming soon it will show future date)

# Future Features

- Road Surface Temps
- Tips Summarized with GPT?
- Community Live Updates?
- Emergeny Resource Locator

# Made By
*- Ethan Cratchley*