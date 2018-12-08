import sys
import os
import numpy as np
import re
path = sys.argv[1]
files = os.listdir(path)
count = 1
for file in files:
	#print(file)
	params = re.search("Yaw(-?\d*.\d*)FS(\d*.\d*)", file)
	
	data = np.genfromtxt(path + file, delimiter=",")[0:4, :]
	data2 = np.vstack([data, ([float(params.groups()[0]), float(params.groups()[1])] + [0] * (12000 - 2))])
	np.savetxt(path + "test" + str(count) + ".csv", data2, delimiter=",")

	count += 1
