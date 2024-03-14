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
    lastpartial_raw = get_last_partial()[0].replace("T"," ").replace("Z","")
    lastpartial = (datetime.strptime(lastpartial_raw, '%Y-%m-%d %H:%M:%S.%f')) + timedelta(hours=1)
    currenttime = datetime.now()
    elapsed = currenttime - lastpartial
    pingstatus = check_pool_ping()

    logging.info("")
    logging.info("--------------------------------------------------")
    logging.info("Checking partial data from Spacefarmers.io")
    logging.info("-> " + pingstatus)
    logging.info("--------------------------------------------------")
    logging.info("")

    #checking if partials are sent, restarting gigahorse if not
    if elapsed > timedelta(minutes=60) and pingstatus == "Network Active":
        logging.info("-> Farm anomaly detected!")
        logging.info("-> Last partial was sent " + str(elapsed) + " ago! Restarting farmer!")
        os.popen("docker restart machinaris-gigahorse")

        #setup Discord webhook notifications, comment out if not used
        webhook = DiscordWebhook(url="<WEBHOOK URL HERE>", content="Farm has been restarted due to lack of partials! There could have been an issue. Please check your farmer.")
        response = webhook.execute()

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
    url = "https://v2.spacefarmers.io/api/farmers/<YOURIDHERE>/partials"

    headers = {
        "accept": "application/json",
        "User-Agent": "submissionDateTimeUtc"
    }
    #response = requests.get(url, headers=headers)
    response = requests.get(url, headers=headers)
    #cleaning up output a bit
    data = response.json()
    results = data['data'][0]
    #logging.info(str(results))
    array = []
    list = []
    for result in results.values():
        array.append(result)
        #logging.info("--> " + str(result))

    #temp.append(array[2])
    for vals in array[2].values():
        list.append(vals)

    temp.append(list[0])
    
    logging.info("xxxx-> " + str(list[0]))
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
