import socket as sck
import threading as thr
import RPi.GPIO as GPIO
import time
import sqlite3

indirizzo = ('192.168.0.135',5015)
s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
s.bind(indirizzo)
path = "/home/pi/Alphabot/databaseAlphabot.db"


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

    def left(self):
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

    def right(self):
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

    def gestisci(self,parola):
        '''
        self.funzioni = {"F":self.forward,"S":self.stop,"B":self.backward,"L":self.left,"R":self.right}
        try:
            self.funzioni[parola]()
        except:
            pass
        '''
        conn = None
        try:
            conn = sqlite3.connect(path)
        except:    
            print("file non trovato")
            
        cur = conn.cursor()
        comandi = None
        try:
            cur.execute(f"SELECT sequenza FROM movimenti WHERE nome = '{parola}'")
            comandi = cur.fetchall()[0][0]
            print(comandi)
        except:
            print("query non valida")
        if(comandi != None):
            self.funzioni = {"F":self.forward,"S":self.stop,"B":self.backward,"L":self.left,"R":self.right}
            for comando in comandi.split(";"):
                try:
                    self.funzioni[comando[0]]()
                except:
                    pass
                time.sleep(float(comando[1:])/1000)
                self.stop()

class Clients_class(thr.Thread):
    def __init__(self, s):
        thr.Thread.__init__(self)   
        self.s = s
        self.daemon = True
    
    def run(self):
        while True:
            connessione, indirizzo = s.accept()
            connessione.sendall("Dispositivo già accoppiato".encode())


def main():
    s.listen()
    connessione, indirizzo = s.accept()
    
    temp = Clients_class(s)
    temp.start()
    
    _ = (connessione.recv(4096)).decode()
    connessione.sendall(("controller accettato").encode())
    gestisciController(connessione)
        
    
def gestisciController(connessione):
    bot = AlphaBot()
    while True:
        messaggio = (connessione.recv(4096)).decode()
        if(messaggio == "esci"):
            connessione.sendall("disaccoppiato".encode())
            break
        bot.gestisci(messaggio)
        print(messaggio)
        

if __name__ == '__main__':
    main()