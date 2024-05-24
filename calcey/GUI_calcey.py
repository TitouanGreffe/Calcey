import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkintermapview
import customtkinter
from tkcalendar import DateEntry
import pandas as pd



root = customtkinter.CTk()
root.geometry(f"{1250}x{750}")
root.title("calcey")
customtkinter.set_appearance_mode("Dark")


#lists---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
label_list = ["Crop name", "Date sowing", "Date harvest", "Fertilizer #1 used", "Fertilizer #2 used", "Fertilizer #3 used", "yield drymass", "yield freshmass", "irrigation", "diesel consumed"  ]
df_crops = pd.read_excel('data/Mapping_data_Calcey.xlsx', sheet_name='Mapping_Fertilizer', usecols='A') 


frame2 =customtkinter.CTkFrame(root, width=100, height=100)
frame3 = customtkinter.CTkFrame(root, width=100, height=100)

frame2.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
frame3.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

label = customtkinter.CTkLabel(frame3, text="Welcome to calcey!",  width=300, height=50, fg_color='transparent',font=customtkinter.CTkFont(family="Circular Std Black",size=30, weight="bold"))
label.pack()


def search_event(event=None):
        map_widget.set_address(entry.get())

entry = customtkinter.CTkEntry(frame2,placeholder_text="type address")
entry.grid(row=12, column=4, sticky="e", padx=(15, 0), pady=5)
entry.bind("<Return>", search_event)

button_5 = customtkinter.CTkButton(frame2,
                                                text="Search",
                                                width=90,
                                                command=search_event)
button_5.grid(row=13, column=4, sticky="e", padx=(12, 0), pady=5)

def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())




# Create the search bar entry widget


#getting coordinates
map_widget = tkintermapview.TkinterMapView(frame2, width=500, height=500, corner_radius=0)
map_widget.grid(row=0, column=4,rowspan = 12, padx=10, pady=10, sticky=tk.E)

def get_coordinates(coordinates_tuple):
    longitude = coordinates_tuple[1]
    latitude = coordinates_tuple[0]
    Longitude.delete(0,"end")
    Latitude.delete(0,"end")
    Longitude.insert(0, longitude)
    Latitude.insert(0, latitude)
    marker = map_widget.set_marker(latitude, longitude)
    

map_widget.add_left_click_map_command(get_coordinates) 


#dropdowns---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#dropdown_unit
Fertilizer1_unit = customtkinter.CTkOptionMenu(frame2, width = 100, values=[' ','kg/ha'] )  
Fertilizer2_unit = customtkinter.CTkOptionMenu(frame2, width = 100, values=[' ','kg/ha']) 
Fertilizer3_unit = customtkinter.CTkOptionMenu(frame2, width = 100, values=[' ','kg/ha']) 
yield_drymass_unit = customtkinter.CTkOptionMenu(frame2, width = 100, values=[' ','kg/ha']) 
irrigation_unit = customtkinter.CTkOptionMenu(frame2, width = 100, values =[' ','m^3/ha'] )  
diesel_consumed_unit = customtkinter.CTkOptionMenu(frame2, width = 100, values = [' ','l/ha']) 

#dropdown_fertilizer
Fert=(' ','Ammonium Sulphate', 'Ammoniumchloride', 'Calcium Ammonium Nitrate', 'Calcium Nitrate', 'Urea', 'Single superphosphate', 'Rock Phosphate', 'Potassium chloride', 'Potassium Sulphate', '15-15-15', '10-26-26')
Fert1 = customtkinter.CTkOptionMenu(frame2, width = 200, values=Fert) 
Fert2 = customtkinter.CTkOptionMenu(frame2, width = 200, values=Fert) 
Fert3 = customtkinter.CTkOptionMenu(frame2, width = 200, values=Fert)  

#dropdown yield
yiel=(' ','drymass', 'freshmass')
yield1 = customtkinter.CTkOptionMenu(frame2, width = 200, values = yiel) 

#dropdown crop
#df_crops.insert(0, "")
crop1 = customtkinter.CTkOptionMenu(frame2, width = 200, values = list(df_crops['List_UI'])) 


# Create a dictionary to store the widgets
widgets = {}

# Create a function to create and place the widgets
def create_widget(row, column, widget_type, **kwargs):
    widget = widget_type(frame2, **kwargs)
    widget.grid(row=row, column=column, padx=10, pady=10)
    widgets[f'widget_{row}_{column}'] = widget
# Create the labels
labels = ["Longitude", "Latitude", "Crop name", "Date sowing", "Date harvest", "Fertilizer #1 used", "Fertilizer #2 used", "Fertilizer #3 used", "Yield", "Water consumed", "Diesel consumed"]
for row, label in enumerate(labels):
    create_widget(row+1,0 , customtkinter.CTkLabel, text=label, font=customtkinter.CTkFont(family="Circular Std Black",size=15, weight="bold"),justify="left", anchor="w")
    

#first column
Crop = customtkinter.CTkEntry(frame2, width = 200,placeholder_text=" ")
Sowing_date = customtkinter.CTkEntry(frame2, width = 200)
cal=DateEntry(frame2, width = 27)
cal.grid(row=4,column=1, padx=10, pady=10)
Harvest_date = customtkinter.CTkEntry(frame2, width = 200)
cal2=DateEntry(frame2, width = 27,selectmode='day')
cal2.grid(row=5,column=1, padx=10, pady=10)
Fertilizer1 = customtkinter.CTkEntry(frame2, width = 200,placeholder_text="optional")
Fertilizer2 = customtkinter.CTkEntry(frame2, width = 200,placeholder_text="optional")
Fertilizer3 = customtkinter.CTkEntry(frame2, width = 200,placeholder_text="optional")

#third column - mass
Fert1_mass = customtkinter.CTkEntry(frame2, width = 200,placeholder_text="optional")
Fert2_mass = customtkinter.CTkEntry(frame2, width = 200,placeholder_text="optional")
Fert3_mass = customtkinter.CTkEntry(frame2, width = 200,placeholder_text="optional")
yield_drymass_mass = customtkinter.CTkEntry(frame2, width = 200,placeholder_text="optional")
irrigation_mass = customtkinter.CTkEntry(frame2, width = 200,placeholder_text="optional")
diesel_consumed_mass= customtkinter.CTkEntry(frame2, width = 200,placeholder_text="optional")

Longitude = customtkinter.CTkEntry(frame2, width = 200,placeholder_text="Please place marker on the map")
Latitude= customtkinter.CTkEntry(frame2, width = 200,placeholder_text="Please place marker on the map")

#grid---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#entry
Longitude.grid(row = 1, column = 1, padx=10, pady=10)
Latitude.grid(row = 2, column = 1, padx=10, pady=10)
crop1.grid(row = 3, column = 1, padx=10, pady=10)
Fert1.grid(row = 6, column = 1, padx=10, pady=10)
Fert2.grid(row = 7, column = 1, padx=10, pady=10)
Fert3.grid(row = 8, column = 1, padx=10, pady=10)
yield1.grid(row = 9, column = 1, padx=10, pady=10)
#irri1.grid(row = 10, column = 1, padx=10, pady=10)

#amount
Fert1_mass.grid(row = 6, column = 2, padx=10, pady=10)
Fert2_mass.grid(row = 7, column = 2, padx=10, pady=10)
Fert3_mass.grid(row = 8, column = 2, padx=10, pady=10)
yield_drymass_mass.grid(row = 9, column = 2, padx=10, pady=10)
irrigation_mass.grid(row = 10, column = 2, padx=10, pady=10)
diesel_consumed_mass.grid(row = 11, column = 2, padx=10, pady=10)

#unit
Fertilizer1_unit.grid(row = 6, column = 3, padx=10, pady=10)
Fertilizer2_unit.grid(row = 7, column = 3, padx=10, pady=10)
Fertilizer3_unit.grid(row = 8, column = 3, padx=10, pady=10)
yield_drymass_unit.grid(row = 9, column = 3, padx=10, pady=10)
irrigation_unit.grid(row = 10, column = 3, padx=10, pady=10)
diesel_consumed_unit.grid(row = 11, column = 3, padx=10, pady=10)

#getting input---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def getInput():

    a=Longitude.get()
    b=Latitude.get()
    c = crop1.get()
    d = cal.get()
    e = cal2.get()
    f = Fert1.get()
    g = Fert2.get()
    h = Fert3.get()
    i = yield1.get()
    #j = irri1.get()
   

    ff = Fert1_mass.get()
    gg =Fert2_mass.get()
    hh = Fert3_mass.get()
    ii = yield_drymass_mass.get()
    jj =irrigation_mass.get()
    kk= diesel_consumed_mass.get()

    fff = Fertilizer1_unit.get()
    ggg = Fertilizer2_unit.get()
    hhh = Fertilizer3_unit.get()
    iii = yield_drymass_unit.get()
    jjj = irrigation_unit.get()
    kkk = diesel_consumed_unit.get()

    root.destroy()

    user_data = {
        "location" : {
        "latitude" : b ,
        "longitude" : a,
},
        "crops" : {
        "name" : c  
},
        "dates" : {
        "sowing" : d,
        "harvest" : e
  },
        "fertilizer1" : {
        "name" : f,
        "amount" : ff,
        "unit" : fff
  },
        "fertilizer2" : {
        "name" : g,
        "amount" : gg,
        "unit" : ggg
  },
        "fertilizer3" : {
        "name" : h,
        "amount" : hh,
        "unit" : hhh
  },
        "yield": {
        "name" : i,
        "amount" : ii,
        "unit" : iii
  },
        "irrigation": {
        "amount" : jj,
        "unit" : jjj
  },
        "diesel": {
        "amount" : kk,
        "unit" : kkk
  }
}
    
    print(user_data)
   
customtkinter.CTkButton(frame2,height = 90, width=110, text = "submit",
           command = getInput).grid(column = 0,row = 13,columnspan= 5, sticky = W)

root.mainloop()






