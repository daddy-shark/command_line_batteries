import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='clb',
    version='0.0.4',
    author='Andrey Okulov',
    author_email='okulov@ya.ru',
    description='Command line batteries (clb)'
                ' - the way to improve the functionality of Bash commands without writing a too difficult Bash code.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sharkman-devops/command_line_batteries',
    packages=setuptools.find_packages(),
    install_requires=[
        'PyYAML>=5.1,<6.0',
        'influxdb>=5.2.2,<6.0',
        'boto3>=1.9.120,<2.0',
        'requests>=2.21.0,<3.0',
    ],
    extras_require={
        'devel': [
            'mypy>=0.701<1.0',
            'pylint>=2.3.1<3.0',
            'pytest>=4.4.1<5.0',
            'twine>=1.13.0<2.0',
        ],
    },
    classifiers=[
        'Intended Audience :: System Administrators',
        'Topic :: System :: Archiving :: Backup',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
)
