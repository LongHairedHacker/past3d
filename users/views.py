from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.sites.models import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.template import loader
from django.utils.http import int_to_base36
from django.http import  Http404

from pastebin.views import LastesGeometriesMixin

from forms import UserCreateForm

class UserCreate(CreateView, LastesGeometriesMixin):
	model = User
	form_class = UserCreateForm
	template_name = 'users/signup.html'

	def get_success_url(self):
		return reverse('send_confirmation', kwargs={'user_id' : self.object.pk})



class SendConfirmationView(TemplateView, LastesGeometriesMixin):
	template_name = 'users/send_confirmation.html'
	email_template_name = 'users/confirmation_email.txt'

	def get_context_data(self, **kwargs):
		context = super(SendConfirmationView, self).get_context_data(**kwargs)
		context['confirm_user'] = User.objects.get(id=kwargs['user_id'])
		return context

	def get(self, request, *args, **kwargs):
		try:
			user = User.objects.get(id=kwargs['user_id'])
		except User.DoesNotExist:
			raise Http404

		if user.is_active:
			raise Http404
			
		site_name = get_current_site(self.request).name
		uid = int_to_base36(user.pk)
		token = default_token_generator.make_token(user)
		link = request.build_absolute_uri(reverse('check_confirmation', kwargs={'user_id' : user.pk, 'token' : token}))

		context = {
			'email': user.email,
			'site_name': site_name,
			'validation_link': link,
			'user': user
		}

		subject = "Validate your registration at %s" % site_name
		email = loader.render_to_string(self.email_template_name, context)
		user.email_user(subject,email)


		return super(SendConfirmationView,self).get(self, request, *args, **kwargs)
		


class CheckConfirmationView(TemplateView, LastesGeometriesMixin):
	template_name = 'users/check_confirmation.html'

	def get_context_data(self, **kwargs):
		context = super(CheckConfirmationView, self).get_context_data(**kwargs)
		context['confirm_user'] = User.objects.get(id=kwargs['user_id'])
		return context

	def get(self, request, *args, **kwargs):
		try:
			user = User.objects.get(id=kwargs['user_id'])
		except User.DoesNotExist:
			raise Http404

		if user.is_active:
			raise Http404

		if not default_token_generator.check_token(user,kwargs['token']):
			raise Http404

		user.is_active = True
		user.save()

		print "Acitvating %s" % user.username

		return super(CheckConfirmationView,self).get(self, request, *args, **kwargs)