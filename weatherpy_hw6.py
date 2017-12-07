# Import Dependencis
import random
import requests as req
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from citipy import citipy

plt.style.use("seaborn")

# Create DataFrame to assign random coordination through out the earth
city_df = pd.DataFrame()

city_df["Latitude"] = ""
city_df["Longitude"] = ""

# Set Randmoized Latitude and Longitude
lat = np.arange(-90,90,15)
lon = np.arange(-180,180,15)

# For each zone
for x in lat:
    for y in lon:
        decimals = list(np.arange(0,15,0.01))
        rand_decimals = random.sample(decimals,50)
        # generate random latitude and longitude
        lat_samples = [x + x_cord for x_cord in rand_decimals]
        lon_samples = [y + y_cord for y_cord in rand_decimals]
        # Assign sample latitude and longitude to city_df dataframe
        city_df = city_df.append(pd.DataFrame.from_dict({"Latitude":lat_samples,
                                       "Longitude":lon_samples}))
city_df = city_df.reset_index(drop=True)


# For selected sample coordinates, find neariest city

city_df["Nearest City"] = ""
city_df["Country Code"] = ""
for index,row in city_df.iterrows():
    city = citipy.nearest_city(row["Latitude"],row["Longitude"])
    city_df.set_value(index,"Nearest City",city.city_name)
    city_df.set_value(index,"Country Code",city.country_code)
    

# return only City, Country Code column.
city_df = city_df[["Nearest City", "Country Code"]]

# Data Cleaning Process (remove duplication)
rmdup_city_df = city_df.drop_duplicates()


rmdup_city_df = rmdup_city_df.reset_index(drop=True)

rmdup_city_df["Latitude"] = ""
rmdup_city_df["Longitude"] = ""
rmdup_city_df["Temperature"] = ""
rmdup_city_df["Wind speed"] = ""
rmdup_city_df["Humidity"] = ""
rmdup_city_df["Cloudiness"] = ""


city_list = rmdup_city_df["Nearest City"].tolist()

# Retch City Weater data from OpenWeathermap


# Save config information.
api_key = "6e4ec6141e342d84f803e57a1dbd40b4"
url = "http://api.openweathermap.org/data/2.5/weather?"
units = "metric"

# Build partial query URL
query_url = url + "appid=" + api_key + "&units=" + units + "&q="
print(query_url)

#for cities in city_list:
#    response = req.get(query_url + cities).json()
#    print("one row processed")
    
for index, row in rmdup_city_df.iterrows():
    try:
        for cities in city_list:
            response = req.get(query_url + cities).json()
            rmdup_city_df.set_value(index,"Latitude",response.get("coord",{}).get("lat"))
            rmdup_city_df.set_value(index,"Longitude",response.get("coord",{}).get("lon"))
            rmdup_city_df.set_value(index,"Temperature",response.get("main",{}).get("temp"))
            rmdup_city_df.set_value(index,"Wind speed",response.get("wind",{}).get("speed"))
            rmdup_city_df.set_value(index,"Humidity",response.get("main",{}).get("humidity"))
            rmdup_city_df.set_value(index,"Cloudiness",response.get("clouds",{}).get("all"))
        print("--",end = "")
    except:
        print("skip")

# Drop cities with missing information
final_city_df = rmdup_city_df.dropna()

final_city_df.to_csv("city_weather.csv")



# Analyzing 
def plot_setting(x_title,x_lim,y_title):
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.grid(True)
    plt.xlim(x_lim)


# 1. Temperature vs Latitude
final_city_df.plot(kind="scatter",x="Latitude",y="Temperature",grid=True,color="blue")

plot_setting("Latitude",[-90,90],"Temperature (C)")
plt.title("Latitude vs Temperature(c)")
plt.axvline(0, color='black',alpha=0.5)
plt.savefig("Temperature vs Latitude")
plt.show()

# 2. Humidity vs Latitude
final_city_df.plot(kind="scatter",x="Latitude",y="Humidity",grid=True,color="blue")

plot_setting("Latitude",[-90,90],"Humidity")
plt.title("Latitude vs Humidity(%)")
plt.axvline(0, color='black',alpha=0.5)
plt.savefig("Humidity vs Latitude")
plt.show()

# 3. Cloudiness vs Latitude
final_city_df["Cloudiness"] = pd.to_numeric(rmdup_city_df["Cloudiness"])
final_city_df.plot(kind="scatter",x="Latitude",y="Cloudiness",grid=True,color="blue")

plot_setting("Latitude",[-90,90],"Cloudiness")
plt.title("Latitude vs Cloudiness")
plt.axvline(0, color='black',alpha=0.5)
plt.savefig("Wind Speed vs Latitude")
plt.show()

# 4. Wind Speed vs Latitude
final_city_df["Wind speed"] = pd.to_numeric(rmdup_city_df["Wind speed"])
final_city_df.plot(kind="scatter",x="Latitude",y="Wind speed",grid=True,color="blue")

plot_setting("Latitude",[-90,90],"Wind speed (mph)")
plt.title("Latitude vs Wind Speed (mph)")
plt.axvline(0, color='black',alpha=0.5)
plt.savefig("Cloudiness vs Latitude")
plt.show()

# 5. Temperature approaching equator
size_temp = np.round((((final_city_df.Temperature)/100)**2)*10,2)

final_city_df.plot(kind="scatter",x="Longitude",y="Latitude",grid=True, edgecolor="black")
plt.xlabel("Longitude")
plt.tight_layout()
plt.title("Temperature")
plt.ylabel("Latitude")
plt.ylim([-85,85])
plt.grid(True)

plt.xlim([-200,200])
plt.subplots_adjust(bottom=.25, left=.25)

plt.axhline(0, color='black',alpha=0.5)
plt.savefig("Temperature vs Equator")

plt.show()