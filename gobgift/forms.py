from django import forms
from django.forms.models import inlineformset_factory
from .models import ListGroup, ListGroupUser, Liste, Gift, Comment


class ListeForm(forms.ModelForm):
    class Meta:
        model = Liste
        fields = ['owner','name']

    def __init__(self, user=None, *args, **kwargs):
        super (ListeForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['owner'].required = False
        self.fields['owner'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super(ListeForm, self).clean()
        cleaned_data['owner'] = self.user

        return cleaned_data

class GiftForm(forms.ModelForm):
    class Meta:
        model = Gift
        fields = ['liste','name', 'photo', 'price', 'siteweb', 'store']

    def __init__(self, liste=None, *args, **kwargs):
        super (GiftForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        self.liste = liste
        self.fields['liste'].required = False
        self.fields['liste'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super(GiftForm, self).clean()
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            cleaned_data['liste'] = instance.liste
        else:
            cleaned_data['liste'] = self.liste


        return cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['gift','user', 'text']

    def __init__(self, gift=None, user=None, *args, **kwargs):
        super (CommentForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        self.gift = gift
        self.user = user
        self.fields['gift'].required = False
        self.fields['gift'].widget = forms.HiddenInput()
        self.fields['user'].required = False
        self.fields['user'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            cleaned_data['gift'] = instance.gift
            cleaned_data['user'] = instance.user
        else:
            cleaned_data['gift'] = self.gift
            cleaned_data['user'] = self.user



        return cleaned_data


class GroupForm(forms.ModelForm):
    class Meta:
        model = ListGroup
        fields = ['name', 'owner']

    def __init__(self, user=None, *args, **kwargs):
        super (GroupForm, self).__init__(*args, **kwargs)
        self.user = user

        self.fields['owner'].required = False
        self.fields['owner'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super(GroupForm, self).clean()
        cleaned_data['owner'] = self.user

        return cleaned_data

GroupUserFormSet = inlineformset_factory(ListGroup, ListGroupUser, extra=2)
