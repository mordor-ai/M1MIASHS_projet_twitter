import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
x = np.random.normal(size=1000)
plt.hist(x, density=True, bins=30)  # `density=False` would make counts
plt.ylabel('Probability')
plt.xlabel('Data');
plt.show()



data = [23, 45, 56, 78, 213]
plt.bar(range(len(data)), data, color='red')
plt.show()



import matplotlib.pyplot as plt
def autolabel(rects):
	for rect in rects:
		height = rect.get_height()
		plt.text(rect.get_x()+rect.get_width()/2.,1.04*height,'%s'%float(height))
plt.xlabel('sex')
plt.ylabel('number')
plt.xticks((0,1),('male','female'))
plt.title('sex ratio analysis')
rect = plt.bar(left = (0,1),height=(0.8,0.5),width=0.25,align = 'center',yerr = 0.0001)
plt.legend(rect,['legend11'],bbox_to_anchor = (0.95,0.95))
autolabel(rect)
plt.show()
