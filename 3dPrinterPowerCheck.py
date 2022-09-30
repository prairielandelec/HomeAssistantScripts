#!/usr/bin/env python
"""
Script to check to see if a Smart Switch/Relay connected to HomeAssistant is on, and if not turn it on
I wrote this script to run after slicing in PrusaSlicer since I use OctoPrint to print directly from PrusaSlicer
My OctoPrint server is connected to the power supply of my printer so if the printer is off, so is the server
This means that most of the PSU related automations inside of OctoPrint don't work for me

This script requires that you have:
1. HomeAssistant installed and running
2. At least one smart switch/relay connected to HomeAssistant
3. The RESTful API enabled in HomeAssistant (this is likely already enabled but if not follow this link):
   https://developers.home-assistant.io/docs/api/rest/
"""

import time
import requests
from tkinter import Tk
from tkinter import messagebox


RELAY_NAME = "YOURRELAYNAME"
HOME_ASST_URL = "http://your.homeassitant.url.here:8123"
TOKEN = "TOKEN"  # ToDo: read this from environment variable

"""
This is the URL that we are going to GET the status information about the relay from
It is likely an ip address (eg. 192.168.x.y) and MUST have your port number that you will be using to access the API. 
This is the same port as your frontend which is likely :8123
This is followed by "/api/states/my.entity" so a complete URL would be:
    "http://192.168.0.1:8123/api/states/switch.powerplug"
"""
STATUS_URL = f"{HOME_ASST_URL}/api/states/switch.{RELAY_NAME}"

"""
This follows the same formula as above, but is for POST messages to turn on the relay that you are trying to control. 
This could require some additional configuration (your relay may be configured in HA as a light for example)
"""
TOGGLE_URL = f"{HOME_ASST_URL}/api/services/switch/turn_on"

"""
This is the payload that is going to be pushed in the POST message, you will 
need to make sure that the entity id matches your entity
"""
DATA = {"entity_id": f"switch.{RELAY_NAME}"}

"""
This is the header that is sent to the API along with your GET and POST messages for authentication
You will need to go to your user profile in the Home Assistant Frontend and create a 
Long-Lived Access Token and paste it below in quotes after the "Authorization":
Content-Type can remain the same
"""
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "content-type": "application/json",
}


def main():
    root = Tk()
    root.withdraw()

    # This will run as long as a break is not hit so if a retry is requested it will hop back to the top of the loop
    while True:

        # get the status of the switch
        response = requests.get(STATUS_URL, headers=HEADERS)

        # handle unsuccessful request response
        if response.status_code != 200:

            # if we cant connect to the API for some reason, keep trying as long as the user clicks "yes"
            if not messagebox.askyesno('Connection Error!', f'Error Code: {response.status_code}\n\nWould You Like To Retry?'):
                break

        # find the dictionary key "state" in the json response
        responsedict = response.json()
        powerstatus = responsedict["state"]

        if powerstatus == "on":
            # if the state is "on" then let us know and move on. May need to change depending on device in HA
            messagebox.showinfo('Connection Success!', f'Connected To API Successfully and Power is {powerstatus.upper()}!')
            break

        elif powerstatus == "off":
            # if the state is "off" then ask if we want to turn it on
            if not messagebox.askyesno(f'Printer Power Is {powerstatus.upper()}!', '\n\nWould You Like To Power On?'):
                break

            # if we do want to turn it on, then send the POST message to the API
            response = requests.post(TOGGLE_URL, headers=HEADERS, json=DATA)
            # ToDo: either remove this response variable or use it

        else:
            # ToDo: add logging and handle cases where powerstatus does not match expected values
            pass

        # wait half a second before hopping back in the loop to give the API a chance to update the state
        time.sleep(0.5)


if __name__ == "__main__":
    main()
