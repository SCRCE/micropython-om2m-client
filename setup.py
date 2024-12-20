from setuptools import setup, find_packages

setup(
    name="micropython-om2m-client",  
    version="0.1.0a1",             
    description="A MicroPython client for interacting with OM2M CSE (Work in Progress).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="jack.scarce.85@gmail.com",
    url="https://github.com/SCRCE/micropython-om2m-client", 
    packages=find_packages(),      
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: Implementation :: MicroPython",
    ],
)
