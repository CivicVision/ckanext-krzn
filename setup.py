import setuptools

version = '0.3.2'

setuptools.setup(
    name='ckanext-krzn',
    version=version,
    description="CKAN extension for KRZN",
    long_description="""\
    """,
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[],
    keywords='',
    author='okfn',
    author_email='dominik.moritz@okfn.org',
    url='',
    license='',
    packages=setuptools.find_packages(
        exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.krzn'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points="""
        [ckan.plugins]
    # Add plugins here
    krzn=ckanext.krzn.plugin:KrznCustomizations

    """,
)
