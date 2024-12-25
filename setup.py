from setuptools import setup, find_packages

setup(
    name="micropython-om2m-client",
    version="0.1.0a7",
    description="A MicroPython client for interacting with OM2M CSE (Work in Progress).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ahmad Hammad",
    author_email="ahmadhammad.uca@gmail.com",
    url="https://github.com/SCRCE/micropython-om2m-client",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: Implementation :: MicroPython",
    ],
    install_requires=[
        "urequests>=0.9.0",  
        "ujson>=1.35",       
        "umqtt.robust>=1.0.0",  
    ],
)
