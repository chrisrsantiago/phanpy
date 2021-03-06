# Copyright (c) 2010 Chris Santiago (http://faltzershq.com/)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='phanpy',
    version='1.1.0',
    description='''A collection of useful helper functions for projects that
    take advantage of suit-pylons.''',
    author='Chris Santiago',
    author_email='chrisrsantiago@aol.com',
    url='http://github.com/chrisrsantiago/phanpy',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Pylons',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License'
    ],
    install_requires=[
        'Pylons>=1.0',
        'python-openid>=2.2.1',
        'FormEncode>=1.2.2',
        'rulebox>=1.1.0',
        'suit>=2.0.1',
        'Markdown-2.0.3'
    ],
    setup_requires=[],
    test_suite='nose.collector',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False
)