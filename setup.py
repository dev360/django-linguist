import os
from setuptools import setup, find_packages

dir_path = os.path.abspath( __file__ ).replace('setup.py','')
os.chdir(dir_path)

data_files = []
for root, subFolders, files in os.walk(os.path.join(dir_path,'linguist','templates')):
    for file in files:
        data_files.append([root, os.path.join(root,file)])


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