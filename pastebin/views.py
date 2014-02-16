from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django.views.generic.base import ContextMixin
from django.core.exceptions import PermissionDenied
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from forms import GeometryForm, AnonymousGeometryForm
from models import Geometry


class LastesGeometriesMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super(LastesGeometriesMixin, self).get_context_data(**kwargs)
		context['latest_geometries'] = Geometry.get_latest()
		return context

class GeometryListView(ListView, LastesGeometriesMixin):
    queryset = Geometry.objects.all().filter(public = True).order_by('date')
    paginate_by = 50
    paginate_orphans = 25
    page_kwarg = 'page'
    context_object_name = 'geometries'
    template_name = 'pastebin/geometry_list.html'


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

class GeometryDelete(DeleteView, LastesGeometriesMixin):
    model = Geometry
    pk_url_kwarg = 'id'
    template_name = 'pastebin/geometry_delete.html'
    success_url ='/'

    def check_user(self, request):
        obj = self.get_object()
        if obj.user and obj.user.id != request.user.id:
            raise PermissionDenied

    def get(self, request, *args, **kwargs):
        self.check_user(request)
        return super(GeometryDelete,self).get(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.check_user(request)
        return super(GeometryDelete,self).delete(self, request, *args, **kwargs)