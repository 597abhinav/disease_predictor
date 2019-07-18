from collections import defaultdict
import pickle
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import cross_validation
from sklearn import svm
from sklearn.linear_model import LogisticRegression

from utils import symptoms_list

data = pd.read_csv("Manual-Data/Training.csv")
data.head()
data.columns
df = pd.DataFrame(data)
df.head()
cols = df.columns
cols = cols[:-1]
print(len(cols))
x = df[cols]
y = df['prognosis']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

def training():
	models = [MultinomialNB(), svm.SVC(kernel='linear',probability=True), LogisticRegression(random_state=0)]
	trained_model = []
	for model in models:

		mnb = model.fit(x_train, y_train)
		print(mnb.score(x_test, y_test))

		
		print ("cross result========")
		scores = cross_validation.cross_val_score(mnb, x_test, y_test, cv=3)
		print (scores)
		print (scores.mean())

		test_data = pd.read_csv("Manual-Data/Testing.csv")

		test_data.head()

		testx = test_data[cols]
		testy = test_data['prognosis']

		mnb.score(testx, testy)
		trained_model.append(mnb)

	with open("trained_model.pickle", "wb") as f:
		pickle.dump(trained_model, f)

if __name__ == '__main__':
	training();