from functools import reduce
from operator import add

from math import cos, pi
from scipy import signal
import matplotlib.pyplot as plt

from migen import *
from migen.fhdl import verilog
import numpy

sample = 5000       #Number of Samples
Fs = 5000           #Sample Frequency
fc = 800           #Cutoff frequ
w_c = 2*fc/Fs       #Digital Frequ
n = 3               #Order of the filter


# A synthesizable FIR filter.
class FIR(Module):
    def __init__(self, coefb,coefa, wsize=32):
        self.coefa = coefa
        self.coefb = coefb
        self.wsize = wsize
        self.i = Signal((self.wsize, True))
        self.o = Signal((self.wsize, True))

        ###

        mulsb = [0]
        mulsa = [0]
        srcb = self.i
        for c in self.coefb:
            sregb = Signal((self.wsize, True))      #Neues Signal sregb erstellen
            self.sync += sregb.eq(srcb)             #Neues Signal mit dem Namen sregb wird mit jedem sync mit dem Wert aus Sourceb geladen
            srcb = sregb                            #Source B entspricht nun sregb -> ist also ein Signal
            c_fpb = int(c*2**(self.wsize - 1))      #Koeffizient c wird mit 2^15 multipliziert
            mulsb.append(c_fpb*sregb)               #Der Ergebnisliste wird der Skallierte Koeffizient multipliziert mit sregb angehängt


        sum_fulla = Signal((2*self.wsize-1, True))
        sum_fullb = Signal((2*self.wsize-1, True))
        sum_full = Signal((2*self.wsize-1, True))

        self.sync += sum_fullb.eq(reduce(add, mulsb))                       #Register
        self.sync += sum_full.eq((sum_fullb+sum_fulla)>> self.wsize)        #Hier passiert ein Fehler


        srca = sum_full
        for c in self.coefa:
            srega = Signal((self.wsize, True))
            self.sync += srega.eq(srca)
            srca = srega
            c_fpa = int(c*2**(self.wsize - 1))
            mulsa.append(c_fpa*srega)
        self.sync += sum_fulla.eq(reduce(add, mulsa))
        self.comb += self.o.eq(sum_full)


# A test bench for our FIR filter.
# Generates a sine wave at the input and records the output.
def fir_tb(dut, frequency, inputs, outputs):
    f = 2**(dut.wsize - 1)                                      #Skallierung
    x = numpy.arange(sample)                                    #Array von 1 - 5000 anlegen
    for x in x:
        y = 0.1*numpy.sin(2 * numpy.pi * frequency * x / Fs)    #Sinus erzeugen mit Frequenz frequency und der Auflösung Fs
        yield dut.i.eq(int(f*y))                                #Neuer erzeugter Wert y nach input i wird hier geschrieben
        inputs.append(y*0.1)                                    #Input Array wird gefüllt
        outputs.append((yield dut.o)/f*0.1*info)                     #Output Array wird mit dem Output des Filters gefüllt
        yield



if __name__ == "__main__":
    # Compute filter coefficients with SciPy.
    #coef = signal.remez(30, [0, 0.1, 0.2, 0.4, 0.45, 0.5], [0, 1, 0])
    #coefb = signal.firwin(100, cutoff = 0.1, window = "hanning", pass_zero=True)
    #coefb, coefa = signal.iirfilter(n,w_c, btype="lowpass", analog=False, ftype="butter")
    coefb, coefa = signal.butter(n, w_c, btype='lowpass', analog=False, output='ba', fs=None)
    print(coefb,coefa)

    #Rescale-----------------------------------------------------------------
    ValueArray = []
    ValueArray.append(abs(numpy.amin(coefb)))
    ValueArray.append(abs(numpy.amax(coefb)))
    ValueArray.append(abs(numpy.amin(coefa)))
    ValueArray.append(abs(numpy.amax(coefa)))
    info = numpy.amax(ValueArray)
    print(info)
    coefb = coefb/info
    coefa = coefa/info
    #-------------------------------------------------------------------------

    # Simulate for different frequencies and concatenate
    # the results.
    in_signals = []
    out_signals = []
    for frequency in [1,10,100,1000]:
        dut = FIR(coefb,coefa)
        tb = fir_tb(dut, frequency, in_signals, out_signals)
        run_simulation(dut, tb)

    # Plot data from the input and output waveforms.
    plt.plot(in_signals)
    plt.plot(out_signals)
    plt.show()
    print(coefb,coefa)

    # Print the Verilog source for the filter.
    fir = FIR(coefb,coefa)
    print(verilog.convert(fir, ios={fir.i, fir.o}))
