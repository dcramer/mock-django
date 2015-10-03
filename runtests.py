#!/usr/bin/env python

import django
from django.conf import settings
# collector import is required otherwise setuptools errors
from nose.core import run, collector


# Trick Django into thinking that we've configured a project, so importing
# anything that tries to access attributes of `django.conf.settings` will just
# return the default values, instead of crashing out.
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
        ],
    )

try:
    django.setup()
except AttributeError:
    # Django 1.7 or lower
    pass


if __name__ == '__main__':
    run()
