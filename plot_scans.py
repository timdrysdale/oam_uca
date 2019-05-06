# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 16:02:01 2017

@author: td4343
"""


def impose_noise_floor(mag,phase,floor):
    for xx,row in enumerate(mag):
        for yy,val in enumerate(row):
            if (val <= floor):
                phase[xx,yy]=np.random.rand(1)*np.pi
                mag[xx,yy] = floor
    return(mag,phase) 

'''
This is a bit harsh on the noise
def impose_noise_floor(mag,phase,floor):
    comp = 10**(mag/20) * np.exp(1j * phase/180.*np.pi) 
    (m,n) = np.shape(mag)
    noise_phase = np.random.rand(m,n) * np.pi
    noise = 10**(floor/20) * np.exp(1j * noise_phase)
    new_mag = 20 * np.log10(np.abs(comp + noise))
    new_phase = np.angle(comp + noise)
    return(new_mag,new_phase)
'''   

          

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

scan = np.load('33by295GHz_IET.npz')

lamps0 = scan["lamps0"]
lamps1 = scan["lamps1"]
lamps2 = scan["lamps2"]
lamps3 = scan["lamps3"]
lamps4 = scan["lamps4"]
lamps5 = scan["lamps5"]
lamps6 = scan["lamps6"]
lphases0 = scan["lphases0"]
lphases1 = scan["lphases1"]
lphases2 = scan["lphases2"]
lphases3 = scan["lphases3"]
lphases4 = scan["lphases4"]
lphases5 = scan["lphases5"]
lphases6 = scan["lphases6"]

[xx,yy] = np.meshgrid(scan["xlist"],scan["ylist"])
  


mode0p = ndimage.rotate(np.reshape(np.abs(lphases3),(33,29)),90)
modep1p = ndimage.rotate(np.reshape(np.abs(lphases4),(33,29)),90)
modep2p = ndimage.rotate(np.reshape(np.abs(lphases5),(33,29)),90)
modep3p = ndimage.rotate(np.reshape(np.abs(lphases6),(33,29)),90)
modem1p = ndimage.rotate(np.reshape(np.abs(lphases2),(33,29)),90)
modem2p = ndimage.rotate(np.reshape(np.abs(lphases1),(33,29)),90)
modem3p = ndimage.rotate(np.reshape(np.abs(lphases0),(33,29)),90)

'''
#modifies the noise in place
(modem3m, modem3p) = impose_noise_floor(modem3m,modem3p,65)
(modep3m, modep3p) = impose_noise_floor(modep3m,modep3p,65)
(modem2m,modem2p) = impose_noise_floor(modem2m,modem2p,65)
(modep2m,modep2p) = impose_noise_floor(modep2m,modep2p,65)
(modem1m,modem1p) = impose_noise_floor(modem1m,modem1p,65)
(modep1m,modep1p) = impose_noise_floor(modep1m,modep1p,65)
'''



fig = plt.figure()

ax0 = fig.add_subplot(421)

ax2 = fig.add_subplot(423)
ax3 = fig.add_subplot(424)
ax4 = fig.add_subplot(425)
ax5 = fig.add_subplot(426)
ax6 = fig.add_subplot(427)
ax7 = fig.add_subplot(428)

vmin = 0
vmax = np.pi
cmap = 'jet'
extent = (0, 1.408, 0, 1.092)
aspect = 1.092/1.408

im = ax0.imshow(mode0p, vmin=vmin, vmax=vmax, cmap=cmap, extent = extent, aspect=aspect)
ax2.imshow(modem1p, vmin=vmin, vmax=vmax, cmap=cmap,aspect=aspect)
ax3.imshow(modep1p, vmin=vmin, vmax=vmax, cmap=cmap,aspect=aspect)
ax4.imshow(modem2p, vmin=vmin, vmax=vmax, cmap=cmap,aspect=aspect)
ax5.imshow(modep2p, vmin=vmin, vmax=vmax, cmap=cmap,aspect=aspect)
ax6.imshow(modem3p, vmin=vmin, vmax=vmax, cmap=cmap,aspect=aspect)
ax7.imshow(modep3p, vmin=vmin, vmax=vmax, cmap=cmap,aspect=aspect)

ax0.set_xticks([])
ax0.set_yticks([])
ax2.set_xticks([])
ax2.set_yticks([])
ax3.set_xticks([])
ax3.set_yticks([])
ax4.set_xticks([])
ax4.set_yticks([])
ax5.set_xticks([])
ax5.set_yticks([])
ax6.set_xticks([])
ax6.set_yticks([])
ax7.set_xticks([])
ax7.set_yticks([])

ax0.set_title('mode 0')
ax2.set_title('mode -1')
ax3.set_title('mode +1')
ax4.set_title('mode -2')
ax5.set_title('mode +2')
ax6.set_title('mode -3')
ax7.set_title('mode +3')

#fig.colorbar(mode0p, ax=ax0)
#fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.4, 0.75, 0.05, 0.2])
fig.colorbar(im, cax=cbar_ax)

plt.tight_layout()
plt.savefig('IET_simphase5GHz.pdf')
plt.show()  



mode0m = ndimage.rotate(np.reshape(np.abs(lamps3),(33,29)),90)
modep1m = ndimage.rotate(np.reshape(np.abs(lamps4),(33,29)),90)
modep2m = ndimage.rotate(np.reshape(np.abs(lamps5),(33,29)),90)
modep3m = ndimage.rotate(np.reshape(np.abs(lamps6),(33,29)),90)
modem1m = ndimage.rotate(np.reshape(np.abs(lamps2),(33,29)),90)
modem2m = ndimage.rotate(np.reshape(np.abs(lamps1),(33,29)),90)
modem3m = ndimage.rotate(np.reshape(np.abs(lamps0),(33,29)),90)



fig = plt.figure()

ax0 = fig.add_subplot(421)
ax2 = fig.add_subplot(423)
ax3 = fig.add_subplot(424)
ax4 = fig.add_subplot(425)
ax5 = fig.add_subplot(426)
ax6 = fig.add_subplot(427)
ax7 = fig.add_subplot(428)

vmin = 65
vmax = 100
cmap = 'jet'

im = ax0.imshow(mode0m, vmin=vmin, vmax=vmax, cmap=cmap, aspect=aspect)
ax2.imshow(modem1m, vmin=vmin, vmax=vmax, cmap=cmap,aspect=aspect)
ax3.imshow(modep1m, vmin=vmin, vmax=vmax, cmap=cmap,aspect=aspect)
ax4.imshow(modem2m, vmin=vmin, vmax=vmax, cmap=cmap,aspect=aspect)
ax5.imshow(modep2m, vmin=vmin, vmax=vmax, cmap=cmap,aspect=aspect)
ax6.imshow(modem3m, vmin=vmin, vmax=vmax, cmap=cmap,aspect=aspect)
ax7.imshow(modep3m, vmin=vmin, vmax=vmax, cmap=cmap,aspect=aspect)

ax0.set_xticks([])
ax0.set_yticks([])
ax2.set_xticks([])
ax2.set_yticks([])
ax3.set_xticks([])
ax3.set_yticks([])
ax4.set_xticks([])
ax4.set_yticks([])
ax5.set_xticks([])
ax5.set_yticks([])
ax6.set_xticks([])
ax6.set_yticks([])
ax7.set_xticks([])
ax7.set_yticks([])

ax0.set_title('mode 0')
ax2.set_title('mode -1')
ax3.set_title('mode +1')
ax4.set_title('mode -2')
ax5.set_title('mode +2')
ax6.set_title('mode -3')
ax7.set_title('mode +3')

cbar_ax = fig.add_axes([0.4, 0.75, 0.05, 0.2])
fig.colorbar(im, cax=cbar_ax)

plt.tight_layout()

plt.savefig('IET_simmag5GHz.pdf')
plt.show()  