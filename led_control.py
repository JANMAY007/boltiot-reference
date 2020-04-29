from boltiot import Bolt
api_key = "XXXXXXXXXXXXXXXXXXXXXXX"
device_id = "BOLTXXXXXX"
mybolt = Bolt(api_key, device_id)
response = mybolt.digitalWrite('0', 'HIGH')
print (response)
