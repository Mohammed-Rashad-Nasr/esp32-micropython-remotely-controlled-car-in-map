################################################################
################################################################
### by      : -Mohammed rashad                               ###
###           -Abdelmuniem bahaa eldien                      ###
###           -Salma alaa                                    ###
###           -Ezz eldien elsaied                            ###
###           -Saed magdy                                    ###
###           -Osman ali                                     ###
###           -Mohammed roshdy                               ###
###           -mohammed muharram                             ###
###                                                          ###
### date    : 29 Dec 2021                                    ###
### version : v12.0                                          ###
###                                                          ###
################################################################
################################################################


#importing micropython libraries
################################################################

from machine import Pin, PWM   
from time import sleep

################################################################


#network initialization and setup
################################################################

import network                                            #import network library
ssid = 'Control'                                          #network name variable
password = '123456789'                                    #password variable
access_point = network.WLAN(network.AP_IF)                #initializing network in access point mode using access_pointt object
access_point.active(True)                                 #activate network
access_point.config(essid = ssid, password = password)    #configure password and ssid
while not access_point.active():                          #wait to ensure that network is active
    pass

################################################################    


#socket initialization and setup
################################################################ 
   
import socket                                                     #import socket library  

# AF_INET - use Internet Protocol v4 addresses
# SOCK_STREAM means that it is a TCP socket
             
socket_object = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  


socket_object.bind(('',80))                                       # specifies that the socket is reachable by any address the machine happens to have on port 80
socket_object.listen(5)                                           # max of 5 socket connections
  
  
  
################################################################    


#variables initialization
################################################################ 

#localization variables
#######################
x       = 0                
y       = 0
heading = 0
#######################

#encoder variables
#######################
Encoder1_Value = 0
Encoder2_Value = 0
#######################

#flag and check variables
#######################
FirstStop_Flag          = False
SecondStop_Flag         = False
SecondStage_Start       = False
ObstacleRoutine_Started = False 
Command_Recieved        = False
Command = ''
#######################

################################################################


#recieve mode of operation from App
################################################################ 

while True :
    conn, addr = s.accept()        #initialize new connectin
    request = conn.recv(1024)      #recieve data from App and store it in request variable
    request = str(request)         #cast request to string in order to slice and itirate it
    mode = request[2]              #b'....' put mode character in mode variable
    if mode == 'm':                #manual mode
        conn.close()               ### in manual mode we close connection to ait for new connection from pressed buttons
        break                      ### exit while 
    elif mode == 'a':              #auto mode
        x2 = int(request[3])       ### get target x position
        y2 = int(request[4])       ### get target y position 
        break                      ### exit while
    else :                         #unknown character recieved
        pass                       ### wait for another character

################################################################ 


#Motors' functions and pins
################################################################ 

#motor pins
##################################
Motor1_Back    = Pin(18, Pin.OUT)    
Motor1_Forward = Pin(19, Pin.OUT)
Motor2_Back    = Pin(26, Pin.OUT)     
Motor2_Forward = Pin(27, Pin.OUT)
##################################

#motor functions
##################################

def forward():
#both motors move in same direction
    Motor1_Forward.on()
    Motor1_Back.off  ()
    Motor2_Forward.on()
    Motor2_Back.off  ()
def stop():
#both motors stop motion
    Motor1_Forward.off()
    Motor1_Back.off   () 
    Motor2_Forward.off()
    Motor2_Back.off   () 
def left(): 
#right motor forward and left motor backward
    Motor1_Forward.on ()
    Motor1_Back.off   ()
    Motor2_Forward.off()
    Motor2_Back.on    ()
def right():
#right motor backward and left motor forward
    Motor1_Forward.off() 
    Motor1_Back.on    () 
    Motor2_Forward.on ()
    Motor2_Back.off   ()

##################################    

################################################################


IR_Pin = Pin(23,Pin.IN)  #IR sensor pin 



#encoders' functions and pins
################################################################ 

#encoder pins 
Encoder1_Pin = Pin(35, Pin.IN)
Encoder2_Pin = Pin(32, Pin.IN)

#encder ISRs
Encoder1_Pin.irq(Encoder1_Function,Pin.IRQ_RISING)
Encoder2_Pin.irq(Encoder2_Function,Pin.IRQ_RISING)

def Encoder1_Function(pin): 
#increase encoder1 value by 1 
    global Encoder1_Value
    Encoder1_Value = Encoder1_Value + 1
def Encoder2_Function(pin):
#increase encoder2 value by 1 
    global Encoder2_Value
    Encoder2_Value = Encoder2_Value + 1 

################################################################




#Mapping functions
################################################################ 

def step () :
#this function moves one step forward in heading direction and update x,y values
    global ObstacleRoutine_Started 
    global Encoder1_Value
    global x
    global x2
    global y2
    global y
    global heading
    global distance
    
    
    while Encoder1_Value < 980:                       #check if step is done or not
        if IR_Pin.value() :                           ### check if there is obstacle or not while moving
            forward()                                 ###### if not done yet and there isn't an obstacle keep moving
        else :                                        ### obstacle detected while moving !!!
            movenew(x2,y2)                            ###### jump to the obstacle avoidence re-routing function
            ObstacleRoutine_Started = True            ###### raise obstacle routine flag 
            stop()                                    ###### stop
            Encoder1_Value = 1000                     ###### make sure that we will not enter this while again after function is done
            break                                     ###### exit while
    
    
    if ObstacleRoutine_Started  == False :            #check if the function entered obstacle avoiding routine or not
        stop()                                        ### if not stop 
        Encoder1_Value = 0                            ### and reset encoder value
        if heading == 0 :                             ### check heading angle to get increasing direcction x or y
            y=y+1                                     ###### step in +ve y
        elif heading == 90 :
            x=x+1                                     ###### step in +ve x
        elif heading == 180:
            y=y-1                                     ###### step in -ve y
        elif heading ==-90 : 
            x=x-1                                     ###### step in -ve x
            
        conn.send(str(x)+str(y)+','+str(heading))     ### send x , y and heading to App
        
    else :
    
        stop()                                        ### if obstacle found and function is done just stop

def rightturn () :
#function to turn 90 degrees right

    global Encoder1_Value  
    global heading
    
    Encoder1_Value = 0                    #reset encoder value
    while Encoder1_Value < 350 :          #check if 90 degree turn is done
        right()                           ### if not done keep turning in right direction
    stop()                                #if done stop
    
    #update heading by adding 90 degrees to current angle
    
    if (heading +90)==270 :
        heading = -90 
    elif (heading+90)==360 :
        heading=0    
    else :
        heading=heading+90
        
def leftturn () :
#function to turn 90 degrees left

    global Encoder1_Value
    global heading
    
    Encoder1_Value = 0                   #reset encoder value
    while Encoder1_Value < 300:          #check if 90 degree turn is done
        left()                           ### if not done keep turning in right direction
    stop()                               #if done stop
 
    #update heading by adding 90 degrees to current angle 
    
    if (heading -90)==-180 :
        heading = 180 
    else :
        heading=heading-90

def movey (ypos):
#function to move in y direction by given steps

    global y
    global Encoder1_Value
    
    Encoder1_Value = 0                                     #reset encoder value
    i = 0                                                  #reset itirator
    if ObstacleRoutine_Started  == False :                 #make sure that we didn't go to movenew
        if (ypos>y) or (ypos == y) :                       ### need to move forward 
            if heading == 0 :                              ###### direction is forward no need to turn
                if ObstacleRoutine_Started  == False :     ######### make sure that we didn't go to movenew
                    for i in range(ypos-y):                ############ move for steps equal to difference between y and targeted y
                        step()
                
            if heading == 90 :                             ###### direction is right we need to rotate to the left by 90 degrees
                if ObstacleRoutine_Started  == False :
                    i = 0
                    leftturn()
                    for i in range(ypos-y):                ############ move for steps equal to difference between y and targeted y
                        step() 
                        
            if heading == 180 :                            ###### direction is back we need to rotate to the left by 180 degrees
                if ObstacleRoutine_Started  == False :
                    leftturn()
                    leftturn()
                    for i in range(ypos-y):                ############ move for steps equal to difference between y and targeted y
                        step()
                        
            if heading == -90 :                            ###### direction is left we need to rotate to the right by 90 degrees
                if ObstacleRoutine_Started  == False :
                    rightturn()
                    for i in range(ypos-y):                ############ move for steps equal to difference between y and targeted y
                        step()
                        
        else :                                             ### need to move backward
            if heading == 0 :                              ###### direction is forward we need to turn right by 180 degrees
                if ObstacleRoutine_Started  == False :
                    rightturn()
                    rightturn()
                    for i in range(y-ypos):                ############ move for steps equal to difference between y and targeted y
                        step()
                        
            if heading == 90 :                             ###### direction is right we need to turn right by 90 degrees
                if ObstacleRoutine_Started  == False :
                    rightturn()
                    for i in range(y-ypos):                ############ move for steps equal to difference between y and targeted y
                        step()
                        
            if heading == 180 :                            ###### direction is backward no need to turn
                if ObstacleRoutine_Started  == False :
                    for i in range(y-ypos):                ############ move for steps equal to difference between y and targeted y
                        step()
                        
            if heading == -90 :                            ###### direction is left we need to turn left by 90 degrees
                if ObstacleRoutine_Started  == False :
                    leftturn()
                    for i in range(y-ypos):                ############ move for steps equal to difference between y and targeted y
                        
                        step()
                         
    Encoder1_Value = 0                                     #reset encoder value again
    
def movex (xpos):
#function to move in x direction by given steps 
 
    global x
    global Encoder1_Value
    
    Encoder1_Value = 0                                     #reset encoder value
    j = 0                                                  #reset itirator
    if ObstacleRoutine_Started ==False :                   #make sure that we didn't go to movenew
        if (xpos>x) or (xpos ==x ) :                       ### need to move right 
            if heading == 0 :                              ###### direction is forward we need to turn right by 90 degrees
                if ObstacleRoutine_Started  == False :     ######### make sure that we didn't go to movenew
                    rightturn()                            
                    for j in range(xpos-x):                ############ move for steps equal to difference between x and targeted x
                        step()
                    
            if heading == 90 :                             ###### direction is right no need to turn 
                if ObstacleRoutine_Started  == False :     ######### make sure that we didn't go to movenew
                    for j in range(xpos-x):                ############ move for steps equal to difference between x and targeted x
                        step()
                        
            if heading == 180 :                            ###### direction is backward we need to turn left by 90 degrees
                if ObstacleRoutine_Started  == False :     ######### make sure that we didn't go to movenew
                    leftturn()
                    for j in range(xpos-x):                ############ move for steps equal to difference between x and targeted x
                        step()
                        
            if heading == -90 :                            ###### direction is left we need to turn left by 180 degrees
                if ObstacleRoutine_Started  == False :     ######### make sure that we didn't go to movenew
                    leftturn()
                    leftturn()
                    for j in range(xpos-x):                ############ move for steps equal to difference between x and targeted x
                        step()
                        
        else :                                             ### need to move left 
            if heading == 0 :                              ###### direction is forward we need to turn left by 90 degrees
                if ObstacleRoutine_Started  == False :     ######### make sure that we didn't go to movenew
                    leftturn()
                    for j in range(x-xpos):                ############ move for steps equal to difference between x and targeted x
                        step()
                        
            if heading == 90 :                             ###### direction is right we need to turn left by 180 degrees
                if ObstacleRoutine_Started  == False :     ######### make sure that we didn't go to movenew
                    leftturn()
                    leftturn()
                    for j in range(x-xpos):                ############ move for steps equal to difference between x and targeted x
                        step()
                        
            if heading == 180 :                            ###### direction is backward we need to turn right by 90 degrees
                if ObstacleRoutine_Started  == False :     ######### make sure that we didn't go to movenew
                    rightturn()
                    for j in range(x-xpos):                ############ move for steps equal to difference between x and targeted x
                        step()
                        
            if heading == -90 :                            ###### direction is left no need to turn 
                if ObstacleRoutine_Started  == False :     ######### make sure that we didn't go to movenew
                    for j in range(x-xpos):                ############ move for steps equal to difference between x and targeted x
                        step()
                        
    Encoder1_Value = 0                                     #reset encoder value again 

def movenew (xx,yy):
#function to auto re-route once robot detected obstacle on its way

    global FirstStop_Flag
    global SecondStop_Flag
    global Encoder1_Value
    global heading
    global x
    global y
    
    
    if (heading == 0) and (x!=3)   :        #obstacle in +ve y direction and not in the last right cell
    
        # step away from obstacle
        Encoder1_Value = 0
        rightturn()
        stop()
        Encoder1_Value = 0
        step()
        stop()
        
        #move y steps then x steps
        movey(yy)
        Encoder1_Value = 0
        stop()
        Encoder1_Value = 0
        stop()
        movex(xx)
        
        
    elif (heading == 0) and (x==3) :        #obstacle in +ve y direction and in the last right cell
    
        # step away from obstacle
        Encoder1_Value = 0
        leftturn()
        stop()
        Encoder1_Value = 0
        step()
        stop()
        
        #move y steps then x steps
        movey(yy)
        Encoder1_Value = 0
        stop()
        Encoder1_Value = 0
        stop()
        movex(xx)
        
        
    elif (heading == 90) and (y!=3):        #obstacle in +ve x direction and not in the last upper cell
    
        # step away from obstacle
        Encoder1_Value = 0
        leftturn()
        stop()
        Encoder1_Value = 0
        step()
        stop()
        
        #move x steps then y steps
        movex(xx)
        Encoder1_Value = 0
        stop()
        Encoder1_Value = 0
        stop()
        movey(yy)
        
        
    elif (heading == 90) and (y==3):        #obstacle in +ve x direction and in the last upper cell
    
        # step away from obstacle
        Encoder1_Value = 0
        rightturn()
        stop()
        Encoder1_Value = 0
        step()
        stop()
        
        #move x steps then y steps
        movex(xx)
        Encoder1_Value = 0
        stop()
        Encoder1_Value = 0
        stop()
        movey(yy)
        
        
    elif (heading == 180) and (x!=3):       #obstacle in -ve y direction and not in the last right cell
    
        # step away from obstacle
        Encoder1_Value = 0
        lefttturn()
        stop()
        Encoder1_Value = 0
        step()
        stop()
        
        #move y steps then x steps
        movey(yy)
        Encoder1_Value = 0
        stop()
        Encoder1_Value = 0
        stop()
        movex(xx)
        
        
    elif (heading == 180) and (x==3):       #obstacle in -ve y direction and in the last right cell
    
        # step away from obstacle
        Encoder1_Value = 0
        rightturn()
        stop()
        Encoder1_Value = 0
        step()
        stop()
        
        #move y steps then x steps
        movey(yy)
        Encoder1_Value = 0
        stop()
        Encoder1_Value = 0
        stop()
        movex(xx)
        
        
    elif (heading == -90) and (y!=3):       #obstacle in -ve x direction and not in the last upper cell
    
        # step away from obstacle
        Encoder1_Value = 0
        rightturn()
        stop()
        Encoder1_Value = 0
        step()
        stop()
        
        #move x steps then y steps
        movex(xx)
        Encoder1_Value = 0
        stop()
        Encoder1_Value = 0
        stop()
        movey(yy)
        
        
    elif (heading == -90) and (y==3):       #obstacle in -ve x direction and in the last upper cell
    
        # step away from obstacle
        Encoder1_Value = 0
        leftturn()
        stop()
        Encoder1_Value = 0
        step()
        stop()
        
        #move x steps then y steps
        movex(xx) 
        Encoder1_Value = 0
        stop()
        Encoder1_Value = 0
        stop()
        movey(yy)
        
       
       
    if ( FirstStop_Flag == True ) and (SecondStage_Start == True ) :    # if stage one has been finished previously and stage two has been started now end the current stage two
        SecondStop_Flag = True
    else :                                                              # if stage one hasn't ended yet and stage two hasn't started yet end the current stage one
        FirstStop_Flag  = True
        SecondStop_Flag = False
   
def moveto (xx,yy):
#function to auto route to the given x and y positions 

    global FirstStop_Flag
    global SecondStop_Flag
    global Encoder1_Value
    
    if xx == 0:
    
        #move y steps then x steps
        movey(yy)
        Encoder1_Value = 0      
        stop()
        Encoder1_Value = 0
        if ObstacleRoutine_Started ==False : ### make sure that we didn't go to movenew
            movex(xx)
            
    else:
    
        #move y steps then x steps
        movey(yy)
        Encoder1_Value = 0
        stop()
        Encoder1_Value = 0
        if ObstacleRoutine_Started ==False : ### make sure that we didn't go to movenew
            movex(xx)
        
        
    if ObstacleRoutine_Started == False :                                  ### make sure that we didn't go to movenew
        if ( FirstStop_Flag == True ) and (SecondStage_Start == True ) :   # if stage one has been finished previously and stage two has been started now end the current stage two
            SecondStop_Flag = True                                         
        else :                                                             # if stage one hasn't ended yet and stage two hasn't started yet end the current stage one
            FirstStop_Flag  = True
            SecondStop_Flag = False
    else :
        stop()                                                             # if we passed movenew just stop

################################################################ 





#the code here will keep running forever in manual mode or until task end in auto mode
################################################################ 
while True :
    if mode == 'm' :                                                        #mode is manual
                                                                            
        while Command_Recieved == False :                                   ### no command waiting flag
                                                                            
            conn, addr = socket_object.accept()                             ###### establish new connection and recieve command
            data = conn.recv(1024)                                          
            data = str(data)                                                
            Command=data[2]                                                 ###### put command in command variable
            Encoder1_Value = 0                                              
            Command_Recieved = True                                         ###### set command recieved flag to true
                                                                            
        while Command_Recieved == True :                                    ### command recieved flag 
                                                                            
            if Command == 'F':                                              ###### command is forward
                                                                            
                if Encoder1_Value >1000 :                                   ######### check if step done
                    stop()                                                  ############ stop if step is done
                                                                            
                    Encoder1_Value = 0                                      ############ reset encoder value
                    Command = ''                                            ############ reset command
                                                                            
                    conn.close()                                            ############ close connection to start a new one in the following command                            
                    Command_Recieved = False                                ############ reset recieved command flag
                                                                            
                else:                                                       
                                                                            
                    forward()                                               ############ if step isn't done keep moving forward
                                                                            
                                                                            
                                                                            
            elif Command == 'L':                                            ###### command is left
                                                                            
                if Encoder1_Value > 300 :                                   ######### check if turn is done
                    stop()                                                  ############ stop if turn is done
                                                                            
                    Encoder1_Value = 0                                      ############ reset encoder value          
                    Command = ''                                            ############ reset command
                                                                            
                    Command_Recieved = False                                ############ reset recieved command flag
                    conn.close()                                            ############ close connection to start a new one in the following command
                else:                                                       
                    left()                                                  ############ if turn isn't done keep turning left
                                                                            
            elif Command == 'R':                                            ###### command is left                   
                                                                            
                                                                            
                if Encoder1_Value > 310 :                                   ######### check if turn is done
                    stop()                                                  ############ stop if turn is done
                                                                            
                    Encoder1_Value = 0                                      ############ reset encoder value
                    Command = ''                                            ############ reset command
                                                                            
                    Command_Recieved = False                                ############ reset recieved command flag
                    conn.close()                                            ############ close connection to start a new one in the following command
                else:                                                       
                    right()                                                 ############ if turn isn't done keep turning right
                                                                            
    else:                                                                   #mode is auto
        if (FirstStop_Flag == True) and (SecondStop_Flag == True) :         ### both of 2 stages are done stop and break
            break
        elif (FirstStop_Flag == False) and (SecondStop_Flag == False) :     ### first stage start move to first x and y positions then stop and grap the object
            moveto(x2,y2)
        elif (FirstStop_Flag == True) and (SecondStop_Flag == False) :      ### second stage recieve new x and y values and go there to park
            Encoder1_Value = 0                                              ###### reset encoder value
            ObstacleRoutine_Started = False                                 ###### reset obstacle routine flag
            SecondStage_Start = True                                        ###### raise second stage flag
            request = conn.recv(1024)                                       ###### recieve new x and y
            request = str(request)
            x2 = int(request[3])
            y2 = int(request[4])
            moveto(x2,y2)                                                   ###### move to new x and y
        

################################################################ 


