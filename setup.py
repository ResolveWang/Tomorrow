from setuptools import setup, find_packages


setup(
    name="multitomorrow",
    version="0.3.0",
    author="ResolveWang",
    author_email="w1796246076@sina.com",
    packages=find_packages(
        exclude=[
            'tests'
        ]
    ),
    install_requires=[
        'gevent==1.2.2',
        'nose==1.3.7'
    ],
    description="Magic decorator syntax for asynchronous code",
    license="MIT License (See LICENSE)",
    long_description='See https://github.com/ResolveWang/Tomorrow',
    url="https://github.com/ResolveWang/Tomorrow"
)
