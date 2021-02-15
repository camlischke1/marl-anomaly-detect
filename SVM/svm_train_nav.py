# evaluate random forest algorithm for classification
import numpy as np
from sklearn.svm import SVC
import pickle


#reading data
input = np.load("../datasets_nav_strategic/Coopnav_50timed_attack.npy", allow_pickle=True)

pre = np.asarray(input[:,0])
a1 = np.asarray(input[:,1])
a2 = np.asarray(input[:,2])
a3 = np.asarray(input[:,3])
Y = np.asarray(input[:,5])

#flattens the np arrays
pre = np.concatenate(pre).ravel()
pre = np.reshape(pre, (pre.shape[0]//54,54))

X = np.column_stack((pre,a1.T,a2.T,a3.T))
X = X.astype('float64')


# define the model
model = SVC(verbose=1,random_state=1234)
model.fit(X,list(Y))

pickle.dump(model, open('../SVMAnomalyNavStrategic.sav', 'wb'))


import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 2000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)