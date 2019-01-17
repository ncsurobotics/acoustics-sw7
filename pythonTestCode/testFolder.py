import sys
from scipy.signal import butter, lfilter
import numpy as np
import matplotlib.pyplot as plt
import os


bottom_left = [-0.0125, 0, -0.0125] # Channel 3
bottom_right = [0.0125, 0, -0.0125] # Channel 4
top_left = [-0.0125, 0, 0.0125] # Channel 1
top_right = [0.0125, 0, 0.0125] # Channel 2
SPEED_OF_SOUND = 1484

def angleOfArrival(hydrophones, tdoa, front=True):
    distance = np.linalg.norm(np.array(hydrophones[1]) - np.array(hydrophones[0])) / 2
    A = tdoa * SPEED_OF_SOUND / 2
    B = np.sqrt(distance ** 2 - A ** 2)
    return np.rad2deg(np.arctan2(-A, front * B))


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
def calculate_shift(ch1, ch2):
    mid = int(len(ch1) / 2)
    xcorr = np.correlate(ch1, ch2, "same")[mid - 32:mid + 32]
    return np.argmax(xcorr) - 32

path = sys.argv[1]

def getYaws(path):


    data = np.genfromtxt(path, delimiter=",")

    yaw = data[4, 0]
    fs = data[4, 1]
    data = np.transpose(data[0:4, :])

    lowcut = 15e3
    highcut = 50e3


    ch1 = data[:, 0]
    ch2 = data[:, 1]
    ch3 = data[:, 2]
    ch4 = data[:, 3]

    fftfreq = np.fft.fftfreq(len(ch1), d=528e-9)
    fft = 20*np.log(np.abs(np.fft.fft(ch1)))
    #plt.plot(fftfreq, fft)
    #plt.show()
    
    ch1_filtered = butter_bandpass_filter(ch1, lowcut, highcut, fs)
    ch2_filtered = butter_bandpass_filter(ch2, lowcut, highcut, fs)
    ch3_filtered = butter_bandpass_filter(ch3, lowcut, highcut, fs)
    ch4_filtered = butter_bandpass_filter(ch4, lowcut, highcut, fs)

    ch1=ch1_filtered
    ch2=ch2_filtered
    ch3 = ch3_filtered
    ch4 = ch4_filtered

    start = 1000
    stop = 2100


    if(np.max(ch1[start:stop]) < 2000):
        return (0, 0)
    

    top_shift = calculate_shift(ch1[start:stop], ch2[start:stop])
    bottom_shift = calculate_shift(ch3[start:stop], ch4[start:stop])
    '''
    plt.figure()
    plt.title(path)
    plt.plot(ch1[start:stop])
    plt.plot(ch2[start:stop])
    plt.legend(["Channel 1", "Channel 2"])
    plt.show(block=False)


    plt.figure()
    plt.title("3+4")
    plt.plot(ch3[start:stop])
    plt.plot(ch4[start:stop])
    plt.legend(["Channel 3", "Channel 4"])
    plt.show(block=False)


    plt.figure()
    plt.title("Channels 1 and 2 shifted")
    plt.plot(np.roll(ch1, -top_shift)[start:stop])
    plt.plot(ch2[start:stop])
    plt.legend(["Channel 1", "Channel 2"])
    plt.show(block=False)

    plt.figure()
    plt.title("Channels 3 and 4 shifted")
    plt.plot(np.roll(ch3, -bottom_shift)[start:stop])
    plt.plot(ch4[start:stop])
    plt.legend(["Channel 3", "Channel 4"])
    plt.show()
    '''
    tdoa = top_shift * 528e-9
    print((top_shift, bottom_shift))
    print(angleOfArrival([top_left, top_right], tdoa))
    tdoa = bottom_shift * 528e-9
    print(angleOfArrival([bottom_left, bottom_right], tdoa))
    return (0, 0)




files = os.listdir(path)
tops = []
bottoms = []
for file in files:


    
    top, bottom = getYaws(path + file)
    '''
    if(np.abs(top) < 32):
        tops.append(top)
    if(np.abs(bottom) < 32):
        bottoms.append(bottom)
    '''


print(tops)
print(bottoms)

print(np.std(tops))
print(np.std(bottoms))
