# config: utf-8
from setuptools import setup
from setuptools import find_packages


def main():
    setup(
        name="cyclone-track",
        version="0.0.1",
        description='Cyclone tracker.',
        author="Ryosuke Tomita",
        packages=find_packages(),
        install_requires=[
            'Cartopy',
            'numpy',
            'scipy',
            'matplotlib',
            'netCDF4',
        ],

        entry_points={
            'console_scripts': [
                'cyclone-track = cyclonetrack:main',
            ],
        }
    )


if __name__ == "__main__":
    main()
