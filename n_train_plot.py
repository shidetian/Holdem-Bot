import pylab
import numpy as np

x = []
y = []

tempY = np.array([205.0, 635.0, 391.0, 282.0, 549.0,
                  1386.0, 767.0, 1150.0, 754.0, 1700.0])/5
y.extend(tempY)
x.extend([4] * len(tempY))
#---------
tempY = np.array([71.0, -587.0, 233.0, -561.0, -1155.0,
                  -942.0, -867.0, 273.0, -685.0, -1492.0])/5
y.extend(tempY)
x.extend([6] * len(tempY))
#------------
tempY = np.array([3555.0, 3663.0, 3261.0, 3324.0, 2582.0,
                  3174.0, 3128.0, 3561.0, 4369.0, 3143.0] )/5
y.extend(tempY)
x.extend([8] * len(tempY))
#---------
tempY = np.array([2761.0, 3442.0, 3604.0, 2919.0, 3157.0,
                  3279.0, 3174.0, 3075.0, 3447.0, 4162.0])/5

y.extend(tempY)
x.extend([10] * len(tempY))
#---------
tempY = np.array([3430.0, 3500.0, 3836.0, 1866.0, 4629.0,
                  3654.0, 3701.0, 3673.0, 4269.0, 3604.0])/5

y.extend(tempY)
x.extend([12] * len(tempY))
#---------
tempY = np.array([6254.0, 5495.0, 4037.0, 4404.0, 3444.0,
                  2898.0, 5399.0, 3487.0, 4719.0, 3953.0])/5

y.extend(tempY)
x.extend([14] * len(tempY))
#---------
tempY = np.array([4556.0, 4484.0, 4390.0, 4944.0, 4406.0,
                  3392.0, 2778.0, 5290.0, 3954.0, 4852.0])/5

y.extend(tempY)
x.extend([16] * len(tempY))
#---------
tempY = np.array( [2968.0, 3110.0, 2382.0, 3064.0, 3176.0,
                   1682.0, 1704.0, 2292.0, 1474.0, 1242.0])/5

y.extend(tempY)
x.extend([18] * len(tempY))

pylab.scatter(x,y)
pylab.xlabel('The number of training in 10000')
pylab.ylabel('Total winnings competing against check-calling bot after 1000 games')
pylab.title('Performance after training against check-calling bot with Lambda=0.9, n_train=140000')
pylab.show()

