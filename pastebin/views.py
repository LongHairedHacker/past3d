from django.views.generic.detail import DetailView

from models import Geometry


class GeometryView(DetailView):
	model = Geometry
	pk_url_kwarg = 'id'
	context_object_name = 'geometry'
	template_name = 'pastebin/geometry.html'