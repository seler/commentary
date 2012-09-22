# -*- coding: utf-8 -*-
from django.views.generic import CreateView, UpdateView
from django.forms.models import modelform_factory
from .models import Comm, MyUser
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.http import Http404
from django.shortcuts import render_to_response
from django.core.mail import send_mail
from django.template import RequestContext


from django import forms


class UserForm(forms.Form):
    users = list(MyUser.objects.all().order_by('username'))

    user = forms.ChoiceField(
            choices=[(u.id, u.username) for u in users],
            label=u"Wybierz użytkownika dla którego chcesz wyświetlić ranking")


@login_required
def home(request):
    user = MyUser.objects.get(id=request.user.id)

    a_todo = user.comm_user_a.filter(point_a__isnull=True, point_b__isnull=False)
    a_waiting = user.comm_user_a.filter(point_a__isnull=True, point_b__isnull=True)
    b_todo = user.comm_user_b.filter(point_b__isnull=True)
    b_waiting = user.comm_user_b.filter(point_b__isnull=False, point_a__isnull=True)

    users = list(MyUser.objects.all())
    users = sorted(users, key=MyUser.rating)

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            selected_user_id = form.cleaned_data.get('user')
            selected_user = MyUser.objects.get(id=selected_user_id)
    else:
        selected_user = user
        form = UserForm(initial={'user': selected_user.id})

    a_trans = selected_user.comm_user_a.all()
    b_trans = selected_user.comm_user_b.all()

    return render_to_response(
        'comm/index.html',
        {
            'form': form,
            'user': user,
            "selected_user": selected_user,
            'a_todo': a_todo,
            'a_waiting': a_waiting,
            'a_closed': a_trans,
            'b_todo': b_todo,
            'b_waiting': b_waiting,
            'b_closed': b_trans,
        }, RequestContext(request))


class CreateComm(CreateView):
    model = Comm
    success_url = '/'

    def get_form_class(self):
        form_class = modelform_factory(
            self.model,
            exclude=('user_a', 'point_a', 'point_b', 'description_a', 'description_b'))
        user = self.request.user

        class CreateCommForm(form_class):
            def clean_user_b(self):
                user_b = self.cleaned_data.get('user_b')
                if user == user_b:
                    raise ValidationError(u"Nie możesz wybrać samego siebie")
                return user_b
        return CreateCommForm

    def form_valid(self, form):
        send_mail('Sprzedający rozpoczął nową transakcję do oceny', 'Sprzedający rozpoczął transakcje w której masz brać udział - po otrzymaniu przedmiotu zaloguj sie i ocen transakcję', 'from@example.com', [form.instance.user_b.email], fail_silently=False)
        self.object = form.save()
        self.object.user_a = self.request.user
        return super(CreateComm, self).form_valid(form)

create_comm = login_required(CreateComm.as_view())


class BUpdateComm(UpdateView):
    model = Comm
    success_url = '/'

    def get_form_class(self):
        return modelform_factory(
            self.model,
            exclude=('user_a', 'user_b', 'point_a', 'description_a', 'description'))

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.user_b:
            raise Http404
        return super(BUpdateComm, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        send_mail('Kupujacy wystawil ocene', 'Kupujący otrzymał już przedmiot - wystawił już swoją ocenę i oczekuje na ocenę tej transakcji z Twojej strony.', 'from@example.com', [form.instance.user_a.email], fail_silently=False)
        return super(BUpdateComm, self).form_valid(form)


bupdate_comm = login_required(BUpdateComm.as_view())


class AUpdateComm(UpdateView):
    model = Comm
    success_url = '/'

    def get_form_class(self):
        return modelform_factory(
            self.model,
            exclude=('user_a', 'user_b', 'point_b', 'description_b', 'description'))

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user != self.object.user_a:
            raise Http404
        return super(AUpdateComm, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        send_mail('Sprzedajacy wystawil ocene', 'Sprzedajacy wystawił już swoją ocenę - transakcja zakończona.', 'from@example.com', [form.instance.user_b.email], fail_silently=False)
        return super(AUpdateComm, self).form_valid(form)


aupdate_comm = login_required(AUpdateComm.as_view())
