import os
import json
import requests
import ibmiotf.device
from os.path import join, dirname
from dotenv import load_dotenv
from watson_developer_cloud import SpeechToTextV1 as SpeechToText

from speech_sentiment_python.recorder import Recorder

def transcribe_audio(path_to_audio_file):
    #username = os.environ.get("BLUEMIX_USERNAME")
    #password = os.environ.get("BLUEMIX_PASSWORD")
    #speech_to_text = SpeechToText(username=username,password=password)

    #with open(join(dirname(__file__), path_to_audio_file), 'rb') as audio_file:
    #    return speech_to_text.recognize(audio_file,content_type='audio/wav')

    sfile= open('speech.wav', "rb")

    response = requests.post("https://stream.watsonplatform.net/speech-to-text/api/v1/recognize?model=pt-BR_BroadbandModel",
    	auth=("<S2T username>", "<S2T password>"),
        headers = {"content-type": "audio/wav"},
        data=sfile)

    #print json.loads(response.text)
    return response.text

def watson_iot(txt1):
    try:
        options = {
            "org": "<IOT Org>",
            "type": "<IOT Type>",
            "id": "<IOT ID>",
            "auth-method": "token",
            "auth-token": "<IOT Token>"
        }
        client = ibmiotf.device.Client(options)
    except ibmiotf.ConnectionException  as e:
        print e# coding=utf-8

    client.connect()
    #myData={'payload' : txt1 , 'cpu' : 60 , 'mem' : 50 }
    myData={ 'd' : { 'text' : txt1 } }
    client.publishEvent("status", "json", myData)

def main():
    recorder = Recorder("speech.wav")

    print("Please say something nice into the microphone\n")
    recorder.record_to_file()

    print("Transcribing audio....\n")
    result = transcribe_audio('speech.wav')

    result_json = json.loads(result)
    text = result_json['results'][0]['alternatives'][0]['transcript']
    print("Text: " + text + "\n")

    #r = requests.post('https://itironode01.mybluemix.net/itiro', data = {'payload':text.strip()})

    watson_iot(text)

    #sentiment, score = get_text_sentiment(text)
    #print(sentiment, score)

if __name__ == '__main__':
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    try:
        main()
    except:
        print("IOError detected, restarting...")
        main()
