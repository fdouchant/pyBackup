from setuptools import setup, find_packages

try:
    from html2rest import html2rest
    from StringIO import StringIO
    import urllib
    
    # read content of article (plain html template) and convert to restructuredText for long_description
    stringIO = StringIO()
    # html_content = urllib.urlopen("http://fabrice.douchant.com/mypyapps-framework-for-python-developments?lang=en").read()
    # html2rest(html_content, writer=stringIO)
    # long_description = stringIO.getvalue()

    long_description = "Coming soon"
except (ImportError, IOError):
    print("Can't use spip article as description, use README.txt instead")
    long_description = open('README.txt').read()

import pyBatch

setup(
    name='pyBatch',
    version='.'.join(map(str, pyBatch.__version__)),
    packages=find_packages(),

    package_data={
        'pyBatch': ['config/*.default', 'logs/.empty'],
    },

    author='Fabrice Douchant',
    author_email='fabrice.douchant@gmail.com',
    description='Allow to run batch surrounded by automated reporting, emailing, ... support.',
    long_description=long_description,
    license='GNU GPLv3',
    keywords='tools batch',
    url="http://fabrice.douchant.com/pybatch-shell-batch-manager?lang=en",

    zip_safe= False,
    requires=['myPyApps'],
    scripts=['batch.py']
)
