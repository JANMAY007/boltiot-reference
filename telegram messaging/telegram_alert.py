import requests                  #for making HTTP requests
import json                      #library for handling json data
import time                      #module for sleep operation


from boltiot import Bolt         #importing Bolt from boltiot module
import conf                      #config file

mybolt = Bolt(conf.bolt_api_key, conf.device_id)

def get_sensor_value_from_pin(pin):
    """Return the sensor value. Returns -999 if request fails"""
    try:
        response = mybolt.analogRead(pin)
        data = json.loads(response)
        if data["success"] != 1:
            print("Request not successful")
            print("This is the response->", data)
            return -999
        sensor_value = int(data["value"])
        return sensor_value
    except Exceptions as e:
        print("Something went wrong when returning the sensor value")
        print(e)
        return -999

def send_telegram_message(message):
     """Sends message via telegram"""
     url = "https://api.telegram.org/" + conf.telegram_bot_id + "/sendMessage"
     data = {
         "chat_id": conf.telegram_chat_id,
         "text": message
     }
     try:
         response = requests.request(
              "POST",
              url,
              params=data
         )
         print("This is the Telegram Message")
         print(response.text)
         telegram_data = json.loads(response.text)
         return telegram_data["oK"]
     except Exception as e:
         print("An error occured in sending the alert message via telegram")
         print(e)
         return False

while True:
    sensor_value = get_sensor_value_from_pin("A0")
    temperature = (100*sensor_value)/1024
    print("The current temperature is: ", temperature)

    if sensor_value == -999:
        print("Request was unsuccessful.  Skipping.")
        time.sleep(10)
        continue

    if temperature >= conf.threshold:
        print("Temperature has exceeded threshold")
        message = "Alert! temp[erature has exceeded " + str(conf.threshold) + ". The current value is " + str(temperature)
        telegram_status = send_telegram_message(message)
        print("This is the telegram status: ",telegram_status)
        
    time.sleep(10)
