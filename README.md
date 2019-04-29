# Pi in the Sky Plan
Ben Lepsch and Jonah Newman

### Plan  

Date (by Mondays)

What we think we will do

What we did  

10/29  
Finish untested code


11/5  
Design the other half of the crossbow in solidworks


11/12  
Begin making the actual crossbow based on the design


11/17  
Continue making the actual crossbow


11/24  
Finish making the actual crossbow


12/1  
Begin testing code


12/8  
Continue testing code


12/15  
Finish code


12/22  
winter break, do nothing


12/29   
winter break, do nothing


1/7  
Extra week to catch up on things we didn’t expect


1/14   
Extra week to catch up on things we didn’t expect


1/21   
finished




### Goal  
For this project we will launch our raspberry pi into the air and have it determine when it's at the apex of its flight, then beep or something so we know it was correct.

The way we did this was writing the code so that as it's launched, it gathers acceleration data and uses a Riemann sum to approximate what time it will reach its apex.

### Ideas:  
Use a crossbow/slingshot hybrid thing to throw the pi up.
This also means we need an aerodynamic shell or something around the pi to protect it when it lands, since we won't be able to catch it.

### Resources:  
Crossbow  
Wood   
Exercise resistance band  
screws/nails  
CNC (maybe, for trigger mechanism)  
Pi  
Pi capsule (3d printed)  
3d printer  
Screws/nuts  
Laser cutter/acrylic  
Accelerometer   
battery  
Breadboard  
Wires  
Tape  
LED  

### CAD
CAD Design for raspberry pi shell:  
![Raspberry Pi Shell](/screenshott.png)  
The holes on the back are for indicator LEDs, a button to change stages, and a power switch.
We later modified the printed part by using a saw to cut a hole into the side so that we could plug the pi into the computer without having to take it out of the shell.


### Looking Back

We mostly stuck with our original ideas throughout this project. We used a crossbow/slingshot hybrid to launch the pi, a 3D-printed shell to protect it on landing, and a Riemann sum of the initial acceleration to predict the apex. We modified the 3D printed shell a few times by drilling out the hole for the button because it wouldn't fit initially, and by cutting out part of the side so we could plug cables into the Pi without removing it from the shell. We also didn't make a crossbow with a leaf spring, but instead used an exercise band to make more of a giant slingshot than a crossbow.

Because of the delay caused by these changes and the code taking MUCH longer to complete than we initially thought, we finished our Pi in the Sky project on March 6th, over a month later than we predicted.
