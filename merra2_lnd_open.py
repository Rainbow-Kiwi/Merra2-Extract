import netCDF4
import pandas as pd
import numpy as np
# import xarray as xr
import datetime
import os
import csv

#opening one file to practice
# filepath = "/media/rina/Seagate Backup Plus Drive/merra2/tavg1_2d_lnd_Nx/"
# filename = "MERRA2_100.tavg1_2d_lnd_Nx.19910101.nc4.nc4"
# mf = netCDF4.Dataset(filepath+filename, "r", format="NETCDF4")

fp = "/media/rina/Seagate Backup Plus Drive/merra2/tavg1_2d_lnd_Nx/"
output = "/media/rina/Seagate Backup Plus Drive/merra2/tavg1_2d_lnd_Nx_data_point.csv"
# mf = xr.open_mfdataset("/media/rina/Seagate Backup Plus Drive/practicemerra/*.nc4", concat_dim="time")

#make dataframe to turn into csv
f_csv = pd.DataFrame(columns = ['date', 'SWLAND', 'PRECTOTLAND', 'LHLAND', 'SHLAND', 'GWETTOP', 'LWLAND', 'EVLAND', 'LAI', 'GWETROOT', 'RZMC'])

#opening all files (true run)
failed_list = []
temp_files = os.listdir("/media/rina/Seagate Backup Plus Drive/merra2/tavg1_2d_lnd_Nx/")
files = []
for temp_file in temp_files:
    files.append(temp_file)

for file in files:
    try:
        mf = netCDF4.Dataset(fp+file)
        print(file)

        #setting stuff
        keys = mf.variables.keys()
        SWLAND = mf.variables['SWLAND']
        PRECTOTLAND = mf.variables['PRECTOTLAND']
        LHLAND = mf.variables['LHLAND']
        SHLAND = mf.variables['SHLAND']
        GWETTOP = mf.variables['GWETTOP']
        LWLAND = mf.variables['LWLAND']
        EVLAND = mf.variables['EVLAND']
        LAI = mf.variables['LAI']
        GWETROOT = mf.variables['GWETROOT']
        RZMC = mf.variables['RZMC']
        lat = mf.variables['lat']
        lon = mf.variables['lon']
        time = mf.variables['time']

        # ftime = netCDF4.num2date(time[:], time.units, only_use_cftime_datetimes=False)

        for hr in range(0, 23):
            hour_dt = netCDF4.num2date(time[hr], time.units, only_use_cftime_datetimes=False)
            hour_str = datetime.datetime.strftime(hour_dt, '%Y-%m-%dT%H:%M:%S')
            hr_SWLAND = (SWLAND[hr][7][7])
            hr_PRECTOTLAND = (PRECTOTLAND[hr][7][7])
            hr_LHLAND = (LHLAND[hr][7][7])
            hr_SHLAND = (SHLAND[hr][7][7])
            hr_GWETTOP = (GWETTOP[hr][7][7])
            hr_LWLAND = (LWLAND[hr][7][7])
            hr_EVLAND = (EVLAND[hr][7][7])
            hr_LAI = (LAI[hr][7][7])
            hr_GWETROOT = (GWETROOT[hr][7][7])
            hr_RZMC = (RZMC[hr][7][7])

            new_row = pd.Series({'date': hour_str, 'SWLAND': hr_SWLAND, 'PRECTOTLAND': hr_PRECTOTLAND, 'LHLAND': hr_LHLAND, 'SHLAND': hr_SHLAND, 'GWETTOP': hr_GWETTOP, 'LWLAND': hr_LWLAND, 'EVLAND': hr_EVLAND, 'LAI': hr_LAI, 'GWETROOT': hr_GWETROOT, 'RZMC': hr_RZMC})
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
