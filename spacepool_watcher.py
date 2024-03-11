import requests
import logging
from datetime import datetime
from datetime import timedelta
from time import sleep
import os
import os.path


def loggingSetup():
    """set up logging to sys.stderr
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')


def main():
    loggingSetup()
    lastpartial_raw = get_last_partial()[0].replace("T"," ").replace("0Z","")

    #2024-03-11T15:04:07.0000000Z
    lastpartial = (datetime.strptime(lastpartial_raw, '%Y-%m-%d %H:%M:%S.%f')) + timedelta(hours=1)
    currenttime = datetime.now()

    #logging.info("Last Partial was received at: " + str(lastpartial))
    #logging.info("Current Time: " + str(currenttime))

    elapsed = currenttime - lastpartial
    logging.info("--------------------------------------------------")
    logging.info("Checking partial data from SpacePool")
    logging.info("--------------------------------------------------")
    logging.info("")

    if elapsed > timedelta(minutes=120):
        logging.info("-> Farm anomaly detected!")
        logging.info("-> Last partial was sent " + str(elapsed) + " ago! Restarting farmer!")
        os.popen("docker restart machinaris-gigahorse")
    else:
        logging.info("-> Farm operating normally")
        logging.info("-> Elapsed time until last partial: " + str(elapsed))

    logging.info("")
    logging.info("--------------------------------------------------")


	
def get_last_partial():
    temp = []
    url = "https://developer.pool.space/api/v1/farms/<your_launcher_id_here>/partials"

    headers = {
        "accept": "application/json",
        "Developer-Key": "<your_developer_key_here>",
        "User-Agent": "<your_user_agent_here>"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    results_debug = data['results']
    #logging.info(str(results_debug))
    results = data['results'][0]
    array = []
    list =[]
    for result in results.values():
        array.append(result)

    temp.append(array[4])
    return temp

if __name__ == "__main__":
    main()