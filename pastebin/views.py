from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse

from forms import GeometryForm
from models import Geometry


class GeometryView(DetailView):
	model = Geometry
	pk_url_kwarg = 'id'
	context_object_name = 'geometry'
	template_name = 'pastebin/geometry.html'


class GeometryCreate(CreateView):
    model = Geometry
    form_class = GeometryForm
    template_name = 'pastebin/geometry_create.html'

    def get_success_url(self):
    	return reverse('geometry_details', kwargs={'id' :self.object.id})