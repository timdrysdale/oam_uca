# -*- coding: utf-8 -*-
"""
Created on Fri May 20 08:20:33 2016

@author: tdd
"""

from TMAA import *


use_time_switching = True

freq_list = np.linspace(1,3,3)*1e9
distance_list = [2.6,2.75,2.9]
sample_frequency = 1e12
dt = 1/sample_frequency
dx = dt * const.c 
switch_frequency = 0.02e9

signal_size = samples_per_switch_period(sample_frequency, 
                                        switch_frequency)
frequency = freq_list[0] #loop later....
rel_period = relative_period(frequency,sample_frequency)
signal = sin_signal(rel_period,np.pi/8.,signal_size)

num_ant = 8.
zero_z = 0
array_radius = 0.5 * const.c / np.min(freq_list)
array = list()
phi_list= (np.linspace(0,1,num_ant+1)*2. * np.pi)[:-1]
start_list = np.arange(num_ant) / num_ant
stop_list =  (np.arange(num_ant) + 1.) / num_ant
for (phi, start, stop) in zip(phi_list, start_list, stop_list):    
    
    pos = vec3()
    pos.set_cylindrical(array_radius,phi,zero_z)
    array.append(Antenna(pos,start,stop))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for ant in array:
            
    plt.plot([ant.pos.x], [ant.pos.y], [ant.pos.z], 'r*')

   
rx_z = 0.7
rx_radius = 2
do_line_rx = True
line_rx = list() 
if (do_line_rx == True):
    num_rx = 72
    xlist = np.linspace(-1,1,num_rx)
    for x in xlist:
        pos = vec3(x,0,rx_z)        
        line_rx.append(pos)
else:
    num_rx = 36
    phi_list= (np.linspace(0,1,num_rx+1)*2. * np.pi)[:-1]
    for phi in phi_list:    
        pos = vec3()
        pos.set_cylindrical(rx_radius,phi,rx_z)
        line_rx.append(pos)    



for rx in line_rx:
    plt.plot([rx.x], [rx.y], [rx.z], 'b+')
    
# Comment or uncomment following both lines to test the fake bounding box:
Xb = np.array([-1,1,-1,1,-1,1,-1,1])
Yb = np.array([-1,-1,1,1,-1,-1,1,1])
Zb = (np.array([-1,-1,-1,-1,1,1,1,1]) + 1)/2
for xb, yb, zb in zip(Xb, Yb, Zb):
   ax.plot([xb], [yb], [zb], 'w')        
    
plt.show()

rx_signals = np.zeros((int(num_rx),int(num_ant),int(signal_size)))
rx_count = -1
for rx in line_rx:
    rx_count = rx_count + 1
    ant_count = -1
    for ant in array:
        ant_count = ant_count + 1
        distance = abs(rx-ant.pos)
        if (use_time_switching == True):
            masked_signal = heavyside(ant.start,ant.stop, signal)
        else:
            masked_signal = heavyside(0,1, signal)    
        offset_signal = apply_offset(distance, sample_frequency, masked_signal) 
             
        trim =  np.size(offset_signal) - np.size(rx_signals[rx_count, ant_count,:])     #hack for length change, fencepost error somewherE?      
        rx_signals[rx_count,ant_count,:] = (
            rx_signals[rx_count, ant_count,:] + 
            (offset_signal[trim:] / distance**2)) 
'''
plt.figure()
for rx_num in np.arange(num_rx):            
        plt.plot(np.sum(rx_signals[rx_num,:,:] + rx_num, axis = 0))                    
plt.show()
'''

'''
rx_num = 6    
         
plt.figure()

for ant_num in np.arange(num_ant):
    plt.plot(rx_signals[rx_num,ant_num,:] + ant_num)


fig.show()    
plt.figure()
'''
rx_num = 6
#for ant_num in np.arange(num_ant):
ant_num = 0

plt.plot(np.fft.fftshift(np.fft.fftfreq(2**19, 1/sample_frequency)),
                            20 * np.log10(np.fft.fftshift(np.abs(np.fft.fft(rx_signals[rx_num,ant_num,:],2**19)))))
plt.xlim([0,2e9])                                

fig.show()   

plt.figure()
phases0 = []
phases1 = []
phases2 = []
phases3 = []

amps0 = []
amps1 = []
amps2 = []
amps3 = []

for rx_num in np.arange(num_rx):
    fft_f = np.fft.fftshift(np.fft.fftfreq(2**19, 1/sample_frequency))
    fft_p = (np.fft.fftshift(np.angle(np.fft.fft(np.sum(rx_signals[rx_num,:,:], axis = 0),2**19))))
    fft_a = (20 * np.log10(np.fft.fftshift(np.abs(np.fft.fft(np.sum(rx_signals[rx_num,:,:], axis = 0),2**19)))))
    #plt.plot(fft_f, fft_p)
    #plt.xlim([0.94e9,1.06e9]) 
    jj = np.min(np.where(fft_f >= 1e9))                               
    phases0 = np.append(phases0, fft_p[jj])
    amps0 = np.append(amps0, fft_a[jj])
    
    jj = np.min(np.where(fft_f >= 0.98e9))                               
    phases1 = np.append(phases1, fft_p[jj])
    amps1 = np.append(amps1, fft_a[jj])

    jj = np.min(np.where(fft_f >= 0.96e9))                               
    phases2 = np.append(phases2, fft_p[jj])  
    amps2 = np.append(amps2, fft_a[jj])

    jj = np.min(np.where(fft_f >= 0.94e9))                               
    phases3 = np.append(phases3, fft_p[jj])
    amps3 = np.append(amps3, fft_a[jj])
    
fig.show()   

   
plt.figure()
plt.plot(phases0)
plt.plot(phases1 + 5)
plt.plot(phases2 + 10)
plt.plot(phases3 + 15)
plt.show()

plt.figure()
plt.plot(amps0)
plt.plot(amps1 )
plt.plot(amps2 )
plt.plot(amps3 )
plt.show()
'''
plt.figure()
plt.plot(np.sum(np.sum(rx_signals**2, axis = 2), axis = 1))    
 
plt.show()     
'''

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for ant in array:
            
    plt.plot([ant.pos.x], [ant.pos.y], [ant.pos.z], 'r*')

   
rx_z = 0.7
rx_radius = 2
do_line_rx = False
line_rx = list() 
if (do_line_rx == True):
    num_rx = 72
    xlist = np.linspace(-1,1,num_rx)
    for x in xlist:
        pos = vec3(x,0,rx_z)        
        line_rx.append(pos)
else:
    num_rx = 36
    phi_list= (np.linspace(0,1,num_rx+1)*2. * np.pi)[:-1]
    for phi in phi_list:    
        pos = vec3()
        pos.set_cylindrical(rx_radius,phi,rx_z)
        line_rx.append(pos)    



for rx in line_rx:
    plt.plot([rx.x], [rx.y], [rx.z], 'b+')
    
# Comment or uncomment following both lines to test the fake bounding box:
Xb = np.array([-1,1,-1,1,-1,1,-1,1])
Yb = np.array([-1,-1,1,1,-1,-1,1,1])
Zb = (np.array([-1,-1,-1,-1,1,1,1,1]) + 1)/2
for xb, yb, zb in zip(Xb, Yb, Zb):
   ax.plot([xb], [yb], [zb], 'w')        
    
plt.show()

rx_signals = np.zeros((int(num_rx),int(num_ant),int(signal_size)))
rx_count = -1
for rx in line_rx:
    rx_count = rx_count + 1
    ant_count = -1
    for ant in array:
        ant_count = ant_count + 1
        distance = abs(rx-ant.pos)
        if (use_time_switching == True):
            masked_signal = heavyside(ant.start,ant.stop, signal)
        else:
            masked_signal = heavyside(0,1, signal)    
        offset_signal = apply_offset(distance, sample_frequency, masked_signal) 
             
        trim =  np.size(offset_signal) - np.size(rx_signals[rx_count, ant_count,:])     #hack for length change, fencepost error somewherE?      
        rx_signals[rx_count,ant_count,:] = (
            rx_signals[rx_count, ant_count,:] + 
            (offset_signal[trim:] / distance**2)) 
'''

'''
rx_num = 6
#for ant_num in np.arange(num_ant):
ant_num = 0

plt.plot(np.fft.fftshift(np.fft.fftfreq(2**19, 1/sample_frequency)),
                            20 * np.log10(np.fft.fftshift(np.abs(np.fft.fft(rx_signals[rx_num,ant_num,:],2**19)))))
plt.xlim([0,2e9])                                

fig.show()   

plt.figure()
phases0 = []
phases1 = []
phases2 = []
phases3 = []

amps0 = []
amps1 = []
amps2 = []
amps3 = []

for rx_num in np.arange(num_rx):
    fft_f = np.fft.fftshift(np.fft.fftfreq(2**19, 1/sample_frequency))
    fft_p = (np.fft.fftshift(np.angle(np.fft.fft(np.sum(rx_signals[rx_num,:,:], axis = 0),2**19))))
    fft_a = (20 * np.log10(np.fft.fftshift(np.abs(np.fft.fft(np.sum(rx_signals[rx_num,:,:], axis = 0),2**19)))))
    #plt.plot(fft_f, fft_p)
    #plt.xlim([0.94e9,1.06e9]) 
    jj = np.min(np.where(fft_f >= 1e9))                               
    phases0 = np.append(phases0, fft_p[jj])
    amps0 = np.append(amps0, fft_a[jj])
    
    jj = np.min(np.where(fft_f >= 0.98e9))                               
    phases1 = np.append(phases1, fft_p[jj])
    amps1 = np.append(amps1, fft_a[jj])

    jj = np.min(np.where(fft_f >= 0.96e9))                               
    phases2 = np.append(phases2, fft_p[jj])  
    amps2 = np.append(amps2, fft_a[jj])

    jj = np.min(np.where(fft_f >= 0.94e9))                               
    phases3 = np.append(phases3, fft_p[jj])
    amps3 = np.append(amps3, fft_a[jj])
    
fig.show()   

   
plt.figure()
plt.plot(phases0)
plt.plot(phases1 + 5)
plt.plot(phases2 + 10)
plt.plot(phases3 + 15)
plt.show()

plt.figure()
plt.plot(amps0)
plt.plot(amps1 )
plt.plot(amps2 )
plt.plot(amps3 )
plt.show()
'''
plt.figure()
plt.plot(np.sum(np.sum(rx_signals**2, axis = 2), axis = 1))    
 
plt.show()     
'''