from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionGetWeather(Action):
    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot("location")
        weather_data = self.get_weather(location)

        if weather_data:
            weather_description = weather_data["weather"][0]["description"]
            temperature = weather_data["main"]["temp"]
            message = f"It's {temperature}°C and {weather_description} in {location} right now."
            dispatcher.utter_message(message)
        else:
            dispatcher.utter_message("Sorry, I couldn't fetch the weather data.")

        return []
    def get_weather(self, location: Text) -> Dict[Text, Any]:
        api_key = "36846ba4cc899361b6eabdc096d68296"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

import os


class ActionAskYield(Action):
    def name(self) -> Text:
        return "action_provide_yield_infos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Use Gooey AI API to fetch response for yield intent
        response = self.fetch_gooey_response("Why are my potatoes small after harvest?")
        dispatcher.utter_message(text=response["Response"])

        return []

    def fetch_gooey_response(self, input_prompt: Text) -> Dict[Text, Any]:
        api_key = os.getenv("GOOEY_API_KEY")
        if api_key is None:
            raise Exception("GOOEY_API_KEY is not set. Please check your environment variables.")

        payload = {"input_prompt": input_prompt}

        try:
            response = requests.post(
                "https://api.gooey.ai/v2/video-bots/",
                headers={"Authorization": "Bearer " + api_key},
                json=payload,
            )
            if not response.ok:
                raise Exception(f"API request failed with status code {response.status_code}: {response.content}")

            return response.json()
        except Exception as e:
            print(f"An error occurred while making the API request: {e}")
            return {"Response": "Sorry, I couldn't fetch the response."}

        return {}
class ActionAskMarketInformation(Action):
    def name(self) -> Text:
        return "action_provide_market_information"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Use Gooey AI API to fetch response for market_information intent
        response = self.fetch_gooey_response("Which seeds are the best for red potatoes?")
        dispatcher.utter_message(text=response["Response"])

        return []

    def fetch_gooey_response(self, input_prompt: Text) -> Dict[Text, Any]:
        api_key = os.getenv("GOOEY_API_KEY")
        if api_key is None:
            raise Exception("GOOEY_API_KEY is not set. Please check your environment variables.")

        payload = {"input_prompt": input_prompt}

        try:
            response = requests.post(
                "https://api.gooey.ai/v2/video-bots/",
                headers={"Authorization": "Bearer " + api_key},
                json=payload,
            )
            if not response.ok:
                raise Exception(f"API request failed with status code {response.status_code}: {response.content}")

            return response.json()
        except Exception as e:
            print(f"An error occurred while making the API request: {e}")
            return {"Response": "Sorry, I couldn't fetch the response."}

        return {}

class ActionAskPestControl(Action):
    def name(self) -> Text:
        return "action_Pest_control"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Use Gooey AI API to fetch response for Pest_control intent
        response = self.fetch_gooey_response("Can you recommend a pest-resistant variety of wheat for planting?")
        dispatcher.utter_message(text=response["Response"])

        return []

    def fetch_gooey_response(self, input_prompt: Text) -> Dict[Text, Any]:
        api_key = os.getenv("GOOEY_API_KEY")
        if api_key is None:
            raise Exception("GOOEY_API_KEY is not set. Please check your environment variables.")

        payload = {"input_prompt": input_prompt}

        try:
            response = requests.post(
                "https://api.gooey.ai/v2/video-bots/",
                headers={"Authorization": "Bearer " + api_key},
                json=payload,
            )
            if not response.ok:
                raise Exception(f"API request failed with status code {response.status_code}: {response.content}")

            return response.json()
        except Exception as e:
            print(f"An error occurred while making the API request: {e}")
            return {"Response": "Sorry, I couldn't fetch the response."}

        return {}

class ActionAskIrrigationFertilization(Action):
    def name(self) -> Text:
        return "action_provide_irrigation_fertilization"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Use Gooey AI API to fetch response for irrigation_fertilization intent
        response = self.fetch_gooey_response("What irrigation techniques are suitable for arid regions?")
        dispatcher.utter_message(text=response["Response"])

        return []

    def fetch_gooey_response(self, input_prompt: Text) -> Dict[Text, Any]:
        api_key = os.getenv("GOOEY_API_KEY")
        if api_key is None:
            raise Exception("GOOEY_API_KEY is not set. Please check your environment variables.")

        payload = {"input_prompt": input_prompt}

        try:
            response = requests.post(
                "https://api.gooey.ai/v2/video-bots/",
                headers={"Authorization": "Bearer " + api_key},
                json=payload,
            )
            if not response.ok:
                raise Exception(f"API request failed with status code {response.status_code}: {response.content}")

            return response.json()
        except Exception as e:
            print(f"An error occurred while making the API request: {e}")
            return {"Response": "Sorry, I couldn't fetch the response."}

        return {}