#RePT Public Transport Recap
#Steven Sturrock

'''
V0.0.1 - Initial version 
V0.0.2 - Created constants for column names and current date variables for validation
V0.0.3 - Set up basic GUI components including themes
V0.0.4 - Set up frames for multiple windows
V0.0.5 - Created classes and import script
V0.1.0 - Set up basic search demo using HE604
'''

#Libraries
from tkinter import *
import csv
import datetime

#Settings
THEME = "Huia"
SOURCE = "trips.csv"

#Column names
ROUTE = 'Route'
VEHICLE = 'Vehicle'
DATE = 'Date'

#Current date (validation)
D = datetime.datetime.now().strftime("%d")
M = datetime.datetime.now().strftime("%m")
Y = datetime.datetime.now().strftime("%Y")

#Design components
HEADING = {"AT":"#00A7E5", "Metlink":"#00364a", "Huia":"#282829", "MAXX":"#ffc02f"}
HEADINGTEXT = {"AT":"#ffffff", "Metlink":"#ffffff", "Huia":"#ffc90e", "MAXX":"#ffffff"}
SUBHEADING = {"AT":"#2d7caf", "Metlink":"#cddc2a", "Huia":"#323d48", "MAXX":"#f4661d"}
SUBHEADINGTEXT = {"AT":"#ffffff", "Metlink":"#00364a", "Huia":"#ffffff", "MAXX":"#ffffff"}
BUTTON = {"AT":"#00A7E5", "Metlink":"#406978", "Huia":"#ffc90e", "MAXX":"#00a3e6"}
BUTTONTEXT = {"AT":"#ffffff", "Metlink":"#ffffff", "Huia":"#282829", "MAXX":"#ffffff"}
FONT = {"Heading":"Arial 40 bold", "Subheading":"Arial 25 bold", "Button":"Arial 18", "Text":"Arial 12"}

#Classes
class Trip:
    def __init__(self, vehicle, route, date, service_id):
        self.vehicle = vehicle.upper()
        self.route = route
        self.date = date
        self.service_id = service_id
        
    def __str__(self):
        return f"Vehicle: {self.vehicle}\nRoute: {self.route}\nDate: {self.date}\nService ID: {self.service_id}"
    
    def vehicle_search(self, search):
        if self.vehicle == search:
            return f"{self.route} - {self.date}"
        else:
            return None

#Load data
with open(SOURCE) as tripfile:
    trips = []
    for i in csv.DictReader(tripfile):
        trips.append(Trip(i['Vehicle'], i['Route'], i['Date'], i['Service No.']))    

#Main program
class GUI:
    def __init__(self):
        #Create window
        self.master = Tk()
        self.master.title("RePT")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        
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
        
        #Show main menu on start
        self.show_window("MenuFrame")
        
    def show_window(self, name):
        self.frame = self.frames[name] #Select the frame
        self.frame.tkraise() #Move frame to top
        
    def create_menu_frame(self): #Main menu
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        
        self.heading = Label(frame, text="RePT", bg=HEADING[THEME], fg=HEADINGTEXT[THEME], font=FONT["Heading"], width=20)
        self.heading.grid(row=0, column=0, sticky="nsew")
        
        self.heading = Label(frame, text="Public Transport Recap", bg=SUBHEADING[THEME], fg=SUBHEADINGTEXT[THEME], font=FONT["Subheading"], width=20)
        self.heading.grid(row=1, column=0, sticky="nsew")        
        
        self.search_button = Button(frame, text="Search trips", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=10, command=lambda: self.show_window("SearchFrame"))
        self.search_button.grid(row=2, column=0, sticky="nsew", pady=10, padx=10)
        
        self.log_button = Button(frame, text="Log trips", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=10, command=lambda: self.show_window("LogFrame"))
        self.log_button.grid(row=3, column=0, sticky="nsew", pady=10, padx=10)        
        
        self.edit_button = Button(frame, text="Edit trip", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=10, command=lambda: self.show_window("EditFrame"))
        self.edit_button.grid(row=4, column=0, sticky="nsew", pady=10, padx=10)                
        
        return frame
        
    def create_search_frame(self): #Vehicle search
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        
        self.search_title = Label(frame, text="Search", bg=HEADING[THEME], fg=HEADINGTEXT[THEME], font=FONT["Heading"], width=20)
        self.search_title.grid(row=0, column=0, columnspan = 2, sticky="nsew")
        
        self.search_header = Label(frame, text="", bg=SUBHEADING[THEME], fg=SUBHEADINGTEXT[THEME], font=FONT["Subheading"])
        self.search_header.grid(row=1, column=1, sticky="nsew")
        
        self.back_button = Button(frame, text="Back", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.show_window("MenuFrame"))
        self.back_button.grid(row=1, column=0)
        
        self.test = Button(frame, text="Search", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.v_search())
        self.test.grid(row=2, column=0)
        
        self.search_results = Label(frame, text="Results will appear here", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Text"], highlightbackground="black", highlightthickness=1)
        self.search_results.grid(row=2, column=1, sticky="nsew")        
        
        return frame
    
    def create_log_frame(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        
        self.title = Label(frame, text="Not yet implemented", bg=HEADING[THEME], fg=HEADINGTEXT[THEME], font=FONT["Heading"], width=20)
        self.title.grid(row=0, column=0, sticky="nsew")
        
        return frame
    
    def create_edit_frame(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        
        self.title = Label(frame, text="Not yet implemented", bg=HEADING[THEME], fg=HEADINGTEXT[THEME], font=FONT["Heading"], width=20)
        self.title.grid(row=0, column=0, sticky="nsew")        
        
        return frame
    
    def v_search(self):
        self.search_header.configure(text=f"Trips on HE604")
        results = []
        for i in trips:
            if i.vehicle_search("AM604") != None:
                results.append(i.vehicle_search("HE604"))
        output = f"{len(results)} trips on HE604"
        for o in range(len(results)):
            output += f"\n{str(results[o])}"
        self.search_results.configure(text=(output))
    def run(self):
        self.master.mainloop()
        
app = GUI()
app.run()