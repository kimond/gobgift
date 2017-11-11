from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView

from gobgift.core.decorators import render_to
from gobgift.groups.forms import GroupForm, ListGroupUserForm
from .models import ListGroup, ListGroupUser


class MyGroups(LoginRequiredMixin, ListView):
    model = ListGroup
    template_name = 'groups/mygroups.html'

    def get_queryset(self):
        user = self.request.user
        return ListGroup.objects.select_related('owner').prefetch_related('users').filter(
            Q(users__user=user) | Q(owner=user)).distinct()


@login_required
def view_group(request, pk):
    list_group = ListGroup.objects.get(id=pk)
    lists_list = list_group.lists.all()
    user = User.objects.get(pk=request.user.pk)
    return render(request, 'groups/list.html', {'listgroup': list_group, 'lists': lists_list, 'user': user})


class GroupCreate(LoginRequiredMixin, CreateView):
    model = ListGroup
    template_name = "groups/create.html"
    form_class = GroupForm

    def get_form_kwargs(self):
        kwargs = super(GroupCreate, self).get_form_kwargs()
        kwargs['user'] = User.objects.get(pk=self.request.user.pk)
        return kwargs

    def get_success_url(self):
        return reverse('groups:mygroups')

    def form_valid(self, form):
        response = super(GroupCreate, self).form_valid(form)
        return response


class GroupEdit(LoginRequiredMixin, UpdateView):
    model = ListGroup
    template_name = "groups/edit.html"
    form_class = GroupForm

    def get_form_kwargs(self):
        kwargs = super(GroupEdit, self).get_form_kwargs()
        kwargs['user'] = User.objects.get(pk=self.request.user.pk)
        return kwargs

    def get_success_url(self):
        return reverse('groups:mygroups')

    def form_valid(self, form):
        # messages.success(self.request, _('The group has been created with success.'))
        response = super(GroupEdit, self).form_valid(form)
        return response


class GroupDelete(LoginRequiredMixin, DeleteView):
    model = ListGroup
    template_name = "groups/delete.html"

    def get_success_url(self):
        return reverse('groups:mygroups')

    def form_valid(self, form):
        return super(GroupDelete, self).form_valid(form)


class GroupUserDelete(LoginRequiredMixin, DeleteView):
    model = ListGroupUser
    template_name = "groups/delete_user.html"

    def get_success_url(self):
        return self.get_object().group.get_edit_url()

    def form_valid(self, form):
        return super(GroupUserDelete, self).form_valid(form)


class ListGroupUserCreate(LoginRequiredMixin, CreateView):
    model = ListGroupUser
    template_name = "groups/create_edit_user.html"
    form_class = ListGroupUserForm

    def dispatch(self, request, *args, **kwargs):
        self.listgroup = ListGroup.objects.get(pk=kwargs['listgroup_pk'])
        return super(ListGroupUserCreate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.listgroup.get_edit_url()

    def get_form_kwargs(self):
        kwargs = super(ListGroupUserCreate, self).get_form_kwargs()
        kwargs['listgroup'] = self.listgroup
        return kwargs

    def form_valid(self, form):
        return super(ListGroupUserCreate, self).form_valid(form)


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        query = User.objects.all()
        if self.q:
            query = query.filter(
                Q(last_name__istartswith=self.q) | Q(first_name__istartswith=self.q)
            )

        return query


class ListGroupAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        user = self.request.user
        query = ListGroup.objects.filter(Q(users__user=user) | Q(owner=user)).distinct()
        if self.q:
            query = query.filter(name__istartswith=self.q)

        return query
