import tkinter as tk
import pandas as pd
from osgeo import gdal
import netCDF4
import numpy as np
import os
import openpyxl
from geopy.geocoders import Photon
import country_converter as coco

import bw2data as bd
import bw2calc as bc
import bw2analyzer as ba
import bw2io as bi
import numpy as np
from scipy import sparse
import uuid
from geopy.geocoders import Nominatim

import customtkinter
from tkintermapview import TkinterMapView
import panel as pn

BIOSPHERE_FLOW_DATABASE_LABELS = ["ecoinvent-3.9.1-biosphere"]

class Purolator(bi.package.BW2Package):
    @classmethod
    def _create_obj(cls, data):
        instance = data["class"](data["name"])

        if data["name"] not in instance._metadata:
            instance.register(**data["metadata"])
        else:
            instance.backup()
            instance.metadata = data["metadata"]
    
        flows = {
            (obj['database'], obj['code']) 
            for label in BIOSPHERE_FLOW_DATABASE_LABELS
            for obj in bd.Database(label)
        }
        
        if isinstance(instance, bd.Method):
            data['data'] = [line for line in data['data'] if line[0] in flows]
        
        instance.write(data["data"])
        return instance


class calcey(customtkinter.CTk):

    APP_NAME = "Calcey"
    WIDTH = 1125
    HEIGHT = 590

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.df_crops = pd.read_excel('../data/Mapping_data_Calcey.xlsx', sheet_name='Mapping_Fertilizer', usecols='A')

        self.title(calcey.APP_NAME)
        self.geometry(str(calcey.WIDTH) + "x" + str(calcey.HEIGHT))
        self.minsize(calcey.WIDTH, calcey.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)
        
        bd.projects.set_current("calcey")
            
        self.brightway_checkin()
        #self.import_method()
        # ============ create two CTkFrames ============

        self.frame_left = customtkinter.CTkFrame(master=self, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=1, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0, width=100)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        customtkinter.set_default_color_theme("blue")
        self.result_label = customtkinter.CTkLabel(self.frame_left, text="Result:", font=customtkinter.CTkFont(family="Circular Std Black", size=15))
        self.result_label.grid(row=6, column=0, padx=(10, 10), pady=(20, 0))

        self.result_entry = customtkinter.CTkEntry(self.frame_left, width=150)
        self.result_entry.grid(row=7, column=0, padx=(10, 10), pady=(5, 0))

        self.label = customtkinter.CTkLabel(self.frame_left, anchor=customtkinter.N,text="Welcome to Calcey!",  width=600, height=50, fg_color='transparent',font=customtkinter.CTkFont(family="Circular Std Black",size=30, weight="bold"))
        self.label.grid(row=0, column=0, padx=(10, 10), pady=(5, 20), columnspan=2)

        self.label2 = customtkinter.CTkLabel(self.frame_left, anchor=customtkinter.W, text="1. Please click on the map to get your coordinates.\n 2. Select the right crop.\n 3. Optional: Enter the amount for yield and fertilizer.\n 4. Press submit.",  width=500, height=50, fg_color='transparent',font=customtkinter.CTkFont(family="Circular Std Black",size=20, weight="bold"))
        self.label2.grid(row=1, column=0, padx=(10, 10), pady=(5, 30), columnspan=2)
    

        self.longitude_label = customtkinter.CTkLabel(self.frame_left, text="Longitude:", font=customtkinter.CTkFont(family="Circular Std Black", size=15))
        self.longitude_label.grid(row=2, column=0, padx=(10, 10), pady=(20, 0))

        self.latitude_label = customtkinter.CTkLabel(self.frame_left, text="Latitude:", font=customtkinter.CTkFont(family="Circular Std Black", size=15))
        self.latitude_label.grid(row=4, column=0, padx=(10, 10), pady=(20, 0))

        self.longitude_entry = customtkinter.CTkEntry(self.frame_left, width=150)
        self.longitude_entry.grid(row=3, column=0, padx=(10, 10), pady=(5, 0))

        self.latitude_entry = customtkinter.CTkEntry(self.frame_left, width=150)
        self.latitude_entry.grid(row=5, column=0, padx=(10, 10), pady=(5, 20))

        self.crop_label = customtkinter.CTkLabel(self.frame_left, text="Please select your crop", font=customtkinter.CTkFont(family="Circular Std Black", size=15))
        self.crop_label.grid(row=2, column=1, padx=(10, 10), pady=(20, 0))
        
        self.crop_entry = customtkinter.CTkOptionMenu(self.frame_left, values = list(self.df_crops['List_UI']),width=300 )
        self.crop_entry.grid(row=3, column=1, padx=(10, 10), pady=(5, 0))

        self.yield_label = customtkinter.CTkLabel(self.frame_left, text="Please enter your yield in kg/ha:", font=customtkinter.CTkFont(family="Circular Std Black", size=15))
        self.yield_label.grid(row=4, column=1, padx=(10, 10), pady=(20, 0))
        
        self.yield_entry = customtkinter.CTkEntry(self.frame_left,width=300 )
        self.yield_entry.grid(row=5, column=1, padx=(10, 10), pady=(5, 20))

        self.fertilizer_label = customtkinter.CTkLabel(self.frame_left, text="Please enter your fertilizer amount in kgN/ha:", font=customtkinter.CTkFont(family="Circular Std Black", size=15))
        self.fertilizer_label.grid(row=6, column=1, padx=(10, 10), pady=(20, 0))
        
        self.fertilizer_entry = customtkinter.CTkEntry(self.frame_left,width=300 )
        self.fertilizer_entry.grid(row=7, column=1, padx=(10, 10), pady=(5, 10))

        self.submit_button = customtkinter.CTkButton(master = self, height=50, width=1110, text="Submit", font=customtkinter.CTkFont(family="Circular Std Black", size=20, weight="bold"), command=self.print_result)
        self.submit_button.grid(column=0, row=13, columnspan=5, pady=(20, 0), padx=(0, 0))

        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=20, width=500, height=500)
        self.map_widget.add_left_click_map_command(self.get_coordinates)
        self.map_widget.grid(row=0, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))


    def get_coordinates(self, coordinates_tuple):
        longitude = coordinates_tuple[1]
        latitude = coordinates_tuple[0]
        self.longitude_entry.delete(0,"end")
        self.latitude_entry.delete(0,"end")
        self.longitude_entry.insert(0, longitude)
        self.latitude_entry.insert(0, latitude)
        marker = self.map_widget.set_marker(latitude, longitude)

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()

    def print_result(self):
        
        # get all inputs from the UI
        value_lon = float(self.longitude_entry.get())
        value_lat = float(self.latitude_entry.get())
        crop = self.crop_entry.get()
        input_yield = self.yield_entry.get()
        n_fert_input = self.fertilizer_entry.get()

        if input_yield == "":
            input_yield = None
        else:
            input_yield = float(input_yield)

        if n_fert_input == "":
            n_fert_input = None
        else:
            n_fert_input = float(n_fert_input)
        
        #value_lat = float(self.input_field_lat.get())
        #value_lon = float(self.input_field_lon.get())
        #crop = self.input_field_crop.get()
        # input_yield = self.input_field_yield.get()   n_fert_input
        
        self.create_main_process(self.name_database, value_lat, value_lon, crop)
        # yield_ = input_yield       n_fert_input
        print("create_main_process finished")
        self.dataframe_exchanges(latitude=value_lat, longitude=value_lon, crop=crop, n_fert_input=n_fert_input)
        print("dataframe_exchanges finished")
        self.generate_edges_to_product()
        print("generate_edges_to_product finished")
        self.calculate_LCA_results()
        #self.calculate_multi_LCA_results()
    
    def country_from_coordinates(self, Latitude: float, Longitude: float):
        lat_str = str(Latitude)
        lon_str = str(Longitude)
        geolocator = Nominatim(user_agent="GetLoc")
        location = geolocator.reverse(lat_str + "," + lon_str, language="en")
        print("location:" , location)
        address = location.address
        print("address:" , address)
        data_address = address.split(',')
        print("data_address:" , data_address)
        country = data_address[len(data_address)-1].lstrip().rstrip()
        country = coco.convert(country, to="name_short")
        return(country)
    
    
    def ISO3_country_from_coordinates(self, Latitude: float,Longitude:float):
        country = self.country_from_coordinates(Latitude, Longitude)
        country_ISO3 = coco.convert(country,to='ISO3')
        print(country, country_ISO3)
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
        country_mapping_file = pd.read_excel("../data/Fertilizer_mapping_country.xlsx", sheet_name = "Mapping_nearest_neighbor", index_col = 0)
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
        print(country_proxy_ISO3)
        
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

        pest_total = df['value'].sum()
        
        return df, pest_total


    def create_final_dataframe(self, yield_data, fert_data, water_data, pest_data, pest_total):
        # yield data
        yield_in_kgperha = yield_data / 10

        # fert data
        series = fert_data.drop('Country')
        df_fert = pd.DataFrame({
             'Parameter': series.index,
             'Value': series.values
        })
        df_fert = df_fert.set_index(df_fert.columns[0])
        df_fert['Value'] = df_fert['Value'] / yield_in_kgperha

        # water_data
        water_m3perkg = water_data.at[0, 'value'] / 1000

        # pest data
        pest_data['value'] = pest_data['value'] / yield_in_kgperha
        pest_data = pest_data.set_index(pest_data.columns[0])
        pest_data.index = [i.capitalize() for i in pest_data.index]

        # display(pest_data)
        
        # pest total
        pest_kgperkg = pest_total / yield_in_kgperha

        return yield_in_kgperha, df_fert, water_m3perkg, pest_data, pest_kgperkg


    def calculate_pest_emissions(self,pest_name, amount):
        # Emission factors
        EF_pest_soil = 0.9
        EF_pest_air = 0.1
        # Initialize an empty list to store the results
        results = []
        # Calculate emissions
        pest_em_soil = amount * EF_pest_soil
        pest_em_air = amount * EF_pest_air
        # Append the results as a dictionary
        results.append({
        'pesticide_name': pest_name,
        'pest_em_soil': pest_em_soil,
        'pest_em_air': pest_em_air
        })

        # Convert the results list to a DataFrame
        self.df_emissions = pd.DataFrame(results)
        self.df_emissions.set_index('pesticide_name', inplace=True)
        return self.df_emissions


    def dataframe_exchanges(self, latitude, longitude, crop, yield_ = None, n_fert_input=None, p2o5_fert_input=None, k2o_fert_input=None):
        self.mapping_flows_uuid = pd.read_excel("../data/Mapping_data_Calcey.xlsx", sheet_name = "Mapping_flows_ecoinvent", index_col =0) ## adjust path before "Mapping_data_Calcey.xlsx"
        all_inputs = list(set(self.mapping_flows_uuid.index))
        all_inputs = [x for x in all_inputs if type(x) != float]
        self.df_output = pd.DataFrame(index = all_inputs , columns = ['Amount'])
        if yield_ is None and n_fert_input is not None:
            print("There is yield input and nitrogen fertilizer input, thanks!")
            yield_data = self.get_background_data_yield(latitude,longitude,crop)
            pest_data, pest_total = self.get_background_data_pest(latitude,longitude,crop) ## add self.
            fert_data = self.get_background_data_fert(latitude,longitude,crop) ## add self.
            water_data = self.get_background_data_water(latitude,longitude,crop) ## add self.
            generic_yield, df_fert_per_kg, water_m3_per_kg, df_pest_per_kg, total_pest_per_kg = self.create_final_dataframe(yield_data,fert_data,water_data,pest_data,pest_total) ## add self.
            self.df_output.loc["Default_pesticide","Amount"] = total_pest_per_kg
            self.df_output.loc["Default_irrigation","Amount"] = water_m3_per_kg/0.8
            self.df_output.loc["Default_nitrogen_fertilizer","Amount"] = n_fert_input
            self.df_output.loc["Default_p2o5_fertilizer","Amount"] = df_fert_per_kg.loc["Mean_P2O5_applied","Value"]
            self.df_output.loc["Default_k2o_fertilizer","Amount"] = df_fert_per_kg.loc["Mean_K2O_applied","Value"]
            self.df_output.loc["Dinitrogen monoxide_to_air","Amount"] = df_fert_per_kg.loc["Mean_Emission_kg_N2O","Value"]
            self.df_output.loc["Ammonia_to_air","Amount"] = df_fert_per_kg.loc["Mean_Emission_kg_NH3","Value"]
            self.df_output.loc["Nitrate_to_water","Amount"] = df_fert_per_kg.loc["Mean_Emission_kg_NO3","Value"]
            self.df_output.loc["Nitrogen_oxides_to_air","Amount"] = df_fert_per_kg.loc["Mean_Emission_NOx","Value"]
            self.df_output.loc["Phosphate_to_water","Amount"] = df_fert_per_kg.loc["Mean_Emission_kg_P","Value"]
            list_pesticides = list(pest_data.index)
            list_compartments = ["pest_em_soil", "pest_em_air"]
            for i in list_pesticides:
                for compartment in list_compartments:
                    df_pesticides_emissions = self.calculate_pest_emissions(i,pest_data.loc[i,"value"])
                    self.df_output.loc[str(i)+""+compartment,"Amount"] = df_pesticides_emissions.loc[i,compartment]
            self.df_output = self.df_output.fillna(0)
        if yield_ is not None and n_fert_input is not None:
            print("There is yield input and nitrogen fertilizer input, thanks!")
            pest_data, pest_total = self.get_background_data_pest(latitude,longitude,crop) ## add self.
            fert_data = self.get_background_data_fert(latitude,longitude,crop) ## add self.
            water_data = self.get_background_data_water(latitude,longitude,crop) ## add self.
            generic_yield, df_fert_per_kg, water_m3_per_kg, df_pest_per_kg, total_pest_per_kg = self.create_final_dataframe(yield_,fert_data,water_data,pest_data,pest_total) ## add self.
            self.df_output.loc["Default_pesticide","Amount"] = total_pest_per_kg
            self.df_output.loc["Default_irrigation","Amount"] = water_m3_per_kg/0.8
            self.df_output.loc["Default_nitrogen_fertilizer","Amount"] = n_fert_input
            self.df_output.loc["Default_p2o5_fertilizer","Amount"] = df_fert_per_kg.loc["Mean_P2O5_applied","Value"]
            self.df_output.loc["Default_k2o_fertilizer","Amount"] = df_fert_per_kg.loc["Mean_K2O_applied","Value"]
            self.df_output.loc["Dinitrogen monoxide_to_air","Amount"] = df_fert_per_kg.loc["Mean_Emission_kg_N2O","Value"]
            self.df_output.loc["Ammonia_to_air","Amount"] = df_fert_per_kg.loc["Mean_Emission_kg_NH3","Value"]
            self.df_output.loc["Nitrate_to_water","Amount"] = df_fert_per_kg.loc["Mean_Emission_kg_NO3","Value"]
            self.df_output.loc["Nitrogen_oxides_to_air","Amount"] = df_fert_per_kg.loc["Mean_Emission_NOx","Value"]
            self.df_output.loc["Phosphate_to_water","Amount"] = df_fert_per_kg.loc["Mean_Emission_kg_P","Value"]
            list_pesticides = list(pest_data.index)
            list_compartments = ["pest_em_soil", "pest_em_air"]
            for i in list_pesticides:
                for compartment in list_compartments:
                    df_pesticides_emissions = self.calculate_pest_emissions(i,pest_data.loc[i,"value"])
                    self.df_output.loc[str(i)+""+compartment,"Amount"] = df_pesticides_emissions.loc[i,compartment]
            self.df_output = self.df_output.fillna(0)
        if yield_ is None and n_fert_input is None:
            print("You don't even know your yield! But we have an answer for you!")
            yield_data = self.get_background_data_yield(latitude,longitude,crop)
            pest_data, pest_total = self.get_background_data_pest(latitude,longitude,crop) ## add self.
            fert_data = self.get_background_data_fert(latitude,longitude,crop) ## add self.
            water_data = self.get_background_data_water(latitude,longitude,crop) ## add self.
            generic_yield, df_fert_per_kg, water_m3_per_kg, df_pest_per_kg, total_pest_per_kg = self.create_final_dataframe(yield_data,fert_data,water_data,pest_data,pest_total) ## add self.
            self.df_output.loc["Default_pesticide","Amount"] = total_pest_per_kg
            self.df_output.loc["Default_irrigation","Amount"] = water_m3_per_kg/0.8
            self.df_output.loc["Default_nitrogen_fertilizer","Amount"] = df_fert_per_kg.loc["Mean_N_applied","Value"]
            self.df_output.loc["Default_p2o5_fertilizer","Amount"] = df_fert_per_kg.loc["Mean_P2O5_applied","Value"]
            self.df_output.loc["Default_k2o_fertilizer","Amount"] = df_fert_per_kg.loc["Mean_K2O_applied","Value"]
            self.df_output.loc["Ammonia_to_air","Amount"] = df_fert_per_kg.loc["Mean_Emission_kg_NH3","Value"]
            self.df_output.loc["Nitrate_to_water","Amount"] = df_fert_per_kg.loc["Mean_Emission_kg_NO3","Value"]
            self.df_output.loc["Nitrogen_oxides_to_air","Amount"] = df_fert_per_kg.loc["Mean_Emission_NOx","Value"]
            self.df_output.loc["Phosphate_to_water","Amount"] = df_fert_per_kg.loc["Mean_Emission_kg_P","Value"]
            list_pesticides = list(pest_data.index)
            list_compartments = ["pest_em_soil", "pest_em_air"]
            for i in list_pesticides:
                for compartment in list_compartments:
                    df_pesticides_emissions = self.calculate_pest_emissions(i,pest_data.loc[i,"value"]) ## add self.
                    self.df_output.loc[str(i)+"_"+compartment,"Amount"] = df_pesticides_emissions.loc[i,compartment]
            self.df_output = self.df_output.fillna(0)

    def generate_edges_to_product(self):
        for name in list(self.mapping_flows_uuid.index):
            self.create_edge(self.df_output.loc[name,"Amount"], name) ## add self.


    def create_edge(self, amount, name):
        #mapping_flows_uuid = mapping_flows_uuid
            self.product.new_edge(
               amount=amount, 
               type= self.type_flow_node_ei(name, self.mapping_flows_uuid), 
               input=self.code_node_ei(name, self.mapping_flows_uuid) 
           ).save()
        
    def code_node_ei(self, input_name,mapping_flows_uuid):
        uuid = self.mapping_flows_uuid.loc[input_name,"uuid"]
        name_database = mapping_flows_uuid.loc[input_name,"database"]
        return(name_database,uuid)

    
    def type_flow_node_ei(self, input_name,mapping_flows_uuid):
        type_ = self.mapping_flows_uuid.loc[input_name,"type"]
        return type_

    
    def create_main_process(self, name_database,Latitude,Longitude,crop):
        country = self.country_from_coordinates(Latitude,Longitude)
        name = "Production of "+crop+" in "+country
        data = {
        "code": uuid.uuid4().hex ,
        "name": name,
        "reference product":crop,
        "location": country,
        "Latitude": Latitude,
        "Longitude": Longitude,
        "database":name_database,
        }
        self.product = self.db.new_node(**data)
        self.product.save()
        return(self.product)

    
    def brightway_checkin(self):
        # bi.bw2setup()
        self.name_database = "Calcey_crop_database"
        if self.name_database in list(bd.databases):
            del bd.databases[self.name_database]
        self.db = bd.Database(self.name_database)
        self.db.register()

    def import_method(self):
        Purolator.import_file("impact_world_plus_201_brightway2_expert_version.e2a8415edfe998674fba2e09bddfd831.bw2package")

    def calculate_multi_LCA_results(self):
        impact_categories = [i for i in bd.methods if "World+" in i[0] and 'Total' in i[2]]
        print(impact_categories)
        #name_database = "ecoinvent 3.9.1 cutoff"
        bd.calculation_setups['bw2_training comparison'] = {'inv':[{self.product:1},
                                                            ],
                                                     'ia':impact_categories}
        multilca = bc.MultiLCA('bw2_training comparison')
        self.results = pd.DataFrame(multilca.results, columns=[i[2] for i in impact_categories])
        self.results.plot(kind='bar')

    def calculate_LCA_results(self):
        lca = bc.LCA(
            demand={self.product: 1},
            method = ('ReCiPe 2016 v1.03, midpoint (H) no LT',
                        'climate change no LT',
                        'global warming potential (GWP1000) no LT'),
        )
        lca.lci()
        lca.lcia()
        self.result_entry.insert(0, str(lca.score))
        print(lca.score)
