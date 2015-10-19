from gobgift.decorators import render_to
from django.contrib.auth import logout as auth_logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q

from .models import ListGroup, Liste, Gift, Comment, Purchase
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
@render_to('mylists.html')
def mylists(request):
    user = User.objects.get(pk=request.user.pk)
    listsList = Liste.objects.filter(owner=user)
    return context(lists=listsList, user=user)


@login_required
@render_to('mygroups.html')
def mygroups(request):
    user = User.objects.get(pk=request.user.pk)
    groupList = ListGroup.objects.filter(Q(users__user=user)|Q(owner=user)).distinct()
    return context(groups=groupList, user=user)

@login_required
@render_to('grouplists.html')
def viewGroup(request, pk):
    listgroup = ListGroup.objects.get(id=pk)
    listsList = listgroup.lists.all()
    user = User.objects.get(pk=request.user.pk)
    return context(listgroup=listgroup, lists=listsList, user=user)


@login_required
@render_to('viewList.html')
def viewlist(request, pk):
    """
    View that show a list
    """
    from_group = None
    liste = Liste.objects.get(id=pk)
    #get the from_group parameter for the back button
    if request.GET.get('from_group'):
        from_group = request.GET.get('from_group')
    return context(liste=liste, from_group=from_group)


@login_required
@render_to('viewList.html')
def editList(request, pk):
    liste = Liste.objects.get(id=pk)
    if liste.owner != request.user:
        return redirect('home')
    return context(liste=liste)


class ListCreate(LoginRequiredMixin, CreateView):
    model = Liste
    template_name = "create_edit_list.html"
    form_class = ListeForm

    def get_success_url(self):
        return reverse('mylists')

    def get_form_kwargs(self):
        kwargs = super(ListCreate, self).get_form_kwargs()
        kwargs['user'] = User.objects.get(pk=self.request.user.pk)
        return kwargs


class ListEdit(LoginRequiredMixin, UpdateView):
    model = Liste
    template_name = "create_edit_list.html"
    form_class = ListeForm

    def get_success_url(self):
        return reverse('mylists')

    def get_form_kwargs(self):
        kwargs = super(ListEdit, self).get_form_kwargs()
        kwargs['user'] = User.objects.get(pk=self.request.user.pk)
        return kwargs

    def form_valid(self, form):
        return super(ListEdit, self).form_valid(form)


class ListDelete(LoginRequiredMixin, DeleteView):
    model = Liste
    template_name = "deleteList.html"

    def get_success_url(self):
        return reverse('mylists')

    def form_valid(self, form):
        return super(ListDelete, self).form_valid(form)


@login_required
def purchasedGift(request, gift_pk):
    gift = Gift.objects.get(id=gift_pk)
    if gift.purchased:
        return redirect(gift.liste.get_view_url())

    # set the gift purchased
    gift.purchased = True
    gift.save()
    # create the link between the purchase and an user
    purchase = Purchase(gift=gift, user=request.user)
    purchase.save()
    return redirect(gift.liste.get_view_url())


@login_required
def cancelPurchasedGift(request, gift_pk):
    gift = Gift.objects.get(id=gift_pk)
    if not gift.purchased:
        return redirect(gift.liste.get_view_url())

    # set the gift not purchased
    gift.purchased = False
    gift.save()
    # create the link between the purchase and an user
    purchase = Purchase.objects.filter(gift=gift, user=request.user).first()
    if purchase.user != request.user:
        return redirect(gift.liste.get_view_url())
    else:
        purchase.delete()

    return redirect(gift.liste.get_view_url())


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


class GroupCreate(LoginRequiredMixin, CreateView):
    model = ListGroup
    template_name = "create_group.html"
    form_class = GroupForm

    def get_form_kwargs(self):
        kwargs = super(GroupCreate, self).get_form_kwargs()
        kwargs['user'] = User.objects.get(pk=self.request.user.pk)
        return kwargs

    def get_success_url(self):
        return reverse('mygroups')

    def form_valid(self, form):
        response = super(GroupCreate, self).form_valid(form);
        return response


class GroupEdit(LoginRequiredMixin, UpdateView):
    model = ListGroup
    template_name = "edit_group.html"
    form_class = GroupForm

    def get_form_kwargs(self):
        kwargs = super(GroupEdit, self).get_form_kwargs()
        kwargs['user'] = User.objects.get(pk=self.request.user.pk)
        return kwargs

    def get_success_url(self):
        return reverse('mygroups')

    def form_valid(self, form):
        # messages.success(self.request, _('The group has been created with success.'))
        response = super(GroupEdit, self).form_valid(form);
        return response


class GroupDelete(LoginRequiredMixin, DeleteView):
    model = ListGroup
    template_name = "deleteGroup.html"

    def get_success_url(self):
        return reverse('mygroups')

    def form_valid(self, form):
        return super(GroupDelete, self).form_valid(form)


class GroupUserDelete(LoginRequiredMixin, DeleteView):
    model = ListGroupUser
    template_name = "deleteGroupUser.html"

    def get_success_url(self):
        return self.get_object().group.get_edit_url()

    def form_valid(self, form):
        return super(GroupUserDelete, self).form_valid(form)


class ListGroupUserCreate(LoginRequiredMixin, CreateView):
    model = ListGroupUser
    template_name = "create_edit_groupuser.html"
    form_class = ListGroupUserForm

    def dispatch(self, request, *args, **kwargs):
        self.listgroup = ListGroup.objects.get(pk=kwargs['listgroup_pk'])
        return super(ListGroupUserCreate,self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.listgroup.get_edit_url()

    def get_form_kwargs(self):
        kwargs = super(ListGroupUserCreate, self).get_form_kwargs()
        kwargs['listgroup'] = self.listgroup
        return kwargs

    def form_valid(self, form):
        return super(ListGroupUserCreate, self).form_valid(form)
