try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='phanpy',
    version='1.0.0',
    description='''A collection of useful helper functions for projects that
    take advantage of suit-pylons.''',
    author='Chris Santiago (Faltzer)',
    author_email='faltzerr@aol.com',
    url='http://faltzershq.com/',
    install_requires=[
        'Pylons>=1.0',
        'python-openid>=2.2.1',
        'FormEncode>=1.2.2',
        'rulebox>=1.1.0',
        'suit>=2.0.1'
    ],
    setup_requires=[],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Pylons',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License'
    ],
)