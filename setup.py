from setuptools import setup, find_packages

setup(
    name='d1py',
    version='0.1.0',
    packages=find_packages(),  # finds all packages inside d1py/
    install_requires=[
        'cyclonedds==0.10.2',
        'numpy',
        'opencv-python',
    ],
    author='Omar Mostafa',
    author_email='omm7813@nyu.com',
    description='Python interface for D1 arm control',
    url='https://github.com/omar-mostafa81/D1Py',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
