import matplotlib.pyplot as plt #For plotting
from math import sin, pi #For generating input signals
import sys #For reading command line arguments
import scipy.signal as sig

### Filter - 6KHz->8Khz Bandpass Filter
### @param [in] input - input unfiltered signal
### @param [out] output - output filtered signal
def filter(x , coefb, coefa):
    y = [0]*48000
    for n in range(3, len(x)):
        y[n] = coefb[0]*x[n] + coefb[1]*x[n-1]+  coefb[2]*x[n-2] -(coefa[1]*y[n-1] + coefa[2]*y[n-2])
    return y

###Read in desired frequency from command line
#frequency = int(sys.argv[1])
frequency = 1000

## Create the filter
Fs = 5000           #Sample Frequ
sample = 5000       #Number of Samples
f = 100             #Sig gen Frequ
n = 2               #Order of Filter
rs = 30             #only for Cheby
fc = 10            #Cut Frequ
w_c = 2*fc/Fs       #Digital Frequ -> 0 - 0.5
[coefb,coefa] = sig.iirfilter(n,w_c ,0,rs, btype="lowpass", analog=False, ftype="butter")

### Create empty arrays
input = [0]*48000
output = [0]*48000

### Fill array with xxxHz signal
for i in range(48000):
    input[i] = sin(2 * pi * frequency * i / 48000) #+ sin(2 * pi * 70 * i / 48000)

### Run the signal through the filter
output = filter(input,coefb,coefa)

### Grab samples from input and output #1/100th of a second
output_section = output[0:4800]
input_section = input[0:4800]

### Plot the signals for comparison
plt.figure(1)
plt.subplot(211)
plt.ylabel('Magnitude')
plt.xlabel('Samples')
plt.title('Unfiltered Signal')
plt.plot(input_section)
plt.subplot(212)
plt.ylabel('Magnitude')
plt.xlabel('Samples')
plt.title('Filtered Signal')
plt.plot(output_section)
plt.show()
