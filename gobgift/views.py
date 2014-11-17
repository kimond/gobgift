from gobgift.decorators import render_to
from django.contrib.auth import logout as auth_logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Liste, Gift, Comment
from .forms import *

from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.backends.google import GooglePlusAuth
from social.backends.utils import load_backends
from social.apps.django_app.utils import psa


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')

def context(**extra):
    return dict({
        'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
        'plus_scope': ' '.join(GooglePlusAuth.DEFAULT_SCOPE),
        'available_backends': load_backends(settings.AUTHENTICATION_BACKENDS)
    }, **extra)

@render_to('home.html')
def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return redirect('done')
    return context()

@login_required
@render_to('home.html')
def done(request):
    """Login complete view, displays user data"""
    return context()

@render_to('home.html')
def validation_sent(request):
    return context(
        validation_sent=True,
        email=request.session.get('email_validation_address')
    )

@render_to('home.html')
def require_email(request):
    backend = request.session['partial_pipeline']['backend']
    return context(email_required=True, backend=backend)

@login_required
@render_to('listes.html')
def listes(request):
    listesList = Liste.objects.all()
    user = User.objects.get(pk=request.user.pk)
    return context(listes=listesList, user=user)

@login_required
@render_to('viewListe.html')
def viewliste(request, pk):
    liste = Liste.objects.get(id=pk)
    return context(liste=liste)

@login_required
@render_to('viewListe.html')
def editListe(request, pk):
    liste = Liste.objects.get(id=pk)
    if liste.owner != request.user:
        return redirect('listes')
    return context(liste=liste)



class ListeCreate(LoginRequiredMixin, CreateView):
    model = Liste
    template_name = "createListe.html"
    form_class = ListeForm

    def get_success_url(self):
        return reverse('listes')

    def get_form_kwargs(self):
        kwargs = super(ListeCreate, self).get_form_kwargs()
        kwargs['user'] = User.objects.get(pk=self.request.user.pk)
        return kwargs


class GiftCreate(LoginRequiredMixin, CreateView):
    model = Gift
    template_name = "createListe.html"
    form_class = GiftForm

    def dispatch(self, request, *args, **kwargs):
        self.liste = Liste.objects.get(pk=kwargs['liste_pk'])
        return super(GiftCreate,self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.liste.get_view_url()

    def get_form_kwargs(self):
        kwargs = super(GiftCreate, self).get_form_kwargs()
        kwargs['liste'] = self.liste
        return kwargs

    def form_valid(self, form):
        return super(GiftCreate, self).form_valid(form)

class GiftEdit(LoginRequiredMixin, UpdateView):
    model = Gift
    template_name = "createListe.html"
    form_class = GiftForm

    def get_success_url(self):
        return self.object.liste.get_view_url()

    def form_valid(self, form):
        return super(GiftEdit, self).form_valid(form)

class GiftDelete(LoginRequiredMixin, DeleteView):
    model = Gift
    template_name = "deleteGift.html"

    def get_success_url(self):
        return self.object.liste.get_view_url()

    def form_valid(self, form):
        return super(GiftEdit, self).form_valid(form)


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = "createListe.html"
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.gift = Gift.objects.get(pk=kwargs['gift_pk'])
        return super(CommentCreate,self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.gift.liste.get_view_url()

    def get_form_kwargs(self):
        kwargs = super(CommentCreate, self).get_form_kwargs()
        kwargs['gift'] = self.gift
        kwargs['user'] = User.objects.get(pk=self.request.user.pk)
        return kwargs

    def form_valid(self, form):
        return super(CommentCreate, self).form_valid(form)

