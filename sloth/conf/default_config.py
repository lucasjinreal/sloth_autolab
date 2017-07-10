# This is sloth's default configuration.
#
# The configuration file is a simple python module with module-level
# variables.  This module contains the default values for sloth's
# configuration variables.
#
# In all cases in the configuration where a python callable (such as a
# function, class constructor, etc.) is expected, it is equally possible
# to specify a module path (as string) pointing to such a python callable.
# It will then be automatically imported.

# LABELS
#
# List/tuple of dictionaries that defines the label classes
# that are handled by sloth.  For each label, there should
# be one dictionary that contains the following keys:
#
#   - 'item' : Visualization item for this label. This can be
#              any python callable or a module path string 
#              implementing the visualization item interface.
#
#   - 'inserter' : (optional) Item inserter for this label.
#                  If the user selects to insert a new label of this class
#                  the inserter is responsible to actually 
#                  capture the users mouse actions and insert
#                  a new label into the annotation model.
#
#   - 'hotkey' : (optional) A keyboard shortcut starting 
#                the insertion of a new label of this class.
#
#   - 'attributes' : (optional) A dictionary that defines the
#                    keys and possible values of this label
#                    class.
#
#   - 'text' : (optional) A label for the item's GUI button.
LABELS = (
    {
        'attributes': {
            'class': 'Vehicle',
            'scale': ["small", "middle", "large", "special", "notcare"]
        },
        'inserter': 'sloth.items.IDRectItemInserter',
        'item': 'sloth.items.IDRectItem',
        'hotkey': 'V',
        'text': 'Vehicle',
    },
    {
        'attributes': {
            'class': 'Pedestrian',
            'type': ['rider', 'pedestrian']
        },
        'inserter': 'sloth.items.IDRectItemInserter',
        'item': 'sloth.items.IDRectItem',
        'hotkey': 'P',
        'text': 'Pedestrian',
    },
)

# HOTKEYS
#
# Defines the keyboard shortcuts.  Each hotkey is defined by a tuple
# with at least 2 entries, where the first entry is the hotkey (sequence),
# and the second entry is the function that is called.  The function
# should expect a single parameter, the labeltool object.  The optional
# third entry -- if present -- is expected to be a string describing the 
# action.
# HOTKEYS = (
#     ('Space',     [lambda lt: lt.currentImage().confirmAll(),
#                    lambda lt: lt.currentImage().setUnlabeled(False),
#                    lambda lt: lt.gotoNext()
#                   ],                                         'Mark image as labeled/confirmed and go to next'),
#     ('Backspace', lambda lt: lt.gotoPrevious(),              'Previous image/frame'),
#     ('PgDown',    lambda lt: lt.gotoNext(),                  'Next image/frame'),
#     ('PgUp',      lambda lt: lt.gotoPrevious(),              'Previous image/frame'),
#     (']',         lambda lt: lt.gotoNext(),                  'Next image/frame'),
#     ('[',         lambda lt: lt.gotoPrevious(),              'Previous image/frame'),
#     ('Tab',       lambda lt: lt.selectNextAnnotation(),      'Select next annotation'),
#     ('Shift+Tab', lambda lt: lt.selectPreviousAnnotation(),  'Select previous annotation'),
#     ('Ctrl+f',    lambda lt: lt.view().fitInView(),          'Fit current image/frame into window'),
#     ('Del',       lambda lt: lt.deleteSelectedAnnotations(), 'Delete selected annotations'),
#     ('ESC',       lambda lt: lt.exitInsertMode(),            'Exit insert mode'),
#     ('Shift+l',   lambda lt: lt.currentImage().setUnlabeled(False), 'Mark current image as labeled'),
#     ('Shift+c',   lambda lt: lt.currentImage().confirmAll(), 'Mark all annotations in image as confirmed'),
# )
HOTKEYS = (
    ('Space', [lambda lt: lt.confirmAll(),
               lambda lt: lt.setUnlabeled(False),
               lambda lt: lt.gotoNextList()
               ], 'Mark image as labeled/confirmed and go to next'),
    ('Backspace', lambda lt: lt.gotoPreviousList(), 'Previous image/frame'),
    ('PgDown', lambda lt: lt.gotoNextList(), 'Next image/frame'),
    ('PgUp', lambda lt: lt.gotoPreviousList(), 'Previous image/frame'),
    (']', lambda lt: lt.gotoNextList(), 'Next image/frame'),
    ('[', lambda lt: lt.gotoPreviousList(), 'Previous image/frame'),
    ('Tab', lambda lt: lt.selectNextAnnotation(), 'Select next annotation'),
    ('Shift+Tab', lambda lt: lt.selectPreviousAnnotation(), 'Select previous annotation'),
    ('Ctrl+f', lambda lt: lt.fitInView(), 'Fit current image/frame into window'),
    ('Del', lambda lt: lt.deleteSelectedAnnotations(), 'Delete selected annotations'),
    ('ESC', lambda lt: lt.exitInsertMode(), 'Exit insert mode'),
    ('Shift+l', lambda lt: lt.setUnlabeled(False), 'Mark current image as labeled'),
    ('Shift+c', lambda lt: lt.confirmAll(), 'Mark all annotations in image as confirmed'),
    ('m', lambda lt: lt.switchDisplayMode(), 'Switch between single/multiple camera modes'),
    ('Ctrl+0', lambda lt: lt.gotoStampIndex(0), 'Goto the first frame.'),
    ('Ctrl+1', lambda lt: lt.gotoStampIndex(1), 'Goto the 1st stamp.'),
    ('Ctrl+2', lambda lt: lt.gotoStampIndex(2), 'Goto the 2nd stamp.'),
    ('Ctrl+3', lambda lt: lt.gotoStampIndex(3), 'Goto the 3rd stamp.'),
    ('Ctrl+4', lambda lt: lt.gotoStampIndex(4), 'Goto the 4th stamp.'),
    ('Ctrl+5', lambda lt: lt.gotoStampIndex(5), 'Goto the 5th stamp.'),
    ('Ctrl+6', lambda lt: lt.gotoStampIndex(6), 'Goto the 6th stamp.'),
    ('Ctrl+7', lambda lt: lt.gotoStampIndex(7), 'Goto the 7th stamp.'),
    ('Ctrl+8', lambda lt: lt.gotoStampIndex(8), 'Goto the 8th stamp.'),
    ('Ctrl+9', lambda lt: lt.gotoStampIndex(9), 'Goto the 9th stamp.'),
    ('Ctrl+[', lambda lt: lt.gotoPreviousStamp(), 'Goto the previous stamp.'),
    ('Ctrl+]', lambda lt: lt.gotoNextStamp(), 'Goto the next stamp.'),
)

# CONTAINERS
#
# A list/tuple of two-tuples defining the mapping between filename pattern and
# annotation container classes.  The filename pattern can contain wildcards
# such as * and ?.  The corresponding container is expected to either a python
# class implementing the sloth container interface, or a module path pointing
# to such a class.
CONTAINERS = (
    ('*.json', 'sloth.annotations.container.JsonContainer'),
    ('*.msgpack', 'sloth.annotations.container.MsgpackContainer'),
    ('*.yaml', 'sloth.annotations.container.YamlContainer'),
    ('*.pickle', 'sloth.annotations.container.PickleContainer'),
    ('*.sloth-init', 'sloth.annotations.container.FileNameListContainer'),
)

# PLUGINS
#
# A list/tuple of classes implementing the sloth plugin interface.  The
# classes can either be given directly or their module path be specified 
# as string.
PLUGINS = (
)

VIEWS = (
    {
        'folder': 'camera_6mm'
    },
    # {
    #     'folder': 'camera_12_5mm'
    # },
    {
        'folder': 'camera_25mm'
    },
    # {
    #     'folder': 'camera_50mm'
    # }
)

GLOBALS = {
    'labeltool': None
}
