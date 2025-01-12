from setuptools import setup, find_packages

setup(
    name="refactor-cli",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "google-generativeai",
        "watchdog",
    ],
    entry_points={
        "console_scripts": [
            "refactor-cli=cli:main",  
        ],
    },
    description="A CLI tool to watch and refactor code files.",
    author="Paul Fruitful",
    author_email="fruitful2007@outlook.com",
    url="https://github.com/paulfruitful/refactor-cli",
)