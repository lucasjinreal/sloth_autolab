LABELS = (
    {
        'attributes': {
            'type': 'lane1',
            'class': 'lane1',
        },
        'inserter': 'sloth.items.PolygonItemInserter',
        'item': 'sloth.items.PolygonItem',
        'hotkey': '1',
        'text': 'lane1',
    },
    {
        'attributes': {
            'type': 'lane2',
            'class': 'lane2',
        },
        'inserter': 'sloth.items.PolygonItemInserter',
        'item': 'sloth.items.PolygonItem2',
        'hotkey': '2',
        'text': 'lane2',
    },
    {
        'attributes': {
            'type': 'lane3',
            'class': 'lane3',
        },
        'inserter': 'sloth.items.PolygonItemInserter',
        'item': 'sloth.items.PolygonItem3',
        'hotkey': '3',
        'text': 'lane3',
    },
    {
        'attributes': {
            'type': 'lane4',
            'class': 'lane4',
        },
        'inserter': 'sloth.items.PolygonItemInserter',
        'item': 'sloth.items.PolygonItem4',
        'hotkey': '4',
        'text': 'lane4',
    },
    {
        'attributes': {
            'type': 'lane5',
            'class': 'lane5',
        },
        'inserter': 'sloth.items.PolygonItemInserter',
        'item': 'sloth.items.PolygonItem5',
        'hotkey': '5',
        'text': 'lane5',
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
HOTKEYS = (
    ('Space', [lambda lt: lt.currentImage().confirmAll(),
               lambda lt: lt.currentImage().setUnlabeled(False),
               lambda lt: lt.gotoNext()
               ], 'Mark image as labeled/confirmed and go to next'),
    ('Backspace', lambda lt: lt.gotoPrevious(), 'Previous image/frame'),
    ('PgDown', lambda lt: lt.gotoNext(), 'Next image/frame'),
    ('PgUp', lambda lt: lt.gotoPrevious(), 'Previous image/frame'),
    ('Tab', lambda lt: lt.selectNextAnnotation(), 'Select next annotation'),
    ('Shift+Tab', lambda lt: lt.selectPreviousAnnotation(), 'Select previous annotation'),
    ('Ctrl+f', lambda lt: lt.view().fitInView(), 'Fit current image/frame into window'),
    ('Del', lambda lt: lt.deleteSelectedAnnotations(), 'Delete selected annotations'),
    ('ESC', lambda lt: lt.exitInsertMode(), 'Exit insert mode'),
    ('Shift+l', lambda lt: lt.currentImage().setUnlabeled(False), 'Mark current image as labeled'),
    ('Shift+c', lambda lt: lt.currentImage().confirmAll(), 'Mark all annotations in image as confirmed'),
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
