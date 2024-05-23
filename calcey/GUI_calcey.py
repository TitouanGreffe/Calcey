import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkintermapview
import customtkinter
import pickle
from tkcalendar import DateEntry
import pandas as pd


root = customtkinter.CTk()
root.geometry(f"{800}x{1000}")
root.title("calcey")
customtkinter.set_appearance_mode("Light")


#lists---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
label_list = ["Crop name", "Date sowing", "Date harvest", "Fertilizer #1 used", "Fertilizer #2 used", "Fertilizer #3 used", "yield drymass", "yield freshmass", "irrigation", "diesel consumed"  ]

df_fertilizer = pd.read_excel('data/Mapping_data_Calcey.xlsx', sheet_name='Mapping_Fertilizer', usecols='A') 


#getting coordinates
map_widget = tkintermapview.TkinterMapView(root, width=800, height=400, corner_radius=0)
map_widget.place(relx=0, rely=1, anchor=tk.SW)

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
n1 = tk.StringVar()
n2 = tk.StringVar()  
n3 = tk.StringVar() 
n4 = tk.StringVar() 
n5 = tk.StringVar() 
n6 = tk.StringVar() 
n7 = tk.StringVar() 
n8 = tk.StringVar() 
n9 = tk.StringVar() 
Fertilizer1_unit = ttk.Combobox(root, width = 10, textvariable = n3, values=('kg/ha') )  
Fertilizer2_unit = ttk.Combobox(root, width = 10, textvariable = n4, values=('kg/ha')) 
Fertilizer3_unit = ttk.Combobox(root, width = 10, textvariable = n5, values=('kg/ha')) 
yield_drymass_unit = ttk.Combobox(root, width = 10, textvariable = n6, values=('kg/ha')) 
irrigation_unit = ttk.Combobox(root, width = 10, textvariable = n8, values =('m^3/ha') )  
diesel_consumed_unit = ttk.Combobox(root, width = 10, textvariable = n9, values = ('l/ha')) 


#dropdown_fertilizer
Fert=('Ammonium Sulphate', 'Ammoniumchloride', 'Calcium Ammonium Nitrate', 'Calcium Nitrate', 'Urea', 'Single superphosphate', 'Rock Phosphate', 'Potassium chloride', 'Potassium Sulphate', '15-15-15', '10-26-26')
m1 = tk.StringVar()
m2 = tk.StringVar()  
m3 = tk.StringVar() 
Fert1 = ttk.Combobox(root, width = 27, textvariable = m1, values=Fert) 
Fert2 = ttk.Combobox(root, width = 27, textvariable = m2, values=Fert) 
Fert3 = ttk.Combobox(root, width = 27, textvariable = m3, values=Fert)  

#dropdown yield
yiel=('drymass', 'freshmass')
o1 = tk.StringVar()
yield1 = ttk.Combobox(root, width = 27, textvariable = o1, values = yiel) 



#dropdown crop
q1 = tk.StringVar()
crop1 = ttk.Combobox(root, width = 27, textvariable = q1, values = list(df_fertilizer['List_UI'])) 

#Label---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Label(root, text="amount").grid(row = 0,column=2, sticky = W)
Label(root, text="unit").grid(row = 0, column=3, sticky = W)
Label(root, text = "Longitude").grid(row = 1, sticky = W)
Label(root, text = "Latitude").grid(row = 2, sticky = W)
Label(root, text = "Crop name").grid(row = 3, sticky = W)
Label(root, text = "Date sowing").grid(row = 4, sticky = W)
Label(root, text = "Date harvest").grid(row = 5, sticky = W)
Label(root, text = "Fertilizer #1 used").grid(row = 6, sticky = W)
Label(root, text = "Fertilizer #2 used").grid(row = 7, sticky = W)
Label(root, text = "Fertilizer #3 used").grid(row = 8, sticky = W)
Label(root, text = "yield").grid(row = 9, sticky = W)
Label(root, text = "water consumed").grid(row = 10, sticky = W)
Label(root, text = "diesel consumed").grid(row = 11, sticky = W)

#Entry---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#first column
Crop = Entry(root, width = 27)
Sowing_date = Entry(root, width = 27)
cal=DateEntry(root, width = 27)
cal.grid(row=4,column=1, padx=10, pady=10)
Harvest_date = Entry(root, width = 27)
cal2=DateEntry(root, width = 27,selectmode='day')
cal2.grid(row=5,column=1, padx=10, pady=10)
Fertilizer1 = Entry(root, width = 27)
Fertilizer2 = Entry(root, width = 27)
Fertilizer3 = Entry(root, width = 27)

#third column - mass
Fert1_mass = Entry(root, width = 27)
Fert2_mass = Entry(root, width = 27)
Fert3_mass = Entry(root, width = 27)
yield_drymass_mass = Entry(root, width = 27)
irrigation_mass = Entry(root, width = 27)
diesel_consumed_mass= Entry(root, width = 27)

Longitude = Entry(root, width = 27)
Latitude= Entry(root, width = 27)

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
        "name" : j,
        "amount" : jj,
        "unit" : jjj
  },
        "diesel": {
        "amount" : kk,
        "unit" : kkk
  }
}
    
    print(user_data)

    #with open('user_data.pkl', 'wb') as fp:
        #pickle.dump(user_data, fp)
        #print('dictionary saved successfully to file')

    
Button(root,height= 5, width=15, bg = 'white', text = "submit",
           command = getInput).grid(row = 14, sticky = W)



root.mainloop()






