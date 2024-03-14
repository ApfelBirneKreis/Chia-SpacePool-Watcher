import requests
import logging
from datetime import datetime
from datetime import timedelta
from time import sleep
import subprocess
import os
import os.path
from discord_webhook import DiscordWebhook


#PLEASE CONFIGURE THE SCRIPT TO YOUR POOL!!!

#-----------------------------------------------------------------------------------------------------------------
#Configuration:
#-Pool API:
url = "<your api url here>"
headers = {
    "accept": "application/json",
    "Developer-Key": "<your dev key here",  #comment out when using Spacefarmers
    "User-Agent": "Farmer_Check"
}
#-Discord Webhook:
use_discord_notifications = True
webhook = DiscordWebhook(url="<your webhook url here>", content="Farm has been restarted due to lack of partials! There could have been an issue. Please check your farmer.")

#-Restarting Command:
restart_farmer = os.popen("docker restart machinaris-gigahorse")

#-Pool: (only set your used Pool to true! Only one true is allowed!)

SpacePool = True
Spacefarmers = False
#----------------------------------------------------------------------------------------------------------------------




#ACTUAL SCRIPT! DONT CHANGE ANYTHING HERE!

#-----------------------------------------------------------------------------------------------------------------------

#setup logging
def loggingSetup():
    """set up logging to sys.stderr
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

#main Script
def main():
    loggingSetup()

    #setup readable datetime format:

    if (SpacePool == True and Spacefarmers == True) or (SpacePool == False and Spacefarmers == False):
        logging.info("MALFORMED CONFIGURATION! Check your Script configuration!")


    if SpacePool == True:
        lastpartial_raw = get_last_partial()[0].replace("T"," ").replace("0Z","")
    if Spacefarmers == True:
        lastpartial_raw = get_last_partial()[0].replace("T"," ").replace("Z","")


    lastpartial = (datetime.strptime(lastpartial_raw, '%Y-%m-%d %H:%M:%S.%f')) + timedelta(hours=1)
    currenttime = datetime.now()
    elapsed = currenttime - lastpartial
    pingstatus = check_pool_ping()

    logging.info("")
    logging.info("--------------------------------------------------")
    logging.info("Checking partial data from your Pool:")
    logging.info("-> Network functioning properly? -> " + str(pingstatus))
    logging.info("--------------------------------------------------")
    logging.info("")

    #checking if partials are sent, restarting gigahorse if not
    if elapsed > timedelta(minutes=60) and pingstatus == True:
        logging.info("-> Farm anomaly detected!")
        logging.info("-> Last partial was sent " + str(elapsed) + " ago! Restarting farmer!")
        restart_farmer
        if use_discord_notifications == True:
            response = webhook.execute()

    if pingstatus == False:
        logging.info("-> Network offline. Not restarting any Farmer!")
    else:
        logging.info("-> Farm operating normally")
        logging.info("-> Elapsed time since last partial: " + str(elapsed))


    logging.info("")
    logging.info("--------------------------------------------------")


#calling SpacePool api for partial data. Cleaning up output	
def get_last_partial():
    temp = []
    
    if SpacePool == True:
        response = requests.get(url, headers=headers)

        #cleaning up output a bit
        data = response.json()
        results = data['results'][0]
        array = []
        for result in results.values():
            array.append(result)

        temp.append(array[4])

    if Spacefarmers == True:
        response = requests.get(url, headers=headers)

        data = response.json()
        results = data['data'][0]
        array = []
        list = []
        for result in results.values():
            array.append(result)
        for vals in array[2].values():
            list.append(vals)

        temp.append(list[0])

    return temp

def check_pool_ping():

    with open(os.devnull, 'w') as DEVNULL:
        try:
            subprocess.check_call(
                ['ping', '-c', '3', 'google.com'],
                stdout=DEVNULL,  # suppress output
                stderr=DEVNULL
            )
            is_up = True
        except subprocess.CalledProcessError:
            is_up = False
    return is_up

if __name__ == "__main__":
    main()
