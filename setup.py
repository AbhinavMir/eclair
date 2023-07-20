from setuptools import setup

setup(
    name='eclair-evm',
    version='1.0.0',
    author='August Radjoe',
    author_email='atg271@gmail.com',
    description='A tool to create library wrappers for Blockchain Business Logic code.',
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
)
