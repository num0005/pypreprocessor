#Install

##Simple

1. download and unpack the contents.
2. copy pypreprocessor.py to the directory where it will be used

*Note: pypreprocessor is intentionally kept small and self-contained
 in a single source file to make it easy to use and/or package with
 other libraries/applications. As long as pypreprocessor exists this
 will remain true.*


##Using pip

1. in a terminal enter:
    sudo pip install git+https://github.com/num0005/pypreprocessor.git

*Note: sudo is only necessary if the location of the python
 libraries requires root priveledges to access.*

This is the easiest method to install pypreprocessor for system-wide
 use. The only downside is, pip currently only supports installing
 to python 2x.


##Using setup.py

1. download and unpack the contents
2. open a terminal in the directory containing the contents
3. in the terminal enter:
    sudo python setup.py install

*Note: sudo is only necessary if the location of the python
 libraries requires root priveledges to access.*

To install for python 3x repeat steps 1 & 2 and for step 3 enter:
    sudo python3 setup.py install
