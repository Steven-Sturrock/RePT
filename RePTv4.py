#RePT Public Transport Recap
#Steven Sturrock

'''
V0.0.1 - Initial version 
V0.0.2 - Created constants for column names and current date variables for validation
V0.0.3 - Set up basic GUI components including themes
V0.0.4 - Set up frames for multiple windows
V0.0.5 - Created classes and import script
V0.1.0 - Set up basic search demo using HE604
V0.1.1 - Added more search functions and made general adjustments
V1.0.0 - Functional search, minimum viable product
V2.0.0 - Added validation
V2.0.1 - Cleaned up code and improved validation
V2.1.0 - Added trip logging functionality
V2.1.1 - Added export functionality for trip logging
V2.1.2 - Added working today button
V2.2.0 - Added trip editing
V2.2.1 - Added missing file handling
V2.2.2 - Added working delete button, removed service_id and resorted to list position
V3.0.0 - Additional commments and load from settings
V3.0.1 - Working settings menu
V3.0.2 - More themes
V3.0.3 - Settings validation
V3.0.4 - Validation improvements, autofill, and LNER theme
V3.0.5 - Minor fixes
V4.0.0 - Many more themes
V4.1.0 - Scaling
V4.1.1 - Minor tweaks to scaling
V4.1.2 - Minor changes
V4.1.3 - Bug fixes
V4.2.0 - Scrollbars, unrefined
V4.2.1 - Bug fixes
'''

#Libraries
from tkinter import *
from tkinter import ttk
import csv
import datetime
import json

#Load settings from config
try:
    with open("config.json", "r") as f:
        config = json.load(f)
        THEME = config["THEME"]
        SOURCE = config["SOURCE"]
        ROUTE = config["ROUTE"]
        VEHICLE = config["VEHICLE"]
        DATE = config["DATE"]
except:
    #Default settings if file missing
    THEME = "AT"
    SOURCE = "trips.csv"
    ROUTE = 'Route'
    VEHICLE = 'Vehicle'
    DATE = 'Date'

#Current date (validation)
D = int(datetime.datetime.now().strftime("%d"))
M = int(datetime.datetime.now().strftime("%m"))
Y = int(datetime.datetime.now().strftime("%Y"))

#Design constants
HEADING = {"AT":"#2d7caf", "Metlink":"#00364a", "Te Huia":"#282829", "MAXX":"#00a3e6", "BUSIT":"#28b44b", "Metro":"#46c1be", "LNER":"#ffffff", "InterCity":"#141b1d", "ScotRail":"#001a45", "CrossCountry":"#ca123f", "Avanti West Coast":"#004f59", "GWR":"#0a493e"}
HEADINGTEXT = {"AT":"#ffffff", "Metlink":"#ffffff", "Te Huia":"#ffc90e", "MAXX":"#ffffff", "BUSIT":"#ffffff", "Metro":"#ffffff", "LNER":"#ce132e", "InterCity":"#f2cd34", "ScotRail":"#ffffff", "CrossCountry":"#ffffff", "Avanti West Coast":"#ffffff", "GWR":"#ffffff"}
SUBHEADING = {"AT":"#00A7E5", "Metlink":"#cddc2a", "Te Huia":"#323d48", "MAXX":"#f4661d", "BUSIT":"#323d48", "Metro":"#009490", "LNER":"#ce132e", "InterCity":"#fa451b", "ScotRail":"#002664", "CrossCountry":"#79002c", "Avanti West Coast":"#ff4713", "GWR":"#09473c"}
SUBHEADINGTEXT = {"AT":"#ffffff", "Metlink":"#00364a", "Te Huia":"#ffffff", "MAXX":"#ffffff", "BUSIT":"#ffffff", "Metro":"#ffffff", "LNER":"#ffffff", "InterCity":"#ffffff", "ScotRail":"#ffffff", "CrossCountry":"#ffffff", "Avanti West Coast":"#ffffff", "GWR":"#ffffff"}
BUTTON = {"AT":"#d4edfc", "Metlink":"#406978", "Te Huia":"#ffc90e", "MAXX":"#ffc02f", "BUSIT":"#c4c4c4", "Metro":"#46c1be", "LNER":"#ffffff", "InterCity":"#ffffff", "ScotRail":"#12356f", "CrossCountry":"#c4c4c4", "Avanti West Coast":"#ffffff", "GWR":"#007569"}
BUTTONTEXT = {"AT":"#282829", "Metlink":"#ffffff", "Te Huia":"#282829", "MAXX":"#282829", "BUSIT":"#323d48", "Metro":"#e7f1f9", "LNER":"#ce132e", "InterCity":"#141b1d", "ScotRail":"#ffffff", "CrossCountry":"#000000", "Avanti West Coast":"#004f59", "GWR":"#ffffff"}
FONT = {"Heading":"Arial 40 bold", "Subheading":"Arial 25 bold", "Button":"Arial 14", "Text":"Arial 12"}

#Classes
class Trip:
    #Set up object
    def __init__(self, vehicle, route, date):
        self.vehicle = vehicle.upper()
        self.route = route
        self.date = date
        
    #Print all vehicle data
    def __str__(self):
        return [f"Vehicle: {self.vehicle}", f"Route: {self.route}", f"Date: {self.date}"]
    
    #Check if search term is equal to self.vehicle and return data if true
    def vehicle_search(self, search, ID):
        if self.vehicle == search:
            return f"{self.route} - {self.date} - ID:{ID}"
        else:
            return None
    
    #Check if search term is equal to self.route and return data if true
    def route_search(self, search, ID):
        if self.route.lower() == search.lower():
            return f"{self.vehicle} - {self.date} - ID:{ID}"
        else:
            return None
    
    #Check if search term is equal to self.date and return data if true
    def date_search(self, search, ID):
        if self.date == search:
            return f"{self.vehicle} - {self.route} - ID:{ID}"
        else:
            return None
        
    def ID_search(self):
        return [f"Vehicle: {self.vehicle}", f"Route: {self.route}", f"Date: {self.date}"]

#Load data from file
try:
    with open(SOURCE) as tripfile:
        trips = []
        for i in csv.DictReader(tripfile):
            trips.append(Trip(i[VEHICLE], i[ROUTE], i[DATE]))
except:
    trips = [] 
    

#Main program
class GUI:
    def __init__(self):
        #Create window
        self.master = Tk()
        self.master.title("RePT")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.geometry("650x375")
        self.master.minsize(650, 375)
        
        #Create container
        self.container = Frame(self.master)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)     
        
        #Create frames dictionary
        self.frames = {}
        self.frames["MenuFrame"] = self.create_menu_frame()
        self.frames["SearchFrame"] = self.create_search_frame()
        self.frames["LogFrame"] = self.create_log_frame()
        self.frames["EditFrame"] = self.create_edit_frame()
        self.frames["SettingsFrame"] = self.create_settings_frame()
        
        #Show main menu on start
        self.show_window("MenuFrame")
        
    def show_window(self, name):
        self.frame = self.frames[name] #Select the frame
        self.frame.tkraise() #Move frame to top
        
    def create_menu_frame(self): #Main menu
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_rowconfigure(3, weight=1)
        frame.grid_rowconfigure(4, weight=1)
        frame.grid_rowconfigure(5, weight=1)
        frame.grid_columnconfigure(0, weight=1)       
        
        #Menu heading
        self.heading = Label(frame, text="RePT", bg=HEADING[THEME], fg=HEADINGTEXT[THEME], font=FONT["Heading"], width=20)
        self.heading.grid(row=0, column=0, sticky="nsew")
        
        #Menu subheading
        self.subheading = Label(frame, text="Public Transport Recap", bg=SUBHEADING[THEME], fg=SUBHEADINGTEXT[THEME], font=FONT["Subheading"], width=20)
        self.subheading.grid(row=1, column=0, sticky="nsew")        
        
        #Search menu button
        self.search_button = Button(frame, text="Search trips", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=10, command=lambda: self.show_window("SearchFrame"))
        self.search_button.grid(row=2, column=0, sticky="nsew", pady=10, padx=10)
        
        #Log menu button
        self.log_button = Button(frame, text="Log trips", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=10, command=lambda: self.show_window("LogFrame"))
        self.log_button.grid(row=3, column=0, sticky="nsew", pady=10, padx=10)        
        
        #Edit menu button
        self.edit_button = Button(frame, text="Edit trips", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=10, command=lambda: self.show_window("EditFrame"))
        self.edit_button.grid(row=4, column=0, sticky="nsew", pady=10, padx=10)
        
        #Settings menu button
        self.settings_button = Button(frame, text="Settings", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=10, command=lambda: self.show_window("SettingsFrame"))
        self.settings_button.grid(row=5, column=0, sticky="nsew", pady=10, padx=10)           
        
        return frame
        
    def create_search_frame(self): #Search for specific trips
        #Create frame
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(6, weight=1)
        frame.grid_columnconfigure(1, weight=1) 
        frame.grid_columnconfigure(3, weight=1)           
        
        #Search heading
        self.search_heading = Label(frame, text="Search", bg=HEADING[THEME], fg=HEADINGTEXT[THEME], font=FONT["Heading"], width=20)
        self.search_heading.grid(row=0, column=0, columnspan = 5, sticky="nsew")
        
        #Search subheading
        self.search_subheading = Label(frame, text="", bg=SUBHEADING[THEME], fg=SUBHEADINGTEXT[THEME], font=FONT["Subheading"])
        self.search_subheading.grid(row=1, column=3, sticky="nsew", columnspan = 2)
        
        #Back button
        self.search_back_button = Button(frame, text="Back", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.show_window("MenuFrame"))
        self.search_back_button.grid(row=1, column=0)
        
        #Vehicle search (label, box, and button)
        self.v_search_label = Label(frame, text="Vehicle:", fg="#406978", font=FONT["Button"])
        self.v_search_label.grid(row=2, column=0)
        
        self.v_search_box = Entry(frame)
        self.v_search_box.grid(row=2, column=1, sticky="ew")
        
        self.v_search_button = Button(frame, text="Search", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.v_search(self.v_search_box.get().upper()))
        self.v_search_button.grid(row=2, column=2, padx=10, pady=5)
        
        #Route search (label, box, and button)
        self.r_search_label = Label(frame, text="Route:", fg="#406978", font=FONT["Button"])
        self.r_search_label.grid(row=3, column=0)        
        
        self.r_search_box = Entry(frame)
        self.r_search_box.grid(row=3, column=1, sticky="ew")
        
        self.r_search_button = Button(frame, text="Search", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.r_search(self.r_search_box.get()))
        self.r_search_button.grid(row=3, column=2, pady=5)
        
        #Date search (label, box, and button)
        self.d_search_label = Label(frame, text="Date:", fg="#406978", font=FONT["Button"])
        self.d_search_label.grid(row=4, column=0)        
        
        self.d_search_box = Entry(frame)
        self.d_search_box.grid(row=4, column=1, sticky="ew")
        
        self.d_search_button = Button(frame, text="Search", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.d_search(self.d_search_box.get()))
        self.d_search_button.grid(row=4, column=2, pady=5)            
        
        #ID search (label, box, and button)
        self.i_search_label = Label(frame, text="Service ID:", fg="#406978", font=FONT["Button"])
        self.i_search_label.grid(row=5, column=0)        
        
        self.i_search_box = Entry(frame)
        self.i_search_box.grid(row=5, column=1, sticky="ew")
        
        self.i_search_button = Button(frame, text="Search", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.i_search(self.i_search_box.get()))
        self.i_search_button.grid(row=5, column=2, pady=5)            
        
        #Results
        self.search_results = Listbox(frame, bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Text"], highlightbackground="black", highlightthickness=1, justify="center")
        self.search_results.grid(row=2, column=3, sticky="nsew", rowspan=5)        
        
        self.search_results_scroll = Scrollbar(frame, command = self.search_results.yview)
        self.search_results_scroll.grid(row=2, column=4, sticky="ns", rowspan=5)
        
        self.search_results.config(yscrollcommand=self.search_results_scroll.set)
        
        return frame
    
    def create_log_frame(self): #Save trips
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")   
        frame.grid_columnconfigure(0, weight=1)   
        frame.grid_columnconfigure(1, weight=1)   
        frame.grid_columnconfigure(2, weight=1) 
        
        #Log Header
        self.log_heading = Label(frame, text="Log trips", bg=HEADING[THEME], fg=HEADINGTEXT[THEME], font=FONT["Heading"], width=20)
        self.log_heading.grid(row=0, column=0, sticky="nsew", columnspan=3)
        
        #Back button
        self.log_back_button = Button(frame, text="Back", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.show_window("MenuFrame"))
        self.log_back_button.grid(row=1, column=0)
        
        #Vehicle (label and box)
        self.v_log_label = Label(frame, text="Vehicle:", fg="#406978", font=FONT["Button"])
        self.v_log_label.grid(row=2, column=0, sticky="e")
        
        self.v_log_box = Entry(frame)
        self.v_log_box.grid(row=2, column=1, sticky="ew")
        
        #Route (label and box)
        self.r_log_label = Label(frame, text="Route:", fg="#406978", font=FONT["Button"])
        self.r_log_label.grid(row=3, column=0, sticky="e")
        
        self.r_log_box = Entry(frame)
        self.r_log_box.grid(row=3, column=1, sticky="ew")
        
        #Date (label and box)
        self.d_log_label = Label(frame, text="Date:", fg="#406978", font=FONT["Button"])
        self.d_log_label.grid(row=4, column=0, sticky="e")
        
        self.d_log_box = Entry(frame)
        self.d_log_box.grid(row=4, column=1, sticky="ew")
        
        self.d_log_today = Button(frame, text="Today", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: [self.d_log_box.delete(0, 'end'), self.d_log_box.insert(0, f"{D:02d}/{M:02d}/{Y:04d}")])
        self.d_log_today.grid(row=4, column=2, sticky="w")
        
        #Log button
        self.log_button = Button(frame, text="Log", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.log_trip(self.v_log_box.get().upper(), self.r_log_box.get(), self.d_log_box.get()))
        self.log_button.grid(row=5, column=0, columnspan=3)
        
        #Save button
        self.save_log_button = Button(frame, text="Save", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.save(self.message_log))
        self.save_log_button.grid(row=6, column=0, columnspan=3)        
        
        #Message box
        self.message_log = Label(frame, text="", fg="#406978", font=FONT["Button"])
        self.message_log.grid(row=7, column=0, columnspan=3)
        
        return frame
    
    def create_edit_frame(self): #Edit existing trips
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)   
        frame.grid_columnconfigure(1, weight=1)   
        frame.grid_columnconfigure(2, weight=1)         
        
        #Log Header
        self.edit_heading = Label(frame, text="Edit trips", bg=HEADING[THEME], fg=HEADINGTEXT[THEME], font=FONT["Heading"], width=20)
        self.edit_heading.grid(row=0, column=0, sticky="nsew", columnspan=3)
        
        #Back button
        self.edit_back_button = Button(frame, text="Back", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.show_window("MenuFrame"))
        self.edit_back_button.grid(row=1, column=0)
        
        #Autofill
        self.autofill_edit_button = Button(frame, text="Autofill", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.autofill_edit(self.i_edit_box.get()))
        self.autofill_edit_button.grid(row=2, column=2, sticky="w")
        
        #ID (label and box)
        self.i_edit_label = Label(frame, text="Service ID:", fg="#406978", font=FONT["Button"])
        self.i_edit_label.grid(row=2, column=0, sticky="e")
        
        self.i_edit_box = Entry(frame)
        self.i_edit_box.grid(row=2, column=1, sticky="ew")        
        
        #Vehicle (label and box)
        self.v_edit_label = Label(frame, text="Vehicle:", fg="#406978", font=FONT["Button"])
        self.v_edit_label.grid(row=3, column=0, sticky="e")
        
        self.v_edit_box = Entry(frame)
        self.v_edit_box.grid(row=3, column=1, sticky="ew")
        
        #Route (label and box)
        self.r_edit_label = Label(frame, text="Route:", fg="#406978", font=FONT["Button"])
        self.r_edit_label.grid(row=4, column=0, sticky="e")
        
        self.r_edit_box = Entry(frame)
        self.r_edit_box.grid(row=4, column=1, sticky="ew")
        
        #Date (label and box)
        self.d_edit_label = Label(frame, text="Date:", fg="#406978", font=FONT["Button"])
        self.d_edit_label.grid(row=5, column=0, sticky="e")
        
        self.d_edit_box = Entry(frame)
        self.d_edit_box.grid(row=5, column=1, sticky="ew")
        
        #Edit button
        self.edit_button = Button(frame, text="Edit", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.edit_trip(self.i_edit_box.get(), self.v_edit_box.get().upper(), self.r_edit_box.get(), self.d_edit_box.get()))
        self.edit_button.grid(row=6, column=0, columnspan=3)
        
        #Delete button
        self.delete_button = Button(frame, text="Delete", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.delete_trip(self.i_edit_box.get()))
        self.delete_button.grid(row=7, column=0, columnspan=3)        
        
        #Save button
        self.save_edit_button = Button(frame, text="Save", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.save(self.message_edit))
        self.save_edit_button.grid(row=8, column=0, columnspan=3)        
        
        #Message box
        self.message_edit = Label(frame, text="", fg="#406978", font=FONT["Button"])
        self.message_edit.grid(row=9, column=0, columnspan=3)
        
        return frame  
    
    def create_settings_frame(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)   
        frame.grid_columnconfigure(1, weight=1)   
        frame.grid_columnconfigure(2, weight=1)            
        
        #Settings Header
        self.settings_heading = Label(frame, text="Settings", bg=HEADING[THEME], fg=HEADINGTEXT[THEME], font=FONT["Heading"], width=20)
        self.settings_heading.grid(row=0, column=0, sticky="nsew", columnspan=3)
        
        #Back button
        self.settings_back_button = Button(frame, text="Back", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.show_window("MenuFrame"))
        self.settings_back_button.grid(row=1, column=0)
        
        #Theme (label and combobox)
        self.theme_label = Label(frame, text="Theme:", fg="#406978", font=FONT["Button"])
        self.theme_label.grid(row=2, column=0, sticky="e")
        
        self.theme_choice = StringVar()
        self.theme_choice.set(THEME)
        self.theme_box = ttk.Combobox(frame, textvariable=self.theme_choice, state="readonly")
        self.theme_box['values'] = sorted(list(HEADING.keys()))
        self.theme_box.grid(row=2, column=1, sticky="ew")
        
        #Source (label and box)
        self.source_label = Label(frame, text="Source:", fg="#406978", font=FONT["Button"])
        self.source_label.grid(row=3, column=0, sticky="e")
        
        self.source_box = Entry(frame)
        self.source_box.insert(0, SOURCE)
        self.source_box.grid(row=3, column=1, sticky="ew")
        
        #Column names label
        self.route_label = Label(frame, text="Column names", fg="#406978", font=FONT["Button"])
        self.route_label.grid(row=4, column=0, columnspan=3)        
        
        #Vehicle (label and box)
        self.vehicle_label = Label(frame, text="Vehicle:", fg="#406978", font=FONT["Button"])
        self.vehicle_label.grid(row=5, column=0, sticky="e")
        
        self.vehicle_box = Entry(frame)
        self.vehicle_box.insert(0, VEHICLE)
        self.vehicle_box.grid(row=5, column=1, sticky="ew")
        
        #Route (label and box)
        self.route_label = Label(frame, text="Route:", fg="#406978", font=FONT["Button"])
        self.route_label.grid(row=6, column=0, sticky="e")
        
        self.route_box = Entry(frame)
        self.route_box.insert(0, ROUTE)
        self.route_box.grid(row=6, column=1, sticky="ew")
        
        #Date (label and box)
        self.date_label = Label(frame, text="Date:", fg="#406978", font=FONT["Button"])
        self.date_label.grid(row=7, column=0, sticky="e")
        
        self.date_box = Entry(frame)
        self.date_box.insert(0, DATE)
        self.date_box.grid(row=7, column=1, sticky="ew")        
        
        #Save button
        self.settings_button = Button(frame, text="Save", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.update_settings(self.theme_box.get(), self.source_box.get(), self.vehicle_box.get(), self.route_box.get(), self.date_box.get()))
        self.settings_button.grid(row=8, column=0, columnspan=3)     
        
        #Message box
        self.message_settings = Label(frame, text="", fg="#406978", font=FONT["Button"])
        self.message_settings.grid(row=9, column=0, columnspan=3)
        
        return frame         
    
    def v_search(self, search): #Search for vehicles in trips list
        self.search_subheading.configure(text=f"Trips on {search}")
        results = []
        for i in range(len(trips)):
            if trips[i].vehicle_search(search, i + 1) != None:
                results.append(trips[i].vehicle_search(search, i + 1))
        self.search_results.delete(0, END)
        self.search_results.insert(END, f"{len(results)} trip(s) on {search}")
        for o in results: #Combine all results into a single string
            self.search_results.insert(END, o)
        
    def r_search(self, search): #Search for routes in trips list
        self.search_subheading.configure(text=f"Trips on {search}")
        results = []
        for i in range(len(trips)):
            if trips[i].route_search(search, i + 1) != None:
                results.append(trips[i].route_search(search, i + 1))
        self.search_results.delete(0, END)
        self.search_results.insert(END, f"{len(results)} trip(s) on {search}")
        for o in results: #Combine all results into a single string
            self.search_results.insert(END, o)   
        
    def d_search(self, search): #Search for date in trips list
        self.search_results.delete(0, END)
        if self.date_check(search) == True:
            self.search_subheading.configure(text=f"Trips on {search}")
            results = []
            for i in range(len(trips)):
                if trips[i].date_search(search, i + 1) != None:
                    results.append(trips[i].date_search(search, i + 1))
            self.search_results.insert(END, f"{len(results)} trip(s) on {search}")
            for o in results: #Combine all results into a single string
                self.search_results.insert(END, o)
        else:
            self.search_subheading.configure(text="Invalid Date")
            output = self.date_check(search).split("\n")
            for o in output:
                self.search_results.insert(END, o)
        
    def i_search(self, search): #Find specific trip with ID
        self.search_results.delete(0, END)
        try:
            if int(search) <= 0: #Error handling if zero or negative is entered
                self.search_subheading.configure(text="Invalid input")
                self.search_results.insert(END, "Please enter a number greater than zero") 
            elif int(search) > len(trips): #Error handling if number is greater than max service ID
                self.search_subheading.configure(text="Trip not found")
                self.search_results.insert(END, "No trip with this ID found")
            else:
                self.search_subheading.configure(text=f"Trip {search}")
                for o in trips[int(search)-1].ID_search():
                    self.search_results.insert(END, o)
        except ValueError: #Error handling if non integer is entered
            self.search_subheading.configure(text="Invalid input")
            self.search_results.insert(END, "Please enter a whole number")
            
    def date_check(self, date): #Check if the date is formatted correctly and not in the future
        try:
            d, m, y = date.split("/") #Split date into parts and check if valid
            if int(y) > Y:
                return("Date can't be in the future")
            elif int(y) == Y and int(m) > M:
                return("Date can't be in the future")
            elif int(m) == M and int(d) > D:
                return("Date can't be in the future")
            elif len(date) != 10:
                return("Invalid date format\nPlease use DD/MM/YYYY")
            elif int(d) > 31 or int(m) > 12:
                return("Invalid date")
            else:
                return True #Return true value if valid
        except:
            return("Invalid date format\nPlease use DD/MM/YYYY")
    
    def log_trip(self, vehicle, route, date): #Add trips to trip list in program
        if self.date_check(date) == True and vehicle != '' and route != '': #Check validity of entry
            trips.append(Trip(vehicle, route, date))
            self.message_log.configure(text=f"Saved trip with ID: {len(trips)}")
            self.v_log_box.delete(0, 'end')
            self.r_log_box.delete(0, 'end')   
        else:
            self.message_log.configure(text="Invalid trip details")
            
    def save(self, message):
        with open(SOURCE, "w", newline='') as  tripfile: #Export trips to CSV file
            fields = [VEHICLE, ROUTE, DATE]
            export = csv.DictWriter(tripfile, fieldnames=fields)
            export.writeheader()
            for i in trips:
                export.writerow({fields[0]:i.vehicle, fields[1]:i.route, fields[2]:i.date}) #Write each trip to file
            message.configure(text="Saved to file")
            
    def edit_trip(self, ID, vehicle, route, date): #Updates trip details
        try:
            ID = int(ID)
            if ID <= 0 or ID > len(trips):
                self.message_edit.configure(text="Please enter a valid ID")
            else:
                if vehicle != '':
                    trips[ID-1].vehicle = vehicle.upper()
                if route != '':
                    trips[ID-1].route = route
                if date != '' and self.date_check(date) == True:
                    trips[ID-1].date = date
                self.message_edit.configure(text="Updated trip details")
        except ValueError:
            self.message_edit.configure(text="Please enter a whole number for ID")
    
    def delete_trip(self, ID): #Deletes trip details
        try:
            ID = int(ID) 
            if ID > 0 and ID <= len(trips): #Check if trip exists, if so replace all details with 'DELETED'
                trips[ID-1].vehicle = "DELETED"
                trips[ID-1].route = "DELETED"
                trips[ID-1].date = "DELETED"
                self.message_edit.configure(text=f"Deleted trip with ID: {ID}")
            else:
                self.message_edit.configure(text="Error, trip not found")
        except ValueError:
            self.message_edit.configure(text="Please enter a whole number for ID")    
    
    def update_settings(self, theme, source, vehicle, route, date): #Updates settings
        if source[-4:] != ".csv":
            self.message_settings.configure(text="Please enter a valid filename (filename.csv)")
        else:
            config = {"THEME":theme, "SOURCE":source, "VEHICLE":vehicle, "ROUTE":route, "DATE":date}
            with open("config.json", "w") as f:
                json.dump(config, f, indent=2)
            self.message_settings.configure(text="Relaunch required")
            
    def autofill_edit(self, ID): #Autofills boxes in editing menu
        self.v_edit_box.delete(0, 'end')
        self.r_edit_box.delete(0, 'end')
        self.d_edit_box.delete(0, 'end')
        try:
            ID = int(ID)
            if ID > 0 and ID <= len(trips): #If trip exists, get details and autofill boxes
                self.v_edit_box.insert(0, trips[ID-1].vehicle)
                self.r_edit_box.insert(0, trips[ID-1].route)
                self.d_edit_box.insert(0, trips[ID-1].date)
            else:
                self.message_edit.configure(text="Error, trip not found")
        except ValueError:
            self.message_edit.configure(text="Please enter a whole number for ID")
    
    def run(self):
        self.master.mainloop()
        
app = GUI()
app.run()