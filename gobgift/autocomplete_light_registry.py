import autocomplete_light
from django.contrib.auth.models import User
from gobgift.models import ListGroup

class UserAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^first_name', 'last_name']

class ListGroupAutocomplete(autocomplete_light.AutocompleteModelTemplate):
    search_fields = ['name']
    attrs = {
        'placeholder': 'Choose groups ',
        'class': 'mdl-textfield__input',
    }
    widget_attrs = {
        'class': 'mdl_autocomplete_light',
    }


autocomplete_light.register(User, UserAutocomplete)
autocomplete_light.register(ListGroup, ListGroupAutocomplete)
