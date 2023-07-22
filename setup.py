from setuptools import setup, find_packages

# Read the content of the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='eclair-cli',
    version='1.0.3',
    author='August Radjoe',
    author_email='atg271@gmail.com',
    description='A tool to create library wrappers for Blockchain Business Logic code.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['src'],
    entry_points={
        'console_scripts': [
            'eclair = src.main:process_arguments',
        ],
    },
    install_requires=[
        'jinja2',
        'web3',
    ],
    url="https://github.com/abhinavmir/eclair",  # Add the GitHub repository URL here
)
