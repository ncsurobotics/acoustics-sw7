import sys
from scipy.signal import butter, lfilter
import numpy as np
import matplotlib.pyplot as plt

def calcOrientation(tdoa):


    SPEED_OF_SOUND = 1484
    sideToSideDistance = np.linalg.norm(hydrophones[3] - hydrophones[2]) / 2
    inlineDistance = np.linalg.norm(hydrophones[1] - hydrophones[0]) / 2 

    sideToSideA = tdoa[1] * SPEED_OF_SOUND / 2
    sideToSideB = np.sqrt(sideToSideDistance ** 2 - sideToSideA ** 2)

    inlineA = tdoa[0] * SPEED_OF_SOUND / 2
    inlineB = np.sqrt(inlineDistance ** 2 - inlineA ** 2)

    front = np.sign(inlineA)
    if front == 0:
        front = 1
    yaw = np.arctan2(-sideToSideA, front * sideToSideB)
    pitch = np.arctan2(inlineA, inlineB)

    return (np.rad2deg(yaw), np.rad2deg(pitch))


def angleOfArrival(hydrophones, tdoa, front=True):
    distance = np.linalg.norm(hydrophones[1] - hydrophones[0]) / 2
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

path = sys.argv[1]
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

bottom_left = [-0.0125, 0, -0.0125] # Channel 3
bottom_right = [0.0125, 0, -0.0125] # Channel 4
top_left = [-0.0125, 0, 0.0125] # Channel 1
top_right = [0.0125, 0, 0.0125] # Channel 2

ch1_filtered = butter_bandpass_filter(ch1, lowcut, highcut, fs)
ch2_filtered = butter_bandpass_filter(ch2, lowcut, highcut, fs)
ch3_filtered = butter_bandpass_filter(ch3, lowcut, highcut, fs)
ch4_filtered = butter_bandpass_filter(ch4, lowcut, highcut, fs)

def find_zeroes(data, start, end):
	zeroes = []
	for i in range(start, end):
		last = data[i]
		current = data[i + 1]
		if(last > 0 and current < 0):
			zeroes.append(i)

	return zeroes


def calculate_shift(ch1, ch2):
	return np.argmax(np.correlate(ch1, ch2, "same")) - int(len(ch1) / 2)


top_shift = calculate_shift(ch1_filtered[1800:3000], ch2_filtered[1800:3000])
bottom_shift = calculate_shift(ch4_filtered[1800:3000], ch3_filtered[1800:3000])
print(top_shift, bottom_shift)


plt.figure()
plt.plot(ch1_filtered)
plt.plot(ch2_filtered)
plt.plot(ch3_filtered)
plt.plot(ch4_filtered)
plt.title("Filtered Data")
plt.legend(["Channel 1", "Channel 2", "Channel 3", "Channel 4"])
plt.show(block=False)

plt.figure()
plt.plot(ch1)
plt.plot(ch2)
plt.plot(ch3)
plt.plot(ch3)
plt.title("Unfiltered Data")
plt.legend(["Channel 1", "Channel 2", "Channel 3", "Channel 4"])
plt.show()

