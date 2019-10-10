import numpy as np

x = np.array([6,2,9,2,5])
w = np.array([[3,4,4],[5,6,6],[7,8,3],[9,9,4],[10,10,5]])
b = np.array([4,4,6])

y = np.dot( x, w)+b
print( y )

delta = 0.5

grad_w = np.dot( x.T , y )
print( grad_w )