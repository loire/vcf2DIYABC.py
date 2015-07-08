# vcf2DIYABC.py

Purpose
-------

Tool to convert vcf file in diyABC input file for SNP data

Requirement
-----------
* python 2.x
* A version compatible with python 3.x is avaible on branch `python3.x`
* Windows users: This script is unable to run if python is not installed on your machine. 
I strongly recommand you do the necessary step to achieve this by following this [link](http://docs.python-guide.org/en/latest/starting/install/win/), since it's probably gonna be useful for many other bioinformatic purposes. 

TODO: I'm currently trying to produce a self contained executable to run the script without the need for a python installation thanks to [py2exe](http://www.py2exe.org/)

Download/Installation
---------------------
Unix users can clone this repository if git is installed on their system with: 

`git clone https://github.com/loire/vcf2DIYABC.snp.git`

a link to a zip archive of this repository is on this page. 

To install, just unzip the archive in a local directory.


Usage
-----
* Unix and mac user can use the terminal and type
```
python vcf2DIYABC.py
```

* On windows, navigate in the file manager to find where you download and uncompressed the repository and then right click on the script file to execute it. 


Once launched, the program will ask you to enter the path and name of your input files.

Input files 
-----------
* a vcf file (tested on 4.0 version of this file format)
* A text file which specify individuals sex and population of origin (This information is not present in a typical vcf file while being needed for DIYABC analysis. This file follow this convention:
```

```



You can find an example of each file in example directory of this repo. A perfect match is required between names of individuals in the vcf file and those in the individuals informations file. 
