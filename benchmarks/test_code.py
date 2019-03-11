from observatory.tracking import TrackingSession, start_run, LocalState

from sklearn.neighbors import KNeighborsClassifier 
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_iris 
from sklearn.model_selection import train_test_split
from sklearn import metrics



import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

def test_function():

    data = pd.read_csv('benchmarks\input\column_2C_weka.csv')
    plt.style.use('ggplot')

    knn = KNeighborsClassifier(n_neighbors= 3)
    x,y = data.loc[:, data.columns != 'class'], data.loc[:, 'class']
    knn.fit(x,y)
    prediction = knn.predict(x)
    #print('Prediction : {}'. format(prediction))

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 1)
    neig = np.arange(1, 25)
    train_accuracy = []
    test_accuracy = []

    with start_run('testmodel', 1, LocalState, 'testexperiment') as run:
        for i, k in enumerate(neig):
            knn = KNeighborsClassifier(n_neighbors=k)
            knn.fit(x_train, y_train)
            #run.record_metric('accuracy', i)
    
if __name__ == "__main__":
    import timeit
    setup = "from __main__ import test_function"
    print (timeit.timeit("test_function()", setup= setup, number= 100))