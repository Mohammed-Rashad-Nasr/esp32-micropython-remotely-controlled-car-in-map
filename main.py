from machine import Pin, PWM

from time import sleep
import network
import socket
#import mpu6050
#import math
#rd = 180/math.pi
#i2c = I2C(scl=Pin(22), sda =Pin(21))
#mpu = mpu6050.accel(i2c)
#values = mpu.get_values()
#def map(x,in_min,in_max,out_min,out_max):
#    return int((x-in_min)*(out_max-out_min)/(in_max-in_min) + out_min)
#x_ang = map(values["AcX"],256,402,-90,90)
#y_ang = map(values["AcY"],256,402,-90,90)
#z_ang = map(values["AcZ"],256,402,-90,90)
#x = rd * (math. atan2(-y_ang,-z_ang)+math.pi)
#{ = rd * (math.atan2(-x_ang,-z_ang)+math.pi)
#z = rd * (math.atan2(-y_ang,-x_ang)+math.pi)
#print(x)
x=0
y=0
heading=0

ssid = 'Control'
password = '123456789'
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid = ssid, password = password)
while not ap.active():
    pass
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('',80))
s.listen(5)

conn, addr = s.accept()
request = conn.recv(1024)
request = str(request)
print(request[2])
mode = request[2]
if mode == 'm':
    conn.close()
else:
    x2 = int(request[3])
    y2 = int(request[4])
    pass
#frequency = 1000      
pinn2 = Pin(26, Pin.OUT)    
pinn1 = Pin(25, Pin.OUT)
pinn4 = Pin(21, Pin.OUT)    
pinn3 = Pin(22, Pin.OUT)
enc =0
encc=0
def forward():
    pinn1.on()
    pinn2.off()
    pinn3.on()
    pinn4.off()

def stop():
    pinn1.off()
    pinn2.off()
    pinn3.off()
    pinn4.off()
def left():
    pinn1.on()
    pinn2.off()
    pinn3.off()
    pinn4.on()
def right():
    pinn1.off()
    pinn2.on()
    pinn3.on()
    pinn4.off()


def encfunc(pin):
    global enc
    enc = enc + 1
def enc2func(pin):
    global encc
    encc = encc + 1
    
def step () :
    global enc
    global x
    global y
    global heading
    if enc >2 :
        sleep(1)
        stop()
        enc = 0
        if heading == 0 :
            y=y+1
        elif heading == 90 :
            x=x+1
        elif heading == 180:
            y=y-1
        elif heading ==-90 :
            x=x-1
        conn.send(str(x)+str(y))
        print(str(x)+str(y)) 
    else:
        forward()

def rightturn () :
    global enc
    global heading
    if enc > 313 :
        stop()
        enc = 0
        if (heading +90)==270 :
            heading = -90 
        elif (heading+90)==360 :
            heading=0
        else :
            heading=heading+90
  
    else:
        right()

def movey (ypos):
    for i in range(ypos):
        step()
    
        
def movex (xpos):
    for i in range(xpos):
        step()
    
    
def moveto (xx,yy):
    movey(yy)
    sleep(0.5)
    stop()
    sleep(0.5)
    rightturn()
    sleep(0.5)
    stop()
    sleep(0.5)
    movex(xx)
    stop()
#enable1 = PWM(Pin(18), frequgncy)  
#enable = PWM(Pin(27), frequency)  
#dc_motor = DCMotor(pinn2, pinn1, enable)
#dc_motor= DCMotor(pinn2, pinn1, enable, 350, 1023)
#dc_motor1 = DCMotor(pinn4, pinn3, enable1)
#dc_motor1 = DCMotor(pinn4, pinn3, enable1, 350, 1023)
enc1 = Pin(33, Pin.IN)
enc1.irq(encfunc,Pin.IRQ_RISING)
enc2 = Pin(32, Pin.IN)
enc2.irq(enc2func,Pin.IRQ_RISING)
flag = ''
flag2=False
while True:
    if mode == 'm' :
   
        while flag2 == False :
        #global enc
            conn, addr = s.accept()
            data = conn.recv(1024)
            data = str(data)
            print(data)
            flag=data[2]
            enc = 0
            flag2=True
        while flag2 == True : 
        #global enc
        
            if flag == 'F': 
       

                if enc >2 :
                    sleep(1)
                    stop()
   
                    enc = 0
                    flag = ''
                 
                    conn.close()
                    flag2=False
                
                else:
                    forward()
            
                
        
            elif flag == 'L': 
            
                if enc > 313 :
                    stop()

                    enc = 0
                    flag = ''
                    flag2=False
                    conn.close()
                else:
                    left()
                
            elif flag == 'R': 
            
                if enc > 313 :
                    stop()

                    enc = 0
                    flag = ''
                    flag2=False
                    conn.close()
                else:
                    right()  
              
    else:
        moveto(x2,y2)
        break
