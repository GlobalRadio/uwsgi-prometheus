import os
import re

from io import open
from setuptools import find_packages, setup


def read(file):
    with open(file, 'r', encoding='utf-8') as f:
        return f.read()


def get_version():
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join('uwsgi_prometheus', '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version()


setup(
    name='uwsgi-prometheus',
    version=version,
    url='https://github.com/GlobalRadio/uwsgi-prometheus',
    license='MIT',
    description='uWSGI stats exporter for Prometheus',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Chris Graham',
    author_email='chris.graham@global.com',
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=2.7",
    install_requires=[
        'prometheus-client',
        'requests',
    ],
    zip_safe=False,
)
