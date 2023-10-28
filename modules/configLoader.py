#================================
import configparser
#CONFIGURATION
config=configparser.ConfigParser()
config.read("../Config/gameConfig.ini")
firstTime=config.getint("GAME_CONFIG","firstTime")
width=config.getint("GAME_CONFIG", "screenWidth")
height=config.getint("GAME_CONFIG", "screenHeight")
fullscreen=config.getint("GAME_CONFIG","fullscreen")
language=config.get("GAME_CONFIG","language")
maxFPS=config.getint("GAME_CONFIG","maxFPS")