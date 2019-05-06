# -*- coding: utf-8 -*-
"""
Created on Fri May 20 08:20:33 2016

@author: tdd

Modified from analyse_mode_scans_for_IET_tutorial on May 6 2019 by Tim Drysdale
"""

import collections
from TMAA import *
from n2ff import unwrap
import numpy as np   
import matplotlib.pyplot as plt

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=False)


def mode_symbol(mode_number):
    if mode_number < 0:
        mode_symbol = 'm'
    elif mode_number >0:
        mode_symbol = 'p'
    else:
        mode_symbol = ''
        
    return mode_symbol   

def mode_data_filename(filename, mode_number):
    return "{}_mode_{}{}.npz".format(filename, 
            mode_symbol(mode_number), 
            abs(mode_number))
    
def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def uca(config, debug = False, verbose = False):
    
    default = {
        "filename": 'example',
        "frequency":5e9,
        "transmitter":{
            "antenna_count": 8,    
            "radius_m": 0.09,
            "modes":[-3,-2,-1,0,1,2,3],
            },
        "farfield":{
            "type":"line",
            "geometry":{
                "arc":{
                    "distance_m": 2.16,
                    "sample_count": 49,
                    "start_rad":0,
                    "stop_rad": np.pi/2,
                    "bounding_box":{
                            "x_m": 2,
                            "y_m": 2,
                            "z_m": 2
                            }
                    },
                "line":{
                    "distance_m": 2.16,
                    "sample_count": 49,
                    "start_m": -2,
                    "stop_m":2,
                    "bounding_box":{
                            "x_m": 2,
                            "y_m": 2,
                            "z_m": 2
                            }
                    },
                "rect":{
                    "distance_m": 2.16, 
                    "sample_count": 121,
                    "x":{
                            "start_m":-1.092/2.,
                            "stop_m":1.092/2.,
                            "count":7
                        },
                    "y":{
                            "start_m":-1.408/2.,
                            "stop_m":1.408/2.,
                            "count":7
                        },
                    "bounding_box":{
                            "x_m": 2,
                            "y_m": 2,
                            "z_m": 2
                            }
                },
                "circle":{
                    "distance_m": 2.16,
                    "sample_count": 49,
                    "radius_m": 0.5,
                    "bounding_box":{
                            "x_m": 2,
                            "y_m": 2,
                            "z_m": 2
                            }
                }
                    
                                               
            }
            
        }                                    
    }
    
    config = update(default, config)    
    
    if debug:
        print("{}".format(config))    

    #-----------Calculate transmitter antenna positions-----------------------#  
    if debug:
        print("{}".format(config))
    array_radius = config['transmitter']['radius_m']
    frequency = config['frequency']
    num_ant = config['transmitter']['antenna_count']
    
       
    k = 2. * np. pi * frequency / 3e8
    zero_z = 0
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
       
    #-----------Calculate farfield sampling positions-------------------------#
    scan_type = config['farfield']['type']
    
    geo = config['farfield']['geometry'][scan_type]
    
    line_rx = list() 
    rx_z = geo['distance_m']
    num_rx = geo['sample_count']
       
    if (scan_type == 'line'):

        xlist = np.linspace(geo['start_m'],geo['stop_m'],num_rx)
        for x in xlist:
            pos = vec3(x,0,rx_z)        
            line_rx.append(pos)
    
    elif (scan_type == 'circle'):
        
        phi_list= (np.linspace(0,1,num_rx+1)*2. * np.pi)[:-1]
        for phi in phi_list:    
            pos = vec3()
            pos.set_cylindrical(geo['radius_m'],phi,rx_z)
            line_rx.append(pos)   
            
    elif (scan_type == 'arc'):
        
        theta_list= np.linspace(geo['start_rad'],geo['stop_rad'],num_rx)
        for theta in theta_list:    
            pos = vec3(np.sin(theta) * rx_z,
                       0,
                       np.cos(theta) * rx_z)
            line_rx.append(pos)               
            
            
    elif (scan_type == 'rect'):
        
        num_rx = 0
        
        ylist = np.linspace(geo['y']['start_m'], 
                            geo['y']['stop_m'], 
                            geo['y']['count'])
        
        xlist = np.linspace(geo['x']['start_m'], 
                            geo['x']['stop_m'], 
                            geo['x']['count'])
        
        for x in xlist:
            for y in ylist:
                pos = vec3(x,y,rx_z)        
                line_rx.append(pos)
                num_rx = num_rx + 1
    
    
    for rx in line_rx:
        plt.plot([rx.x], [rx.y], [rx.z], 'b+')
        
    # Comment or uncomment following both lines to test the fake bounding box:
    Xb = np.array([-1,1,-1,1,-1,1,-1,1])* geo['bounding_box']['x_m']
    Yb = np.array([-1,-1,1,1,-1,-1,1,1])*  geo['bounding_box']['y_m']
    Zb = np.array([0,0,0,0,1,1,1,1]) * geo['bounding_box']['z_m']
    for xb, yb, zb in zip(Xb, Yb, Zb):
       ax.plot([xb], [yb], [zb], 'w')
    
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_zlabel('z (m)')
    
    ax.dist = 10
    plt.savefig('{}_{}_geometry.pdf'.format(config['filename'],scan_type), bbox_inches='tight', pad_inches=0)   
    plt.show()
    plt.close()
    
    
    #----------------- Calculate Far Field------------------------------------#
    
    plt.figure()


    # calculate the phase offset to apply to each transmitter    
    for mode_number in config['transmitter']['modes']:
        
        if debug:
            print("Mode {}".format(mode_number))
            
        lphases0 = []
        lamps0 = []
        tx0 = np.array([0,1,2,3,4,5,6,7],dtype='float') * 2 * np.pi * mode_number / num_ant
       
        count = 0.0 
        for rx in line_rx:
            if debug and verbose:
                print(("%d %d %f"%(float(count) / float(num_rx), count, np.size(lamps0))))
                
            count = count + 1.0
            ff = 0
            
            for tx, dphi in zip(array,tx0):
                r = rx.distanceTo(tx.pos)
                ff = ff + np.exp(1j * ( k * r + dphi )) / (4. * np.pi * r)
            
            lphases0 = np.append(lphases0, np.angle(ff))
            lamps0 = np.append(lamps0,np.abs(ff))    
        
            
        filename = mode_data_filename(config['filename'], mode_number)
            
        np.savez(filename,
                 lamps = lamps0,
                 lphases = lphases0,
                 line_rx = line_rx)
        
if __name__ == "__main__":
    
    for geometry in ['arc','line','rect','circle']:
    
        config = {
                'filename': 'test',
                'farfield':{
                        'type': geometry
                }
            }

        uca(config, debug=True)


            