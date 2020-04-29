import email_conf
from boltiot import Email, Bolt
import json, time

min_lim = 10
max_lim = 299

mybolt = Bolt(email_conf.API_KEY, email_conf.DEVICE_ID)
mailer = Email(email_conf.MAILGUN_API_KEY, email_conf.SANDBOX_URL, email_conf.SENDER_EMAIL, email_conf.RECEIPENT_EMAIL)

while True:
    print("Reading your sensor value")
    response = mybolt.analogRead('A0')
    data = json.loads(response)
    print("Sensor value is: " + str(data['value']))
    try:
        sensor_value = int(data['value'])
        if sensor_value > max_lim or sensor_value < min_lim:
             print("Making Request to mailgun to send an email")
             response = mailer.send_email("Alert", "The Current temperature sensor value is " + str(sensor_value))
             response_text = json.loads(response.text)
             print("Response received fron  mailgun is: " + str(response_text['message']))
    except Exception as e:
        print("Error occured: Below are the details")
        print (e)
    time.sleep(10) 
