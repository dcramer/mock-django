mock-django
~~~~~~~~~~~

A simple library for mocking certain Django behavior, such as the ORM.

Using mock-django objects
-------------------------
Inside your virtualenv:

.. code:: python

   >>> from django.conf import settings
   >>> settings.configure() # required to convince Django it's properly configured
   >>> from mock_django.query import QuerySetMock
   >>> class Post(object): pass
   ...
   >>> qs = QuerySetMock(Post, 1, 2, 3)
   >>> list(qs.all())
   [1, 2, 3]
   >>> qs.count()
   3
   >>> list(qs.all().filter())
   [1, 2, 3]

See tests for more examples.


Testing
-------

.. image:: https://secure.travis-ci.org/dcramer/mock-django.png
   :alt: Build Status
   :target: http://travis-ci.org/dcramer/mock-django

``tox``
