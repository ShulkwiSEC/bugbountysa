from setuptools import setup, find_packages
import codecs

with codecs.open('README.md', 'r', 'utf-8') as f:
    long_description = f.read()

setup(
    name='bugbountysa',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.28.0',
        'colorama>=0.4.6',
        'tabulate>=0.9.0',
        'rich>=13.0.0',
        'python-dateutil>=2.8.2',
        'tqdm>=4.65.0',
        'urllib3>=2.0.0',
    ],
    entry_points={
        'console_scripts': [
            'bugbountysa=core:scarp',
        ],
    },
    author='ShulkwiSEC',
    author_email='shulkwisec@gmail.com',  # Replace with your email
    description='A tool for managing Bug Bounty SA programs in Saudi Arabia',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ShulkwiSEC/bugbountysa',  # Replace with your repository URL
    project_urls={
        'Bug Reports': 'https://github.com/ShulkwiSEC/bugbountysa/issues',
        'Source': 'https://github.com/ShulkwiSEC/bugbountysa',
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Security',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Security',
    ],
    keywords='bug bounty, security, pentesting, saudi arabia, automation',
    python_requires='>=3.8',
    include_package_data=True,
    zip_safe=False,
)
