# encoding-compression-investigation
This project aims to evaluate different combinations of readily available encryption and compression algorithms in Python with respect to autonomous vehicle network transmission

Dependencies:
* pynacl
* pycryptodome
* fernet
* numpy
* glob
* pandas
* matplotlib
* scipy

TODOs:
* investigate timings
* continue work on [presentation](https://docs.google.com/presentation/d/14oVvg1r6otz2AWvUPbUb9OIdrnhWZbaUL2YM-4GuaRQ/edit?usp=sharing "link to private Google Slide") (graphs, written sections)
* add data folder for visual simplicity in directory
* allow for blank args in results_processor.get_data()
* switch variables to underlined_lowercase from camelCase
* continue related work investigation
* consider adding console status updates
* prepare code for release
* documentation
* work on readme
* find file size where preferred order switches - between 10 and 95MB - binary search
* implement asymmetric key encryption
* implement lossy compression algorithm
* broad narrative
* more test file types and sizes
* consider Python Style Guide