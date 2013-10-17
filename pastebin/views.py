from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django.views.generic.base import ContextMixin

from forms import GeometryForm, AnonymousGeometryForm
from models import Geometry


class LastesGeometriesMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super(LastesGeometriesMixin, self).get_context_data(**kwargs)
		context['latest_geometries'] = Geometry.get_latest()
		return context


class GeometryView(DetailView):
	model = Geometry
	pk_url_kwarg = 'id'
	context_object_name = 'geometry'
	template_name = 'pastebin/geometry.html'


class GeometryCreate(CreateView, LastesGeometriesMixin):
    model = Geometry
    template_name = 'pastebin/geometry_create.html'

    def get_success_url(self):
    	return reverse('geometry_details', kwargs={'id' :self.object.id})

    def get_form_class(self):
    	if self.request.user.is_authenticated() :
    		return GeometryForm
    	else:
    		return AnonymousGeometryForm

    def form_valid(self, form):
    	res = super(GeometryCreate, self).form_valid(form)
		
    	if self.request.user.is_authenticated() :
    		self.object.user = self.request.user
    		self.object.save()

    	return res