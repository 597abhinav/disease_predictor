from collections import defaultdict
import pickle
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

from utils import symptoms_list

data = pd.read_csv("Manual-Data/Training.csv")
df = pd.DataFrame(data)
cols = df.columns
cols = cols[:-1]

x = df[cols]
y = df['prognosis']

d = defaultdict(set)

for i in range(4920):
	for index, val in enumerate(x.iloc[i]):
		if val == 1:
			d[y.iloc[i]].add(symptoms_list[index])

models = []
with open("trained_model.pickle", "rb") as f:
	models = pickle.load(f)

def disease(user_symptoms):
	result = []
	for mnb in models:
		# print(cols[52])
		sample_x = user_symptoms
		# print(len(sample_x))
		sample_x = np.array(sample_x).reshape(1,len(sample_x))
		# print(sample_x)
		# print(mnb.predict(sample_x))
		# print(mnb.predict_proba(sample_x))
		temp = pd.DataFrame(mnb.predict_proba(sample_x), columns=mnb.classes_).to_dict()
		final_dict = {}

		for key, val in temp.items():
			final_dict[key] = val[0]
		# print(final_dict)

		temp = sorted(final_dict.items(), key=lambda item: item[1],reverse=True)
		for val in temp[:3]:
			result.append(val)
	return result[:3]

############################################################################################################## result

## taking symptoms
def get_symptoms_list(disease):
	symp_mpd=list(d[disease])
	return symp_mpd


def diagnosis(symp_mpd, intens_mpd):
	i=0
	user_symptoms = [0]*132
	for i in range(len(cols)):				
		if(cols[i] in symp_mpd):
			user_symptoms[i]=intens_mpd[cols[i]] #take values from intense mpd
		else:
			user_symptoms[i]=0

	prob_diseases = disease(user_symptoms)
	return prob_diseases[0]


if __name__ == "__main__":
	user_symptoms = [0.75 if i%2 == 0 else 1 for i in range(len(cols))]
	prob_diseases = disease(user_symptoms)

	print("\n probable diseases ")
	print(prob_diseases)
	# print("\n symptoms of most_prob_disease")
	# print(d[prob_diseases[0][0]])

	# diagnosis("Fungal infection")





# ###################################################### take intensities of each symptoms of most_prob_disease

# mpd=prob_diseases[0][0]
# symp_mpd=list(d[prob_diseases[0][0]])
# # print(symp_mpd)
# # print("\n most_prob_disease ")
# # print(mpd)
# #instensity of symptoms most prob disease

# intens_mpd={}  		

# ################################take input from forntend

# for i in symp_mpd:
# 	print(i)
# 	if i == "dehydration":
# 		intens_mpd[i]=0.25
# 	elif i == "vomiting":
# 		intens_mpd[i]=0.25
# 	elif i=="diarrhoe":
# 		intens_mpd[i]=0.01
# 	else:
# 		intens_mpd[i]=0.02

# print(intens_mpd)
# # reverse mapping 
# i=0
# for i in range(len(cols)):				
# 	if(cols[i] in symp_mpd):
# 		user_symptoms[i]=intens_mpd[cols[i]] #take values from intense mpd
# 	else:
# 		user_symptoms[i]=0
# print(user_symptoms)


# prob_diseases = disease(user_symptoms)
# print("\n probable diseases ")
# print(prob_diseases)





