#from django import forms
from django.forms.models import inlineformset_factory
from .models import ListGroup, ListGroupUser, Liste, Gift, Comment
from PIL import Image
import StringIO
import autocomplete_light
import floppyforms.__future__ as forms

class TextInput(forms.TextInput):
    template_name = 'gobgift/form_layout/textinput.html'
    def get_context(self, name, value, attrs):
        ctx = super(TextInput, self).get_context(name, value, attrs)
        ctx['attrs']['class'] = 'mdl-textfield__input'
        return ctx

class NumericInput(forms.NumberInput):
    template_name = 'gobgift/form_layout/numinput.html'
    def get_context(self, name, value, attrs):
        ctx = super(NumericInput, self).get_context(name, value, attrs)
        ctx['attrs']['class'] = 'mdl-textfield__input'
        ctx['attrs']['pattern'] = '-?[0-9]*(\.[0-9]+)?'
        return ctx


class CharField(forms.CharField):
    widget = TextInput


class NumField(forms.CharField):
    widget = NumericInput

    def to_python(self, value):
        """
        Validates that the input is a decimal number. Returns a Decimal
        instance. Returns None for empty values. Ensures that there are no more
        than max_digits in the number, and no more than decimal_places digits
        after the decimal point.
        """
        if value in self.empty_values:
            return None
        if self.localize:
            value = formats.sanitize_separators(value)
            value = smart_text(value).strip()
            try:
                value = Decimal(value)
            except DecimalException:
                raise ValidationError(self.error_messages['invalid'], code='invalid')
        return value


class ListeForm(autocomplete_light.SelectMultipleHelpTextRemovalMixin,
                autocomplete_light.VirtualFieldHandlingMixin,
                autocomplete_light.GenericM2MRelatedObjectDescriptorHandlingMixin,
                forms.ModelForm):
    name = CharField()
    groups = autocomplete_light.ModelMultipleChoiceField('ListGroupAutocomplete')
    class Meta:
        model = Liste
        fields = ['owner','name', 'groups']

    def __init__(self, user=None, *args, **kwargs):
        super (ListeForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['owner'].required = False
        self.fields['owner'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super(ListeForm, self).clean()
        instance = getattr(self, 'instance', None)
        cleaned_data['owner'] = self.user

        return cleaned_data

class GiftForm(forms.ModelForm):
    name = CharField()
    price = NumField(required=False)
    siteweb = CharField(required=False)
    store = CharField(required=False)
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

        photo = cleaned_data.get('photo')
        if not photo:
            return cleaned_data
        photo_file = StringIO.StringIO(photo.read())
        photoio = Image.open(photo_file)
        # valid if image width is grester than 1024
        photo_width, photo_height = photoio.size
        if photo_width > 1024:
            new_width = 1024
            new_height = new_width * photo_height / photo_width
            photoio = photoio.resize((new_width, new_height), Image.ANTIALIAS)
            photo_file = StringIO.StringIO()
            photoio.save(photo_file, 'JPEG')
            photo.file = photo_file


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
    name = CharField()
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

class ListGroupUserForm(forms.ModelForm):
    user = autocomplete_light.ModelChoiceField('UserAutocomplete')
    class Meta:
        model = ListGroupUser
        fields = ['user','is_admin','group']

    def __init__(self, listgroup=None, *args, **kwargs):
        super (ListGroupUserForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        self.listgroup = listgroup
        self.fields['group'].required = False
        self.fields['group'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super(ListGroupUserForm, self).clean()
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            cleaned_data['group'] = instance.listgroup
        else:
            cleaned_data['group'] = self.listgroup
            if ListGroupUser.objects.filter(group=cleaned_data['group'], user=cleaned_data['user']).exists():
                raise forms.ValidationError( 'Solution with this Name already exists for this problem')


        return cleaned_data
