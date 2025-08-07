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
'''

#Libraries
from tkinter import *
import csv
import datetime

#Settings
THEME = "Metlink"
SOURCE = "trips.csv"

#Column names
ROUTE = 'Route'
VEHICLE = 'Vehicle'
DATE = 'Date'

#Current date (validation)
D = int(datetime.datetime.now().strftime("%d"))
M = int(datetime.datetime.now().strftime("%m"))
Y = int(datetime.datetime.now().strftime("%Y"))

#Design constants
HEADING = {"AT":"#2d7caf", "Metlink":"#00364a", "Huia":"#282829", "MAXX":"#ffc02f"}
HEADINGTEXT = {"AT":"#ffffff", "Metlink":"#ffffff", "Huia":"#ffc90e", "MAXX":"#ffffff"}
SUBHEADING = {"AT":"#00A7E5", "Metlink":"#cddc2a", "Huia":"#323d48", "MAXX":"#f4661d"}
SUBHEADINGTEXT = {"AT":"#ffffff", "Metlink":"#00364a", "Huia":"#ffffff", "MAXX":"#ffffff"}
BUTTON = {"AT":"#d4edfc", "Metlink":"#406978", "Huia":"#ffc90e", "MAXX":"#00a3e6"}
BUTTONTEXT = {"AT":"#282829", "Metlink":"#ffffff", "Huia":"#282829", "MAXX":"#ffffff"}
FONT = {"Heading":"Arial 40 bold", "Subheading":"Arial 25 bold", "Button":"Arial 14", "Text":"Arial 12"}

#Classes
class Trip:
    def __init__(self, vehicle, route, date, service_id):
        self.vehicle = vehicle.upper()
        self.route = route
        self.date = date
        self.service_id = service_id
        
    #Print all vehicle data
    def __str__(self):
        return f"Vehicle: {self.vehicle}\nRoute: {self.route}\nDate: {self.date}\nService ID: {self.service_id}"
    
    #Check if search term is equal to self.vehicle and return data if true
    def vehicle_search(self, search):
        if self.vehicle == search:
            return f"{self.route} - {self.date} - ID:{self.service_id}"
        else:
            return None
    
    #Check if search term is equal to self.route and return data if true
    def route_search(self, search):
        if self.route == search:
            return f"{self.vehicle} - {self.date} - ID:{self.service_id}"
        else:
            return None
    
    #Check if search term is equal to self.date and return data if true
    def date_search(self, search):
        if self.date == search:
            return f"{self.vehicle} - {self.route} - ID:{self.service_id}"
        else:
            return None
    
    #Check if search term is equal to self.service_id and return data if true
    def id_search(self, search):
        if self.service_id == search:
            return self
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
        
        #Menu heading
        self.heading = Label(frame, text="RePT", bg=HEADING[THEME], fg=HEADINGTEXT[THEME], font=FONT["Heading"], width=20)
        self.heading.grid(row=0, column=0, sticky="nsew")
        
        #Menu subheading
        self.subheading = Label(frame, text="Public Transport Recap", bg=SUBHEADING[THEME], fg=SUBHEADINGTEXT[THEME], font=FONT["Subheading"], width=20)
        self.subheading.grid(row=1, column=0, sticky="nsew")        
        
        #Search menu button
        self.search_button = Button(frame, text="Search trips", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=10, command=lambda: self.show_window("SearchFrame"))
        self.search_button.grid(row=2, column=0, sticky="nsew", pady=10, padx=10)
        
        #Log menu heading
        self.log_button = Button(frame, text="Log trips", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=10, command=lambda: self.show_window("LogFrame"))
        self.log_button.grid(row=3, column=0, sticky="nsew", pady=10, padx=10)        
        
        #Edit menu heading
        self.edit_button = Button(frame, text="Edit trip", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=10, command=lambda: self.show_window("EditFrame"))
        self.edit_button.grid(row=4, column=0, sticky="nsew", pady=10, padx=10)                
        
        return frame
        
    def create_search_frame(self): #Vehicle search
        #Create frame
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        
        #Search heading
        self.search_heading = Label(frame, text="Search", bg=HEADING[THEME], fg=HEADINGTEXT[THEME], font=FONT["Heading"], width=20)
        self.search_heading.grid(row=0, column=0, columnspan = 4, sticky="nsew")
        
        #Search subheading
        self.search_subheading = Label(frame, text="", bg=SUBHEADING[THEME], fg=SUBHEADINGTEXT[THEME], font=FONT["Subheading"])
        self.search_subheading.grid(row=1, column=3, sticky="nsew")
        
        #Back button
        self.back_button = Button(frame, text="Back", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.show_window("MenuFrame"))
        self.back_button.grid(row=1, column=0)
        
        #Vehicle search
        self.v_label = Label(frame, text="Vehicle:", fg="#406978", font=FONT["Button"])
        self.v_label.grid(row=2, column=0)
        
        self.v_box = Entry(frame)
        self.v_box.grid(row=2, column=1, sticky="ew")
        
        self.v_button = Button(frame, text="Search", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.v_search(self.v_box.get().upper()))
        self.v_button.grid(row=2, column=2)
        
        #Route search
        self.r_label = Label(frame, text="Route:", fg="#406978", font=FONT["Button"])
        self.r_label.grid(row=3, column=0)        
        
        self.r_box = Entry(frame)
        self.r_box.grid(row=3, column=1, sticky="ew")
        
        self.r_button = Button(frame, text="Search", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.r_search(self.r_box.get()))
        self.r_button.grid(row=3, column=2)
        
        #Date search
        self.d_label = Label(frame, text="Date:", fg="#406978", font=FONT["Button"])
        self.d_label.grid(row=4, column=0)        
        
        self.d_box = Entry(frame)
        self.d_box.grid(row=4, column=1, sticky="ew")
        
        self.d_button = Button(frame, text="Search", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.d_search(self.d_box.get()))
        self.d_button.grid(row=4, column=2)            
        
        #ID search
        self.i_label = Label(frame, text="Trip ID:", fg="#406978", font=FONT["Button"])
        self.i_label.grid(row=5, column=0)        
        
        self.i_box = Entry(frame)
        self.i_box.grid(row=5, column=1, sticky="ew")
        
        self.i_button = Button(frame, text="Search", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.i_search(self.i_box.get()))
        self.i_button.grid(row=5, column=2)            
        
        #Results
        self.search_results = Label(frame, text="Results will appear here", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Text"], highlightbackground="black", highlightthickness=1)
        self.search_results.grid(row=2, column=3, sticky="nsew", rowspan=5)        
        
        return frame
    
    def create_log_frame(self): #Unfinished
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        
        self.title = Label(frame, text="Coming soon", bg=HEADING[THEME], fg=HEADINGTEXT[THEME], font=FONT["Heading"], width=20)
        self.title.grid(row=0, column=0, sticky="nsew")
        
        self.back_button = Button(frame, text="Back", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.show_window("MenuFrame"))
        self.back_button.grid(row=1, column=0)               
        
        return frame
    
    def create_edit_frame(self): #Unfinished
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        
        self.title = Label(frame, text="Coming soon", bg=HEADING[THEME], fg=HEADINGTEXT[THEME], font=FONT["Heading"], width=20)
        self.title.grid(row=0, column=0, sticky="nsew")
        
        self.back_button = Button(frame, text="Back", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], width=5, command=lambda: self.show_window("MenuFrame"))
        self.back_button.grid(row=1, column=0)        
        
        return frame
    
    def v_search(self, search): #Search for vehicles in trips list
        self.search_subheading.configure(text=f"Trips on {search}")
        results = []
        for i in trips:
            if i.vehicle_search(search) != None:
                results.append(i.vehicle_search(search))
        output = f"{len(results)} trip(s) on {search}"
        for o in range(len(results)):
            output += f"\n{str(results[o])}"
        self.search_results.configure(text=(output))
        
    def r_search(self, search): #Search for routes in trips list
        self.search_subheading.configure(text=f"Trips on {search}")
        results = []
        for i in trips:
            if i.route_search(search) != None:
                results.append(i.route_search(search))
        output = f"{len(results)} trip(s) on {search}"
        for o in range(len(results)):
            output += f"\n{str(results[o])}"
        self.search_results.configure(text=(output))    
        
    def d_search(self, search): #Search for date in trips list
        if self.date_check(search) == True:
            self.search_subheading.configure(text=f"Trips on {search}")
            results = []
            for i in trips:
                if i.date_search(search) != None:
                    results.append(i.date_search(search))
            output = f"{len(results)} trip(s) on {search}"
            for o in range(len(results)):
                output += f"\n{str(results[o])}"
            self.search_results.configure(text=(output))
        elif self.date_check(search) == False:
            self.search_subheading.configure(text="Invalid Date")
            self.search_results.configure(text="Please enter a date that is not in the future")
        else:
            self.search_subheading.configure(text="Invalid Date")
            self.search_results.configure(text=self.date_check(search))
        
    def i_search(self, search): #Find specific trip with ID
        try:
            if int(search) <= 0: #Error handling if zero or negative is entered
                self.search_subheading.configure(text="Invalid input")
                self.search_results.configure(text="Please enter a number greater than zero") 
            elif int(search) > len(trips): #Error handling if number is greater than max service ID
                self.search_subheading.configure(text="Trip not found")
                self.search_results.configure(text="No trip with this ID found")
            else:
                self.search_subheading.configure(text=f"Trip {search}")
                results = None
                for i in trips:
                    if i.id_search(search) != None:
                        results = i.id_search(search)
                self.search_results.configure(text=results)   
        except ValueError: #Error handling if non integer is entered
            self.search_subheading.configure(text="Invalid input")
            self.search_results.configure(text="Please enter a whole number")
            
    def date_check(self, date):
        try:
            d, m, y = date.split("/")
            if int(y) > Y:
                return False
            elif int(y) == Y and int(m) > M:
                return False
            elif int(m) == M and int(d) > D:
                return False
            else:
                return True
        except:
            return("Invalid date format\nPlease use MM/DD/YYYY")
    def run(self):
        self.master.mainloop()
        
app = GUI()
app.run()