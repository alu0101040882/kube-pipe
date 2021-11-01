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




enc = OneHotEncoder(handle_unknown='ignore',sparse=True)



enc = enc.fit(X_train)
X_train = enc.transform(X_train)
X_test = enc.transform(X_test)
