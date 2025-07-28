#RePT Public Transport Recap
#Steven Sturrock

'''
V0.0.1 - Initial version 
V0.0.2 - Created constants for column names and current date variables for validation
V0.0.3 - Set up basic GUI components including themes
V0.0.4 - Set up frames for multiple windows
'''

#Libraries
from tkinter import *
import csv
import datetime

#Settings
THEME = "Metlink"

#Column names
ROUTE = 'Route'
VEHICLE = 'Vehicle'
DATE = 'Date'

#Current date (validation)
D = datetime.datetime.now().strftime("%d")
M = datetime.datetime.now().strftime("%m")
Y = datetime.datetime.now().strftime("%Y")

#Design components
HEADING = {"AT":"#00A7E5", "Metlink":"#00364a", "Huia":"#282829"}
HEADINGTEXT = {"AT":"#ffffff", "Metlink":"#ffffff", "Huia":"#ffc90e"}
SUBHEADING = {"AT":"#0073BD", "Metlink":"#cddc2a", "Huia":"#323d48"}
SUBHEADINGTEXT = {"AT":"#ffffff", "Metlink":"#00364a", "Huia":"#ffffff"}
BUTTON = {"AT":"#e4f5fb", "Metlink":"#406978", "Huia":"#ffc90e"}
BUTTONTEXT = {"AT":"#535353", "Metlink":"#ffffff", "Huia":"#282829"}
FONT = {"Heading":"Arial 40 bold", "Subheading":"Arial 25 bold", "Button":"Arial 18", "Text":"Arial 12"}

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
        
        return frame
        
    def create_search_frame(self): #Vehicle search
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        
        self.title = Label(frame, text="Search for trips", bg=HEADING[THEME], fg=HEADINGTEXT[THEME], font=FONT["Heading"], width=20)
        self.title.grid(row=0, column=0, columnspan = 2, sticky="nsew")
        
        self.sh = Label(frame, text="Sub Heading", bg=SUBHEADING[THEME], fg=SUBHEADINGTEXT[THEME], font=FONT["Subheading"])
        self.sh.grid(row=1, column=1, sticky="nsew")
        
        self.b = Label(frame, text="Button", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], highlightbackground="black", highlightthickness=1)
        self.b.grid(row=1, column=0)
        
        self.t = Label(frame, text="Text", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Text"], highlightbackground="black", highlightthickness=1)
        self.t.grid(row=2, column=1, sticky="nsew")        
        
        return frame
    
    def create_log_frame(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        
        self.title = Label(frame, text="Not yet implemented", bg=HEADING[THEME], fg=HEADINGTEXT[THEME], font=FONT["Heading"], width=20)
        self.title.grid(row=0, column=0, sticky="nsew")
        
        return frame
        
    def run(self):
        self.master.mainloop()
        
app = GUI()
app.run()