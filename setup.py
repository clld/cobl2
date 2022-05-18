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
        'clldutils>=3.11.1',
        'clld>=9.1.0',
        'clldmpg>=4.2.0',
        'clld-cognacy-plugin>=0.2.1',
        'sqlalchemy>=1.4.35',
        'Markdown>=3.3.6',
    ],
    extras_require={
        'dev': ['flake8', 'waitress'],
        'test': [
            'tox',
            'mock>=4.0.3',
            'psycopg2>=2.8.6',
            'pytest>=7.1.2',
            'pytest-clld>=1.1.0',
            'pytest-mock>=3.5.1',
            'pytest-cov>=3.0.0',
            'coverage>=6.3.2',
            'selenium>=3.141',
            'zope.component>=4.6.2',
        ],
    },
    test_suite="cobl2",
    entry_points="""\
[paste.app_factory]
main = cobl2:main
""")
