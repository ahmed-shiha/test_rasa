# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests 

class ActionWeather(Action):
    
   

    def name(self) -> Text:
        return "action_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            def weatherCity(city):
                API_KEY = "130043fb9b9b18097d439d12b5bb680f"
                base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
     #http://api.openweathermap.org/data/2.5/weather?q=singapore&APPID=130043fb9b9b18097d439d12b5bb680f&units=metric&exclude=hourly,minutely,alerts
                Final_url = base_url + "appid=" + API_KEY + "&q=" + city + "&units=metric&exclude=hourly,minutely,alerts"
                weather_data = requests.get(Final_url).json()
                return weather_data

            # retrieve saved slot from rasa 
            city = tracker.get_slot('city')
            
        # list possible cities     
            possible_cities=["Singapore","Malaysia","Thailand"] 
            # read & parse the information and generate response
    
            if city in possible_cities:
                weatherAPIMain = weatherCity(city)['main']
                temperature = weatherAPIMain['temp']
                weatherAPIJson = weatherCity(city)
                condition = weatherAPIJson['weather'][0]["description"]
                wind = weatherAPIJson['wind']['speed']
                response = "The current temperature in {} is {} degres Celsius. It is {} and the wind speed is {} meter per second ".format(city,temperature,condition,wind)
                
            else:    
                response = "Sorry, currently I am limited to information from Singapore, Malaysia and Thailand only."
        
            dispatcher.utter_message(response)   
        
            return [{"event": "restart"}]
