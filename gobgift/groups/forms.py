from dal import autocomplete
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from gobgift.core.forms import CharField
from .models import ListGroupUser, ListGroup


class GroupForm(forms.ModelForm):
    name = CharField()

    class Meta:
        model = ListGroup
        fields = ['name', 'owner']

    def __init__(self, user=None, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.user = user

        self.fields['owner'].required = False
        self.fields['owner'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super(GroupForm, self).clean()
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            cleaned_data['owner'] = instance.owner
        else:
            cleaned_data['owner'] = self.user

        return cleaned_data


class ListGroupUserForm(forms.ModelForm):
    is_admin = forms.BooleanField(required=False)
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='user-autocomplete',
            attrs={
                'data-placeholder': 'User',
            }
        )
    )

    class Meta:
        model = ListGroupUser
        fields = ['user', 'is_admin', 'group']

    def __init__(self, listgroup=None, *args, **kwargs):
        super(ListGroupUserForm, self).__init__(*args, **kwargs)

        self.listgroup = listgroup
        self.fields['group'].required = False
        self.fields['group'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super(ListGroupUserForm, self).clean()
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            cleaned_data['group'] = instance.group
        else:
            cleaned_data['group'] = self.listgroup
        if not cleaned_data.get('user'):
            raise forms.ValidationError(_('Please choose an user.'))
        if ListGroupUser.objects.filter(group=cleaned_data['group'], user=cleaned_data['user']).exists():
            raise forms.ValidationError(_('This user is already in the group.'))
        elif self.listgroup.owner == cleaned_data['user']:
            raise forms.ValidationError(_('This user is the owner of the group'))

        return cleaned_data
