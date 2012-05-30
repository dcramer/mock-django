#!/usr/bin/env python
from django.conf import settings
# collector import is required otherwise setuptools errors
from nose.core import run, collector


# Trick Django into thinking that we've configured a project, so importing
# anything that tries to access attributes of `django.conf.settings` will just
# return the default values, instead of crashing out.
if not settings.configured:
    settings.configure()


if __name__ == '__main__':
    run()
