from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Required, Optional

from utils import symptoms_list

choices = [(index, name) for index, name in enumerate(symptoms_list)]
class SubmissionForm(FlaskForm):
	symptoms = SelectMultipleField('Symptoms', 
					default=choices[0],
					choices=choices[:40],
					validators=[Optional()])
	symptoms1 = SelectMultipleField('Symptoms', 
					default=choices[40],
					choices=choices[40:80],
					validators=[Optional()])
	symptoms2 = SelectMultipleField('Symptoms',
					default=choices[80], 
					choices=choices[80:],
					validators=[Optional()])
	submit = SubmitField('PREDICTION RESULTS')
