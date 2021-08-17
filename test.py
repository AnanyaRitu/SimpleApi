# ekhane request diye diye test korbo api chole naki.

import requests
# bole dicchi base url konta
BASE = "http://127.0.0.1:5000/"
# base url/helloworld e get request pathacchi.
# name parameter jeta string hobe.
# response = requests.get(BASE + "helloworld/Sumit")
data = [{"name": "how to drink water", "views": 1000, "likes": 10},
        {"name": "how to walk", "views": 2000, "likes": 20},
        {"name": "how to sleep", "views": 3000, "likes": 30}]
for i in range(len(data)):
    response = requests.put(BASE + "video/"+str(i), data[i])
    print(response.json())
input()
'''response = requests.delete(BASE + "video/0")
print(response)
input()  # eta dile enter press na korle porer step e jay na. 
response = requests.get(BASE + "video/4")
print(response.json())'''
response = requests.patch(BASE + "video/1", {"likes": 100})
print(response.json())
