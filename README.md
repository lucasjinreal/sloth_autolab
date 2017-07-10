# sloth

> this sloth label tool is Tencent Auto-Lab version, maintained by Jinfagang.

# Synopsis

We reconstruct the original sloth into our project, mainly add more features.

* Customize to our categories, such as Car, Pedestrain, Cyclist.
* 4 camera simultaneously label.
* more

# Caution

this version of sloth has been updated into Python3 and PyQt5, for better support future changes. But the usage and functions are not very big changed.

# Install

**update 2017-7-9** Both system can using PyQt5 from:
```
sudo pip3 install pyqt5
```
this is the legacy requirements, we will only using PyQt5 in the future.

to install this version of sloth, please install PyQT5 first:
### Linux

```
sudo apt install python-qt4 python3-qt4
```
### masOS

this will install both PyQt4 and PyQt5, PyQt4 no longer support for macOS sierra. we will using PyQt5 on macOS.
```
brew tap cartr/qt4
brew tap-pin cartr/qt4
brew install qt
brew install pyside
brew install pyqt5
```



[![Build Status](https://travis-ci.org/cvhciKIT/sloth.svg)](https://travis-ci.org/cvhciKIT/sloth)

sloth is a tool for labeling image and video data for computer vision research.

The documentation can be found at http://sloth.readthedocs.org/ .

# Latest Releases

2013/11/29 v1.0: 2e69fdae40f89050fbaeef22491eee2a92e78b4f [.zip](https://github.com/cvhciKIT/sloth/archive/v1.0.zip) [.tar.gz](https://github.com/cvhciKIT/sloth/archive/v1.0.tar.gz)

For a full list, visit https://github.com/cvhciKIT/sloth/releases

`sloth examples/example1_labels.json`
