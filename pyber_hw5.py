# Dependencis and set up
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Load in csv
ride_data = pd.read_csv("ride_data.csv")
city_data = pd.read_csv("city_data.csv")

# merge ride_data + city_data
ride_city_data = pd.merge(ride_data, city_data, how="left", on=["city", "city"])
ride_city_data.head()

# data uniquness check
a = len(ride_data["city"])
b = len(ride_data["city"].unique())

# Average Fare per City
per_city_fare = ride_data.groupby(["city"]).mean()["fare"]

# Number of Rides Per City
ride_per_city = ride_data.groupby(["city"]).count()["ride_id"]

################################################################
#create roundup, roundoff function
import math
def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

def rounddown(x):
    return x - (x%5)

################################################################

# create x_axis (Total Number of Rides/City)
x_axis = np.arange(0, roundup(ride_per_city.values.max())+1, 5)

# create y_axis (Average Fee)
y_axis = np.arange(rounddown(int(per_city_fare.values.min())), roundup(int(per_city_fare.values.max())+1),5)

######### Bubble Plot of Ride Sharing Data
n=len(city_data["type"].unique())
colors = cm.rainbow(np.random.rand(n))

size = city_data["driver_count"].tolist()

plt.scatter(ride_per_city, per_city_fare, s=size, color=colors)
plt.xlabel("Total Number of Rides (Per City)")
plt.ylabel("Average Fare ($)")
plt.title("Pyber Ride Sharing Data (2016)")
plt.show()


######### Total Fares by City Type

type_group = ride_city_data.groupby("type")

fare_by_type = type_group["fare"].sum()
fare_by_type_chart = fare_by_type.plot(kind='pie', figsize=(5,5))
plt.title("% of Total Fares by City Type")
plt.xlabel("")
plt.ylabel("")
plt.show()

######### Total Rides by City Type

ride_by_type = type_group["ride_id"].count()
ride_by_type_chart = ride_by_type.plot(kind='pie', figsize=(5,5))
plt.title("% of Total Rides by City Type")

plt.show()
