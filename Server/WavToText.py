from __future__ import division
import wave
import numpy as np
import sys

if (len(sys.argv) > 1):
    name = sys.argv[1]
else:
    name = 's0_6000.wav'

sensorSets = []

sensorSets.append(wave.open(name, 'r'))

signal = sensorSets[0].readframes(-1)
signal = np.fromstring(signal, 'Int16')
signal=signal/np.amax(signal)
file=open("s0_6000.txt","w")
file.write('%d\n' % len(signal))
for i in range(len(signal)):
    file.write('%f\n' % signal[i])
file.close()
