from flask import Flask, render_template, redirect, url_for, request, make_response
import threading as thr
import time
app = Flask(__name__)
import sqlite3
import random
import string
from datetime import datetime
import random
import string
import json
from AlphaBot import AlphaBot
import threading as thr

import RPi.GPIO as GPIO
bot = AlphaBot()
DR = 16
DL = 19
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)


def gestisciMotori(diz):
     try:
         print(int(diz["pwmL"]),int(diz["pwmR"]),int(diz["time"]))
         bot.set_motor(int(diz["pwmL"]),-int(diz["pwmR"]))
         #bot.set_motor(0,int(diz["pwmR"]));
         time.sleep(float(diz["time"])/3);print("finito")
         bot.stop()
     except Exception as e:
         print(e)

@app.route('/api/v1/sensors/obstacles', methods=['GET'])
def sensore():
    sinistra = GPIO.input(DR)
    destra = GPIO.input(DL)
    sensori={"Left":sinistra,"Right":destra}
    return json.dumps(sensori)

@app.route('/api/v1/motors/both', methods=['GET'])
def motors():
    diz = request.args.to_dict()
    x = thr.Thread(target=gestisciMotori, args=(diz,))
    x.start()
    return "finito"	


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')