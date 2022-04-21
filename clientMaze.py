import requests
from itsdangerous import json
from unicodedata import category
from time import sleep
ml = 0 
mr = 0
ultimo = 0

risposta = requests.get("http://192.168.0.136:5000/api/v1/sensors/obstacles").json()
l = 1
if(risposta["Left"] == 1):
    l = 1
while True:
    ml = 0 
    mr = 0
    risposta = requests.get("http://192.168.0.136:5000/api/v1/sensors/obstacles").json()
    print(risposta)
    if(risposta["Left"]==1):
        ml = 40
    if(risposta["Right"]==1):
        mr = 41
    if(risposta["Right"]==0 and risposta["Left"] == 0):
        risposta = requests.get(f"http://192.168.0.136:5000/api/v1/motors/both?pwmL=-40&pwmR=-40&time=5")
        sleep(0.5)
        
        risposta = requests.get(f"http://192.168.0.136:5000/api/v1/motors/both?pwmL={40*l}&pwmR={-40*l}&time=3")
        sleep(0.3)
       
    risposta = requests.get(f"http://192.168.0.136:5000/api/v1/motors/both?pwmL={ml}&pwmR={mr}&time=2")
    sleep(0.14)      
