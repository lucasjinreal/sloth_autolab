"""
sloth
-----

sloth is a tool for labeling image and video data for computer vision research.

The documentation can be found at http://sloth.readthedocs.org/ .

"""
import os
from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES
import sloth


# the following installation setup is based on django's setup.py
def full_split(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return full_split(head, [tail] + result)


# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
sloth_dir = 'sloth'

for dir_path, dir_names, file_names in os.walk(sloth_dir):
    for i, dir_name in enumerate(dir_names):
        if dir_name.startswith('.'):
            del dir_names[i]
    if '__init__.py' in file_names:
        packages.append('.'.join(full_split(dir_path)))
        if 'labeltool.ui' in file_names:
            data_files.append([dir_path, [os.path.join(dir_path, 'labeltool.ui')]])
    elif file_names:
        data_files.append([dir_path, [os.path.join(dir_path, f) for f in file_names]])

setup(
    name='sloth_autolab',
    version=sloth.VERSION,
    description='The Sloth Labeling Tool',
    author='Tencent Auto-Lab',
    url='http://sloth_autolab.readthedocs.org/',
    requires=['PyQt5', 'numpy', 'importlib'],
    packages=packages,
    data_files=data_files,
    scripts=['sloth/bin/sloth']
)
