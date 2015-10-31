from setuptools import setup, find_packages


setup(
    name='gobgift',
    version="1.0",
    description='A wishlist manager application',
    #long_description=readme,
    author='Kim Desrosiers',
    author_email='kimdesro@gmail.com',
    url='http://gobgift.kimond.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
