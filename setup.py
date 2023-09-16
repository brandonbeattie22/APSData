import setuptools

# with open("README.md", "r") as fh:

#     long_description = fh.read()

setuptools.setup(

     name='APSData',  

     version='1.1',

     author="Brandon Beattie",

     author_email="brandonbeattie@telosair.com",

     description="Converting APS text files to pandas.DataFrame",

    #  long_description=long_description,

#    long_description_content_type="text/markdown",

    #  url="https://github.com/brandonbeattie22/TelosAir_Gateway",

     packages=setuptools.find_packages(),

     classifiers=[

         "Programming Language :: Python :: 3",

         "Operating System :: OS Independent",

     ],
     install_requires=['numpy', 'pandas'],
 )