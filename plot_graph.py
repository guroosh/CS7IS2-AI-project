import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d

# x = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
# y = [0.0, 0.0, 0.0, 0.0, 0.0, 0.10294117647058823, 0.6617647058823529, 0.59375, 2.6029411764705883, 4.349206349206349, 5.4714285714285715, 7.806451612903226, 10.897058823529411, 16.857142857142858, 11.338461538461539, 17.434782608695652, 16.5, 28.06896551724138, 25.236363636363638, 27.557692307692307, 43.90196078431372, 47.80701754385965, 47.0, 33.0, 34.75, 39.0, 51.0, 42.5, 31.0, 51.5, 128.25, 106.5, 76.66666666666667]
x30 = []
y30 = []
x40 = []
y40 = []
with open('convergence_graph.tsv', 'r') as inp:
    for i in inp:
        i = i[:-1]
        x30.append(float(i.split(' ')[0]))
        y30.append(float(i.split(' ')[1]))
ysmoothed = gaussian_filter1d(y30, sigma=2)
plt.plot(x30, y30, 'r')
# plt.plot(x40, y40, 'b')
plt.plot(x30, ysmoothed)
plt.xlabel('Grid Size (M) : MxM')
plt.ylabel('No. of iterations to find the shortest path')
plt.show()
