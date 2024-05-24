import tkinter as tk
from tkinter import *
import tkintermapview
import customtkinter
from tkcalendar import DateEntry
import pandas as pd
from customtkinter import CTkComboBox



root = customtkinter.CTk()
root.geometry(f"{1400}x{800}")
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
Fertilizer1_unit = CTkComboBox(frame2, width = 200, values=[' ','kg/ha'] ) 
#Fertilizer1_unit.set('Please select (optional)') 
Fertilizer2_unit = CTkComboBox(frame2, width = 200, values=[' ','kg/ha']) 
#Fertilizer2_unit.set('Please select (optional)')
Fertilizer3_unit = CTkComboBox(frame2, width = 200, values=[' ','kg/ha']) 
#Fertilizer3_unit.set('Please select (optional)')
yield_drymass_unit = CTkComboBox(frame2, width = 200, values=[' ','kg/ha']) 
#yield_drymass_unit.set('Please select (optional)')
irrigation_unit = CTkComboBox(frame2, width = 200, values =[' ','m^3/ha'] )  
#irrigation_unit.set('Please select (optional)')
diesel_consumed_unit = CTkComboBox(frame2, width = 200, values = [' ','l/ha']) 
#diesel_consumed_unit.set('Please select (optional)')

#dropdown_fertilizer
Fert=(' ','Ammonium Sulphate', 'Ammoniumchloride', 'Calcium Ammonium Nitrate', 'Calcium Nitrate', 'Urea', 'Single superphosphate', 'Rock Phosphate', 'Potassium chloride', 'Potassium Sulphate', '15-15-15', '10-26-26')
Fert1 = CTkComboBox(frame2, width = 200, values=Fert,)
#Fert1.set('Please select (optional)') 
Fert2 = CTkComboBox(frame2, width = 200, values=Fert) 
#Fert2.set('Please select (optional)') 
Fert3 = CTkComboBox(frame2, width = 200, values=Fert)  
#Fert3.set('Please select (optional)') 

#dropdown yield
yiel=(' ','drymass', 'freshmass')
yield1 = CTkComboBox(frame2, width = 200, values = yiel) 
#yield1.set('Please select (optional)')

#dropdown crop
#df_crops.insert(0, ["Please select"])
crop1 = CTkComboBox(frame2, width = 200, values = list(df_crops['List_UI']))
crop1.set('Please select (mandatory)')


# Create a dictionary to store the widgets
widgets = {}

# Create a function to create and place the widgets
def create_widget(row, column, widget_type, **kwargs):
    widget = widget_type(frame2, **kwargs)
    widget.grid(row=row, column=column, padx=10, pady=10)
    widgets[f'widget_{row}_{column}'] = widget
# Create the labels
labels = ["Longitude", "Latitude", "Crop name", "Date sowing", "Date harvest"," " , " ", "Fertilizer #1 used", "Fertilizer #2 used", "Fertilizer #3 used", "Yield", "Water consumed", "Diesel consumed"]
for row, label in enumerate(labels):
    create_widget(row+1,0 , customtkinter.CTkLabel, text=label, font=customtkinter.CTkFont(family="Circular Std Black",size=15, weight="bold"),justify="left", anchor="w")

option = customtkinter.CTkLabel(frame2, text="option",font=customtkinter.CTkFont(family="Circular Std Black",size=15, weight="bold")) 
option.grid(row = 7, column = 1, padx=10, pady=10)  
unit = customtkinter.CTkLabel(frame2, text="unit",font=customtkinter.CTkFont(family="Circular Std Black",size=15, weight="bold")) 
unit.grid(row = 7, column = 3, padx=10, pady=10)
mass = customtkinter.CTkLabel(frame2, text="amount", font=customtkinter.CTkFont(family="Circular Std Black",size=15, weight="bold"))   
mass.grid(row = 7, column = 2, padx=10, pady=10)  

#first column
Crop = customtkinter.CTkEntry(frame2, width = 200,placeholder_text=" ")
Sowing_date = customtkinter.CTkEntry(frame2, width = 200)
cal=DateEntry(frame2, width = 27)
cal.grid(row=4,column=1, padx=10, pady=10)
Harvest_date = customtkinter.CTkEntry(frame2, width = 200)
cal2=DateEntry(frame2, width = 27,selectmode='day')
cal2.grid(row=5,column=1, padx=10, pady=10)
Fertilizer1 = customtkinter.CTkEntry(frame2, width = 200)
Fertilizer2 = customtkinter.CTkEntry(frame2, width = 200)
Fertilizer3 = customtkinter.CTkEntry(frame2, width = 200)

#third column - mass
Fert1_mass = customtkinter.CTkEntry(frame2, width = 200)
Fert2_mass = customtkinter.CTkEntry(frame2, width = 200)
Fert3_mass = customtkinter.CTkEntry(frame2, width = 200)
yield_drymass_mass = customtkinter.CTkEntry(frame2, width = 200)
irrigation_mass = customtkinter.CTkEntry(frame2, width = 200)
diesel_consumed_mass= customtkinter.CTkEntry(frame2, width = 200)

Longitude = customtkinter.CTkEntry(frame2, width = 200,placeholder_text="Please place marker on the map")
Latitude= customtkinter.CTkEntry(frame2, width = 200,placeholder_text="Please place marker on the map")

#grid---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#entry
Longitude.grid(row = 1, column = 1, padx=10, pady=10)
Latitude.grid(row = 2, column = 1, padx=10, pady=10)
crop1.grid(row = 3, column = 1, padx=10, pady=10)
Fert1.grid(row = 8, column = 1, padx=10, pady=10)
Fert2.grid(row = 9, column = 1, padx=10, pady=10)
Fert3.grid(row = 10, column = 1, padx=10, pady=10)
yield1.grid(row = 11, column = 1, padx=10, pady=10)

#amount
Fert1_mass.grid(row = 8, column = 2, padx=10, pady=10)
Fert2_mass.grid(row = 9, column = 2, padx=10, pady=10)
Fert3_mass.grid(row = 10, column = 2, padx=10, pady=10)
yield_drymass_mass.grid(row = 11, column = 2, padx=10, pady=10)
irrigation_mass.grid(row = 12, column = 2, padx=10, pady=10)
diesel_consumed_mass.grid(row = 13, column = 2, padx=10, pady=10)

#unit
Fertilizer1_unit.grid(row = 8, column = 3, padx=10, pady=10)
Fertilizer2_unit.grid(row = 9, column = 3, padx=10, pady=10)
Fertilizer3_unit.grid(row = 10, column = 3, padx=10, pady=10)
yield_drymass_unit.grid(row = 11, column = 3, padx=10, pady=10)
irrigation_unit.grid(row = 12, column = 3, padx=10, pady=10)
diesel_consumed_unit.grid(row = 13, column = 3, padx=10, pady=10)

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
   
customtkinter.CTkButton(frame2,height = 90, width=110, text = "submit",font=customtkinter.CTkFont(family="Circular Std Black",size=20, weight="bold"),
           command = getInput).grid(column = 0,row = 13,columnspan= 5, sticky = E)

root.mainloop()






