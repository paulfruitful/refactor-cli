from setuptools import setup, find_packages

setup(
    name="refactor-cli",
    version="0.1.0", 
    packages=find_packages(),
    install_requires=[
        "google-generativeai",
        "watchdog",
        "keyboard"
    ],
    entry_points={
        "console_scripts": [
            "refactor-cli=refactor_cli.cli:main", 
        ],
    },
    description="A CLI tool to watch and refactor code files.",
    long_description=open('README.md').read(), 
    long_description_content_type='text/markdown', #
    author="Paul Fruitful",
    author_email="fruitful2007@outlook.com",
    url="https://github.com/paulfruitful/refactor-cli",
    license='MIT', 
        classifiers=[ # Added classifiers for better categorization on PyPI
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords='refactor, cli, watchdog, code quality',
    python_requires='>=3.7', 
    package_data={'': ['README.md']}, 
    include_package_data=True, 
)
