# -*- coding: utf-8 -*-
"""
Created on Fri May 20 08:20:33 2016

@author: tdd
"""

from TMAA import *
from n2ff import unwrap
   

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=False)

frequency = 5e9; 
k = 2. * np. pi * frequency / 3e8

num_ant = 8.
zero_z = 0

array_radius = 0.09 #9 cm radius, 18cm diameter

array = list()
phi_list= (np.linspace(0,1,num_ant+1)*2. * np.pi)[:-1] 
start_list = np.arange(num_ant) / num_ant
stop_list =  (np.arange(num_ant) + 1.) / num_ant
for (phi, start, stop) in zip(phi_list, start_list, stop_list):    
    
    pos = vec3()
    pos.set_cylindrical(array_radius,phi,zero_z)
    array.append(Antenna(pos,start,stop))

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection='3d')
for ant in array:
   plt.plot([ant.pos.x], [ant.pos.y], [ant.pos.z], 'r*')

   
rx_z = 2.16

scan_type = 'rect'
line_rx = list() 

if (scan_type == 'line'):
    num_rx = 121
    xlist = np.linspace(-2,2,num_rx)
    for x in xlist:
        pos = vec3(x,0,rx_z)        
        line_rx.append(pos)

elif (scan_type == 'circle'):
    num_rx = 72
    phi_list= (np.linspace(0,1,num_rx+1)*2. * np.pi)[:-1]
    for phi in phi_list:    
        pos = vec3()
        pos.set_cylindrical(rx_radius,phi,rx_z)
        line_rx.append(pos)    
        
elif (scan_type == 'rect'):
    num_rx = 0
    ylist = np.linspace(-1.408/2.,1.408/2,33) #65
    xlist = np.linspace(-1.092/2.,1.092/2.,29) #56
    for x in xlist:
        for y in ylist:
            pos = vec3(x,y,rx_z)        
            line_rx.append(pos)
            num_rx = num_rx + 1


for rx in line_rx:
    plt.plot([rx.x], [rx.y], [rx.z], 'b+')
    
# Comment or uncomment following both lines to test the fake bounding box:
Xb = np.array([-1,1,-1,1,-1,1,-1,1])*2
Yb = np.array([-1,-1,1,1,-1,-1,1,1])*2
Zb = (np.array([-1,-1,-1,-1,1,1,1,1]) + 1)/2
for xb, yb, zb in zip(Xb, Yb, Zb):
   ax.plot([xb], [yb], [zb], 'w')

ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_zlabel('z (m)')

ax.dist = 10
plt.savefig('iet-%s-3D.pdf'%(scan_type), bbox_inches='tight', pad_inches=0)   
plt.show()


plt.figure()
lphases0 = []
lphases1 = []
lphases2 = []
lphases3 = []
lphases4 = []
lphases5 = []
lphases6 = []

lamps0 = []
lamps1 = []
lamps2 = []
lamps3 = []
lamps4 = []
lamps5 = []
lamps6 = []

tx0 = np.array([0,1,2,3,4,5,6,7],dtype='float') * 2 * np.pi * -3. / 8.
tx1 = np.array([0,1,2,3,4,5,6,7],dtype='float') * 2 * np.pi * -2. / 8.
tx2 = np.array([0,1,2,3,4,5,6,7],dtype='float') * 2 * np.pi * -1. / 8.
tx3 = np.array([0,1,2,3,4,5,6,7],dtype='float') * 2 * np.pi * 0. / 8.
tx4 = np.array([0,1,2,3,4,5,6,7],dtype='float') * 2 * np.pi * 1. / 8.
tx5 = np.array([0,1,2,3,4,5,6,7],dtype='float') * 2 * np.pi * 2. / 8.
tx6 = np.array([0,1,2,3,4,5,6,7],dtype='float') * 2 * np.pi * 3. / 8.



print("Farfields"  )  
count = 0.0 
for rx in line_rx:
    print(("%d %d %f"%(float(count) / float(num_rx), count, np.size(lamps0))))
    count = count + 1.0
    ff = 0
    
    for tx, dphi in zip(array,tx0):
        r = rx.distanceTo(tx.pos)
        ff = ff + np.exp(1j * ( k * r + dphi )) / (4. * np.pi * r)
    
    lphases0 = np.append(lphases0, np.angle(ff))
    lamps0 = np.append(lamps0,np.abs(ff))    

    ff = 0
    for tx, dphi in zip(array,tx1):
        r = rx.distanceTo(tx.pos)
        ff = ff + np.exp(1j * ( k * r + dphi )) / (4. * np.pi * r)
    
    lphases1 = np.append(lphases1, np.angle(ff))
    lamps1 = np.append(lamps1,np.abs(ff))    
    
    ff = 0
    for tx, dphi in zip(array,tx2):
        r = rx.distanceTo(tx.pos)
        ff = ff + np.exp(1j * ( k * r + dphi )) / (4. * np.pi * r)
    
    lphases2 = np.append(lphases2, np.angle(ff))
    lamps2 = np.append(lamps2,np.abs(ff))    
    
    ff = 0
    for tx, dphi in zip(array,tx3):
        r = rx.distanceTo(tx.pos)
        ff = ff + np.exp(1j * ( k * r + dphi )) / (4. * np.pi * r)
    
   
    lphases3 = np.append(lphases3, np.angle(ff))
    lamps3 = np.append(lamps3,np.abs(ff))       
  
    ff = 0
    for tx, dphi in zip(array,tx4):
        r = rx.distanceTo(tx.pos)
        ff = ff + np.exp(1j * ( k * r + dphi )) / (4. * np.pi * r)
    

    lphases4 = np.append(lphases4, np.angle(ff))
    lamps4 = np.append(lamps4,np.abs(ff))  
    
    ff = 0
    for tx, dphi in zip(array,tx5):
        r = rx.distanceTo(tx.pos)
        ff = ff + np.exp(1j * ( k * r + dphi )) / (4. * np.pi * r)
    
    lphases5 = np.append(lphases5, np.angle(ff))
    lamps5 = np.append(lamps5,np.abs(ff))        

    ff = 0
    for tx, dphi in zip(array,tx6):
        r = rx.distanceTo(tx.pos)
        ff = ff + np.exp(1j * ( k * r + dphi )) / (4. * np.pi * r)
    
    lphases6 = np.append(lphases6, np.angle(ff))
    lamps6 = np.append(lamps6,np.abs(ff))  


np.savez('33by295GHz_IET.npz',
         lamps0=lamps0,
         lamps1=lamps1,
         lamps2=lamps2,
         lamps3=lamps3,
         lamps4=lamps4,
         lamps5=lamps5,
         lamps6=lamps6,
         lphases0=lphases0,
         lphases1=lphases1,
         lphases2=lphases2,
         lphases3=lphases3,
         lphases4=lphases4,
         lphases5=lphases5,
         lphases6=lphases6,
         xlist=xlist,
         ylist=ylist,
         rx_z=rx_z)