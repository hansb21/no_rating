from usuario import usuario

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import preprocessing

user = usuario(id=int(input("entre id: ")))

x = np.arange(2).reshape(-1, 1)
y = np.array([0.0784313, 0.51829268])
lab_encoder = preprocessing.LabelEncoder()
train_y = lab_encoder.fit_transform(y)
print(x)
print(train_y)
model = LogisticRegression(solver="liblinear", random_state=0).fit(x, train_y)
print(model.classes_)
print(model.predict_proba(x))
print(model.predict(x))
