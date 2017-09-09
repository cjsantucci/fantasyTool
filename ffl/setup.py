from setuptools import setup

setup(
    name = 'ffl',
    version = '1.0',
    description = "XML data parser for fantasy sports",
    author = 'Chris Sandy and Ken Kohler',
    author_email = 'cjsantucci@gmail.com',
    license = 'MIT',
    url = 'https://github.com/cjsantucci/fantasyTool/',
    packages = [ "ffl", "compute", "grabbers", "vis" ],
    install_requires = []
)