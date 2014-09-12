import re
import os
from setuptools import find_packages, setup


PKG = 'ccarps'
VERSIONFILE = os.path.join(PKG, "version.py")
long_description = """The Community Codex Adaptive RolePlay System is a
Creative Commons-licensed game framework.
"""
install_requires = []

verstr = "unknown"
try:
	verstrline = open(VERSIONFILE, "rt").read()
except EnvironmentError:
	pass # Okay, there is no version file.
else:
	VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
	mo = re.search(VSRE, verstrline, re.M)
	if mo:
		__version__ = mo.group(1)
	else:
		msg = "if %s.py exists, it is required to be well-formed" % VERSIONFILE
		raise RuntimeError(msg)

setup(
	name=PKG,
	version=__version__,
	install_requires=install_requires,
	entry_points={
		'console_scripts': [
			'ccarps = ccarps.gate:ccarps_main'
		],
	},
	packages=find_packages(),
	package_dir={'ccarps':'ccarps'},
	package_data={},
	author='Sina Mashek',
	author_email='mashek@thescoundrels.net',
	maintainer='Sina Mashek',
	maintainer_email='mashek@thescoundrels.net',
	long_description=long_description,
	description='CCARPS is a CC-licensed game framework.',
	license='MIT',
	url='http://wizardspire.com/ccarps',
	platforms=['any'],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Environment :: Console',
		'Environment :: Web Environment',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
	],
)
