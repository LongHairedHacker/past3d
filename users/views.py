from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.sites.models import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.template import loader
from django.utils.http import int_to_base36

from pastebin.views import LastesGeometriesMixin

from forms import UserCreateForm

class UserCreate(CreateView, LastesGeometriesMixin):
	model = User
	form_class = UserCreateForm
	template_name = 'pastebin/geometry_create.html'
	email_template_name = 'users/validate_email.txt'

	def form_valid(self, form):
		res = super(UserCreate, self).form_valid(form)
		
		site_name = get_current_site(self.request).name
		uid = int_to_base36(self.object.pk)
		token = default_token_generator.make_token(self.object)

		context = {
			'email': self.object.email,
			'site_name': site_name,
			'validation_link': "%s - %s" % (uid, token),
			'user': self.object
		}

		subject = "Validate your registration at %s" % site_name
		email = loader.render_to_string(self.email_template_name, context)
		self.object.email_user(subject,email)

		return res

	def get_success_url(self):
		return reverse('login')

