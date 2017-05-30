from decimal import Decimal, DecimalException

import floppyforms.__future__ as forms
from django.utils import formats
from django.utils.encoding import smart_text


class TextInput(forms.TextInput):
    template_name = 'core/form_layout/textinput.html'

    def get_context(self, name, value, attrs):
        ctx = super(TextInput, self).get_context(name, value, attrs)
        ctx['attrs']['class'] = 'mdl-textfield__input'
        return ctx


class TextAreaInput(forms.Textarea):
    template_name = 'core/form_layout/textarea.html'

    def get_context(self, name, value, attrs):
        ctx = super(TextAreaInput, self).get_context(name, value, attrs)
        ctx['attrs']['class'] = 'mdl-textfield__input'
        ctx['attrs']['rows'] = '4'
        return ctx


class NumericInput(forms.NumberInput):
    template_name = 'core/form_layout/numinput.html'

    def get_context(self, name, value, attrs):
        ctx = super(NumericInput, self).get_context(name, value, attrs)
        ctx['attrs']['class'] = 'mdl-textfield__input'
        ctx['attrs']['step'] = 'any'
        ctx['attrs']['pattern'] = '-?[0-9]*(\.[0-9]+)?'
        return ctx


class TextAreaField(forms.CharField):
    widget = TextAreaInput


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
                raise forms.ValidationError(self.error_messages['invalid'],
                                            code='invalid')
        return value
