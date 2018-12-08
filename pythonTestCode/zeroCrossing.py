from scipy.signal import butter, lfilter



import numpy as np
import matplotlib.pyplot as plt
import sys	
data = np.genfromtxt("../../Waveforms/conf1/Settings4/Test1.csv", delimiter=",", skip_header=3)
#plt.plot(data[:,0], data[:,1:])

t = data[:,0]
t = np.divide(t, 1000)
ch1 = data[:, 1]
ch2 = data[:, 2]



def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

fs = 1 / (t[1] - t[0])
lowcut = 20e3 / fs
highcut = 30e3 / fs

ch1_filtered = butter_bandpass_filter(ch1, 18e3, 26e3, 1 / (t[1] - t[0]), order=2)
ch2_filtered = butter_bandpass_filter(ch2, 18e3, 26e3, 1 / (t[1] - t[0]), order=2)

plt.plot(t, ch1)
plt.plot(t, ch1_filtered)
plt.show()

def find_zeroes(data, start, end):
	zeroes = []
	for i in range(start, end):
		last = data[i]
		current = data[i + 1]
		if(last > 0 and current < 0):
			zeroes.append(i)

	return zeroes
