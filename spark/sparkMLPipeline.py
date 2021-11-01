from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import VectorAssembler
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("ML Pyspark") \
    .getOrCreate()


# Carga del dataset de entrenamiento
loanData = spark.createDataFrame(pd.read_csv("TrainingData.csv"))

train, test = loanData.randomSplit(weights=[0.8,0.2], seed=200)

loanData.show(n=3)


categorical_cols = ["Married/Single","House_Ownership","Car_Ownership","Profession","CITY","STATE"]
index_cols = [col + "_index" for col in categorical_cols]
# Ml pipeline
encoder = StringIndexer(inputCols=categorical_cols,outputCols=index_cols)
assembler = VectorAssembler(inputCols=index_cols,outputCol="features")
lr = LogisticRegression(maxIter=10, regParam=0.001,labelCol="Risk_Flag")
pipeline = Pipeline(stages=[encoder,assembler,lr]) 


model = pipeline.fit(train)

prediction = model.transform(train)

selected = prediction.select("id", "probability", "prediction")
for row in selected.collect():
    id, prob, prediction = row 
    print(
        "(%d) --> prob=%s, prediction=%f" % (
            id, str(prob), prediction  
        )
    ) 
    
