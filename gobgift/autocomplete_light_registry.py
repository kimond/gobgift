import autocomplete_light
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from gobgift.models import ListGroup

class UserAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['first_name', 'last_name', 'username']
    attrs = {
        'placeholder': 'Search for user',
        'class': 'mdl-textfield__input',
    }
    widget_attrs = {
        'class': 'mdl_autocomplete_light',
    }

    def choice_label(self, choice):
        """
        Return the human-readable representation of a choice. This simple
        implementation returns the textual representation.
        """
        text = choice.first_name + " " + choice.last_name
        return force_text(text)

class ListGroupAutocomplete(autocomplete_light.AutocompleteModelTemplate):
    search_fields = ['name']
    attrs = {
        'placeholder': 'Type a group name',
        'class': 'mdl-textfield__input',
    }
    widget_attrs = {
        'class': 'mdl_autocomplete_light',
    }
    def choices_for_request(self):
        user = self.request.user
        self.choices = self.choices.filter(Q(users__user=user)|Q(owner=user)).distinct()

        return super(ListGroupAutocomplete, self).choices_for_request()


autocomplete_light.register(User, UserAutocomplete)
autocomplete_light.register(ListGroup, ListGroupAutocomplete)
