import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from tensorflow.python.keras.callbacks import EarlyStopping
from tensorflow.python.keras.regularizers import l2
from tensorflow.python.keras.layers import Dense, LSTM, Dropout, Activation
from tensorflow.python.keras.models import Model, load_model, Sequential
from tensorflow.python.keras.utils.np_utils import to_categorical
from tensorflow.keras.activations import sigmoid
import tensorflow as tf

threshold =.10

#create timeseries for leftover data x needs (samples,num_steps,features54) and y needs actions
def leftover_timeseries(indices,testX,actions,truth):
    dataX = []
    dataY = []
    trueList = []
    for i in range(len(indices)):
        dataX.append(testX[indices[i],:,:90])
        dataY.append(actions[indices[i]])
        trueList.append(truth[indices[i]])
    return np.asarray(dataX), np.asarray(dataY), np.asarray(trueList)


model0 = load_model('../SeparateAgents/Agent0NetworkStar.keras')
model1 = load_model('../SeparateAgents/Agent1NetworkStar.keras')
model2 = load_model('../SeparateAgents/Agent2NetworkStar.keras')
binary_model = load_model('../BinaryNets/LSTMStarWhiteRandom.keras')

for i in range(1,21):
    eps = np.round((i*0.05),2)*100
    testX = np.load('fgsm_data_star/fgsm_test_starX' + str(eps) + '.npy')
    testY = np.load('fgsm_data_star/fgsm_test_starY'+ str(eps) + '.npy')
    trueActions = np.load('fgsm_data_star/fgsm_star_trueActions'+ str(eps) + '.npy')
    print(testX.shape)
    print(testY.shape)

    pred = np.array(binary_model.predict(testX))
    pred = np.argmax(pred,axis=1)

    #print(accuracy_score(testY,pred))
    #print(classification_report(testY,pred))
    #print(testY.shape)
    matrixA = confusion_matrix(testY,pred)
    #print(matrixA)

    indices_fn = []
    for i in range(len(pred)):
        if pred[i] == 0: #and testY[i] == 1:
            #all data predicted negative
            indices_fn.append(i)
    indices_fn = np.asarray(indices_fn)
    #print(indices_fn.shape)


    #now time to clean up with predictive models
    #create timeseries for leftover data
    newX, newY, newTruth = leftover_timeseries(indices_fn,testX,trueActions,testY)

    pred0 = np.array(model0.predict(newX))
    pred1 = np.array(model1.predict(newX))
    pred2 = np.array(model2.predict(newX))

    pred0 = np.argwhere(pred0 >= threshold)
    pred0 = np.split(pred0[:,1], np.unique(pred0[:, 0], return_index=True)[1][1:])

    pred1 = np.argwhere(pred1 >= threshold)
    pred1 = np.split(pred1[:,1], np.unique(pred1[:, 0], return_index=True)[1][1:])

    pred2 = np.argwhere(pred2 >= threshold)
    pred2 = np.split(pred2[:,1], np.unique(pred2[:, 0], return_index=True)[1][1:])

    #anomaly detection
    binary_anomalies = []
    for i in range(len(pred0)):
        combined = np.unique(np.concatenate((pred0[i],pred1[i],pred2[i]),axis=0).ravel())
        result = all(elem in combined for elem in newY[i,-1])
        if result:
            binary_anomalies.append(0)
        else:
            binary_anomalies.append(1)
    binary_anomalies = np.array(binary_anomalies)

    #print(accuracy_score(newTruth,binary_anomalies))
    #print(classification_report(newTruth,binary_anomalies))
    matrix = confusion_matrix(newTruth,binary_anomalies)
    #print(matrix)


    print("FN (success rate of fooling model @ " + str(eps) + ":  " + str(float(matrix[1][0])/(float(matrixA[1][0])+float(matrixA[1][1]))))
    print("TP:  " + str((float(matrix[1][1]) + float(matrixA[1][1]))/(float(matrixA[1][0])+float(matrixA[1][1]))))
