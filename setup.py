from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in parason/__init__.py
from parason import __version__ as version

setup(
	name="parason",
	version=version,
	description="Parason",
	author="Parason",
	author_email="Parason",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
