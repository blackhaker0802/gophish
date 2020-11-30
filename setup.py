from setuptools import setup
setup(
    name = 'gophish',
    version = '1.0',
    packages=['gophish', 'gophish.Resources'],           # 1
    package_dir={'gophish.Resources': 'gophish'},          # 2
    package_data={'gophish.Resources': ['../Resources/*']},
    install_requires=[
        'colorama',
        'pyfiglet==0.8.post1',
        'pyshorteners',
        'selenium',
        'watchdog'
    ],
    entry_points = {
        'console_scripts': [
            'gophish = gophish.__main__:main'
        ]
    })
