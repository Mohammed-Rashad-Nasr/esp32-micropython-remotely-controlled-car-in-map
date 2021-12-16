from machine import Pin, PWM

from time import sleep
import network
import socket

x=0
y=0
heading=0
end =False  
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
    while enc < 313:
        forward()
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
    print(str(y)+str(x)) 

def rightturn () :
    global enc
    global heading
    while enc < 313:
        right()
    stop()
    if (heading +90)==270 :
        heading = -90 
    elif (heading+90)==360 :
        heading=0
    else :
        heading=heading+90
         

def movey (ypos):
    i = 0
    for i in range(ypos):
        step()
    
        
def movex (xpos):
    j = 0
    for j in range(xpos):
        step()
    
   
def moveto (xx,yy):
    global end
    global enc
    if xx == 0:
        movey(yy)
    else:
        movey(yy)
        enc = 0
        sleep(0.5)
        stop()
        sleep(0.5)
        rightturn()
        enc = 0
        sleep(0.5)
        stop()
        sleep(0.5)
        movex(xx)
    end = True

enc1 = Pin(33, Pin.IN)
enc1.irq(encfunc,Pin.IRQ_RISING)
enc2 = Pin(32, Pin.IN)
enc2.irq(enc2func,Pin.IRQ_RISING)
flag = ''
flag2=False
while True :
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
        if end == False :
            moveto(x2,y2)
        else
            break
        
