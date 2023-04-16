
# esp32-micropython-remotely-controlled-car-in-map

remotely operated car using esp32 microcontroller with micropython firmware and application connected over wifi to mobila app created using MIT app inventor. Car controlled using application and keeps tracking its position on the map given start position and encoders readings. Car has two control modes each has different features.

#### manual mode :
---
- control buttons (forward , left , right)
- voice commands 
-------

#### Automatic mode :
-------
- go to (x,y) position
- obstacles avoiding and rerouting  
## Acknowledgements
<a href="https://appinventor.mit.edu/">
<img src="https://community.appinventor.mit.edu/uploads/default/original/3X/7/c/7c8b59c5b1b374747bd042cc1a052ca161689272.png" /img width=80>
</a>
<a href="https://micropython.org/">
<img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Micropython-logo.svg" /img width=50>
</a>
 
## Manual mode 

in this mode we control car inside map using control buttons and voice command in mobile app
![manual](https://github.com/Mohammed-Rashad-Nasr/esp32-micropython-remotely-controlled-car-in-map/blob/main/manual.gif)

## Auto mode 

in this mode we control car inside map using (x,y) coordinates for the destination cell then car moves to that cell and avoids obstacles while moving then grips an object after that it accepts cell to go back and drop the object
![auto](https://github.com/Mohammed-Rashad-Nasr/esp32-micropython-remotely-controlled-car-in-map/blob/main/auto.gif)


## Map 

the map I used is simple occupancy grid and has limited (x,y) cells 


## auto mode algorithm 
the algorithm is very simple and based on functions and recursion only . 
- Car moves to (x,y) cell by moving forward or backward depending on current y position for number of steps = |y - current y position| then turns right or left depending on current x position and starts moving for number of steps = |x - current x position|

- if obstacle detected while executing the previous procedure execution moves to new function which decides where to move in order to avoid collosion . The highest priority is for moving to the right direction that means if all directions are possible Car will turn right and starts re-routing but in some conditions this will not be possible for example if it was in the last right cell then it has to move to the left direction 

- the function of re-routing uses the same function of moving from current position to given (x,y) so if it should go to the desired position again following the same steps but if it founds a new obstacle it will move again to the obstacle avoiding function and avoids it so here recursion will take place


