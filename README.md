This Script uses the Spacepool api to check for your latest partial you sent to the pool.
If the partial is older than a set ammount of minutes it autorestarts your farm.
![image](https://github.com/ApfelBirneKreis/Chia-SpacePool-Watcher/assets/84158946/cd3c18f3-0c55-4dcf-8a6e-2225595b2368)

Currently it only works with the machinaris container on unraid but can be adapted to work with almost everything

On unraid you need two modules + python itself installed:

To install the modules use:
pip install requests
pip install discord-webhook


Also a weebhook can be configured to send a notification if your farm gets restarted.
