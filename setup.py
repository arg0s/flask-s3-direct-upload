"""
Flask-S3-Direct-Upload
-------------

Sets up S3 upload policies for you to directly upload from client side javascript to S3 bypassing your Flask server.
"""
from setuptools import setup


setup(
    name='Flask-S3-Direct-Upload',
    version='1.0',
    url='http://github.com/arg0s/flask-s3-direct-upload',
    license='BSD',
    author='arg0s',
    author_email='arvi@alumni.iastate.edu',
    description='Sets up S3 upload policies for you to directly upload from client side javascript to S3 bypassing your Flask server.',
    py_modules=['flask_s3_direct_upload'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'arrow'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
