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

from logger.logger import myLogger, sys
import time
from logger.logger import printer as print
sys.stdout = myLogger(name = __file__.split(".")[0]+".log")

import createHTML

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
        


def getAllDataInLoop(url: list = url, refresh : int = 60):
    """
    """
    while True:
        allTempList, allHumList, allSwitchList = getAllData(url)
        getData(allTempList)
        getData(allHumList)
        getData(allSwitchList) 
        # print("\n")
        time.sleep(refresh)



def getData(dataList):
        for e in dataList:
            print(e)




# allTempList, allhumList, allswitchList = getAllData(url)

# createHTML.getData(allTempList)

getAllDataInLoop(refresh=0)