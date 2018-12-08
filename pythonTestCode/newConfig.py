import matplotlib.pyplot as plt
from simulator import *
SPEED_OF_SOUND = 1484
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


# Assumes robot is at the origin
def calcActualOrientation(pinger_loc):
    x, y, z = pinger_loc
    yaw = np.rad2deg(np.arctan2(y, x))
    pitch = np.rad2deg(np.arctan2(z, np.sqrt(x ** 2 + y ** 2)))    
    return (yaw, pitch)


pitches = []
calculated_pitches = []
yaws = []
calculated_yaws = []
circle = range(0, 180)
for i in circle:
    angle = np.deg2rad(i)
    loc = [3 * np.cos(angle), 3 * np.sin(angle), 10]
    pitch_tdoa = calcTDOA(left_top, left_bottom, loc)
    yaw_tdoa = calcTDOA(left_top, right_top, loc)
    yaw, pitch = calcActualOrientation(loc)
    calculated_pitch = angleOfArrival([left_top, left_bottom], pitch_tdoa)
    calculated_yaw = angleOfArrival([left_top, right_top], yaw_tdoa)
    pitches.append(pitch)
    calculated_pitches.append(calculated_pitch)
    yaws.append(yaw - 90)

    calculated_yaws.append(calculated_yaw)



plt.plot(np.subtract(circle, 90), yaws)
plt.plot(np.subtract(circle, 90), calculated_yaws)
plt.show()

plt.plot(circle, pitches)
plt.plot(circle, calculated_pitches)
plt.show()