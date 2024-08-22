from setuptools import setup

__author__ = 'samuelchristlie'
__version__ = '4.0.3-beta'


long_description = 'This Python script enables you to download ongoing Instagram livestreams as a video file.'

setup(
    name='pyinstalive',
    version=__version__,
    author=__author__,
    url='https://github.com/samuelchristlie/PyInstaLive',
    packages=['pyinstalive'],
    entry_points={
        'console_scripts': [
            'pyinstalive = pyinstalive.__main__:run',
        ]
    },
    install_requires=[
        'argparse',
        'configparser'
    ],
    include_package_data=True,
    platforms='any',
    long_description=long_description,
    keywords='instagram-livestream-recorder record-instagram-livestreams live instagram record livestream video '
             'recorder downloader download save',
    description='Download Instagram livestreams.',
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)
