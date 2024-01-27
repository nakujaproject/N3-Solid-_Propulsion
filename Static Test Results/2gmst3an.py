import numpy as np
from numpy import trapz
import matplotlib.pyplot as plt

res = [-1.96, 6.52, 32.93, 106.96, 232.50, 407.07, 407.07, 327.83, -7.39, 189.24, 504.78, 425.87, 325.22, 507.50, 744.02, 854.57, 1010.43, 1247.39, 1503.48, 1767.28, 2024.46, 2291.52, 2535.98, 2822.83, 3490.54, 4520.87, 5464.57, 6212.28, 7114.67, 8775.87, 10631.09, 12837.61, 15387.61, 19189.89, 23925.65, 30516.85, 47374.02, 49804.35, 73932.83, 425678.28, 606592.75, 549624.94, 521149.25, 464179.16, 435701.75, 378730.22, 321759.16, 264788.16, 236310.77, 207833.05]
time = []

for i in range(len(res)):
    time.append((0.0125)*i)
    res[i] = (res[i]/1000)*9.81

res_ar = np.array(res)
area = trapz(res_ar, dx = 7.013/len(res))
print(area)

plt.plot(time, res)
plt.title("FOUR Grain Motor 2st Static Test")
plt.xlabel('TIME(s)')
plt.ylabel('THRUST(N)')
plt.show()
