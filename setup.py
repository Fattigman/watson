from setuptools import setup, find_packages
import wseaborn   
setup(
    name='wseaborn',
    version='0.1.0',
    description='A tool for aggregating and visualizing time data',
    author='Jacob Karlström',
    author_email='jacob.karlstrom@gmail.com',
    packages=find_packages(),
    py_modules=['wseaborn'],
    install_requires=[
        'matplotlib',
        'seaborn'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': [
            'wseaborn=wseaborn:main',
        ],
    },
)