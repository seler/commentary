# -*- coding: utf-8 -*-
from django.views.generic import ListView, CreateView, UpdateView
from django.forms.models import modelform_factory
from .models import Comm


class CreateComm(CreateView):
    model = Comm

    def get_form_class(self):
        return modelform_factory(
            self.model,
            exclude=('user_a', 'point_a', 'point_b', 'description_a', 'description_b'))


create_comm = CreateComm.as_view()


class BUpdateComm(UpdateView):
    model = Comm

    def get_form_class(self):
        return modelform_factory(
            self.model,
            exclude=('user_a', 'user_b', 'point_a', 'description_a', 'description'))


bupdate_comm = BUpdateComm.as_view()

class AUpdateComm(UpdateView):
    model = Comm

    def get_form_class(self):
        return modelform_factory(
            self.model,
            exclude=('user_a', 'user_b', 'point_b', 'description_b', 'description'))


aupdate_comm = AUpdateComm.as_view()


