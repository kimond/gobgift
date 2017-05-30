from dal import autocomplete
from django import forms

from gobgift.core.forms import CharField
from gobgift.groups.models import ListGroup
from .models import Wishlist


class WishlistForm(autocomplete.FutureModelForm):
    name = CharField()
    groups = forms.ModelMultipleChoiceField(
        queryset=ListGroup.objects.all(),
        required=False,
        widget=autocomplete.ModelSelect2Multiple(
            url='listgroup-autocomplete',
            attrs={
                'data-placeholder': 'Groups',
            }
        )
    )

    class Meta:
        model = Wishlist
        fields = ['owner', 'name', 'groups']

    def __init__(self, user=None, *args, **kwargs):
        super(WishlistForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['owner'].required = False
        self.fields['owner'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super(WishlistForm, self).clean()
        cleaned_data['owner'] = self.user

        return cleaned_data
