2. Installation of ffmpeg: \
a. Ubuntu: `apt install -y ffmpeg`. \
b. Windows: A full documentation of how to is [here](https://www.wikihow.com/Install-FFmpeg-on-Windows).
> Also I had shown this on my [video](https://www.youtube.com/watch?v=MMRtEvGpzdk)

---

3. `git clone https://github.com/DreamCatcher96/FileStreamBot-DX.git`, to clone and the repository.
4. `cd FileStreamBot-DX/`, to enter the directory.
5. `pip3 install -r requirements.txt`, to install python libraries/dependencies/requirements for the project.

----
6. Create a new `config.ini` using the sample available at `mega/working_dir/config.ini.sample` at `mega/working_dir/`.
```
# Here is a sample of config file and what it should include:
[pyrogram]
# More info on API_ID and API_HASH can be found here: https://docs.pyrogram.org/intro/setup#api-keys
api_id = 
api_hash = 

[plugins]
root = mega/telegram/plugins

[bot-configuration]
# More info on Bot API Key/token can be found here: https://core.telegram.org/bots#6-botfather
api_key = 
session = megadlbot
# Watch this video to understand what the dustbin is: https://www.youtube.com/watch?v=vgzMacnI5Z8
dustbin = 
allowed_users = [123123123, 321321321]
# a list of user ids who are allowed to use this bot

[database]
# In this section db_host is the address of the machine where the MongoDB is running, if you are running 
# both the bot and Mongo on same machine leave it as local host.
# db_username and db_password are the username and password we assigned roleas with at the first step 
# while we installed Database
db_host = localhost

# for the following section fill in the FQDN with which end users can reach the host machine, bindaddress is the address of the adapter to bind with while running webserver and the port for the webserver to listen.
[web_server]
bind_address = 0.0.0.0
fqdn = localhost
port = 8080
```

---

7.  Run with `python3.9 -m mega`, stop with <kbd>CTRL</kbd>+<kbd>C</kbd>.
> It is recommended to use [virtual environments](https://docs.python-guide.org/dev/virtualenvs/) while running the app, this is a good practice you can use at any of your python projects as virtualenv creates an isolated Python environment which is specific to your project.


### Deploying on Heroku:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Before clicking the Deploy button make sure you have the following details with you too:
1. Create a free account on cloud.mongodb.com (This is for the DB and you need its details for the config file as explained above, also keep a note that if you host mongoDB community edition on your own its totally free otherwise you might have limitations).
2. Create a Telegram channel (This one for the dustbin. As mentioned above watch this [video](https://www.youtube.com/watch?v=vgzMacnI5Z8) to understand what the dustbin is.) 
3. Well as obvious as it can be create a bot with @BotFather, also get your API ID and API Hash from my.telegram.org.  



### Deploying on Heroku:

  [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/dxbotz/File-To-Link-PM)

