#importing the picomodule
import pico_module as pm

#importing the fft/toa calc code
from fft import calcOrientation

#importing numpy
import numpy as np
import csv
import time
import matplotlib.pyplot as plt


#import hub
import seawolf as sw
sw.loadConfig("../../../seawolf/conf/seawolf.conf");
sw.init("Acoustics : Main");


DB = True



def writeCSV(fname, data):
  f = open(fname+str(time.time()) + ".csv", "w")
  wr = csv.writer(f)
  wr.writerows(data)
  f.close()

def angleOfArrival(h1, h2, tdoa, front=True):
  v_s = 1484
  distance = np.linalg.norm(h2 - h1) / 2
  A = tdoa * v_s / 2
  B = np.sqrt(distance ** 2 - A ** 2) 
  return np.rad2deg(np.arctan2(-A, front * B))

def max_shift(ch1, ch2, db=False):
  if db:
    plt.plot(np.correlate(ch1, ch2, "same"))
    plt.show()
  return np.argmax(np.correlate(ch1, ch2, "same")) - int(len(ch1) / 2)

def amalAdd(data, Fs):
  top_left = np.array([-0.0125, 0, 0.0125])
  top_right = np.array([0.0125, 0, 0.0125])
  bottom_left = np.array([-0.0125, 0, -0.0125])
  bottom_right = np.array([0.0125, 0, 0.0125])
  dt = 1 / Fs
  print(data.shape)
  ch1 = data[0, 1000:4000]
  ch2 = data[1, 1000:4000]
  ch3 = data[2, 1000:4000]
  ch4 = data[3, 1000:4000]
  top_shift = max_shift(ch1, ch2) 
  bottom_shift = max_shift(ch4, ch3) 
  left_shift = max_shift(ch1, ch4) 
  right_shift = max_shift(ch2, ch3)

  top_diff = top_shift * dt
  bottom_diff = bottom_shift * dt
  left_diff = left_shift * dt
  right_diff = right_shift * dt
  '''
  plt.figure()
  plt.title("Shifted channel 4 and 3")
  plt.plot(ch4)
  plt.plot(np.roll(ch3, bottom_shift))
  plt.show(block=False)
  
  plt.figure()
  plt.title("Raw channel 4 and 3")
  plt.plot(ch4)
  plt.plot(ch3)
  plt.show()
  '''
  top = angleOfArrival(top_left, top_right, top_diff)
  bottom = angleOfArrival(bottom_left, bottom_right, bottom_diff)
  plt.figure()
  plt.plot(ch1)
  plt.plot(ch2)
  plt.plot(ch3)
  plt.plot(ch4)
  plt.show() 
  left = angleOfArrival(top_left, bottom_left, left_diff)
  right = angleOfArrival(top_right, bottom_right, right_diff)
  print(top_diff, bottom_diff, left_diff, right_diff)
  print("Yaw:", top)
  #print("Pitch:", left, right)
  
  

	

#connecting to picotec 1 is db 0 is no db
pico = pm.pico_init(1 if DB else 0)
pf = 22 * 10**3
#entering data loop
c = 0
try:
  while True:
    #getting data and making frequency right
    dataO = pm.pico_get_data(pico)
    Fs = (1.0 / pm.pico_get_sample_interval()) * 10**9
    #transposing data and making numpy array
    data = np.array(zip(*dataO))
    #yaw, pitch, good = calcOrientation(data[200:1000, :], Fs, pf, DB)
    #out="Yaw:%s Pitch:%s FS:%s GOOD:%s" % (str(yaw), str(pitch), Fs, str(good))
    yaw = sw.var.get("SEA.Yaw")
    c += 1
    out = 'Yaw%.3fFS%sCount%d' % (yaw, Fs, c)
    """
    if good:
      pass
      #sw.var.set("Acoustics.Pitch", pitch)
      #sw.var.set("Acoustics.Yaw", yaw)
    else:
      #sw.var.set("Acoustics.Pitch", 1000)
      #sw.var.set("Acoustics.Yaw", 1000)
      pass
    """
    if DB:
      print out
      #plt.figure()
      #plt.plot(data)
      #plt.legend(["ch1", "ch2", "ch3", "ch4"])
      #plt.show()
      writeCSV(out, dataO)
      print data.shape
      amalAdd(np.transpose(data), Fs)
      print "-----------------------"
    
    
#closing pico at end
finally:
  pm.pico_close(pico)
  

