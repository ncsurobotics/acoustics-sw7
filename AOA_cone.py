import numpy as np
import pythonTestCode.simulator as sim
import math


v_sound = sim.v_sound
hydrophone_spacing = 0.025  # (m)

# from acoustics pdf

d1 = sim.calcTDOA(left=sim.left_top,right=sim.right_top) * v_sound
d2 = sim.calcTDOA(left=sim.left_top, right=sim.left_bottom) * v_sound


c1 = d1**2 / (hydrophone_spacing**2 - d1**2)
c2 = d2**2 / (hydrophone_spacing**2 - d2**2)

# calculate yaw and pitch

yaw = math.degrees(math.atan(math.sqrt((c1 + c1 * c2)/(1 - c1 * c2))))
pitch = math.degrees(math.atan(math.sqrt((c1 + 1)/(c2 + c1 * c2))))

print("cone yaw: ", yaw)
print("cone pitch: ", pitch)

# test
print(math.degrees(np.arctan(sim.pinger_locs[0, 1]/sim.pinger_locs[0, 0])), "yaw")
print(math.degrees(np.arctan2(sim.pinger_locs[0, 2], math.sqrt(sim.pinger_locs[0, 1]**2 + sim.pinger_locs[0, 0]**2))), "pitch")













