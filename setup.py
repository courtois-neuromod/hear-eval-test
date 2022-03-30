
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='soundnetbrain_hear',
    version='0.0.1',
    description='Soundnet finuted by brain data from Neuromod Project, wrapper for HEAR benchmark.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/brzin-bzh/soundnetbrain_hear',
    packages=setuptools.find_packages(),
    author='Nicolas Farrugia',
    author_email='Nicolas.farrugia@imt-atlantique.fr',
    license='Apache License 2.0',
    install_requires=['numpy'
                      ],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
)