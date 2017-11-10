from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView

from gobgift.gifts.forms import GiftForm, CommentForm
from gobgift.wishlists.models import Wishlist
from .models import Gift, Purchase, Comment


@login_required
def purchase_gift(request, gift_pk):
    gift = Gift.objects.get(id=gift_pk)
    if gift.purchased:
        return redirect(gift.wishlist.get_view_url())

    # set the gift purchased
    gift.purchased = True
    gift.save()
    # create the link between the purchase and an user
    purchase = Purchase(gift=gift, user=request.user)
    purchase.save()
    return redirect(gift.wishlist.get_view_url())


@login_required
def cancel_purchase_gift(request, gift_pk):
    gift = Gift.objects.get(id=gift_pk)
    if not gift.purchased:
        return redirect(gift.wishlist.get_view_url())

    # set the gift not purchased
    gift.purchased = False
    gift.save()
    # create the link between the purchase and an user
    purchase = Purchase.objects.filter(gift=gift, user=request.user).first()
    if purchase.user != request.user:
        return redirect(gift.wishlist.get_view_url())
    else:
        purchase.delete()

    return redirect(gift.wishlist.get_view_url())


class GiftCreate(LoginRequiredMixin, CreateView):
    model = Gift
    template_name = "gifts/create_edit.html"
    form_class = GiftForm

    def dispatch(self, request, *args, **kwargs):
        self.wishlist = Wishlist.objects.get(pk=kwargs['liste_pk'])
        return super(GiftCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.wishlist.get_view_url()

    def get_form_kwargs(self):
        kwargs = super(GiftCreate, self).get_form_kwargs()
        kwargs['wishlist'] = self.wishlist
        return kwargs

    def form_valid(self, form):
        return super(GiftCreate, self).form_valid(form)


class GiftEdit(LoginRequiredMixin, UpdateView):
    model = Gift
    template_name = "gifts/create_edit.html"
    form_class = GiftForm

    def get_success_url(self):
        return self.object.wishlist.get_view_url()

    def form_valid(self, form):
        return super(GiftEdit, self).form_valid(form)


class GiftDelete(LoginRequiredMixin, DeleteView):
    model = Gift
    template_name = "gifts/delete.html"

    def get_success_url(self):
        return self.object.wishlist.get_view_url()

    def form_valid(self, form):
        return super(GiftDelete, self).form_valid(form)


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = "lists/create.html"
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.gift = Gift.objects.get(pk=kwargs['gift_pk'])
        return super(CommentCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.gift.wishlist.get_view_url()

    def get_form_kwargs(self):
        kwargs = super(CommentCreate, self).get_form_kwargs()
        kwargs['gift'] = self.gift
        kwargs['user'] = User.objects.get(pk=self.request.user.pk)
        return kwargs

    def form_valid(self, form):
        return super(CommentCreate, self).form_valid(form)
