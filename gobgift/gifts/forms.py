import tempfile
from io import StringIO

from PIL import Image
from django import forms

from gobgift.core.forms import CharField, TextAreaField
from .models import Gift, Comment


class GiftForm(forms.ModelForm):
    name = forms.CharField()
    description = TextAreaField(required=False)
    price = forms.DecimalField(required=False)
    website = forms.CharField(required=False)
    store = CharField(required=False)

    class Meta:
        model = Gift
        fields = ['wishlist', 'name', 'photo', 'description', 'price', 'website', 'store']

    def __init__(self, wishlist=None, *args, **kwargs):
        super(GiftForm, self).__init__(*args, **kwargs)

        self.wishlist = wishlist
        self.fields['wishlist'].required = False
        self.fields['wishlist'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super(GiftForm, self).clean()
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            cleaned_data['wishlist'] = instance.wishlist
        else:
            cleaned_data['wishlist'] = self.wishlist

        photo = cleaned_data.get('photo')
        if not photo:
            return cleaned_data
        photo_file = tempfile.TemporaryFile()
        photo_file.write(photo.read())
        photo_io = Image.open(photo_file)
        # valid if image width is grester than 1024
        photo_width, photo_height = photo_io.size
        if photo_width > 1024:
            new_width = 1024
            new_height = int(new_width * photo_height / photo_width)
            photo_io = photo_io.resize((new_width, new_height), Image.ANTIALIAS)
            photo_file = tempfile.TemporaryFile()
            photo_io.save(photo_file, 'JPEG')
            photo.file = photo_file

        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['gift', 'user', 'text']

    def __init__(self, gift=None, user=None, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

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
