
import requests
import json
data_dict = {"start":"2020-01-01 11:00:00", "end":"2020-02-27 14:34:00"}
r = requests.post("http://127.0.0.1:9001/sentiments/report",  data=data_dict)

print (r.text)