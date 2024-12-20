from setuptools import setup, find_packages

setup(
    name="micropython-om2m-client",  # Package name on PyPI
    version="0.1.0a1",               # Version (pre-alpha for WIP)
    description="A MicroPython client for interacting with OM2M CSE (Work in Progress).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/micropython-om2m-client",  # Replace with your GitHub repo URL
    packages=find_packages(),       # Automatically find the package (e.g., om2m_client)
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: Implementation :: MicroPython",
    ],
)
