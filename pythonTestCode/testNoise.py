import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.signal import lfilter, butter

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


data = np.genfromtxt(sys.argv[1], delimiter=",", skip_header=3)

for f in sys.argv[2:]:
	print(f)
	np.vstack([data, np.genfromtxt(f, delimiter=",", skip_header=3)])

#data = data[int(sys.argv[1]):int(sys.argv[2])]

# Cuts the data down to an appropriate size and isolates channels
t = data[:, 0]
ch1 = data[:,1]


fs = 1e6/(t[1]-t[0])

print(fs)
ch1_filtered = butter_bandpass_filter(ch1, 15e3, 50e3, fs, 2)

freq = np.fft.fftfreq(len(ch1), d = 1/fs)
length = len(freq) / 2#int(3e7 / freq[1])
print(length)
freq = freq[0:length]
fft = np.abs(np.fft.fft(ch1))[0:length]
fft_filtered = np.abs(np.fft.fft(ch1_filtered))[0:length]

plt.figure()
plt.title("Unfiltered FFT")
plt.plot(freq, 20 * np.log(fft))
plt.show(block=False)


plt.figure()
plt.title("Filtered FFT")
plt.plot(freq, 20 * np.log(fft_filtered))
plt.show(block=False)

plt.figure()
plt.title("Unfiltered time domain")
plt.plot(t, ch1)
plt.show(block=False)


plt.figure()
plt.title("Filtered time domain")
plt.plot(t, ch1_filtered)
plt.show()