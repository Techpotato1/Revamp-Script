from base64 import decode
import datetime
import os
import random
import shutil
import time
import webbrowser
import requests
import json
from requests import get
import pyttsx3
from colorama import init, Fore, Back, Style
from datetime import datetime
import keyboard
import wikipedia
import sys
from toolboxlibrary import *

# essential for Windows environment
init()

# print the the options for the user to choose from


def printoptions():
    print("""What would you like to do next? \n
1. Check the time
2. Check the date
3. Change the weather location
4. Check the weather
5. Change your name
6. Wikipedia
7. Exit \n
Developer Options:
8. Clear the screen
9. Delete the info folder
10. List the contents of the current directory
11. Check the time that the program was last run
12. Open a URL
13. Autofill the weather location from IP
14. Print your public IP address
15. List the contents of the info folder
16. Generate a random number
17. Calculate PI
\n""")

# get the weather from the API


def getweather():
    # base URL
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    # City Name
    CITY = weatherlocation
    # updating the URL
    URL = BASE_URL + "q=" + CITY + "&appid=" + "!! WEATHER API!!"
    # HTTP request
    response = requests.get(URL)
    # checking the status code of the request
    if response.status_code == 200:
        # getting data in the json format
        data = response.json()
        # getting the main dict block
        main = data['main']
        # getting temperature
        temperature = main['temp']
        # getting the humidity
        humidity = main['humidity']
        # getting the pressure
        pressure = main['pressure']
        # weather report
        report = data['weather']
        # convert the temperature to fahrenheit
        temperature = temperature * (9/5) - 459.67
        # round the temperature to 2 decimal places
        temperature = round(temperature, 2)
        print(f"{CITY:-^30}")
        print(f"Temperature: {temperature}")
        print(f"Humidity: {humidity}")
        print(f"Pressure: {pressure}")
        print(f"Weather Report: {report[0]['description']}")
    else:
        # showing the error message
        print_with_color("Error in the HTTP request",
                         color=Fore.RED, brightness=Style.DIM)
        print("Try checking the city name")

# get the approximate location of the user from their IP address
def getcity(ip_address):
    # URL to send the request to
    request_url = 'https://geolocation-db.com/jsonp/' + ip_address
# Send request and decode the result
    response = requests.get(request_url)
    result = response.content.decode()
# Clean the returned string so it just contains the dictionary data for the IP address
    result = result.split("(")[1].strip(")")
# Convert this data into a dictionary
    result = json.loads(result)
# get the city name from the result
    postal = result['postal']
    return postal

# Wrapper function
def main():

    # Calls CalcPi with the given limit
    pi_digits = calcPi(
        int(input("Enter the number of decimals to calculate to: ")))

    i = 0

    # Prints the output of calcPi generator function
    # Inserts a newline after every 40th number
    for d in pi_digits:
        print(d, end='')
        i += 1
        if i == 40:
            print("")
            i = 0


# Create a folder in the same directory as the script called "info"
try:
    os.mkdir("info")
except FileExistsError:
    pass

# Gets the IP address of the user
ip_address = get('https://api.ipify.org').text
name = ""
choice = ""
weatherlocation = ""
oldtimeanddate = ""
engine = pyttsx3.init()
engine.setProperty('rate', 120)
wikipediacount = 3
wikipediachoice = "0"

# Get the contents of the current directory
contentsofdir = os.listdir(os.getcwd())
contentsofinfodir = os.listdir("info")

# format the date nicely
date = datetime.now()
date = date.strftime("%A, %B %d, %Y")

# setts the currenttime variable to the current time
currenttime = gettime()

# if userinfo.txt exists, open it and read the name
try:
    with open("info/userinfo.txt", "rb") as f:
        nameencoded = f.read()
        name = nameencoded.decode("utf-8", "strict")
except:
    pass

# if weatherlocation.txt exists, open it and read the file
try:
    with open("info/weatherlocation.txt", "r") as f:
        weatherlocation = f.read()
except FileNotFoundError:
    pass

# an unused function to get the last contents of the info folder
try:
    with open("info/currentdir", "r") as f:
        olddircontents = f.read()
except FileNotFoundError:
    pass

# if timeanddate.txt exists, open it and read the file
try:
    with open("info/timeanddate.txt", "r") as f:
        oldtimeanddate = f.read()
except FileNotFoundError:
    pass

# write the time and date to a file called timeanddate.txt
with open("info/timeanddate.txt", "w") as f:
    f.write("Date last run: \n")
    f.write(date)
    f.write("\n")
    f.write(currenttime)

# CLEARS THE SCREEN
clearscreen()

# if there is nothing in name, ask for it
if name == "":
    name = input("What is your name? \n")

# create a file called userinfo.txt and write the name to it/
try:
    with open("info/userinfo.txt", "wb") as file:
        nameencoded = name.encode("utf-8", "strict")
        file.write(nameencoded)
except:
    print_with_color("Error creating file!",
                     color=Fore.RED, brightness=Style.DIM)
    print_with_color("You will be asked for your name the next time you open the program.",
                     color=Fore.RED, brightness=Style.DIM)

# get the user's name and greet them
print("Hello, " + name + "!")
print("Today's date is " + date)
print("The time is " + currenttime)

#Don't exit the program until the user enters 7 
while choice != "7":

    # prints the options for the user to choose from
    printoptions()

    # asks the user to choose an option
    choice = input("Enter your choice: ")
    # clears the screen
    clearscreen()

    # if the user chooses 1, check the time
    if choice == "1" or choice == "time":
        timeold = ""
        while not keyboard.is_pressed("esc"):
            curtime = gettimespecific()
            if not timeold == curtime:
                timeold = curtime
                clearscreen()
                print("The time is " + timeold + "\nPress 'esc' to exit")

    # if the user chooses 2, check the date
    elif choice == "2" or choice == "date":
        print(date)

    # if the user chooses 3, get the weather location
    elif choice == "3":
        weatherlocation = input("What is your city? \n")
        with open("info/weatherlocation.txt", "w") as file:
            file.write(weatherlocation)

    # if the user chooses 4, get the weather
    elif choice == "4" or choice == "weather":
        if weatherlocation == "":
            weatherlocation = input(
                "What is your city? (Zip codes will work) \n")
            with open("info/weatherlocation.txt", "w") as file:
                file.write(weatherlocation)
            getweather()
            print("\n")
        else:
            getweather()
            print("\n")

    # if the user chooses 5, get the user's name
    elif choice == "5" or choice == "name":
        name = input("What is your name? \n")
        try:
            with open("info/userinfo.txt", "w") as file:
                file.write(name)
            print_with_color("Name Changed to: " + name, color=Fore.GREEN)
        except:
            print_with_color("Invalid Name!", color=Fore.RED)

    elif choice == "6" or choice == "wikipedia":
        print("1. Search Wikipedia \n" + "2. Change sentence count")
        wikipediachoice = input("What would you like to do \n")
        if wikipediachoice == "1":
            try:
                clearscreen()
                searchterm = input(
                    'Enter a search term: \n' + '(Use parentheses to denote the type, ex: "Mars (Planet)") \n')
                clearscreen()
                print("Loading!")
                print(wikipedia.summary(searchterm, sentences=wikipediacount))
            except wikipedia.exceptions.DisambiguationError:
                print_with_color("Invalid Search Term!", color=Fore.RED)
                print_with_color("Try again!", color=Fore.RED)
        elif wikipediachoice == "2":
            try:
                clearscreen()
                wikipediacount = int(
                    input('Enter the number of sentences to display: \n'))
                print_with_color("Number of sentences changed to: " +
                                 str(wikipediacount), color=Fore.GREEN)
            except:
                print_with_color("Invalid Number!", color=Fore.RED)
        else:
            print_with_color("Invalid number!", color=Fore.RED)

    # if the user chooses 6, exit the program
    elif choice == "7" or choice == "exit":
        clearscreen()
        i = input("Press Enter to continue or type cancel to cancel: \n")
        if i == "Cancel" or "cancel" in i:
            print("Canceled\n")
            choice = ""
        else:
            print("Goodbye!")
            time.sleep(0.5)
            try:
                sys.exit()
            except:
                os._exit(0)

    # if the user chooses 10, clear the screen
    elif choice == "8" or choice == "clear":
        print("Clearing screen...")
        time.sleep(0.5)
        clearscreen()

    # if the user chooses 11, delete the info folder
    elif choice == "9" or choice == "delete info":
        try:
            shutil.rmtree("info")
            print_with_color("Deleting info folder...",
                             color=Fore.RED, brightness=Style.DIM)
            time.sleep(0.5)
            print_with_color("Done!", color=Fore.GREEN, brightness=Style.DIM)
        except FileNotFoundError:
            pass

    # if the user chooses 12, list the contents of the current directory
    elif choice == "10" or choice == "list current dir":
        print("Contents of the current directory: \n")
        for i in contentsofdir:
            print(i)
        print("\n")

    # if the user chooses 13, display the time the program was last run
    elif choice == "11" or choice == "time last run":
        if oldtimeanddate == "":
            print("No previous time and date")
        else:
            print(oldtimeanddate)

    # if the user chooses 14, ask the user what url they want to open
    elif choice == "12" or choice == "open url":
        # ask the user what url they want to open
        urlopen = input("What is the url you want to open? \n")
        # open the url in the default browser
        webbrowser.open(urlopen)

    # if the user chooses 15, locate their current location using their IP address
    elif choice == "13" or choice == "ip locate":
        weatherlocation = getcity(ip_address)
        with open("info/weatherlocation.txt", "w") as file:
            file.write(weatherlocation)
        print("Your city is " + weatherlocation + "." + "\n")

    # if the user chooses 16, display their current IP address
    elif choice == "14" or choice == "ip":
        print("Your IP address is " + ip_address + "." + "\n")

    # if the user chooses 17, display contents of the info folder
    elif choice == "15" or choice == "list info":
        print("Contents of the info directory: \n")
        contentsofinfodir = os.listdir("info")
        for i in contentsofinfodir:
            print(i)
        print("\n")

    # if the user chooses 20, choose a random number
    elif choice == "16" or choice == "randomnum":
        firstbetween = int(input("What is the smallest number? \n"))
        secondbetween = int(input("What is the largest number? \n"))
        if firstbetween > secondbetween:
            print_with_color("The first number must be smaller than the second number. \n",
                             color=Fore.RED, brightness=Style.DIM)
        else:
            print("Your random number is " +
                  str(random.randint(firstbetween, secondbetween)) + "." + "\n")
    elif choice == "17" or choice == "pi":
        start = datetime.now()
        try:
            main()
            print_with_color("Done!", color=Fore.GREEN, brightness=Style.DIM)
        except KeyboardInterrupt:
            print_with_color("Canceled!", color=Fore.RED, brightness=Style.DIM)
            pass
        end = datetime.now()
        # format the time difference nicely
        time_difference = end - start
        print("Time taken: " + str(time_difference) + "\n")

    else:
        print_with_color("Invalid choice." + "\n",
                         color=Fore.RED, brightness=Style.DIM)
