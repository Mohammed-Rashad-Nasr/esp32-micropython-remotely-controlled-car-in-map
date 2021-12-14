from machine import Pin, PWM,I2C
from dcmot import DCMotor 
from time import sleep
import network
import socket
import MPU6050
import math
rd = 180/math.pi
i2c = I2C(scl=Pin(22), sda =Pin(21))
mpu = mpu6050.accel(i2c)
values = mpu.get_values()
def map(x,in_min,in_max,out_min,out_max):
    return int((x-in_min)*(out_max-out_min)/(in_max-in_min) + out_min)
x_ang = map(values["AcX"],256,402,-90,90)
y_ang = map(values["AcY"],256,402,-90,90)
z_ang = map(values["AcZ"],256,402,-90,90)
x = rd * (math.atan2(-y_ang,-z_ang)+math.pi)
y = rd * (math.atan2(-x_ang,-z_ang)+math.pi)
z = rd * (math.atan2(-y_ang,-x_ang)+math.pi)
print(x)
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
    pass
frequency = 150000       
pin1 = Pin(5, Pin.OUT)    
pin2 = Pin(4, Pin.OUT)
pin3 = Pin(21, Pin.OUT)    
pin4 = Pin(22, Pin.OUT)
enc =0    
def encfunc(pin):
    global enc
    enc = enc + 1
    print(enc)
enable = PWM(Pin(18), frequency)  
enable1 = PWM(Pin(23), frequency)  
dc_motor = DCMotor(pin1, pin2, enable)
dc_motor = DCMotor(pin1, pin2, enable, 350, 1023)
dc_motor1 = DCMotor(pin3, pin4, enable)
dc_motor1 = DCMotor(pin3, pin4, enable, 350, 1023)
enc1 = Pin(2, Pin.IN)
enc1.irq(encfunc,Pin.IRQ_RISING)
def right():
    dc_motor1.stop()        
    dc_motor.forward(100)
def left():
    dc_motor.stop()
    dc_motor1.forward(10)        
def forward():
    dc_motor.forward(10)
    dc_motor1.forward(10)        
def stp():
    dc_motor.stop()
    dc_motor1.stop()        
flag = 0
while True:
    s.settimeout(0.5)
    
    try:
        conn, addr = s.accept()
        data = conn.recv(1024)
        data = str(data)
        print(data)
        if data[2] == 'F':
            flag = 1
    except:
        pass
    print('z')
    if flag == 1:
            if enc >100:
                stp()
                enc = 0
                flag = 0
                conn.close()
            else:
                forward()
                print('x')
    
