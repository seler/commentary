# -*- coding: utf-8 -*-
import random

from django.db import models
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
        return self.comm_user_a.count()

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
        ordering = ('username',)


def make_random_string(length=8, universe='', small_letters=True, big_letters=True,
                  numbers=True, special=True, force_all_types=True,
                  avoid_ambiguous_characters=False):

    pu = (
        'abcdefghijklmnoqprstuwvxyz',
        'ABCDEFGHIJKLMNOPQRSTUWVXYZ',
        '0123456789',
        '!@#%$&*^',
    )

    ambiguous_characters = 'O01lIqg'

    custom_universe = True
    if not universe:
        universe = ''
        if small_letters:
            universe += pu[0]
        if big_letters:
            universe += pu[1]
        if numbers:
            universe += pu[2]
        if special:
            universe += pu[3]
        custom_universe = False

    def mkstring(length, universe):
        string = ''
        for i in range(length):
            string += random.choice(universe)
        return string

    string_ok = False

    if avoid_ambiguous_characters:
        for c in ambiguous_characters:
            universe = universe.replace(c, '')

    while not string_ok:
        string = mkstring(length, universe)
        string_ok = all((
            any(map(lambda i: i in string, pu[0])) or not small_letters,
            any(map(lambda i: i in string, pu[1])) or not big_letters,
            any(map(lambda i: i in string, pu[2])) or not numbers,
            any(map(lambda i: i in string, pu[3])) or not special,
        )) or not force_all_types or custom_universe

    return string


class Comm(models.Model):
    POINT_CHOICES = (
        (True, "+1"),
        (False, "-1"),
    )
    user_a = models.ForeignKey(User,
        related_name="comm_user_a",
        verbose_name=u"sprzedający",
        null=True,
        blank=True)
    user_b = models.ForeignKey(User,
        related_name="comm_user_b",
        null=True,
        verbose_name=u"kupujący")
    point_a = models.NullBooleanField(
        choices=POINT_CHOICES,
        null=True,
        verbose_name=u"oceń kupującego")
    point_b = models.NullBooleanField(
        choices=POINT_CHOICES,
        blank=True,
        null=True,
        verbose_name=u"oceń sprzedającego")
    description = models.TextField(
        null=True,
        verbose_name="opis przedmiotu")
    description_a = models.TextField(
        null=True,
        verbose_name="opisz kupującego")
    description_b = models.TextField(
        blank=True,
        null=True,
        verbose_name="opisz sprzedającego")
    add_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u"komentarz"
        verbose_name_plural = u"komentarze"

    def __unicode__(self):
        return "komentarz %d" % self.pk
