import os

from setuptools import find_packages, setup

try:
    with open(
        os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8"
    ) as f:
        long_description = f.read()
except:
    long_description = None

setup(
    name="barman-prices-exp",
    version=0.1,
    description="Calculate automatically prices using exponential function",
    long_description=long_description,
    author="Yoann Pietri",
    author_email="me@nanoy.fr",
    url="https://github.com/barmanaginn/barman-prices-exp",
    license="GPLv3",
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    entry_points="""
[barman.plugin]
barman_prices_exp=barman_prices_exp:BarmanPluginMeta
""",
)
