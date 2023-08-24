# APSData

## To Install
Prerequisites:
 - Python3
 - pip or pip3 (for Python3)
 - GIT CLI (preferred, but optional)
 - numpy
 - pandas

### GIT CLI
_If you are on OS X, GIT CLI comes with XCode Command Line Tools, which you may already have. OS X also has options for package managers like Homebrew or MacPorts: https://git-scm.com/download/mac. For other OS's: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git_

### Package Install
To install this library with the GIT CLI, do `pip3 install --upgrade git+https://github.com/brandonbeattie22/APSData.git` or `python3 -m pip install --upgrade git+https://github.com/brandonbeattie22/APSData.git`.

To install without the GIT CLIT, download this package and unzip it. Open a terminal and navigate into the package's first outer folder and do `python3 setup.py install`.

## To Use

```python
from APSData.files import read_APS_file, read_folder_APS

# Reading a singular file
PATH_TO_FILE = "./folder_with_APS_data/aps_file.txt"
df = read_APS_file(PATH_TO_FILE)

# Reading a folder of APS data .txt files
PATH_TO_FOLDER = "./folder_with_APS_data"
df = read_folder_APS(PATH_TO_FOLDER)
```
