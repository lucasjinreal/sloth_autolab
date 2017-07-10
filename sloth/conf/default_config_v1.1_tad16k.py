LABELS = (
    {"attributes": {"type": "sign_w",
                    "class": "warning(w)",
                    "sign_w": ["w1", "w2", "w3", "w4", "w5", "w6", "w7", "w8", "w9", "w10",
                               "w11", "w12", "w13", "w14", "w15", "w16", "w17", "w18", "w19", "w20",
                               "w21", "w22", "w23", "w24", "w25", "w26", "w27", "w28", "w29", "w30",
                               "w31", "w32", "w33", "w34", "w35", "w36", "w37", "w38", "w39", "w40",
                               "w41", "w42", "w43", "w44", "w45", "w46", "w47", "w48", "w49", "w50",
                               "w51", "w52", "w53", "w54", "w55", "w56", "w57", "w58", "w59", "w60",
                               "w61", "w62", "w63", "w64", "w65", "w66", "w67", "wo"]},
     "item": "sloth.items.SWRectItem",
     "inserter": "sloth.items.RectItemInserter",
     "text": "warning traffic sign",
     'hotkey': 'w'
     },

    {"attributes": {"type": "sign_p",
                    "class": "prohibitory(i)",
                    "sign_p": ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9", "p10",
                               "p11", "p12", "p13", "p14", "p15", "p16", "p17", "p18", "p19", "p20",
                               "p21", "p22", "p23", "p24", "p25", "p26", "p27", "p28", "p29", "pm*", "pa*",
                               "pd", "pc", "pn", "pnl", "pl*", "pr*", "ph*", "pw*", "ps", "pg", "pb", "pe", "pne",
                               "po"]},
     "item": "sloth.items.SPRectItem",
     "inserter": "sloth.items.RectItemInserter",
     "text": "prohibitory traffic sign",
     'hotkey': 'i'
     },

    {"attributes": {"type": "sign_m",
                    "class": "mandatory(m)",
                    "sign_m": ["i1", "i2", "i3", "i4", "i5", "i6", "i7", "i8", "i9", "i10",
                               "i11", "i12", "i13", "i14", "i15", "ip", "il*", "io"]},
     "item": "sloth.items.SMRectItem",
     "inserter": "sloth.items.RectItemInserter",
     "text": "mandatory traffic sign",
     'hotkey': 'm'
     },

    {"attributes": {"type": "vehicle",
                    "class": "vehicle(v)",
                    "veh": ["vehicle"]},
     "item": "sloth.items.VERectItem",
     "inserter": "sloth.items.RectItemInserter",
     "text": "vehicle",
     'hotkey': 'v'
     },

    {"attributes": {"type": "pedestrian",
                    "class": "pedestrian(p)",
                    "ped": ["pedestrian"]},
     "item": "sloth.items.PDRectItem",
     "inserter": "sloth.items.RectItemInserter",
     "text": "pedestrian",
     'hotkey': 'p'
     },

    {"attributes": {"type": "light",
                    "class": "light(l)",
                    "light": ["red", "yellow", "green", 'person', 'bike', "other"]},
     "item": "sloth.items.LTRectItem",
     "inserter": "sloth.items.RectItemInserter",
     "text": "light",
     'hotkey': 'l'
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
