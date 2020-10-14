from setuptools import setup, find_packages


setup(
    name='cobl2',
    version='0.0',
    description='cobl2',
    long_description='',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'clldutils>=3.5.4',
        'clld>=7.2',
        'clldmpg>=4.0',
        'clld-cognacy-plugin>=0.2',
        'clld-phylogeny-plugin>=1.4.0',
        'markdown',
    ],
    extras_require={
        'dev': ['flake8', 'waitress'],
        'test': [
            'tox',
            'mock>=4.0.2',
            'psycopg2>=2.8.6',
            'pytest>=6.0',
            'pytest-clld>=1.0.2',
            'pytest-mock>=3.3.1',
            'pytest-cov>=2.10.1',
            'coverage>=5.3',
            'selenium>=3.141',
            'zope.component>=4.6.2',
        ],
    },
    test_suite="cobl2",
    entry_points="""\
[paste.app_factory]
main = cobl2:main
""")
