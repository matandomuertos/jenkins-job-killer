from setuptools import setup, find_packages

setup(
    name="jjkiller",
    version="0.1",
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