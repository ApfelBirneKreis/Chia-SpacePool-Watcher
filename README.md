POOLS SUPPORTED: SpacePool, Spacefarmers.io

This Script uses the Spacepool or Spacefarmer api to check for your latest partial you sent to the pool.
If the partial is older than a set ammount of minutes it autorestarts your farm.

- ![image](https://github.com/ApfelBirneKreis/Chia-SpacePool-Watcher/assets/84158946/cd3c18f3-0c55-4dcf-8a6e-2225595b2368)

Currently it only works with the machinaris container on unraid but can be adapted to work with almost everything

On unraid you need two modules + python itself and the user.scripts plugin installed:

To install the modules use:
- pip install requests
- pip install discord-webhook

To call the script use the userscript plugin on Unraid. mine runs every 10mins with a Cronjob.

Also a weebhook can be configured to send a notification if your farm gets restarted.
