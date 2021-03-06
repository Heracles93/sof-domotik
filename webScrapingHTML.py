"""
https://www.datacamp.com/community/tutorials/web-scraping-using-python
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = ("http://192.168.1.40", "http://192.168.1.34", "http://192.168.1.48")
url = ("http://192.168.1.34", "http://192.168.1.48")

from logger.logger import myLogger, sys
import time
from logger.logger import printer as print
sys.stdout = myLogger(name = "log/"+__file__.split(".")[0]+".log")

# import createHTML

def connectHTML(url: str):
    """
    """
    html = urlopen(url)
    # convert to soup elegant format
    soup = BeautifulSoup(html, 'lxml')
    all_links = soup.find_all("p")
    linklst = []
    for i in range(0, len(all_links)):
        link = str(all_links[i]).replace("<p>", "")
        link = link.replace("</p>", "")
        linklst.append(link)
    return linklst

def getTempretature(url: str, nbr : int = 0):
    """
    """
    templst = []
    txt = connectHTML(url)
    for e in txt:
        if e.find("Température")!=-1:
            value = e.split(" ")[-2]
            value = value.replace('style="color:#FF0000">', "")
            value = value.replace("</span>", "")
            templst.append(value)
    return templst[nbr-1]

def getHumidity(url: str, nbr : int = 0):
    """
    """
    humLst = []
    txt = connectHTML(url)
    for e in txt:
        if e.find("Humidité")!=-1:
            humLst.append(e.split(" ")[-3])
    return humLst[nbr-1]

def getSwitchState(url: str, nbr : int = 0):
    """
    """
    switchStateLst = []
    txt = connectHTML(url)
    for e in txt:
        if e.find("button")!=-1:
            if e.find("ON")!=-1:
                switchStateLst.append(True)
            else: 
                switchStateLst.append(False)
    return switchStateLst[nbr-1]




def getAllData(url: list):
    """
    """
    allTempList = []
    allswitchList = []
    allhumList = []
    for webserver in url:
        templistName = webserver+"_Temp"
        tempList = []
        switchListName = webserver+"_Switch"
        switchList = []
        humListName = webserver+"_Hum"
        humList = []
        for i in range (0,2):
            try:
                tempList.append(getTempretature(webserver, i))
                time.sleep(1)
                humList.append(getHumidity(webserver, i))
                time.sleep(1)
                switchList.append(getSwitchState(webserver, i))
                time.sleep(1)
            except:
                sys.stdout.write("URLError : "+webserver+" No route to host !\n", msgLevel="error")
        allTempList.append((templistName, tempList[::-1]))
        allhumList.append((humListName, humList[::-1]))
        allswitchList.append((switchListName, switchList[::-1]))
    return allTempList, allhumList, allswitchList
        
# def getData(dataList):
#         for e in dataList:
#             print(e)

def DHTreplace(content, old, new):
    if new != "2147483647":
        content = content.replace(old, new)
    else:
        content = content.replace(old, "971")
    return content


# -----------------------------
def getAllDataInLoop(url: list = url, refresh : int = 60):
    """
    """
    fileToOpen = "index1.html"

    while True:
        allTempList, allHumList, allSwitchList = getAllData(url)
        # getData(allTempList)
        # getData(allHumList)
        # getData(allSwitchList) 
        # print("\n")
        # print(allTempList)
        # print(allHumList)
        # print(allSwitchList)


        with open(fileToOpen) as fl:
            SWITCHSTATELEDCACHETTE = str(allSwitchList[1][1][0])
            DHT11TEMPCACHETTEHUMIDE = str(allTempList[1][1][0])
            DHT11HUMCACHETTEHUMIDE = str(allHumList[1][1][0])
            DHT11TEMPCACHETTECHAUDE = str(allTempList[1][1][1])
            DHT11HUMCACHETTECHAUDE = str(allHumList[1][1][1])
            DHT11TEMPSALON = str(allTempList[0][1][0])
            DHT11HUMSALON = str(allHumList[0][1][0])
            content = fl.read()
            content = content.replace("TIMESOF-DOMOTIK", time.ctime())
            content = content.replace("SWITCHSTATELEDCACHETTE", SWITCHSTATELEDCACHETTE)
            content = DHTreplace(content, "DHT11TEMPCACHETTEHUMIDE", DHT11TEMPCACHETTEHUMIDE)
            content = DHTreplace(content, "DHT11HUMCACHETTEHUMIDE", DHT11HUMCACHETTEHUMIDE)
            content = DHTreplace(content, "DHT11TEMPCACHETTECHAUDE", DHT11TEMPCACHETTECHAUDE)
            content = DHTreplace(content, "DHT11HUMCACHETTECHAUDE", DHT11HUMCACHETTECHAUDE)
            content = DHTreplace(content, "DHT11TEMPSALON", DHT11TEMPSALON)
            content = DHTreplace(content, "DHT11HUMSALON", DHT11HUMSALON)
            # print(content)

        html = open("index.html", mode="w")
        html.write(content)


        print("Content updated")
        time.sleep(refresh)








# allTempList, allhumList, allswitchList = getAllData(url)

# createHTML.getData(allTempList)
if __name__ == "__main__":
    getAllDataInLoop(refresh=1)
    