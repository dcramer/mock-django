from setuptools import setup, find_packages

setup(
    name='mock-django',
    version='0.1.0',
    description='',
    author='David Cramer',
    author_email='dcramer@gmail.com',
    url='http://github.com/dcramer/mock-django',
    packages=find_packages(),
    install_requires=[
        'nose',
        'unittest2',
        'mock>=0.8',
    ],
    test_suite='nose.collector',
    zip_safe=False,
    include_package_data=True,
)
