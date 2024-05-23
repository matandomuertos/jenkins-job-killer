from setuptools import setup, find_packages

setup(
    name="jjkiller",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
        "jenkins",
        "tabulate"
    ],
    entry_points={
        'console_scripts': [
            'jjkiller = jjkiller.main:main'
        ]
    }
)