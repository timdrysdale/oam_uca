# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 16:02:01 2017

@author: td4343

Modified May 6 2019 from analyse_mode_scans_for_IET_tutorial.py

"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

from uca import mode_data_filename

def impose_noise_floor(mag,phase,floor):
    for xx,row in enumerate(mag):
        for yy,val in enumerate(row):
            if (val <= floor):
                phase[xx,yy]=np.random.rand(1)*np.pi
                mag[xx,yy] = floor
    return(mag,phase) 

       
def get_1d_data_uca(filename, mode_number):
    filename_npz = mode_data_filename(filename, mode_number)
    
    data = np.load(filename_npz)
    
    ok_types = ['line','circle','arc']
    geo = data['geometry']
    
    if not (geo in ok_types):
        print("Data from {} scan is not well represented in 1D".format(geo))
        return
    
    x_list = []
    
    if geo == 'arc':
        for pos in data['line_rx']:
            angle = np.arctan(pos[0]/pos[2]) #x/z
            x_list.append(angle)
        return np.array(x_list), data['lamps'], data['lphases']     
        
        
                
    
if __name__ == "__main__":
    
    from uca import *
    
    filename = 'test'
    
    config = {
            'filename': filename,
            'farfield':{
                    'type': 'arc'
            }
        }

    uca(config, debug=True)
    plt.figure()
    
    for mode_number in [0,1,2,3]:
        angle, amp, phase = get_1d_data_uca(filename, mode_number)
        plt.plot(angle,amp, label = mode_number)
    plt.legend()    
    plt.show()    
    
