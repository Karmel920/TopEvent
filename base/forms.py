from django.forms import ModelForm
from .models import Project, UserDetails
from django.contrib.auth.models import User


class UserDetailsCreationForm(ModelForm):
    class Meta:
        model = UserDetails
        fields = ['name', 'email']


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class UserDetailsForm(ModelForm):
    class Meta:
        model = UserDetails
        fields = ['avatar', 'bio', 'name', 'email']
