import os
from setuptools import setup, find_packages

inst_dir = os.path.abspath( __file__ ).replace('setup.py','')
os.chdir(inst_dir)

data_files = []

for dirpath, dirnames, filenames in os.walk(os.path.join(inst_dir, 'linguist', 'templates')):
    if filenames:
        data_files.append(  [os.path.relpath(dirpath, inst_dir), 
                            [os.path.relpath(os.path.join(dirpath, f), inst_dir) for f in filenames]])

setup(
    name='django-linguist',
    version='0.1.0.0',
    description='Simple model translation for Django',
    long_description=open('README.rst').read(),
    author='Christian Toivola',
    author_email='dev360@dev360.com',
    license='BSD',
    url='https://github.com/dev360/django-linguist/',
    platforms='any',
    packages=find_packages(exclude=['tests']),
    data_files = data_files,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)