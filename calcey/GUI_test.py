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

class calcey:
        def __init__(self):
            bd.projects.set_current("calcey")
                
            self.brightway_checkin()
            
            self.root = tk.Tk()
            self.frame = tk.Frame(self.root)
            self.frame.pack()

            self.input_field_lat = tk.Entry(self.frame, width=20)
            self.input_field_lat.pack()

            self.input_field_lon = tk.Entry(self.frame, width=20)
            self.input_field_lon.pack()

            self.input_field_crop = tk.Entry(self.frame, width=20)
            self.input_field_crop.pack()

            self.button = tk.Button(self.frame, 
                                text="CLICK ME", 
                                fg="red",
                                command=self.print_result)

            self.button.pack(side=tk.LEFT)


    def print_result(self):
        """Gets all input data from the user interface (UI), then creates the product process and its exchanges and edges."""
        value_lat = float(self.input_field_lat.get())
        value_lon = float(self.input_field_lon.get())
        crop = self.input_field_crop.get()
        # input_yield = self.input_field_yield.get()   n_fert_input
        
        self.create_main_process(self.name_database, value_lat, value_lon, crop)
        # yield_ = input_yield       n_fert_input
        print("create_main_process finished")
        self.dataframe_exchanges(latitude=value_lat, longitude=value_lon, crop=crop)
        print("dataframe_exchanges finished")
        self.generate_edges_to_product()
        print("generate_edges_to_product finished")
        self.calculate_LCA_results()


    def get_background_data_yield(self, input_lat: float, input_lon: float, crop: str):
        """Gets yield data, based on the coordinates and crop provided in the UI."""
        df = pd.read_csv("../data/FAOSTAT_data_yield.csv")
        country = self.country_from_coordinates(Latitude=input_lat, Longitude=input_lon)
        FAO_yield = float(df.loc[(df['Area'] == country) & (df['Year'] == 2022) & (df['Item'] == crop), 'Value'].iloc[0])
        return FAO_yield
    
    def run(self):
        self.root.mainloop()

    def country_from_coordinates(self, Latitude: float, Longitude: float):
        """Gets the name of the country and region from the UI, and uses coco convert in case the language is not English."""
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
        """This converts the output "country" from the country_from_coordinates function to ISO3 format."""
        country = self.country_from_coordinates(Latitude, Longitude)
        country_ISO3 = coco.convert(country,to='ISO3')
        print(country, country_ISO3)
        return(country_ISO3)
    
    
    ####### crop mapping #################
    
    
    def get_crop_mapping_file(self, sheet_name: str):
        """This loads the crop mapping file that maps fertilizer use based on the crop chosen in the UI to the background database, but if that crop is not in the fertilizer database, it will choose the next most relevant crop in the database, defined in the mapping file. 
        The file also maps pesticides in a similar way as was done for fertilizers.
        This file also maps the UI flows to ecoinvent fertilizer names, regions, uuids, sphere type and database."""
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
        """FInds a proxy for the closest country to the UI coordinates, if the current country cannot be found in the background databases."""
        country_ISO3 = self.ISO3_country_from_coordinates(Latitude, Longitude)
        country_mapping_file = pd.read_excel("../data/Fertilizer_mapping_country.xlsx", sheet_name = "Mapping_nearest_neighbor", index_col = 0)
        country_proxy_ISO3 = country_mapping_file.loc[country_ISO3,"iso3_nearest"][0]
        return(country_proxy_ISO3)
    
    
    
    ################## get background data ###########################
    
    def get_background_data_fert(self, Latitude: float, Longitude: float, crop:str):
        """
        Gets background data for Latitude, Longitude, crop.
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
        """Gets yield data from background databases for the UI chosen coordinates and crop."""
        df = pd.read_csv("../data/FAOSTAT_data_yield.csv")
        country = self.country_from_coordinates(Latitude=input_lat, Longitude=input_lon)
        FAO_yield = float(df.loc[(df['Area'] == country) & (df['Year'] == 2022) & (df['Item'] == crop), 'Value'].iloc[0])
        return FAO_yield
    
    
    def get_background_data_water(self, input_lat: float, input_lon: float, crop: str):
        """Gets water use data from the background water use database for the UI chosen coordinates and crop."""
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
        """Creates the final dataframe for the crop product that consists of the yield, fertilizer use, water use and pesticide use."""
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
        """This function is used to calculate emissions from pesticide application, using default emissions factors. 
        pest_name is the name of the pesticide that either comes from the user interface or if the user does not specify, 
        it will take names from the background database. 
        Amount represents the quantity specified by the user interface or from the background database."""
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

        #Convert the results list to a DataFrame
        self.df_emissions = pd.DataFrame(results)
        self.df_emissions.set_index('pesticide_name', inplace=True)
        return self.df_emissions


    def dataframe_exchanges(self, latitude, longitude, crop, yield_ = None, n_fert_input=None, p2o5_fert_input=None, k2o_fert_input=None):
        """Creates the dataframe of exchanges for the crop product, based on the UI provided data, i.e., coordinates, crop type and yield."""
        self.mapping_flows_uuid = pd.read_excel("../data/Mapping_data_Calcey.xlsx", sheet_name = "Mapping_flows_ecoinvent", index_col =0) ## adjust path before "Mapping_data_Calcey.xlsx"
        all_inputs = list(set(self.mapping_flows_uuid.index))
        all_inputs = [x for x in all_inputs if type(x) != float]
        self.df_output = pd.DataFrame(index = all_inputs , columns = ['Amount'])
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
            list_pesticides = list(pest_data.index)
            list_compartments = ["pest_em_soil", "pest_em_air"]
            for i in list_pesticides:
                for compartment in list_compartments:
                    df_pesticides_emissions = self.calculate_pest_emissions(i,pest_data.loc[i,"value"]) ## add self.
                    self.df_output.loc[str(i)+"_"+compartment,"Amount"] = df_pesticides_emissions.loc[i,compartment]
            self.df_output = self.df_output.fillna(0)

    def generate_edges_to_product(self):
        """Generates the edges for all the exchanges built in the function above, dataframe_exchanges."""
        for name in list(self.mapping_flows_uuid.index):
            self.create_edge(self.df_output.loc[name,"Amount"], name) ## add self.


    def create_edge(self, amount, name):
            """Generates the edge for the crop product itself, where the amount will be the functional unit of 1 kg."""
        #mapping_flows_uuid = mapping_flows_uuid
            self.product.new_edge(
               amount=amount, 
               type= self.type_flow_node_ei(name, self.mapping_flows_uuid), 
               input=self.code_node_ei(name, self.mapping_flows_uuid) 
           ).save()
        
    def code_node_ei(self, input_name,mapping_flows_uuid):
        """Generates the nodes for inputs (input_name) that are matched with ecoinvent processes using the uuid of the process."""
        uuid = self.mapping_flows_uuid.loc[input_name,"uuid"]
        name_database = mapping_flows_uuid.loc[input_name,"database"]
        return(name_database,uuid)

    
    def type_flow_node_ei(self, input_name,mapping_flows_uuid):
        """Defines the flow type of each node, either technosphere of biosphere."""
        type_ = self.mapping_flows_uuid.loc[input_name,"type"]
        return type_

    
    def create_main_process(self, name_database,Latitude,Longitude,crop):
        """Creates the main crop product node that we are interested in calculating the impacts."""
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
        """
        Set up and register a Brightway2 database for crop data.

        This method sets up a Brightway2 database with a specified name ("Calcey_crop_database").
        If a database with the specified name already exists, it deletes the existing database
        and creates a new one. The new database is then registered for further use.

        Attributes:
        -----------
        name_database : str
            The name of the Brightway2 database to be set up and registered.

        Raises:
        -------
        ValueError
            If the database cannot be registered.
        """
        # bi.bw2setup()
        self.name_database = "Calcey_crop_database"
        if self.name_database in list(bd.databases):
            del bd.databases[self.name_database]
        self.db = bd.Database(self.name_database)
        self.db.register()


    def calculate_LCA_results(self):
        """Calculates the final LCA results using the ReCiPe method for only the climate change indicator of the crop product."""
        lca = bc.LCA(
            demand={self.product: 1},
            method = ('ReCiPe 2016 v1.03, midpoint (H) no LT',
                        'climate change no LT',
                        'global warming potential (GWP1000) no LT'),
        )
        lca.lci()
        lca.lcia()
        print(lca.score)
