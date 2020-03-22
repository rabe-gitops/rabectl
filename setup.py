import os
from setuptools import setup, find_packages

# Get current location
here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    readme = f.read()

# Setup
setup(
    name='rabectl',
    version='0.1.0',
    description='Rabe GitOps CLI',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Claudio Scalzo',
    author_email='claudio.scalzo@outlook.com',
    url='https://www.rabegitops.it/',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6.*, <4',
    entry_points={
        'console_scripts': [
            'rabectl=rabectl:main',
        ],
    },
    install_requires=[
        'awscli',
        'boto3',
        'click',
        'pyfiglet',
        'pyinquirer',
        'gitpython',
        'pygithub',
        'python-terraform'
    ]
)

