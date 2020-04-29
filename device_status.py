from boltiot import Bolt
api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXX"
device_id = "BOLTXXXXXXX"
mybolt = Bolt(api_key, device_id)
response = mybolt.isOnline()
print (response)
