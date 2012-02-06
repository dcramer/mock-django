from setuptools import setup, find_packages

setup(
    name='mock-django',
    version='0.1.0',
    description='',
    license='Apache License 2.0',
    author='David Cramer',
    author_email='dcramer@gmail.com',
    url='http://github.com/dcramer/mock-django',
    packages=find_packages(),
    install_requires=[
        'nose',
        'unittest2',
        'mock',
    ],
    tests_require=[
        'mock==dev',
    ],
    test_suite='nose.collector',
    zip_safe=False,
    include_package_data=True,
)
