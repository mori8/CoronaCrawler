#-*- coding:utf-8 -*-

import requests
import os
import json
import time
import datetime
import CCCounter

logFilePath = os.path.dirname(os.path.abspath(__file__)) + "/lastdata.txt"
slackUrlFilePath = os.path.dirname(os.path.abspath(__file__)) + "/slack.txt"
def needPush(newItem):
    lastItem = 0

    try:
        with open(logFilePath, "r") as f:
            lastItem = json.load(f)
    except:
        pass
    print("last : ", lastItem, ", new : ", newItem)
    if type(lastItem) != type(newItem):
        return True
        
    if lastItem["confirmed"] != newItem["confirmed"] or lastItem["recovered"] != newItem["recovered"] or lastItem["dead"] != newItem["dead"]:
        return True
    
    return False

def saveData(newItem):
    with open(logFilePath, "w") as f:
        jsonData = json.dumps(newItem)
        f.write(jsonData)
    
def pushSlack(newItem):
    pushUrl = ""
    try:
        with open(slackUrlFilePath, "r") as f:
            pushUrl = f.readline()
            if pushUrl[len(pushUrl) - 1] == '\n':
                pushUrl = pushUrl[:len(pushUrl) - 1]
    except:
        print("Failed to get webhook url.")
        return
    headers = {'Content-type': 'application/json; charset=utf-8'}
    sendString = "국내 확진자 : {}, 국내 완치자 : {}, 국내 사망자 : {}".format(newItem["confirmed"], newItem["recovered"], newItem["dead"])
    data = {"text": sendString}
    
    try:
        print(data)
        result = requests.post(pushUrl, headers=headers, data=json.dumps(data))
        if result.status_code == 200:
            saveData(newItem)
        else:
            print("Failed to send data. response code : " + str(result.status_code))
    except:
        print("Failed to send message.")

if __name__ == '__main__':
    sleepInterval = 60 * 30
    while True:
        print(datetime.datetime.now())
        newItem = CCCounter.main()

        if needPush(newItem):
            pushSlack(newItem)
            
        time.sleep(sleepInterval)