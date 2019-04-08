# Python Script for the implementation of the motor control project conducted at 
# EPAL Rodopolis
# Rodopoli 62055
# Serres
# http://epal-rodop.ser.sch.gr
# contact: Konstantinos Chertouras - Coach IOT Team - EPAL Rodopolis IOT team (chertour at sch.gr )
# In this script we setup the logic where the user set a desired temperature and this value is send to AWS in order
# to be availiable for the Raspberry Pi to obtain
#
#


from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import datetime
import random
import requests


# Class needed to hold the value returned from the callback function
class saveTemp:
    def __init__(self, temperature=None):
        self.temperature = temperature

    def setTemp(self, temperature):
        self.temperature = temperature
    def getTemp(self):
        return self.temperature 

#Instantiate Object
d=saveTemp()  


#Function used as a callback to retrieve sensor value
def getTemp(client, userdata, message):
    print("\nReceived Document from topic:", message.topic , "with payload: ")
    #print(message.payload)
    message=(message.payload).decode('utf-8');
    print("Parsing to get temperature...")
    payloadDict = json.loads(message)
    #print (payloadDict) 
    try:
        envTemperature = payloadDict["state"]["reported"]["temperature"]
    except:
        print ("Could not get the Enviromental temperature")
    #Save temperature to object
    d.setTemp(envTemperature)


def printStatus(client, userdata, message):
    print("\nReceived Document from topic:", message.topic , "with payload: ")
    payloadDict = json.loads(message.payload)
    try:
       envTemperature = payloadDict['current']["state"]["reported"]["temperature"]
       print("Received Sensor Temperature:",envTemperature)
    except:
        print ("Could not get the Enviromental temperature")
    



#AWS Thing Name
THING_NAME = "Raspberry"
#Topics in which i subscribe
topic_shadow_update = "$aws/things/"+THING_NAME+"/shadow/update" 
topic_shadow_update_accepted = "$aws/things/"+THING_NAME+"/shadow/update/accepted" 
topic_shadow_ask_report = "$aws/things/"+THING_NAME+"/shadow/get"
topic_shadow_report_document= "$aws/things/"+THING_NAME+"/shadow/update/documents"
topic_shadow_get_report = "$aws/things/"+THING_NAME+"/shadow/get/accepted"

#Subscription intitialization to the Shadow Service

#In here you define the AMAZON IOT Platform values
#You should study the guide availiable at:
#
#https://github.com/aws/aws-iot-device-sdk-python
#
#




myMQTTClient = AWSIoTMQTTClient("xxxxxxxxxxxxxxxxxxxxxxxxx")
myMQTTClient.configureEndpoint("xxxxxxxxxxxxxxxxxxx.iot.eu-west-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/cert_ire/xxxxxxxxxxxxxxxx.pem", "/home/pi/cert_ire/xxxxxxxxx.pem.key", "/home/pi/cert_ire/xxxxxxxxxxxxxxxxxxxx.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5) # 5 secss
myMQTTClient.connect()

#Subscription to topic to get current temperature from sensor
#Get the current reported temperature
myMQTTClient.subscribe(topic_shadow_get_report, 1, getTemp)
myMQTTClient.subscribe(topic_shadow_report_document,1,printStatus)
myMQTTClient.publish(topic_shadow_ask_report, "" ,0)

time.sleep(3)
#Report temperature again
print('--------------------------------------')
print('Reported Temperature is: ', d.getTemp())
print('--------------------------------------')
#Ask for a temperature to achive
temperature=float(input("Please enter a desired temperature:"))
print("Trying to sent to AWS the desired shadow value...")
#Pack to JSON to sent to Shadow broker
json_update =json.dumps( {"state": {"desired" :{"temperature":temperature}}})
#Publish 
if (myMQTTClient.publish(topic_shadow_update, json_update, 0)==True):
    print ("Connected to AWS Succesfully...")   
    print ("Waiting to adjust...")
else:
    print ("Could not reach AWS...")
    print ("Check Internet Connection...")
    print ("Will now exit...")
    exit


#Main Loop
while True:
    time.sleep(5)
