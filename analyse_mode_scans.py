# -*- coding: utf-8 -*-
"""
Created on Fri May 20 08:20:33 2016

@author: tdd
"""

from TMAA import *
from n2ff import unwrap
from detect_peaks import detect_peaks

def chain(signal,mult):
    chain_signal = []
    for i in np.arange(mult):
        chain_signal = np.append(chain_signal,signal)
    return(chain_signal)
    
def zeropad(signal, size):
    pad_width = size - np.size(signal)
    if (pad_width > 0): 
        padded_signal = np.pad(signal, [0,pad_width], mode='constant')
    else:
        padded_signal = signal[0:size]   #hopefully user notices!
    return(padded_signal)
    


from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=False)

use_time_switching = True

#freq_list = np.linspace(4,6,3)*1e9
#distance_list = [2.16,1.66]
sample_frequency = 1e12
dt = 1/sample_frequency
dx = dt * const.c 
switch_frequency = 0.1e9

signal_size = samples_per_switch_period(sample_frequency, 
                                        switch_frequency)
frequency = 5e9; #loop later....
rel_period = relative_period(frequency,sample_frequency)
signal = sin_signal(rel_period,np.pi/8.,signal_size)

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
#rx_radius = 2
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
    xlist = np.linspace(-1.408/2.,1.408/2,33) #65
    ylist = np.linspace(-1.092/2.,1.092/2.,29) #56
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
plt.savefig('UCA8-%s-3D.pdf'%(scan_type), bbox_inches='tight', pad_inches=0)   
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


rx_signals_noswitch = np.zeros((int(num_rx),int(num_ant),int(signal_size)))
rx_count = -1

print("Signals")

for rx in line_rx:
    rx_count = rx_count + 1
    ant_count = -1
    
    print(("%f"%(float(rx_count)/float(num_rx))))
    for ant in array:
        ant_count = ant_count + 1
        distance = abs(rx-ant.pos)
        masked_signal = heavyside(0,1, signal)    
        offset_signal = apply_offset(distance, sample_frequency, masked_signal) 
             
        trim =  np.size(offset_signal) - np.size(rx_signals[rx_count, ant_count,:])     #hack for length change, fencepost error somewherE?      
        rx_signals_noswitch[rx_count,ant_count,:] = (
            rx_signals_noswitch[rx_count, ant_count,:] + 
            (offset_signal[trim:] / distance**2)) 



plt.figure()


rx_num = 6
ant_num = 0

fft_size = 2**22
mult = int(np.floor(fft_size / np.size(rx_signals[0,0,:])))

freq = np.fft.fftshift(np.fft.fftfreq(fft_size, 1/sample_frequency))
window = np.hamming(fft_size)

signal_noswitch = zeropad(chain(rx_signals_noswitch[rx_num,ant_num,:], mult),fft_size) * window

signal_switch   = zeropad(chain(rx_signals[rx_num,ant_num,:],   mult),fft_size) * window

example_noswitch_fft = np.fft.fftshift(np.abs(np.fft.fft(signal_noswitch, fft_size)))
example_switch_fft   = np.fft.fftshift(np.abs(np.fft.fft(signal_switch,   fft_size)))

example_amp_noswitch = 20 * np.log10(example_noswitch_fft)
example_amp_switch = 20 * np.log10(example_switch_fft)

plt.plot(freq, example_amp_noswitch, label = 'no switching')
plt.plot(freq, example_amp_switch, label = 'switching')
    
                               
plt.xlim([0.8e9,1.2e9])                                
plt.ylim([0, 100])

fig.show()   


rx_num = 36
voff = 0.25
for ant_num in np.arange(num_ant):
    plt.plot(rx_signals[rx_num,ant_num,:] + ant_num * voff,label='%d'%ant_num)
#plt.legend(ncol = 4, loc = 'lower right')
#plt.ylim([-0.8,2.0])
plt.show()



rx_num = 6

fft_size = 2**22
mult = int(np.floor(fft_size / np.size(rx_signals[0,0,:])))

freq = np.fft.fftshift(np.fft.fftfreq(fft_size, 1/sample_frequency))
window = np.hamming(fft_size)

one_period_noswitch = np.sum(rx_signals_noswitch[rx_num,:,:], axis = 0)
one_period_switch   = np.sum(rx_signals[rx_num,:,:],          axis = 0)

signal_noswitch = zeropad(chain(one_period_noswitch, mult),fft_size) * window

signal_switch   = zeropad(chain(one_period_switch,   mult),fft_size) * window

example_noswitch_fft = np.fft.fftshift(np.abs(np.fft.fft(signal_noswitch, fft_size)))
example_switch_fft   = np.fft.fftshift(np.abs(np.fft.fft(signal_switch,   fft_size)))

example_amp_noswitch = 20 * np.log10(example_noswitch_fft)
example_amp_switch = 20 * np.log10(example_switch_fft)


plt.figure()
plt.plot(one_period_noswitch, label = 'no switch')
plt.plot(one_period_switch, label = 'switch')
plt.legend()
plt.show()


plt.figure()
plt.plot(freq, example_amp_noswitch, label = 'no switching')
plt.plot(freq, example_amp_switch, label = 'switching')
                              
plt.xlim([4.65e9,5.35e9])                                
plt.ylim([0, 100])

fig.show()   


rx_num = 6
plt.figure(figsize=(8,5))
fstart = 0.93e9
fstop  = 1.07e9
fstart_index = np.max(np.where(fstart > freq))
fstop_index  = np.max(np.where(fstop > freq))
max_signal = np.max(example_noswitch_fft[fstart_index:fstop_index])
example_amp_noswitch = np.clip(20 * np.log10(example_noswitch_fft[fstart_index:fstop_index]/max_signal),-41,0)
example_amp_switch = np.clip(20 * np.log10(example_switch_fft[fstart_index:fstop_index]/max_signal),-41,0)

noswitch_peaks = detect_peaks(example_amp_noswitch)
switch_peaks = detect_peaks(example_amp_switch)

fz = freq[fstart_index:fstop_index]/1e9

plt.plot(fz, example_amp_noswitch, 'k:', label = 'no switching')
plt.plot(fz, example_amp_switch, 'k-',label = 'switching')
plt.plot(fz[noswitch_peaks], example_amp_noswitch[noswitch_peaks],'ks')                              

labels = ['$l$=-3','$l$=-2','$l$=-1','$l$=0','$l$=1','$l$=2','$l$=3']
for (pk, lbl) in zip(switch_peaks,labels):
    plt.plot(fz[pk], example_amp_switch[pk],'ko')
    plt.annotate(lbl,
                 xy = (fz[pk], example_amp_switch[pk]),
                 xytext = (-20,20), 
                 textcoords = 'offset points', ha = 'right', va = 'bottom',
                 bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
                 arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))                              
                 
plt.xlim([0.92,1.08])                                
plt.ylim([-40, 1])
plt.savefig('UCA8_switch_fft.pdf',bbox_inches='tight', pad_inches=0) 
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


fft_size = 2**20
mult = int(np.floor(fft_size / np.size(rx_signals[0,0,:])))

freq = np.fft.fftshift(np.fft.fftfreq(fft_size, 1/sample_frequency))
window = np.hamming(fft_size)

#trial run to find peaks, assume in same place in rest of data (can sanity 
#by looking at amplitude data)
rx_num = 0

one_period_switch   = np.sum(rx_signals[rx_num,:,:],          axis = 0)   
signal_switch   = zeropad(chain(one_period_switch,   mult),fft_size) * window
switch_fft   = np.fft.fftshift(np.abs(np.fft.fft(signal_switch,   fft_size)))

fstart = 4.65e9
fstop  = 5.35e9
fstart_index = np.max(np.where(fstart > freq))
fstop_index  = np.max(np.where(fstop > freq))

freq_zoom = freq[fstart_index:fstop_index] 
switch_fft_zoom =switch_fft[fstart_index:fstop_index]   
#threshold the data
switch_fft_zoom_amp = 20 * np.log10(switch_fft_zoom)
max_val = np.max(switch_fft_zoom_amp)
threshold = 30
min_val = max_val - threshold
switch_fft_zoom_amp = np.clip(20 * np.log10(switch_fft_zoom), min_val, max_val)

#find peaks
peak = detect_peaks(switch_fft_zoom_amp, show=False)
plt.figure()
plt.plot(freq_zoom, switch_fft_zoom_amp)
plt.plot(freq_zoom[peak],switch_fft_zoom_amp[peak], 'r+')
plt.xlim([fstart,fstop])
plt.show() 

#this gives us seven peaks
#peak = peak_zoom + fstart_index
print("Farfields"  )  
for rx_num in np.arange(num_rx):
    '''
    one_period_switch   = np.sum(rx_signals[rx_num,:,:],          axis = 0)   
    signal_switch   = zeropad(chain(one_period_switch,   mult),fft_size) * window
    switch_fft   = np.fft.fftshift(np.abs(np.fft.fft(signal_switch,   fft_size)))
    switch_amp = 20 * np.log10(switch_fft)
    switch_phase = np.angle(switch_fft)
    '''
    #save some memory by not having intermediate variables? 
      
    print(("%f"%(float(rx_num)/float(num_rx))))
    fft = np.fft.fftshift(
        np.fft.fft(
            zeropad(
                chain(
                    np.sum(rx_signals[rx_num,:,:],axis = 0),
                mult),
            fft_size) * 
        window,fft_size))    
    
    switch_phase = np.angle(fft[fstart_index:fstop_index])             
    switch_amp = 20 * np.log10(fft[fstart_index:fstop_index])  
    
    lphases0 = np.append(lphases0, switch_phase[peak[0]])
    lamps0 = np.append(lamps0, switch_amp[peak[0]])

    lphases1 = np.append(lphases1, switch_phase[peak[1]])
    lamps1 = np.append(lamps1, switch_amp[peak[1]])

    lphases2 = np.append(lphases2, switch_phase[peak[2]])
    lamps2 = np.append(lamps2, switch_amp[peak[2]])

    lphases3 = np.append(lphases3, switch_phase[peak[3]])
    lamps3 = np.append(lamps3, switch_amp[peak[3]])

    lphases4 = np.append(lphases4, switch_phase[peak[4]])
    lamps4 = np.append(lamps4, switch_amp[peak[4]])

    lphases5 = np.append(lphases5, switch_phase[peak[5]])
    lamps5 = np.append(lamps5, switch_amp[peak[5]])

    lphases6 = np.append(lphases6, switch_phase[peak[6]])
    lamps6 = np.append(lamps6, switch_amp[peak[6]])
      
'''
plt.figure()
plt.plot(lphases0)
plt.plot(lphases1 + 5)
plt.plot(lphases2 + 10)
plt.plot(lphases3 + 15)
plt.plot(lphases4 + 20)
plt.plot(lphases5 + 25)
plt.plot(lphases6 + 30)
plt.show()

plt.figure(figsize=(8,8))


plt.plot(xlist,lamps2,'k-', label='0.98 GHz')
plt.plot(xlist,lamps4,'k-', label='1.02 GHz')

plt.plot(xlist,lamps1,'k:' , label='0.96 GHz')
plt.plot(xlist,lamps5,'k:' , label='1.04 GHz')

plt.plot(xlist,lamps0,'k-.', label='0.94 GHz')
plt.plot(xlist,lamps6,'k-.', label='1.06 GHz')

plt.plot(xlist,lamps3,'k--' , label='1.00 GHz')


plt.xlabel('x (m)')
plt.ylabel('transmitted power (arb dB)')
plt.legend(ncol=4, loc = 'lower center')
plt.ylim([25,103])
plt.savefig('UCA8-%s-powerdB.pdf'%(scan_type), bbox_inches='tight', pad_inches=0)  
plt.show()


fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection='3d')
for ant in array:
            
    plt.plot([ant.pos.x], [ant.pos.y], [ant.pos.z], 'r*')
'''
   
