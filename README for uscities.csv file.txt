README for uscities.csv file
A simple data file containing information about all U.S. cities, including 14 fields (listed below) and 30,844 rows (number of cities included). Note that there are repeat names of cities (such as Paris, Texas, Paris, Kentucky, Paris, Ohio, etc.). For geographic mapping, there a both county fips values as well and latitude and longitude values.  

Sources
	https://simplemaps.com/data/us-cities
	https://www.kaggle.com/datasets/sergejnuss/united-states-cities-database/

Fields
	city: The name of the city/town.
	city_ascii: city as an ASCII string.
	state_id: The state or territory's USPS postal abbreviation.
	state_name: The name of the state or territory that contains the city/town.
	county_fips: The 5-digit FIPS code for the primary county. The first two digits correspond to the state's FIPS code.
	county_name: The name of the primary county (or equivalent) that contains the city/town.
	lat: The latitude of the city/town.
	lng: The longitude of the city/town.
	population: An estimate of the city's urban population. (2019).
	density: The estimated population per square kilometer.
	military: TRUE if this place is a military establishment such as a fort or base.
	incorporated: TRUE if the place is a city/town. FALSE if the place is just a commonly known name for a populated area.
	timezone: The city's time zone in the tz database format. (e.g. America/Los_Angeles)
	zips: A string containing all five-digit zip codes in the city/town, delimited by a space.