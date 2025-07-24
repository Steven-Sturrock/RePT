#RePT Public Transport Recap
#Steven Sturrock

'''
V0.0.1 - Initial version 
V0.0.2 - Created constants for column names and current date variables for validation
V0.0.3 - Set up basic GUI components including themes
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
HEADING = {"AT":"#00A7E5", "Metlink":"#00364a"}
HEADINGTEXT = {"AT":"#ffffff", "Metlink":"#ffffff"}
SUBHEADING = {"AT":"#0073BD", "Metlink":"#cddc2a"}
SUBHEADINGTEXT = {"AT":"#ffffff", "Metlink":"#00364a"}
BUTTON = {"AT":"#e4f5fb", "Metlink":"#406978"}
BUTTONTEXT = {"AT":"#535353", "Metlink":"#ffffff"}
FONT = {"Heading":"Arial 40 bold", "Subheading":"Arial 25 bold", "Button":"Arial 20", "Text":"Arial 11"}

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("RePT")
        
        Title = Label(master, text="RePT", bg=HEADING[THEME], fg=HEADINGTEXT[THEME], font=FONT["Heading"], width=15)
        Title.grid(row=0, column=0, columnspan = 2, sticky=NSEW)
        
        sh = Label(master, text="Sub Heading", bg=SUBHEADING[THEME], fg=SUBHEADINGTEXT[THEME], font=FONT["Subheading"])
        sh.grid(row=1, column=1, sticky=NSEW)
        
        b = Label(master, text="Button", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Button"], highlightbackground="black", highlightthickness=1)
        b.grid(row=1, column=0)
        
        t = Label(master, text="Text", bg=BUTTON[THEME], fg=BUTTONTEXT[THEME], font=FONT["Text"], highlightbackground="black", highlightthickness=1)
        t.grid(row=2, column=1, sticky=NSEW)        
        
root = Tk()
app = GUI(root)
root.mainloop()