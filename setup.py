import setuptools

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(name='pybtpanel',
                 version='1.1',
                 author='zzqfbzz',
                 description='一个宝塔面板api的包',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url='https://github.com/zzqfbzz/pybtpanel',
                 packages=setuptools.find_packages(),
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "Operating System :: Unix",
                     "Operating System :: MacOS :: MacOS X",
                     "Operating System :: Microsoft :: Windows",
                 ],
                 install_requires=["requests"],

                 )
