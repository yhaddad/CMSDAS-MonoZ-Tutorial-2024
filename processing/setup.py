from setuptools import setup

requirements = [
    'numpy','coffea','tensorflow'
]

setup(
    name='ristretto',
    version='0.0.1',
    description="strong coffea is an ristretto",
    author="Yacine Haddad",
    author_email='yhaddad@cern.ch',
    packages=[
        'ristretto',
    ],
    package_dir={'ristretto':
                 'ristretto'},
    entry_points={
        'console_scripts': [
            'binopt=binopt.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='binopt',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
)


