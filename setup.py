from setuptools import setup, find_packages

setup(
    name="CI",             
    version="1.0.0",                 
    author="Group 9",              
    description="Continuous Integration Automation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),        # Automatically find Python packages
    install_requires=[
        "flask>=2.0.0",             # Match dependencies in requirements.txt
        "pytest>=8.0.0",
        "pdoc>=14.0.0",
        "pip>=23.0",
        "GitPython>=3.1.44",
        "requests>=2.32.3",
        "python-dotenv>=1.0.1"
    ],
    python_requires=">=3.13",
)
