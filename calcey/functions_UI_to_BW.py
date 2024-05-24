import pandas as pd
from osgeo import gdal
import netCDF4
import numpy as np
import os
import openpyxl
from geopy.geocoders import Photon
import country_converter as coco


class calcey:

    def __init__(self):
        pass
    
    ####### lat lon country convert stuff #################
    
    def country_from_coordinates(self, Latitude: float, Longitude: float):
        lat_str = str(Latitude)
        lon_str = str(Longitude)
        geolocator = Photon(user_agent="measurements")
        location = geolocator.reverse(lat_str + "," + lon_str)
        address = location.address
        data_address = address.split(',')
        country = data_address[len(data_address)-1].lstrip().rstrip()
        return(country)
    
    
    def ISO3_country_from_coordinates(self, Latitude: float,Longitude:float):
        country = self.country_from_coordinates(Latitude, Longitude)
        country_ISO3 = coco.convert(country,to='ISO3')
        return(country_ISO3)
    
    
    ####### crop mapping #################
    
    
    def get_crop_mapping_file(self, sheet_name: str):
        crop_mapping_df = pd.read_excel("../data/Mapping_data_Calcey.xlsx", sheet_name=sheet_name, index_col = 0)
        return crop_mapping_df
    
    
    def crop_proxy_excelwithsheet(self, crop:str, sheet_name: str ,level:int=1):
        '''
        crop_mapping_file should be something like
        crop_mapping_file = pd.read_excel([path_file], sheet_name = [sheet_name], index_col = 0)
        '''
        crop_mapping_file = self.get_crop_mapping_file(sheet_name)
        return(crop_mapping_file.loc[crop,"Level_"+str(level)])
    
    
    ####### country mapping #################
    
        
    def country_fertilizer_proxy_location(self, Latitude: float, Longitude: float):
        country_ISO3 = self.ISO3_country_from_coordinates(Latitude, Longitude)
        country_mapping_file = pd.read_excel("../data/Fertilizer_mapping_country.xlsx", sheet_name = "Mapping_nearest_neighbor", index_col = 2)
        country_proxy_ISO3 = country_mapping_file.loc[country_ISO3,"iso3_nearest"][0]
        return(country_proxy_ISO3)
    
    
    
    ################## get background data ###########################
    
    def get_background_data_fert(self, Latitude: float, Longitude: float, crop:str):
        """
        Latitude, Longitude, crop
        """
        # get fetilizer data
        df_amount_fert_crop_country = pd.read_excel("../data/Ludemann2022_fertilizer_Country_clean_ISO3.xlsx")
        df_amount_fert_crop_country = df_amount_fert_crop_country.set_index(["Country_ISO3","Crop"])
    
        # get the crop mapping file
        crop_mapping_file = self.get_crop_mapping_file(sheet_name="Mapping_Fertilizer")
        
        # get country proxy in ISO 3 format
        country_proxy_ISO3 = self.country_fertilizer_proxy_location(Latitude, Longitude)
        
        try:
            return(df_amount_fert_crop_country.loc[(country_proxy_ISO3,crop)])
        except KeyError:
            for level in range(1,len(crop_mapping_file.columns)-1):
                try:
                    crop_proxy_value = self.crop_proxy_excelwithsheet(crop=crop,sheet_name="Mapping_Fertilizer",level=level)
                    return(df_amount_fert_crop_country.loc[(country_proxy_ISO3,crop_proxy_value)])
                except KeyError:
                    pass
    
    
    def get_background_data_yield(self, input_lat: float, input_lon: float, crop: str):
        # get yield data
        df = pd.read_csv("../data/FAOSTAT_data_yield.csv")
        country = self.country_from_coordinates(Latitude=input_lat, Longitude=input_lon)
        FAO_yield = float(df.loc[(df['Area'] == country) & (df['Year'] == 2022) & (df['Item'] == crop), 'Value'].iloc[0])
        return FAO_yield
    
    
    def get_background_data_water(self, input_lat: float, input_lon: float, crop: str):
        path_to_folder = "../data/NC_background_water/"
    
        crop_water = self.crop_proxy_excelwithsheet(crop=crop, sheet_name="Mapping_water")
        
        df_list = []
        for filename in os.listdir(path_to_folder):
            # Check if the file is a .nc file
            if filename.endswith('.nc') and crop_water in filename:
                # Open the file
                ds = netCDF4.Dataset(path_to_folder + filename, 'r')
        
                # identify the correct grid element
                lat_var = ds.variables['lat'][:]
                lon_var = ds.variables['lon'][:]
                lat_idx = np.argmin(np.abs(lat_var - input_lat))
                lon_idx = np.argmin(np.abs(lon_var - input_lon))
        
                try:
                    # Get the raster data (assuming it's in the same variable)
                    value = ds.variables['wf_unit_irrigated_blue'][:].data[lat_idx, lon_idx]
    
                except KeyError:
                    value = np.NaN
    
                # 1e20 is the null value in this dataset, so we have to replace it
                value = 0 if value > 10000000000000 else value
                
                # Create a new DataFrame for each iteration
                new_df = pd.DataFrame({'filename': [filename], 'value': [value]})
        
                # Append the new DataFrame to the list
                df_list.append(new_df)
                
                # Close the file
                ds.close()
        
        # Concatenate the DataFrames in the list
        df = pd.concat(df_list, ignore_index=True)
    
        sep = crop_water + "_"
        df[['crop_name', 'water_footprint']] = df['filename'].str.split(sep, n=1, expand=True)
        df['water_footprint'] = df['water_footprint'].str.rstrip('.nc')
        df = df.drop(['filename', 'crop_name'], axis=1)
        df = df.loc[:, ['water_footprint', 'value']]
    
        return df
    
    
    def get_background_data_pest(self, input_lat: float, input_lon: float, crop: str):
        """
        test
        """
        path_to_folder = "../data/NC_background_pest/"
    
        crop_pest = self.crop_proxy_excelwithsheet(crop=crop, sheet_name="Mapping_pesticides")
        
        df_list = []
        for filename in os.listdir(path_to_folder):
            # Check if the file is a .nc file
            if filename.endswith('.nc') and crop_pest in filename:
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
                    local_high_value = 0 if local_high_value == -1 else local_high_value
                except KeyError:
                    local_high_value = np.NaN
        
                try:
                    # Get the raster data (assuming it's in the same variable)
                    low_est = ds.variables['apr_L'][:].data[1]
        
                    # Get the local value (using the same lat and lon coordinates)
                    local_low_value = low_est[lat_idx, lon_idx]
                    local_low_value = 0 if local_low_value == -1 else local_low_value
                except KeyError:
                    local_low_value = np.NaN
                    
                value = (local_high_value + local_low_value) / 2
                
                # Create a new DataFrame for each iteration
                new_df = pd.DataFrame({'filename': [filename], 'value': [value]})
        
                # Append the new DataFrame to the list
                df_list.append(new_df)
                
                # Close the file
                ds.close()
        
        # Concatenate the DataFrames in the list
        df = pd.concat(df_list, ignore_index=True)
    
        sep = crop_pest + "_"
        df[['crop_name', 'pesticide_name']] = df['filename'].str.split(sep, n=1, expand=True)
        df['pesticide_name'] = df['pesticide_name'].str.rstrip('.nc')
        df = df.drop(['filename', 'crop_name'], axis=1)
        df = df.loc[:, ['pesticide_name', 'value']]
    
        return df


