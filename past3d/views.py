from django.views.generic.base import TemplateView

from pastebin.views import LastesGeometriesMixin


class HomeView(TemplateView, LastesGeometriesMixin):
	template_name = 'home.html'
