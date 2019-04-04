import sys
import Adafruit_DHT
import requests
import time

while True:
    #Important 
    #Main function which reads the values of DHT11 senson connected to pin 4 
    #In xxxxxxxx at paylod you should put your api thingspeak key
   
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    #
    #
    #
    print ('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
    payload = {'api_key': 'xxxxxxxxxx' , 'field1': temperature, 'field2':humidity}
    r = requests.post('https://api.thingspeak.com/update', params=payload)
    print("Server Responded : ", r.text)
    print (temperature)

    time.sleep(1)
