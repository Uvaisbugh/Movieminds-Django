from django import forms
from .models import *
from django import forms
from .models import Comment
from Accounts.models import UserProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile

class BioUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write something about yourself...'}),
        }
    
class ProfileEditForm(forms.ModelForm):
    # Fields from User model
    email = forms.EmailField(required=True, label="Email Address")
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    username = forms.CharField(max_length=30, required=True, label="Username")

    # Field from UserProfile model
    profile_picture = forms.ImageField(required=False, label="Profile Picture")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_picture']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pass the user instance explicitly
        super(ProfileEditForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['username'].initial = user.username
            if hasattr(user, 'profile'):
                self.fields['profile_picture'].initial = user.profile.profile_picture

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(username=self.instance.username).exists():
            raise ValidationError("This email address is already in use.")
        return email

    def save(self, commit=True):
        # Save User model fields
        user = self.instance
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        if commit:
            user.save()

        # Save UserProfile fields
        if hasattr(user, 'profile'):
            profile = user.profile
            profile.profile_picture = self.cleaned_data['profile_picture']
            if commit:
                profile.save()

        return user


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Correctly call the parent class's __init__

        # Corrected the field name to 'content' as defined in the `fields` and model
        self.fields['content'].widget.attrs.update({
            'class': "text-gray-600 focus:outline-none focus:border focus:border-pgreen font-normal w-full flex items-center p-3 text-base rounded border"
        })

    class Meta:
        model = Comment
        fields = ('content',)  # Ensure the field matches the model's attribute
        labels = {
            "content": "Change your comment below"  # Fixed the key to match the field name
        }

class AddMovieForm(forms.ModelForm):
    actors = forms.ModelMultipleChoiceField(
        queryset=Actor.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # or forms.SelectMultiple for dropdown
        required=False,
        label="Select Actors"
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a category",
        required=True
    )
    poster = forms.ImageField(required=False, label="Movie Poster")
    
    class Meta:
        model = Movie
        fields = ['title', 'description', 'category', 'actors', 'poster','release_date', 'youtube_link']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter movie title'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter a brief description'}),
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'title': 'Movie Title',
            'description': 'Description',
        }

