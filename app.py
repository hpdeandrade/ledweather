# imports
import os
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from places import *

# matplotlib configuration
plt.rcParams["font.size"] = 8
plt.rcParams["axes.axisbelow"] = True
plt.rcParams["figure.dpi"] = 100
plt.rcParams["savefig.dpi"] = 100

# map boundaries
lon_min = 302
lon_max = 320
lat_min = -32
lat_max = -14

# user inputs
places = [Miramontes, Jaragua]
grib_files = [f for f in os.listdir("./input") if f[-5:] == "grib2"]
grib_files.sort()
grib_dates = [f[12:20] for f in grib_files]

# set output table
output_table = {"date": [], "place": [], "latitude": [], "longitude": [], "prec_nearest (kg/m2)": [], "prec_interp (kg/m2)": []}

# iterate over dates and places
for date in grib_dates:

    data = xr.open_dataset(f"input/MERGE_CPTEC_{date}.grib2", engine="cfgrib")
    date_str = data.valid_time.dt.strftime("%d %B %Y").values

    for place in places:

        lat = place.lat
        lon = place.lon
        prec_nearest = round(float(data.prec.sel(latitude=lat, longitude=lon, method="nearest").values), 2)
        prec_interp = round(float(data.prec.interp(latitude=lat, longitude=lon).values), 2)

        output_table["date"].append(data.valid_time.values)
        output_table["place"].append(place.__name__)
        output_table["latitude"].append(lat)
        output_table["longitude"].append(lon)
        output_table["prec_nearest (kg/m2)"].append(prec_nearest)
        output_table["prec_interp (kg/m2)"].append(prec_interp)

        print(f"{place.__name__} on {date_str}:\nprec_nearest: {prec_nearest} kg/m2 | prec_interp: {prec_interp} kg/m2")

# save output table
output_table = pd.DataFrame(output_table)
output_table.to_csv("output.csv", index=False, encoding="utf-8")

# msg
print("Success!")