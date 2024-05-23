import pandas as pd
from osgeo import gdal
import netCDF4
import numpy as np
import os
import openpyxl

def crop_proxy_excelwithsheet(crop:str, file_path: str, sheet_name: str ,level:int=1):
    '''
    crop_mapping_file should be something like
    crop_mapping_file = pd.read_excel([path_file], sheet_name = [sheet_name], index_col = 0)
    '''
    crop_mapping_file = pd.read_excel(file_path, sheet_name = sheet_name, index_col = 0)
    return(crop_mapping_file.loc[crop,"Level_"+str(level)])

def get_pest_background_data(input_lat: float, input_lon: float, crop: str, path_to_folder: str):
    df_list = []
    for filename in os.listdir(path_to_folder):
        # Check if the file is a .nc file
        if filename.endswith('.nc') and crop in filename:
            # Open the file
            ds = netCDF4.Dataset(path_to_folder + filename, 'r')
    
            # identify the correct grid element
            lat_var = ds.variables['lat'][:]
            lon_var = ds.variables['lon'][:]
            lat_idx = np.argmin(np.abs(lat_var - input_lat))
            lon_idx = np.argmin(np.abs(lon_var - input_lon))
    
            try:
                # Get the raster data (assuming it's in the same variable)
                high_est = ds.variables['apr_H'][:].data[1]
    
                # Get the local value (using the same lat and lon coordinates)
                local_high_value = high_est[lat_idx, lon_idx]
            except KeyError:
                local_high_value = np.NaN
    
            try:
                # Get the raster data (assuming it's in the same variable)
                low_est = ds.variables['apr_L'][:].data[1]
    
                # Get the local value (using the same lat and lon coordinates)
                local_low_value = low_est[lat_idx, lon_idx]
            except KeyError:
                local_low_value = np.NaN
                
            
            # Create a new DataFrame for each iteration
            new_df = pd.DataFrame({'filename': [filename], 'local_high_value': [local_high_value], 'local_low_value': [local_low_value]})
    
            # Append the new DataFrame to the list
            df_list.append(new_df)
            
            # Close the file
            ds.close()
    
    # Concatenate the DataFrames in the list
    df = pd.concat(df_list, ignore_index=True)

    sep = crop + "_"
    df[['crop_name', 'pesticide_name']] = df['filename'].str.split(sep, n=1, expand=True)
    df['pesticide_name'] = df['pesticide_name'].str.rstrip('.nc')
    df = df.drop(['filename', 'crop_name'], axis=1)
    df = df.loc[:, ['pesticide_name', 'local_low_value', 'local_high_value']]

    return df