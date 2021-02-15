import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from tensorflow.python.keras.models import Sequential, load_model
import tensorflow as tf

#same results for same model, makes it deterministic
np.random.seed(1234)
tf.random.set_seed(1234)

#reading data
input = np.load("../datasets_nav_strategic/Coopnav_100timed_attack.npy", allow_pickle=True)

pre = np.asarray(input[:,0])
a1 = np.asarray(input[:,1])
a2 = np.asarray(input[:,2])
a3 = np.asarray(input[:,3])
testY = np.asarray(input[:,5])

#flattens the np arrays
pre = np.concatenate(pre).ravel()
pre = np.reshape(pre, (pre.shape[0]//54,54))
testX = np.column_stack((pre,a1.T,a2.T,a3.T))
testX = testX.astype('float64')
testY = testY.astype('int32')

model = load_model('BinaryDenseNetworkNavStrategic.keras')

pred = np.array(model.predict(testX))
pred = np.argmax(pred,axis=1)

print(accuracy_score(testY,pred))
print(classification_report(testY,pred))
matrix = confusion_matrix(testY,pred)
print(matrix)
print(float(matrix[0][0])/(float(matrix[0][0])+float(matrix[0][1])))
print(float(matrix[0][1])/(float(matrix[0][0])+float(matrix[0][1])))
print(float(matrix[1][0])/(float(matrix[1][0])+float(matrix[1][1])))
print(float(matrix[1][1])/(float(matrix[1][0])+float(matrix[1][1])))