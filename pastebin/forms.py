from django.forms import ModelForm

from models import Geometry


class GeometryForm(ModelForm):
	class Meta:
		model = Geometry
		fields = ['name', 'description', 'file', 'sourcefile']