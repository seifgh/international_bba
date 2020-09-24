from django import forms


from .models import *


class SubsriberForm( forms.ModelForm ):

    class Meta:
        model = Subscriber
        exclude = ('creation_date',)

class CatalogEmailForm( forms.ModelForm ):

    class Meta:
        model = CatalogEmail
        exclude = ('is_viewed','creation_date')

class RegistrationForm( forms.ModelForm ):

    class Meta:
        model = Registration
        exclude = ('is_viewed','creation_date')


class TrainerForm( forms.ModelForm ):

    class Meta:
        model = Trainer
        exclude = ('is_viewed','verification_key', 'is_verified','creation_date')

class ContactForm( forms.ModelForm ):

    class Meta:
        model = Contact
        exclude = ('is_viewed','creation_date', 'creation_date')
