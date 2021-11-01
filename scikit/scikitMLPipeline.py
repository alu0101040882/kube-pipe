import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder


# Carga del dataset de entrenamiento
loanData = pd.read_csv("TrainingData.csv")


# Visualizar las primeras entradas para comprobar que se haya cargado correctamenteF
print(loanData.head())  


X_train,X_test, y_train, y_test = train_test_split(loanData.iloc[:,[1,2,3,4,5,6,7,8,9,10,11]],loanData.iloc[:,[12]],test_size=0.2)



#Creación de los pipelines
LogisticRegressionPipeline = make_pipeline(OneHotEncoder(handle_unknown='ignore'),LogisticRegression())

""" DecisionTreePipeline = make_pipeline(OneHotEncoder(handle_unknown='ignore'),DecisionTreeClassifier())

RandomForestPipeline = make_pipeline(OneHotEncoder(handle_unknown='ignore'),RandomForestClassifier()) """


#Creacion de la lista de los pipelines
pipelines = [LogisticRegressionPipeline] 

for pipeline in pipelines:
    pipeline.fit(X_train, y_train)


for i, model in enumerate(pipelines):
    print("Precision del pipeline {} : {} %".format(i , model.score(X_test,y_test)))