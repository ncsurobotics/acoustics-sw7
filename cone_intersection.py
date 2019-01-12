import matplotlib.pyplot as plt
import numpy as np


v_sound = float(3) # speed of sound underwater
dt = .002 # time difference of arrival
# from acoustics pdf
# .025m is the distance between hydrophones

a = v_sound*dt/2

b = ((.025**2-a**2)**(1/2))/2

# a and b from acoustics pdf

m = b/a

n = b/a

#m and n from wolfram alpha equation

denom = (m**2+1)*n**2
y_s = ((m**2*n**2-1)/denom)**(1/2)
# the original equation had a negative numerator creating a imaginary number as the answer
z_s = ((m**2*(n**2+1)/denom)**(1/2))
# something must be wrong because this reduces to just one


print("the y slope is",y_s,"x")
print('the z slope is',z_s,'x')

# x = np.arange(10)
# y = [(y_s * i) for i in x]
# z= [(z_s * i)for i in x]
# plt.plot(x,y)
# plt.plot(x,z)
# plt.show()
# plt.plot(x,z)
# plt.show()




