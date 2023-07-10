# encoding-compression-investigation
This project aims to evaluate different combinations of readily available encryption and compression algorithms in Python with respect to autonomous vehicle network transmission

Dependencies:
* fernet
* glob
* matplotlib
* numpy
* pandas
* pycryptodome
* pynacl
* scipy

TODOs:
* continue work on [presentation](https://docs.google.com/presentation/d/14oVvg1r6otz2AWvUPbUb9OIdrnhWZbaUL2YM-4GuaRQ/edit?usp=sharing "link to private Google Slide") (graphs, written sections)
* add data folder for visual simplicity in directory
* continue related work investigation
* prepare code for release
    * documentation
    * work on readme
    * switch variables to underlined_lowercase from camelCase
    * consider adding console status updates
    * consider Python Style Guide

After initial release:
* allow for blank args in results_processor.get_data()
* find file size where preferred order switches - between 10 and 95MB - binary search
* implement asymmetric key encryption
* implement lossy compression algorithm