import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


filename = os.path.join('data', 'out')
data = np.genfromtxt(filename + '-results.csv', delimiter=',', dtype=int)

plt.figure(figsize=(30,12))
plt.plot(data[:, 1:])
plt.legend(['Draws', 'O-wins', 'X-wins'])
plt.grid()

data = data[:, 1:]
plt.savefig(filename +'-learning.png')
data[1:] -= data[:-1]
w = pd.DataFrame(data).rolling(100).aggregate(np.sum)
w[:100] = np.cumsum(data[:100], axis=1)

plt.figure(figsize=(30,12))
plt.plot(w)
plt.legend(['Draws', 'O-wins', 'X-wins'])
plt.savefig(filename +'-learning-cum.png')