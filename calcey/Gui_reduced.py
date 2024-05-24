import customtkinter
from tkintermapview import TkinterMapView
import pandas as pd

customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):

    APP_NAME = "Calcey"
    WIDTH = 1100
    HEIGHT = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.df_crops = pd.read_excel('data/Mapping_data_Calcey.xlsx', sheet_name='Mapping_Fertilizer', usecols='A')

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)


        # ============ create two CTkFrames ============

        self.frame_left = customtkinter.CTkFrame(master=self, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=1, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0, width=100)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.label = customtkinter.CTkLabel(self.frame_left, text="Welcome to Calcey!",  width=300, height=50, fg_color='transparent',font=customtkinter.CTkFont(family="Circular Std Black",size=30, weight="bold"))
        self.label.grid(row=0, column=0, padx=(80, 80), pady=(10, 0))

        self.label2 = customtkinter.CTkLabel(self.frame_left, text="Please click on the map\n to get your coordinates and select the crop.",  width=300, height=50, fg_color='transparent',font=customtkinter.CTkFont(family="Circular Std Black",size=20, weight="bold"))
        self.label2.grid(row=1, column=0, padx=(80, 80), pady=(5, 50))

        self.longitude_label = customtkinter.CTkLabel(self.frame_left, text="Longitude:")
        self.longitude_label.grid(row=2, column=0, padx=(80, 80), pady=(5, 0))

        self.latitude_label = customtkinter.CTkLabel(self.frame_left, text="Latitude:")
        self.latitude_label.grid(row=4, column=0, padx=(80, 80), pady=(5, 0))

        self.longitude_entry = customtkinter.CTkEntry(self.frame_left, width=150)
        self.longitude_entry.grid(row=3, column=0, padx=(80, 80), pady=(5, 0))

        self.latitude_entry = customtkinter.CTkEntry(self.frame_left, width=150)
        self.latitude_entry.grid(row=5, column=0, padx=(80, 80), pady=(5, 50))

        self.crop_label = customtkinter.CTkLabel(self.frame_left, text="Crop")
        self.crop_label.grid(row=6, column=0, padx=(80, 80), pady=(5, 0))
        
        self.crop_entry = customtkinter.CTkOptionMenu(self.frame_left, values = list(self.df_crops['List_UI']), )
        self.crop_entry.grid(row=7, column=0, padx=(80, 80), pady=(5, 0))

        self.submit_button = customtkinter.CTkButton(master = self, height=50, width=110, text="Submit", font=customtkinter.CTkFont(family="Circular Std Black", size=20, weight="bold"), command=self.getInput)
        self.submit_button.grid(column=0, row=13, columnspan=5, pady=(20, 0))

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
    
    def getInput(self):

        self.a=self.longitude_entry.get()
        self.b=self.latitude_entry.get()
        self.c = self.crop_entry.get()
        
        self.user_data = {
            "location" : {
            "latitude" : self.b ,
            "longitude" : self.a,
    },
            "crops" : {
            "name" : self.c
            }
        }
        self.destroy()

        print(self.user_data)

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()