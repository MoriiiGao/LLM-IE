import time
import logging
import os
import socket
import configparser

 

def getWorkSpace() :
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # print(current_directory)
    # root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
    return current_directory
 

config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")