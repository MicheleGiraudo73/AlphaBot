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


token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))

def validate(username, password):
    completion = False
    conn = None
    try:
        conn = sqlite3.connect('databaseAlphabot.db')
    except:
        print("__")
    
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM USERS")
    except:
        print("CIAO")
    rows = cur.fetchall()
    
    for row in rows:
        dbUser = row[0]
        dbPass = row[1]
        
        if dbUser==username:
            completion=check_password(dbPass, password)
    return completion

def check_password(hashed_password, user_password):
    return hashed_password == user_password

def accessi(user):
    con = None
    con= sqlite3.connect('databaseAlphabot.db')
    cur = con.cursor()
    now = datetime.now()
    data_str = now.strftime("%d/%m/%y %H:%M:%S")
    cur.execute(f"INSERT INTO Accessi (Username,OraData) VALUES ('{user}','{data_str}')")
    cur.execute("commit")
    con.close()

@app.route('/', methods=['GET', 'POST'])

def login():
    error = None
    if request.method == 'POST': #se uguale a GET fa il return della pagina login
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            resp = make_response(redirect(url_for('i')))
            resp.set_cookie('username', username)
            print(request.cookies.get('username'))
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


import RPi.GPIO as GPIO
class AlphaBot(object):
    
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA  = 50
        self.PB  = 50

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

    def right(self):
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def stop(self):
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def left(self):
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def backward(self, speed=30):
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def forward(self, speed=30):
	    
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        
    def set_pwm_a(self, value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def set_pwm_b(self, value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)    
        
    def set_motor(self, left, right):
        if (right >= 0) and (right <= 100):
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif (right < 0) and (right >= -100):
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if (left >= 0) and (left <= 100):
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif (left < 0) and (left >= -100):
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)



        
        
    def gestisci(self,comando,user):
            #self.funzioni = {"F":self.forward,"S":self.stop,"B":self.backward,"L":self.left,"R":self.right}
        #try:
         #   self.funzioni[parola]()
        #except:
        #    pass
        conn = None
        try:
            conn = sqlite3.connect('./databaseAlphabot.db')
        except:    
            print("file non trovato")
        
        cur = conn.cursor()
        comandi = None
        try:
            cur.execute(f"SELECT sequenza FROM movimenti WHERE nome = '{comando}'")
            comandi = cur.fetchall()[0][0]
            now = datetime.now()
            data_str = now.strftime("%d/%m/%y %H:%M:%S")
            cur.execute(f"INSERT INTO RegistroMovimento (username,movimento,OraData) VALUES ('{user}','{comandi}','{data_str}')")
            cur.execute("commit")
            print(comandi)
        except:
            print("query non valida")
        
        self.funzioni = {"F":self.forward,"S":self.stop,"B":self.backward,"L":self.left,"R":self.right}
        for comando in comandi.split(";"):
            try:
                self.funzioni[comando[0]]()
            except:
                pass    
            time.sleep(float(comando[1:])/1000)
            self.stop()

def regMov(user,mov):
    con = None
    con= sqlite3.connect('databaseAlphabot.db')
    cur = con.cursor()
    now = datetime.now()
    data_str = now.strftime("%d/%m/%y %H:%M:%S")
    cur.execute(f"INSERT INTO RegistroMovimento (username,movimento,OraData) VALUES ('{user}','{mov}','{data_str}')")
    cur.execute("commit")
    con.close()
    
bot = AlphaBot()
@app.route(f'/{token}', methods=['GET', 'POST'])
def index():
    us=request.cookies.get('username')
    accessi(us)
    
    if request.method == 'POST':
        
        if(request.form['inputQuery'] != ''):
            #print(request.form['inputQuery'])
            bot.gestisci(request.form['inputQuery'],request.cookies.get('username'))
        elif request.form.get('avanti') == 'avanti':
            regMov(request.cookies.get('username'),"avanti")
            bot.forward()
        elif  request.form.get('indietro') == 'indietro':
            regMov(request.cookies.get('username'),"indietro")
            bot.backward()
        elif  request.form.get('destra') == 'destra':
            regMov(request.cookies.get('username'),"destra")
            bot.right()
        elif  request.form.get('sinistra') == 'sinistra':
            regMov(request.cookies.get('username'),"sinistra")
            bot.left()
        elif  request.form.get('stop') == 'stop':
            regMov(request.cookies.get('username'),"stop")
            bot.stop()
        else:
            print("errore")
    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')