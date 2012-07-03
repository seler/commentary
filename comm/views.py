# -*- coding: utf-8 -*-
from django.views.generic import ListView, CreateView, UpdateView
from django.forms.models import modelform_factory
from .models import Comm
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.http import Http404
from django.shortcuts import render_to_response
from django.core.mail import send_mail
from django.contrib.auth.models import User

class MyUser(User):

    def a_positive_points(self):
        return self.comm_user_a.filter(point_b=True).count()
    def a_negative_points(self):
        return self.comm_user_a.filter(point_b=False).count()
    def b_positive_points(self):
        return self.comm_user_b.filter(point_a=True).count()
    def b_negative_points(self):
        return self.comm_user_b.filter(point_a=False).count()
    def a_points(self):
        return self.a_positive_points() - self.a_negative_points()
    def b_points(self):
        return self.b_positive_points() - self.b_negative_points()
    def points(self):
        return self.a_points() + self.b_points()
    def a_count(self):
        return self.comm_user_b.count()
    def b_count(self):
        return self.comm_user_b.count()
    def count(self):
        return self.a_count() + self.b_count()
    def rating(self):
        if self.count():
            return self.points() / float(self.count()) * 100
        return 0
    
    class Meta:
        proxy = True

@login_required
def home(request):
    user = request.user

    a_todo = user.comm_user_a.filter(point_a__isnull=True, point_b__isnull=False)
    b_todo = user.comm_user_b.filter(point_b__isnull=True)

    users = list(MyUser.objects.all())
    users = sorted(users, key=MyUser.rating)
       
    return render_to_response(
        'comm/index.html',
        {
            "users": users,
            'a_todo': a_todo,
            'b_todo': b_todo,
        })

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
        subject = 'Sprzedający rozpoczął nową transakcję do oceny'
        dupa = subject
        
        send_mail(subject, dupa, 'from@example.com', [form.instance.user_b.email], fail_silently=False)
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
        send_mail('Kupujacy wystawil ocene', 'Here is the message.', 'from@example.com', [form.instance.user_a.email], fail_silently=False)
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
        send_mail('Sprzedajacy wystawil ocene', 'Here is the message.', 'from@example.com', [form.instance.user_b.email], fail_silently=False)
        return super(AUpdateComm, self).form_valid(form)


aupdate_comm = login_required(AUpdateComm.as_view())


