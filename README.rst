mock-django
~~~~~~~~~~~

A simple library for mocking certain Django behavior, such as the ORM.

Using mock-django objects
-------------------------
Inside your virtualenv::

>>> from django.conf import settings # required to confince Django we've properly configured
>>> settings.configure()
>>> from mock_django.query import QuerySetMock
>>> class Post(object): pass
>>> qs = QuerySetMock(Post, 1, 2, 3)
>>> list(qs.all())
[1, 2, 3]
>>> qs.count()
3


Testing
-------

.. image:: https://secure.travis-ci.org/dcramer/mock-django.png
   :alt: Build Status
   :target: http://travis-ci.org/dcramer/mock-django

``python setup.py test``
