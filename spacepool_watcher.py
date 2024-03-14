import requests
import logging
from datetime import datetime
from datetime import timedelta
from time import sleep
import os
import os.path
from discord_webhook import DiscordWebhook




#setup logging
def loggingSetup():
    """set up logging to sys.stderr
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

#main Script
def main():
    loggingSetup()



    #setup readable datetime format
    lastpartial_raw = get_last_partial()[0].replace("T"," ").replace("0Z","")
    lastpartial = (datetime.strptime(lastpartial_raw, '%Y-%m-%d %H:%M:%S.%f')) + timedelta(hours=1)
    currenttime = datetime.now()
    elapsed = currenttime - lastpartial
    pingstatus = check_pool_ping()

    logging.info("")
    logging.info("--------------------------------------------------")
    logging.info("Checking partial data from SpacePool")
    logging.info("-> " + pingstatus)
    logging.info("--------------------------------------------------")
    logging.info("")

    #checking if partials are sent, restarting gigahorse if not
    if elapsed > timedelta(minutes=60) and pingstatus == "Network Active":
        logging.info("-> Farm anomaly detected!")
        logging.info("-> Last partial was sent " + str(elapsed) + " ago! Restarting farmer!")
        os.popen("docker restart machinaris-gigahorse")
        #setup Discord webhook notifications
        #webhook = DiscordWebhook(url="https://discord.com/api/webhooks/############################################################", content="Farm has been restarted due to lack of partials! There could have been an issue. Please check your farmer.")
        #response = webhook.execute()
    if pingstatus == "Network Error":
        logging.info("-> Network offline. Not restarting any Farmer!")
    else:
        logging.info("-> Farm operating normally")
        logging.info("-> Elapsed time since last partial: " + str(elapsed))


    logging.info("")
    logging.info("--------------------------------------------------")


#calling SpacePool api for partial data. Cleaning up output	
def get_last_partial():
    temp = []

    #calling api
    url = "https://developer.pool.space/api/v1/farms/#############################################/partials"

    headers = {
        "accept": "application/json",
        "Developer-Key": "########################################################",
        "User-Agent": "#################################################"
    }
    response = requests.get(url, headers=headers)

    #cleaning up output a bit
    data = response.json()
    results = data['results'][0]
    array = []
    for result in results.values():
        array.append(result)

    temp.append(array[4])
    return temp

def check_pool_ping():

    with open(os.devnull, 'w') as DEVNULL:
        try:
            subprocess.check_call(
                ['ping', '-c', '3', 'developer.pool.space'],
                stdout=DEVNULL,  # suppress output
                stderr=DEVNULL
            )
            is_up = True
        except subprocess.CalledProcessError:
            is_up = False
    return is_up

if __name__ == "__main__":
    main()
