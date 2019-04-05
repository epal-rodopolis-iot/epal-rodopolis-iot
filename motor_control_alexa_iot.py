from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import paho.mqtt.publish as publish
import logging
import time
import argparse
import json
import datetime
import random
import requests
import Adafruit_DHT
import sys
#mathworks related

import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.output(18,GPIO.LOW)





#  ThingSpeak Channel Settings

# The ThingSpeak Channel ID - Set yours here

channelID = "xxxxxxxxxxxx"


# The Write API Key for the channel

apiKey = "xxxxxxxxxxxxxxxxxx"

useUnsecuredTCP = True
tTransport = "tcp"
tPort = 1883
tTLS = None
#
#
#


topic = "channels/" + channelID + "/publish/" + apiKey


#AWS Thing Name
THING_NAME_1 = "Raspberry"
THING_NAME_2 = "Raspberry_LED"



#Main function which open or closes the motor when inspects a difference lower or euqal to 1 Celcius

def adjustLed(client, userdata, message):
    print("\n\nReceived a Delta message from:", message.topic)
    message=(message.payload).decode('utf-8')
    payloadDict = json.loads(message)
    power_state = payloadDict["state"]["power_state"] 
    #Print the desired LED state
    print ("Desired LED STATUS is :" ,power_state )
    

    if (power_state == 'ON' ):
        GPIO.output(18,GPIO.HIGH)
    else:
        GPIO.output(18,GPIO.LOW)
    led_container={"state":{"reported":{"power_state":  power_state  }, "desired": None}}
    json_data_reported = json.dumps(led_container) 
    myMQTTClient.publish(led_topic_shadow_update, json_data_reported, 0)
    
        



def adjustTemp(client, userdata, message):
    
    print("\n\nReceived a Delta message from:", message.topic)
    
    #Publish the new temperature
    topic_shadow_update = "$aws/things/"+THING_NAME_1+"/shadow/update" 
    
    #Parse the message to extract the setted temperature
    message=(message.payload).decode('utf')
    payloadDict = json.loads(message)
    temperature_setted = payloadDict["state"]["temperature"] 
    #Print the desired temperature
    print ("Desired Temperature is :" ,temperature_setted )
       
    #Get the current ambient temperature
    sensor_temp=d.getTemp ()
    
    # Compare two temperatures (ambient and  setted )
    # if there is a difference of one degree Celcius between them then close the motor
    
    if (float(abs(sensor_temp  - (temperature_setted))) <=1.0 ):
        print("Motor stopping - Temperature Reached...")
        GPIO.output(18,GPIO.LOW)
        #Setting temperature equal to setted to avoid constant motor on/off and delta
        container={"state":{"reported":{"temperature":  temperature_setted  }}}
        #Ubdating the state by publish to topic
        json_data_reported = json.dumps(container) 
        myMQTTClient.publish(topic_shadow_update, json_data_reported, 0)
    else:
         # Open the motor to chil...
         print("Motor is running to compensate difference...")
         GPIO.output(18,GPIO.HIGH)
      
   
# Print the "$aws/things/"+THING_NAME_1+"/shadow/update/documents" document topic
def documentAccepted(client, userdata, message):
    payloadDict = json.loads((message.payload).decode('utf-8'))
    try:
        e.setTemp(payloadDict["current"]["state"]["desired"]["temperature"])
    except:
        e.setTemp(e.getTemp())
    print("Received a new message from:" , message.topic ,
          "- Reported Temperature is: " ,payloadDict["current"]["state"]["reported"]["temperature"])  
  



def documentAcceptedLed(client, userdata, message):
    payloadDict = json.loads((message.payload).decode('utf-8'))
    try:
        f.setPowerState(payloadDict["current"]["state"]["reported"]["power_state"])
    except:
        f.setPowerState(f.getPowerState())
    
    print("Reported led state is: " , f.getPowerState())





# Class needed to hold the value returned from the callback function ,
# "Reported Led power state : " ,payloadDict["current"]["state"]["reported"]["power_state"]
class saveTemp:
    def __init__(self, temperature=None):
        self.temperature = temperature
    def setTemp(self, temperature):
        self.temperature = temperature
    def getTemp(self):
        return self.temperature 

class settedTemp:
    def __init__(self, temperature=None):
        self.temperature = temperature
    def setTemp(self, temperature):
        self.temperature = temperature
    def getTemp(self):
        return self.temperature 

class settedPowerState:
    def __init__(self, powerState="OFF"):
        self.powerState = powerState
    def setPowerState(self, powerState):
        self.powerState = powerState
    def getPowerState(self):
        return self.powerState 
#Instantiate Object
d=saveTemp()    
e=settedTemp()
f=settedPowerState()



#Topics in which i subscribe
topic_shadow_update = "$aws/things/"+THING_NAME_1+"/shadow/update" 
topic_shadow_update_delta = "$aws/things/"+THING_NAME_1+"/shadow/update/delta" 
topic_shadow_update_accepted = "$aws/things/"+THING_NAME_1+"/shadow/update/accepted" 
topic_shadow_ask_report = "$aws/things/"+THING_NAME_1+"/shadow/get"
topic_shadow_report_document= "$aws/things/"+THING_NAME_1+"/shadow/update/documents"
topic_shadow_get_report = "$aws/things/"+THING_NAME_1+"/shadow/get/accepted"
topic_shadow_delete = "$aws/things/"+THING_NAME_1+"/shadow/delete"

#Led shadow documents
led_topic_shadow_update = "$aws/things/"+THING_NAME_2+"/shadow/update" 
led_topic_shadow_update_delta = "$aws/things/"+THING_NAME_2+"/shadow/update/delta" 
led_topic_shadow_update_accepted = "$aws/things/"+THING_NAME_2+"/shadow/update/accepted" 
led_topic_shadow_ask_report = "$aws/things/"+THING_NAME_2+"/shadow/get"
led_topic_shadow_report_document= "$aws/things/"+THING_NAME_2+"/shadow/update/documents"
led_topic_shadow_get_report = "$aws/things/"+THING_NAME_2+"/shadow/get/accepted"
led_topic_shadow_delete = "$aws/things/"+THING_NAME_2+"/shadow/delete"


#Subscription intitialization to the Shadow Service

#In here you define the AMAZON IOT Platform values
#You should study the guide availiable at:
#
#https://github.com/aws/aws-iot-device-sdk-python
#
#


myMQTTClient = AWSIoTMQTTClient("xxxxxxxxxxxxxxx")
myMQTTClient.configureEndpoint("xxxxxxxxxxxxxxxxxxxxxxxxxxxx.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/cert_ire/xxxxxxx", "/home/pi/cert_ire/xxxxxxxxxxx", "/home/pi/cert_ire/xxxxxxxxxxx")



myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5) # 5 secss
myMQTTClient.connect()


#Subscription to topic to get the delta topic having the difference desired - reported from sensor
#Get the current reported temperature
myMQTTClient.subscribe(topic_shadow_update_delta, 1, adjustTemp)
myMQTTClient.subscribe(led_topic_shadow_update_delta, 1, adjustLed)

myMQTTClient.subscribe(led_topic_shadow_report_document, 1, documentAcceptedLed)
myMQTTClient.subscribe(topic_shadow_report_document, 1, documentAccepted)


#Get temperature


humidity, temperature = Adafruit_DHT.read_retry(11, 4)
temp=temperature

#Set initial led status
led_container={"state":{"reported":{"power_state": "OFF" }}}
led_json_data_reported = json.dumps(led_container)
myMQTTClient.publish(led_topic_shadow_update, led_json_data_reported, 0)

print('Initial delay to receive any messages...')
time.sleep(2)


choice = True
#Ask to Clear the IOT cached set temperature
while choice:
    yes_no = input ('Do you want to clear the Shadow Document State Y/N:')

    if (yes_no=='Y' or yes_no=='y'):
        myMQTTClient.publish(topic_shadow_delete, "", 0)
        myMQTTClient.publish(led_topic_shadow_delete, "", 0)
        choice=False
    elif (yes_no=='N'):
        print ('Leaving Shadow Unchanged')
        choice=False
    else :
        print ("You Pressed an invalid key. Please press Y or N ")


#Main While Loop in which:
#
# We construct the update shadow document containing the reported state 
# We forward values to Thingspeak to create the enviromental variables
#

##Initialize states
e.setTemp(0)

# The Hostname of the ThinSpeak MQTT service
mqttHost = "mqtt.thingspeak.com"
#Main While Loop
while True:
   
      
      humidity, sensor_temperature = Adafruit_DHT.read_retry(11, 4)
      #temp=temperature
      #Set the Sensor Temperature - SIMULATION MODE
      #sensor_temperature= temp 
      #Get the Led Status - SIMULATION MODE
      power_state = f.getPowerState() 
      ######################################################
      tPayload = "field2=" + str(sensor_temperature) 
      try:
        publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)

      except (KeyboardInterrupt):
        break

      except:
        print ("There was an error while publishing the data.")
     


     ########################################################
      
      #Create the JSON Payload to update the shadow document
      container={"state":{"reported":{"temperature":  sensor_temperature }}}
      json_data_reported = json.dumps(container)
      #Save the enviromental temperature to Global Variable via Class 
      d.setTemp(sensor_temperature)
      #Publish to topics
      #myMQTTClient.publish("MyFirstThingTopic", json_data_reported, 0)
      
      desired_temp=float(e.getTemp())
      tempDiff=float(abs(sensor_temperature  - desired_temp))
      if ( tempDiff >= 1.0 ):
          myMQTTClient.publish(topic_shadow_update, json_data_reported, 0)
      print("Temp diff:" , tempDiff)


      

      time.sleep(5)
      
