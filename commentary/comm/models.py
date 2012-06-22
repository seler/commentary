import random
import hashlib

from django.db import models
from django.conf import settings


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
    person_a = models.ForeignKey('Person')
    person_b = models.ForeignKey('Person', null=True, blank=True)
    point_a = models.NullBooleanField(null=True)
    point_b = models.NullBooleanField(null=False)
    hash = models.CharField(max_length=128)
    description = models.TextField()
    add_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)

    def make_password(self):
        return make_random_string()

    def make_hash(self, password):
        return hashlib.sha512(password + settings.SALT).hexdigest()


class Person(models.Model):
    nick = models.CharField(max_length=128)
