from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from gobgift.core.decorators import render_to
from gobgift.groups.models import ListGroup
from .forms import WishlistForm
from .models import Wishlist


class MyLists(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = 'lists/mylists.html'

    def get_queryset(self):
        user = self.request.user
        return Wishlist.objects.filter(owner=user).distinct()


@login_required
def view_list(request, pk):
    """
    View that show a list
    """
    from_group = None
    wishlist = Wishlist.objects.get(id=pk)
    # get the from_group parameter for the back button
    if request.GET.get('from_group'):
        from_group = request.GET.get('from_group')
    return render(request, 'lists/view.html', {'liste': wishlist, 'from_group': from_group})


@login_required
@render_to('lists/view.html')
def edit_list(request, pk):
    wishlist = Wishlist.objects.get(id=pk)
    if wishlist.owner != request.user:
        return redirect('home')
    return render(request, 'lists/view.html', {'liste': wishlist})


class ListCreate(LoginRequiredMixin, CreateView):
    model = Wishlist
    template_name = "lists/create_edit.html"
    form_class = WishlistForm

    def get_success_url(self):
        return reverse('lists:mylists')

    def get_form_kwargs(self):
        kwargs = super(ListCreate, self).get_form_kwargs()
        kwargs['user'] = User.objects.get(pk=self.request.user.pk)
        return kwargs


class ListEdit(LoginRequiredMixin, UpdateView):
    model = Wishlist
    template_name = "lists/create_edit.html"
    form_class = WishlistForm

    def get_success_url(self):
        return reverse('lists:mylists')

    def get_form_kwargs(self):
        kwargs = super(ListEdit, self).get_form_kwargs()
        kwargs['user'] = User.objects.get(pk=self.request.user.pk)
        return kwargs

    def form_valid(self, form):
        return super(ListEdit, self).form_valid(form)


class ListDelete(LoginRequiredMixin, DeleteView):
    model = Wishlist
    template_name = "lists/delete.html"

    def get_success_url(self):
        return reverse('lists:mylists')

    def form_valid(self, form):
        return super(ListDelete, self).form_valid(form)
