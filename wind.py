import netCDF4
import pandas as pd
import numpy as np
# import xarray as xr
import datetime
import os
import csv

#opening one file to practice
# filepath = "/media/rina/Seagate Backup Plus Drive/merra2/tavg1_2d_lfo_Nx/"
# filename = "MERRA2_100.tavg1_2d_lfo_Nx.19910101.nc4.nc4"
# mf = netCDF4.Dataset(filepath+filename, "r", format="NETCDF4")

fp = "/media/sf_E_DRIVE/merra2/wind/"
# output = "/media/sf_E_DRIVE/merra2/wind.csv"
output = "/media/sf_E_DRIVE/merra2/wind_RJA.csv"
# mf = xr.open_mfdataset("/media/rina/Seagate Backup Plus Drive/practicemerra/*.nc4", concat_dim="time")

#make dataframe to turn into csv
f_csv = pd.DataFrame(columns = ['date', 'V10M', 'U10M'])

#opening all files (true run)
failed_list = []
temp_files = os.listdir("/media/sf_E_DRIVE/merra2/wind/")
files = []
for temp_file in temp_files:
    files.append(temp_file)

for file in files:
    try:
        mf = netCDF4.Dataset(fp+file)
        print(file)

        #setting stuff
        keys = mf.variables.keys()
        V10M = mf.variables['V10M']
        U10M = mf.variables['U10M']
        lat = mf.variables['lat']
        lon = mf.variables['lon']
        time = mf.variables['time']

        # ftime = netCDF4.num2date(time[:], time.units, only_use_cftime_datetimes=False)

        for hr in range(0, 23):
            hour_dt = netCDF4.num2date(time[hr], time.units, only_use_cftime_datetimes=False)
            hour_str = datetime.datetime.strftime(hour_dt, '%Y-%m-%dT%H:%M:%S')
            
            #hour lat lon
            # -11, -62.5
            # hr_V10M = (V10M[hr][5][6])
            # hr_U10M = (U10M[hr][5][6])
            # -10, -61.875
            hr_V10M = (V10M[hr][7][7])
            hr_U10M = (U10M[hr][7][7])



            new_row = pd.Series({'date': hour_str, 'V10M': hr_V10M, 'U10M': hr_U10M})
            f_csv = f_csv.append(new_row, ignore_index=True)
            # print(len(f_csv))


    except:
        print("FAILED")
        failed_list.append(file)

        pass

# export data to csv
f_csv.to_csv(output)
print("Failed files: ")
for item in failed_list:
    print (item)
