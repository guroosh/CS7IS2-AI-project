import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d

# x = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
# y = [0.0, 0.0, 0.0, 0.0, 0.0, 0.10294117647058823, 0.6617647058823529, 0.59375, 2.6029411764705883, 4.349206349206349, 5.4714285714285715, 7.806451612903226, 10.897058823529411, 16.857142857142858, 11.338461538461539, 17.434782608695652, 16.5, 28.06896551724138, 25.236363636363638, 27.557692307692307, 43.90196078431372, 47.80701754385965, 47.0, 33.0, 34.75, 39.0, 51.0, 42.5, 31.0, 51.5, 128.25, 106.5, 76.66666666666667]
x = []
y1 = []
y2 = []
y3 = []
y4 = []
y5 = []
y6 = []
# y_astar = []
with open('mutation_change_daata.txt', 'r') as inp:
    for i in inp:
        i = i[:-1]
        x.append(float(i.split(', ')[0]))
        y1.append(float(i.split(', ')[1]))
        y2.append(float(i.split(', ')[2]))
        y3.append(float(i.split(', ')[3]))
        y4.append(float(i.split(', ')[4]))
        y5.append(float(i.split(', ')[5]))
        y6.append(float(i.split(', ')[6]))


# ysmoothed = gaussian_filter1d(y30, sigma=2)
def smooth(l1):
    return gaussian_filter1d(l1, sigma=2)


y1 = smooth(y1)
y2 = smooth(y2)
y3 = smooth(y3)
y4 = smooth(y4)
y5 = smooth(y5)
y6 = smooth(y6)

plt.plot(x, y6, 'k', label='Global minima (based on A*)')
plt.plot(x, y1, 'r', label='No mutation')
plt.plot(x, y2, 'g', label='30% mutation')
plt.plot(x, y3, 'b', label='50% mutation')
plt.plot(x, y4, 'c', label='70% mutation')
plt.plot(x, y5, 'm', label='100% mutation')
# plt.plot(x40, y40, 'b')
# plt.plot(x30, ysmoothed)
plt.legend(loc="upper left")
plt.xlabel('Grid Size (M) : MxM')
plt.ylabel('Length of best path (after 400 iterations)')
plt.show()
