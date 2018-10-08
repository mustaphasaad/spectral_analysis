import numpy as np
import matplotlib.pyplot as plt
import os
import peakutils
from scipy import signal

#loads spectrum file.
dirpath = os.getcwd()
filepath = dirpath + '/co60.spe'
file = open(filepath)
lines = file.readlines()

#parses spectrum file.
for i in range(len(lines)):
    if lines[i][0:10] == '$MEAS_TIM:':
        livetime,realtime = lines[i+1].split(' ')
    if lines[i][0:6] == '$DATA:':
        start,end = lines[i+1].split(' ')
        counts = lines[i+2:i+3+int(end)]
        counts = np.array(list(map(int,counts)))
    if lines[i][0:10] == '$ENER_FIT:':
        offset,slope = lines[i+1].split(' ')
        offset = float(offset)
        slope = float(slope)
        break        

channels = np.array(range(int(start),int(end)+1))
energies = slope * channels + offset

smoothed_data = signal.wiener(counts)

for i in np.arange(1,10,1):
    smoothed_data = signal.wiener(smoothed_data)

#plots spectrum with identified peaks.
plt.figure(0)
indices = peakutils.peak.indexes(smoothed_data, min_dist = 10, thres=0.5)
plt.plot(channels, counts)
plt.plot(indices, counts[indices], 'x')

#gaussian model.
def gaussian(x,a,b,sigma):
  return a*np.exp(-np.power((x - b)/sigma, 2.)/2.)

#fitting identified peaks to gaussian model and plots on top of spectrum.
gauss_param = []
for index in indices:
    gauss_param.append(peakutils.peak.gaussian_fit(channels[index-20:index+20],smoothed_data[index-20:index+20],center_only=0))
    FWHM = 2.355 * gauss_param[-1][-1]
    x_val = np.arange(int(gauss_param[-1][1]-3*FWHM),int(gauss_param[-1][1]+3*FWHM))
    plt.plot(x_val,gaussian(x_val,gauss_param[-1][0],gauss_param[-1][1],gauss_param[-1][2]))

plt.plot(channels,smoothed_data)
plt.show()