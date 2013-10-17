from django.forms import ModelForm
from django import forms

from models import Geometry


class GeometryForm(ModelForm):
	class Meta:
		model = Geometry
		fields = ['name', 'description', 'public', 'expiration',  'file', 'sourcefile']


class AnonymousGeometryForm(ModelForm):
	expiration =  forms.ChoiceField(choices=Geometry.EXPIRATION_CHOICES[:-1])
	class Meta:
		model = Geometry
		fields = ['name', 'description', 'public', 'expiration',  'file']

