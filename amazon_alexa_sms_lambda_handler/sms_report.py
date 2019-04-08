# Python Script for the implementation of the SMS Send through the Alexa Service and the Lambda Function Platform at AWS
# EPAL Rodopolis
# Rodopoli 62055
# Serres
# http://epal-rodop.ser.sch.gr
# contact: Konstantinos Chertouras - Coach IOT Team - EPAL Rodopolis IOT team (chertour at sch.gr )
# In this script we setup the logic where the user through a voice command initiates the sending of an SMS 
# with the current temperature logged from Raspberry Pi
# WARNING: 
# THIS SCRIPT RUNS ONLY WITHIN THE LAMBDA AWS ENVIROMENT - IT DOES NOT RUN IN A STANDALONE ENVIRONMENT
# iNSPIRED BY: 
#
# 1. https://medium.com/@arthurltonelli/building-an-iot-device-with-alexa-aws-python-and-raspberry-pi-274d941ef3c3 (Arthur Tonelli) 
# 2. https://github.com/alexa/skill-sample-python-fact (AWS tutorial)
# 3. https://github.com/aws/aws-iot-device-sdk-python/ (ΑWS tutorial)




import json
import os
from botocore.vendored import requests
import datetime
import boto3

session_attributes = {}
should_end_session = True
reprompt_text = None
alexa_id = os.environ.get('AWS_ALEXA_SKILLS_KIT_ID')


def build_response(session_attributes, speechlet_response):
    """
    Builds a Python dict of version, session, and speechlet reponse. This is
    the core dict (response message) to be returned by the lamabda function.

    Args:
        session_attributes: Python dict of session
        speechlet_response: Python dict of speechlet response
    Returns:
        Python dict of response message
    """
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    """
    Builds a Python dict of a speechlet response for the response message
    dict. Output speech will be read by Alexa. The card dict will be displayed
    if the Alexa device has a screen and can display cards. The reprompt
    message will be read if session remains open and there is no clear
    intent from the user. Should end session will close the session or
    allow it to remain open.

    Args:
        title: string of card title
        output: string of output text
        reprompt_text: string of reprompt text
        should_end_session: boolean to end session
    Returns:
        Python dict of response speechlet
    """
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def handle_session_end_request():
    """
    Builds a response with a blank message and no session data. If using
    session data this function would specifically have session_attributes = {}
    and should_end_session = True.

    Args:
        None
    Returns:
        Python dict of response message
    """
    
    speech_output = None
    response =build_response(session_attributes,
        build_speechlet_response(0,
        speech_output, reprompt_text, should_end_session))
    return response

def sms_intent(intent):
    """
    Updates power state of IoT shadow. Builds a response confirming the update
    or requesting the user repeat the query if state is not "ON" or "OFF".

    Args:
        intent: Python dict of intent
    Returns:
        Python dict of response message
    """
    card_title = "SMS"

    sms_state = intent.get('slots',{}).get('SMSState',{}).get('value')
    if sms_state and (sms_state.upper() == 'ON' ):
        shadow_client = boto3.client('iot-data', 'eu-west-1')
        response = shadow_client.get_thing_shadow(thingName='Raspberry')
        streamingBody = response["payload"]
        rawDataBytes = streamingBody.read()
        rawDataString = rawDataBytes.decode('utf-8')
        jsonState = json.loads(rawDataString)
        temperature=jsonState["state"]["reported"]["temperature"]
        now = datetime.datetime.now()
        temptime=now.strftime("%Y-%m-%d %H:%M")
        #jsonState = json.loads(streamingBody.read() jsonState["state"]["reported"]["temperature"])
        textToSend = 'Temperature is ' + str(temperature) +' at ' + str(temptime)
        
        payload = { 
                'key':'xxxxxxxxxxx',	
                'text':textToSend,
                'to':'xxxxxxxxxxxxx',
                'type':'json',
                'from' :'AWS'}
        r = requests.post('https://easysms.gr/api/sms/send', payload)
        speech_output = "OK I will send an sms"
    else:
        speech_output = "I did not understand that. Please repeat your request."
    
    response = build_response(session_attributes,
        build_speechlet_response(card_title,
        speech_output, reprompt_text, should_end_session))
    return response





    
def on_intent(intent_request, session):
    """
    Called when the user specifies an intent for this skill. Calls a behavior
    method based on the intent type.

    Args:
        intent_request: Python dict of request
        session: Python dict of session
    Returns:
        Python dict of response message
    """
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent['name']

    if intent_name == "SMSIntent":
        return sms_intent(intent)
    else: 
        return handle_session_end_request()    

def lambda_handler(event, context):
    # TODO implement
    
    request_type = event['request']['type']

    if request_type == "IntentRequest":
       return on_intent(event['request'], event['session'])

