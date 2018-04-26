from sys import exit
import platform
from os import getcwd
import re
from subprocess import call

# OSError

required = re.compile(r'^2\.7\.[0-9]*$')
try:
    print required.match(platform.python_version()).group()
except AttributeError:
    print 'python version 2.7.x is required for this package.'
    exit(0)

email = 'the.innovation.express@gmail.com'

to  = './build'
fr  = '.'
url = 'https://github.com/nbond008/scuff/tree/proto-1'

print 'checking for pip:'
try:
    call(['pip', '-V'])
except OSError:
    print 'this package requires pip. please contact your administrator about installing pip on this machine.'
    exit(0)
    # try:
    #     call(['easy_install', '--user', 'pip'])
    # except OSError:
    #     print 'please '

# print 'affirming package structure:'
#
# setup = open('setup.py', 'w')
# setup_contents = '''
# from setuptools import setup
#
# setup(
#     name         = 'scuff',
#     version      = '0.3',
#     description  = 'The Innovation Express capstone project',
#     url          = 'https://github.com/nbond008/scuff',
#     author       = 'Nick Bond and Gabe Waksman',
#     author_email = 'the.innovation.express@gmail.com',
#     license      = 'Georgia Tech',
#     packages     = ['.'],
#     zip_safe     = False
# )
# '''
#
# try:
#     setup.write(setup_contents)
#     setup.close()
# except IOError:
#     'writing \'setup.py\' failed. please email the authors at %s' % email
#     exit(0)

print 'catching dependencies:'

try:
    print 'looking for PIL...'
    from PIL import Image
    print 'PIL already installed.'
except ImportError:
    print 'PIL not found. installing via pip...'
    try:
        call(['pip', 'install', 'Pillow'])
    except OSError:
        print 'cannot install via pip. please email the authors at %s' % email

try:
    print '\nlooking for numpy...'
    import numpy
    print 'numpy already installed.'
except ImportError:
    print 'numpy not found. installing via pip...'
    try:
        call(['pip', 'install', 'numpy'])
    except OSError:
        print 'cannot install via pip. please email the authors at %s' % email

try:
    print '\nlooking for matplotlib...'
    import matplotlib
    print 'matplotlib already installed.'
except ImportError:
    print 'matplotlib not found. installing via pip...'
    try:
        call(['pip', 'install', 'matplotlib'])
    except OSError:
        print 'cannot install via pip. please email the authors at %s' % email

try:
    print '\nlooking for Tkinter...'
    import _tkinter
    import Tkinter as tk
    # print 'testing Tkinter...'
    # tk._test()
except ImportError:
    print 'Tkinter not found. please contact your administrator about reinstalling Python.'
    exit(0)
except AttributeError:
    print 'Tkinter not found. please contact your administrator about reinstalling Python.'
    exit(0)

print '\n'

try:
    print 'installing Scuff Finder Desktop...'
    call(['pip', 'install', fr, '-i', url, '-t', to])
except OSError:
    print 'installation failed. please email the authors at %s' % email
    exit(0)

# try:
#     import __init__ as test
# except ImportError:
#     print 'installation failed. please email the authors at %s' % email

export_path = '%s/scuff_data.csv' % getcwd()

print 'configuring Scuff Finder Desktop...'
import tkFileDialog
new_path = tkFileDialog.askdirectory()

if new_path:
    export_path = '%s/scuff_data.csv' % new_path

print 'configuring Scuff Finder Desktop...\n'

conf = open('.config.txt', 'w')
conf.write(export_path)
conf.close()

ex = open(export_path, 'w')
ex.write('Sample, Resolution, Scuff Intensity, Scuff Area, Orientation')
ex.close()

print 'successfully configured Scuff Finder Desktop.\nScuff Finder Desktop should now be ready to use.'
