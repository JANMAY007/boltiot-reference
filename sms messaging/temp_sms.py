import sms_conf
from boltiot import Sms, Bolt
import json, time

min_limit = 200
max_limit = 300

mybolt = Bolt(sms_conf.API_KEY, sms_conf.DEVICE_ID)
sms = Sms(sms_conf.SID, sms_conf.AUTH_TOKEN, sms_conf.TO_NUMBER, sms_conf.FROM_NUMBER)

while True:
    print ("Reading Sensor Value")
    response = mybolt.analogRead('A0')
    data = json.loads(response)
    print("Sensor value is: " + str(data['value']))
    try:
        sensor_value = int(data['value'])
        if sensor_value > max_limit or sensor_value < min_limit:
            print("Making request to Twilio to send a SMS")
            response = sms.send_sms("The Current temperature sensor value is " +str(response))
            print("Response received from Twilio is: " + str(response.status))
    except Exception as e:
        print ("Error occured: Below are the details")
        print (e)
    time.sleep(10)
