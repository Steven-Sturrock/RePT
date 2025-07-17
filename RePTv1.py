#RePT Public Transport Recap
#Steven Sturrock

'''
V0.0.1 - Initial version 
V0.0.2 - Created constants for column names and current date variables for validation
'''

#Libraries
from tkinter import *
import csv
import datetime

#Column names
ROUTE = 'Route'
VEHICLE = 'Vehicle'
DATE = 'Date'

#Current date (validation)
D = datetime.datetime.now().strftime("%d")
M = datetime.datetime.now().strftime("%m")
Y = datetime.datetime.now().strftime("%Y")
