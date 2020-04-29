import conf, json, time, math, statistics
from boltiot import Email,Bolt

max_lim = 299
min_lim = 10

def compute_bounds(history_data,frame_size,factor):
    if len(history_data)<int(frame_size) :
        return None

    if len(history_data)>int(frame_size) :
        del history_data[0:len(history_data)-int(frame_size)]
    Mn=statistics.mean(history_data)
    Variance=0
    for data in history_data :
        Variance += math.pow((data-Mn),2)

    Zn = int(factor) * math.sqrt(int(Variance) / int(frame_size))
    High_bound = history_data[int(frame_size)-1]+Zn
    Low_bound = history_data[int(frame_size)-1]-Zn
    return [High_bound,Low_bound]

tempo = Bolt(conf.API_KEY, conf.DEVICE_ID)
mailer = Email(conf.MAILGUN_API_KEY, conf.SANDBOX_URL, conf.SENDER_EMAIL, conf.RECEIPENT_EMAIL)
history_data=[]

while True:
    print("Collecting sensor response")
    response = tempo.analogRead('A0')
    data = json.loads(response)
    print("Sensor value " +str(data['value']))
    try:
        sensor_value = int(data['value'])
        if sensor_value>max_lim or sensor_value<min_lim:
           print("Making request to Mailgun to send email")
           respo = mailer.send_email("ALERT:","Temperature exceeds from threshold limit")
           response_text = json.loads(respo.text)
           print("Response received from mailgun is: " +str(response_text['message']))
    except Exception as e:
           print("ERROR: Below are the details")
           print (e)
    time.sleep(10)

    bound = compute_bounds(history_data,conf.FRAME_SIZE,conf.MUL_FACTOR)
    if not bound:
        required_data_count=int(conf.FRAME_SIZE)-len(history_data)
        print("Not enough data to compute Z-score. Need ",required_data_count," more data points" )
        history_data.append(int(data['value']))
        time.sleep(10)
        continue

    try:
       if sensor_value > bound[0] :
           print ("Someone has opened the door. Sending an Email")
           response1 = mailer.send_email("ALERT:","Someone has opened the fridge door")
           print("This is the response",response1)
       history_data.append(sensor_value);
    except Exception as e:
       print ("Error", e)
    time.sleep(10)  



