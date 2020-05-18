from math import cos, pi
from scipy import signal
import scipy.signal as sig
import matplotlib.pyplot as plt
import numpy

plt.close('all')


Fs = 5000           #Sample Frequ
sample = 5000       #Number of Samples
f = 100             #Sig gen Frequ
n = 2               #Order of Filter
rs = 30             #only for Cheby
fc = 100            #Cut Frequ
w_c = 2*fc/Fs       #Digital Frequ -> 0 - 0.5
[b,a] = sig.iirfilter(n,w_c ,0,rs, btype="lowpass", analog=False, ftype="butter")

[w,h] = sig.freqz(b,a,2000)
w = Fs*w/(2*pi)
h_db = 20*numpy.log10(abs(h))

plt.figure()
plt.plot(w, h_db);plt.xlabel('Frequency(Hz)')
plt.ylabel('Magnitude(db)')
plt.grid('ON')
plt.show()
print(a,b)

x = numpy.arange(sample)
y = numpy.sin(2 * numpy.pi * f * x / Fs)
plt.plot(x, y)
plt.xlabel('sample(n)')
plt.ylabel('voltage(V)')
plt.show()
