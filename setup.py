from setuptools import setup, find_packages
from curlgoogle import __version__

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="curlgoogle",
    packages=find_packages(include=["curlgoogle", "curlgoogle.*"]),
    version=__version__,
    license='MIT',
    description="A simple lightweight python package for curl-based requests to google drive.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Hamid Kamkari",
    author_email="hamidrezakamkari@gmail.com",
    url="https://github.com/HamidrezaKmK/curlgoogle",
    entry_points={
        'console_scripts' : [
            'curlgoogle_upload = curlgoogle.console:upload',
            'curlgoogle_download = curlgoogle.console:download',
        ]
    },
    keywords=[
        "Google drive",
        "Cloud storage",
        "Google drive API",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Education",
        "Programming Language :: Python :: Implementation",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
)