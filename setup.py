from setuptools import setup, find_packages
from pip.req import parse_requirements


install_reqs = parse_requirements('requirements.txt')

setup(
    name="tomorrow",
    version="0.3.0",
    author="ResolveWang",
    author_email="w1796246076@sina.com",
    packages=find_packages(
        exclude=[
            'tests'
        ]
    ),
    install_requires=install_reqs,
    description="""
        Magic decorator syntax for asynchronous code.
    """,
    license="MIT License (See LICENSE)",
    long_description=open("README.rst").read(),
    url="https://github.com/ResolveWang/Tomorrow"
)
