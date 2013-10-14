from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django.views.generic.base import ContextMixin

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

    def get_context_data(self, **kwargs):
		context = super(CreateView, self).get_context_data(**kwargs)
		context['latest_geometries'] = Geometry.get_latest()
		return context