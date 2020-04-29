from boltiot import Bolt
api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"
device_id = "BOLTXXXXXXX"
mybolt = Bolt(api_key, device_id)
response = mybolt.restart()
print(response)
