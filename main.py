from flask import Flask
from flask import render_template, redirect, url_for,request, flash

from forms import SubmissionForm
import geocoder
from model import disease, get_symptoms_list, diagnosis
import reverse_geocoder as rg 
import pprint 
from utils import get_symptoms
import requests, json 


app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'


@app.route('/', methods=['GET', 'POST'])
def index():
	form = SubmissionForm()
	val = False
	prob_disease = []
	if request.method == 'POST':
		user_symptoms = [0]*132
		user_symptoms = get_symptoms(request, user_symptoms)
		if all(val == 0 for val in user_symptoms):
			flash("Provide Symptoms for Prediction!!")
			return redirect('/')
		prob_disease = disease(user_symptoms)
		val = True

	return render_template("index.html", form=form, val=val, prob_disease=prob_disease)


values = {'Very Low': 0, 'Low': 0.25, 'Medium': 0.5, 'High': 0.75, "Very High": 1}

@app.route('/diagnosis/<disease>', methods=['GET', 'POST'])
def prediction(disease):
	symptoms = get_symptoms_list(disease)
	intens_mpd = {}
	disease_prob = ()
	val = False
	if request.method == "POST":
		for sympt in symptoms:
			intens_mpd[sympt] = values[request.form.getlist(sympt)[0]]
		# print(symptoms, intens_mpd)
		disease_prob = diagnosis(symptoms, intens_mpd)
		val = True

	return render_template("diagnosis.html", symptoms=symptoms, val=val, result=disease_prob)
	# return render_template("predict.html", prob_disease=prob_disease)


def reverseGeocode(coordinates): 
	    result = rg.search(coordinates) 
	    for key in  result:
	    	for x, val in key.items():
	    		if x == 'name':
	    			return(val)


@app.route("/consult-doctor", methods=['GET', 'POST'])
def c_doctor():
	g = geocoder.ip('me')
	# print(g.latlng)
	place=""
	coordinates =(g.latlng) 
	      
	place=reverseGeocode(coordinates) 
	# print(place)

	

	# enter your api key here 
	api_key = 'AIzaSyC5EY379oJ4RmMaMR69O-qmjM53RVGcnDo'

	# url variable store url 
	url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

	# The text string on which to search 
	query = "doctors in "+place

	# get method of requests module 
	# return response object 
	r = requests.get(url + 'query=' + query +
							'&key=' + api_key) 

	# json method of response object convert 
	# json format data into python format data 
	x = r.json() 

	# now x contains list of nested dictionaries 
	# we know dictionary contain key value pair 
	# store the value of result key in variable y 
	y = x['results'] 

	# keep looping upto lenght of y
		
	# Print value corresponding to the 
	# 'name' key at the ith index of y  

	# print("y ")
	# print(y);
	result = []
	for i in range(len(y)): 
		# print(y[i]['name']+str(y[i]['geometry']['location']['lat'])+str(y[i]['geometry']['location']['lng'])+"\n")
		temp = [y[i]['name'], y[i]['geometry']['location']['lat'], y[i]['geometry']['location']['lng']]
		result.append(temp)
		# print(y[i]['geometry']['location']['lat'])
		# print(y[i]) 

	return render_template("consultation.html", result=json.dumps(result), coordinates=json.dumps(coordinates))

	#################

if __name__ == '__main__':
	app.run(debug=True)