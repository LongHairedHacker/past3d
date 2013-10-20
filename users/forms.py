from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

class UserCreateForm(ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
	
	class Meta:
		model = User
		fields = ['username', 'email']


	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		
		return password1


	def clean_email(self):
		email = self.cleaned_data.get("email")
		if User.objects.filter(email = email):
			raise forms.ValidationError("Email already in use.")

		return email


	def save(self, commit=True):
		user = super(UserCreateForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		user.is_active = False
		if commit:
			user.save()
		return user