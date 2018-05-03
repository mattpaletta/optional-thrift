try:
	from setuptools import setup, find_packages
except ImportError:
	import ez_setup

	ez_setup.use_setuptools()
	from setuptools import setup, find_packages



setup(
		name="optionalthrift",
		version="0.0.1",
		url='https://github.com/mattpaletta/optional-thrift',
		packages=find_packages(),
		include_package_data=True,
		install_requires=['thrift'],
		author="Matthew Paletta",
		author_email="mattpaletta@gmail.com",
		description="An optional thrift wrapper for local debuggging.",
		license="BSD",
		classifiers=[
			'Development Status :: 3 - Alpha',
			'Intended Audience :: Developers',
			'License :: OSI Approved :: BSD License',
			'Operating System :: OS Independent',
			'Programming Language :: Python',
			'Topic :: Communications',
		]
)
