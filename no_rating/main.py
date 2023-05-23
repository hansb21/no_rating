from usuario import usuario

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import preprocessing

user = usuario(id=int(input("entre id: ")))

tmpnota = [user.array_nota[movie]['nota'] for movie in user.array_nota.keys()]

x = np.arange(len(tmpnota)).reshape(-1, 1)
y = np.array(tmpnota)
lab_encoder = preprocessing.LabelEncoder()
train_y = lab_encoder.fit_transform(y)
model = LogisticRegression(solver="liblinear", random_state=0).fit(x, train_y)
print(model.classes_)
print(model.predict_proba(x))
print(model.predict(x))
