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
        'clld>=4.6',
        'clldmpg~=3.1',
        'clldutils>=2.8',
        'clld-cognacy-plugin>=0.1',
        'clld-phylogeny-plugin',
        'markdown',
    ],
    extras_require={
        'dev': ['flake8', 'waitress'],
        'test': [
            'psycopg2',
            'tox',
            'mock',
            'pytest>=3.1',
            'pytest-clld',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
            'selenium',
            'zope.component>=3.11.0',
        ],
    },
    test_suite="cobl2",
    entry_points="""\
[paste.app_factory]
main = cobl2:main
""")
