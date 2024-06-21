from setuptools import setup

requirements = [
    'hist','coffea','tensorflow'
]

setup(
    name='dasmonoz',
    version='0.0.1',
    description="DAS EXO long exercise",
    author="Yacine Haddad",
    author_email='yhaddad@cern.ch',
    packages=[
        'dasmonoz',
    ],
    package_dir={'dasmonoz':
                 'dasmonoz'},
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='dasmonoz',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
)


