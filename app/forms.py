from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, FloatField
from wtforms.validators import DataRequired, Optional

class SymptomForm(FlaskForm):
    symptoms = SelectMultipleField('Symptômes', coerce=int, validators=[DataRequired()])
    latitude = FloatField('Latitude', validators=[Optional()])
    longitude = FloatField('Longitude', validators=[Optional()])
    submit = SubmitField('Obtenir un pré-diagnostic')