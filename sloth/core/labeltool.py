"""
This is the core labeltool module.
"""
import os
import sys
import json
# from PyQt4.QtGui import *
# from PyQt4.QtCore import *
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QCheckBox
from PyQt5.Qt import *
from PyQt5 import QtGui
from sloth.annotations.model import *
from sloth.annotations.container import AnnotationContainerFactory, AnnotationContainer
from sloth.conf import config
from sloth.core.cli import LaxOptionParser, BaseCommand
from sloth.core.utils import import_callable
from sloth import VERSION
from sloth.core.commands import get_commands
from sloth.gui import MainWindow
from sloth.utils.calibration import Calibration
import logging

LOG = logging.getLogger(__name__)

try:
    import okapy.videoio as okv
except ImportError:
    pass


class LabelTool(QObject):
    """
    This is the main label tool object.  It stores the state of the tool, i.e.
    the current annotations, the containers responsible for loading and saving
    etc.

    It is also responsible for parsing command line options, call respective
    commands or start the gui.
    """
    usage = "\n" + \
            "  %prog [options] [filename]\n\n" + \
            "  %prog subcommand [options] [args]\n"

    help_text = "Sloth can be started in two different ways.  If the first argument\n" + \
                "is any of the following subcommands, this command is executed.  Otherwise the\n" + \
                "sloth_autolab GUI is started and the optionally given label file is loaded.\n" + \
                "\n" + \
                "Type '%s help <subcommand>' for help on a specific subcommand.\n\n"

    # Signals
    statusMessage = pyqtSignal(str)
    annotationsLoaded = pyqtSignal()
    pluginLoaded = pyqtSignal(QAction)
    # This still emits a QModelIndex, because Qt cannot handle emiting
    # a derived class instead of a base class, i.e. ImageFileModelItem
    # instead of ModelItem
    currentImageChanged = pyqtSignal()

    # TODO clean up --> prefix all members with _
    def __init__(self, parent=None):
        """
        Constructor.  Does nothing except resetting everything.
        Initialize the labeltool with either::

            execute_from_commandline()

        or::

            init_from_config()
        """
        QObject.__init__(self, parent)

        self.n_view = len(config.VIEWS)

        self._container_factory = None
        self._container = AnnotationContainer()
        self._model = AnnotationModel([])
        self._mainwindow = None
        self._keepAnnos = False

        self._container_list = [AnnotationContainer()] * self.n_view
        self._model_list = [AnnotationModel([])] * self.n_view
        self._current_image_list = [None] * self.n_view

        self.mulcam_mode = True
        self.max_id_dict = {}

        self._img_width = 0
        self._img_height = 0
        self._calib = None
        self._cur_row = -1

        self._opened_file_name = None

    def updateAnnotations(self, anno, scene_id, factor=1.5):
        if not self._calib:
            self._img_width = self._mainwindow.annotation_scenes[0]._pixmap.width()
            self._img_height = self._mainwindow.annotation_scenes[0]._pixmap.height()
            self._calib = Calibration(self.n_view, self._img_width, self._img_height)

        for scene in self._mainwindow.annotation_scenes:
            idx = scene.getIndex()
            if idx is not scene_id:
                ann = anno.copy()
                ann_new = self._calib.getConvertedAnno(ann, scene_id, idx)
                scene.updateAnnotations(ann_new)

        self._mainwindow.updateStatusBar()

    def main_help_text(self):
        """
        Returns the labeltool's main help text, as a string.

        Includes a list of all available subcommands.
        """
        usage = self.help_text % self.prog_name
        usage += 'Available subcommands:\n'
        commands = list(get_commands().keys())
        commands.sort()
        for cmd in commands:
            usage += '  %s\n' % cmd
        return usage

    def execute_from_commandline(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(argv[0])

        # Preprocess options to extract --settings and --pythonpath.
        # These options could affect the commands that are available, so they
        # must be processed early.
        parser = LaxOptionParser(usage=self.usage,
                                 version=VERSION,
                                 option_list=BaseCommand.option_list)
        try:
            options, args = parser.parse_args(self.argv)
        except:
            pass  # Ignore any option errors at this point.

        # Initialize logging
        loglevel = (logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG)[
            int(options.verbosity)]
        logging.basicConfig(level=loglevel,
                            format='%(asctime)s %(levelname)-8s %(name)-30s %(message)s')  # , datefmt='%H:%M:%S.%m')

        # Disable PyQt log messages
        logging.getLogger("PyQt5").setLevel(logging.WARNING)

        # Handle options common for all commands
        # and initialize the labeltool object from
        # the configuration (default config if not specified)
        if options.pythonpath:
            sys.path.insert(0, options.pythonpath)
        self.init_from_config(options.config)

        # check for commands
        try:
            subcommand = args[1]
        except IndexError:
            subcommand = None

        # handle commands and command line arguments
        if subcommand == 'help':
            if len(args) > 2:
                self.fetch_command(args[2]).print_help(self.prog_name, args[2])
                sys.exit(0)
            else:
                sys.stdout.write(self.main_help_text() + '\n')
                parser.print_lax_help()
                sys.exit(1)

        elif self.argv[1:] == ['--version']:
            # LaxOptionParser already takes care of printing the version.
            sys.exit(0)

        elif self.argv[1:] in (['--help'], ['-h']):
            sys.stdout.write(self.main_help_text() + '\n')
            parser.print_lax_help()
            sys.exit(0)

        elif subcommand in get_commands():
            self.fetch_command(subcommand).run_from_argv(self.argv)
            sys.exit(0)

        else:
            # Setup GUI
            self._mainwindow = MainWindow(self)
            self._mainwindow.show()

            # Load plugins
            self.loadPlugins(config.PLUGINS)

            # check if args contain a labelfile filename to load
            if len(args) > 1:
                try:
                    self.loadAnnotations(args[1], handleErrors=False)

                    # goto to first image
                    self.gotoNextList()
                except Exception as e:
                    LOG.fatal("Error loading annotations: %s" % e)
                    if (int(options.verbosity)) > 1:
                        raise
                    else:
                        sys.exit(1)
            else:
                self.clearAnnotations()

    def fetch_command(self, subcommand):
        """
        Tries to fetch the given subcommand, printing a message with the
        appropriate command called from the command line if it can't be found.
        """
        try:
            app_name = get_commands()[subcommand]
        except KeyError:
            sys.stderr.write("Unknown command: %r\nType '%s help' for usage.\n" %
                             (subcommand, self.prog_name))
            sys.exit(1)
        if isinstance(app_name, BaseCommand):
            # If the command is already loaded, use it directly.
            klass = app_name
        else:
            pass
            # TODO implement load_command_class
            # klass = load_command_class(app_name, subcommand)

        # set labeltool reference
        klass.labeltool = self

        return klass

    def init_from_config(self, config_module_path=""):
        """
        Initializes the labeltool from the given configuration
        at ``config_module_path``.  If empty, the default configuration
        is used.
        """
        # Load config
        if config_module_path:
            config.update(config_module_path)

        # Instatiate container factory
        self._container_factory = AnnotationContainerFactory(config.CONTAINERS)

    def loadPlugins(self, plugins):
        self._plugins = []
        for plugin in plugins:
            if type(plugin) == str:
                plugin = import_callable(plugin)
            p = plugin(self)
            self._plugins.append(p)
            action = p.action()
            self.pluginLoaded.emit(action)

    # Annotation file handling
    def createAnnotations(self, fname):
        fname = str(fname)
        seqinfo = json.load(open(fname, 'r'))

        seq_id = seqinfo['ID']
        print('=== You are solving from ID: {}'.format(seq_id))
        anno_dir = 'annotations-' + str(seq_id)
        print('=== Load annotations from dir: '.format(anno_dir))
        if not os.path.exists(anno_dir):
            print('=== This dir seems not exist. Let go fucking exit...')
            exit(0)
        anno_dir = os.path.join(os.path.dirname(fname), anno_dir)
        if not os.path.isdir(anno_dir):
            os.mkdir(anno_dir)

        img_dir_list = seqinfo['img_dir'].split(',')
        img_fmt = seqinfo['img_format']
        start_frame = int(seqinfo['start_frame'])
        end_frame = int(seqinfo['end_frame'])
        anno_file_list = []

        for img_dir in img_dir_list:
            anno_file = os.path.join(anno_dir, img_dir + '.json')
            anno_file_list.append(anno_file)

            if os.path.isfile(anno_file):
                continue

            anno_list = []
            for f_id in range(start_frame, end_frame + 1):
                anno = {}
                anno['annotations'] = []
                anno['class'] = 'image'
                anno['filename'] = os.path.join('..', img_dir, img_fmt % f_id)
                anno_list.append(anno)

            with open(anno_file, 'w') as f:
                json.dump(anno_list, f, indent=4, sort_keys=True)

        self.camera_names = img_dir_list

        return anno_file_list

    def createMaxIDDict(self, anno_file_list):
        max_id_dict = {}
        for label in config.LABELS:
            max_id_dict[label['attributes']['class']] = 0

        for anno_file in anno_file_list:
            with open(anno_file, 'r') as f:
                items = json.load(f)
                for item in items:
                    if not item['annotations']:
                        continue
                    for anno in item['annotations']:
                        if 'class' in anno and 'ID' in anno:
                            c = anno['class']
                            idx = int(anno['ID'])
                            if c in max_id_dict and idx > max_id_dict[c]:
                                max_id_dict[c] = idx

        return max_id_dict

    def loadAnnotations(self, f_name, handleErrors=True):
        f_name = str(f_name)  # convert from QString
        self._opened_file_name = f_name
        self._seq_name = os.path.basename(f_name)

        # check if f_name is exist or not
        if not os.path.exists(f_name):
            print('seq_info json file not exist: {}'.format(f_name))
            exit(0)
        try:
            anno_file_list = self.createAnnotations(f_name)
            self.max_id_dict = self.createMaxIDDict(anno_file_list)

            for i in range(self.n_view):
                anno_file = anno_file_list[i]
                self._container_list[i] = self._container_factory.create(anno_file)
                self._model_list[i] = AnnotationModel(self._container_list[i].load(anno_file))

            self._container = self._container_list[0]
            self._model = self._model_list[0]

            msg = "Successfully loaded %s (%d files, %d annotations)" % \
                  (f_name, self._model.root().numFiles(), self._model.root().numAnnotations())
        except Exception as e:
            if handleErrors:
                msg = "Error: Loading failed (%s)" % str(e)
            else:
                raise

        self.statusMessage.emit(msg)
        self.annotationsLoaded.emit()

    def annotations(self):
        if self._model is None:
            return None
        return self._model.root().getAnnotations()

    def changeIDForAll(self, id_orig, id_new):
        success = False

        row = self._mainwindow.treeview_list[0].currentIndex().row()
        if row < 0:
            row = self._cur_row
        print('row:', row)

        step = 400
        row_start = int(row / 400) * 400
        row_end = min(row_start + 400, self._model_list[0].rowCount() - 1)

        print('start:', row_start, 'end:', row_end)

        try:
            for i in range(self.n_view):
                # create new container if the filename is different
                fname = self._container_list[i].filename()

                # Get annotations dict
                ann = self._model_list[i].root().getAnnotations()

                for ann_per_frame in ann[row_start:row_end]:
                    for ann_per_target in ann_per_frame['annotations']:
                        if ann_per_target['ID'] == id_orig:
                            ann_per_target['ID'] = id_new

                self._container_list[i].save(ann, fname)

                # self._model.writeback() # write back changes that are cached in the model itself, e.g. mask updates
                # msg = "Successfully saved %s (%d files, %d annotations)" % \
                #     (fname, self._model.root().numFiles(), self._model.root().numAnnotations())
                msg = "Successfully saved files."
                success = True
                self._model_list[i].setDirty(False)

            self.loadAnnotations(self._opened_file_name)

            row = (row + 1) % self._model_list[0].rowCount()
            for i in range(self.n_view):
                self._mainwindow.treeview_list[i].setCurrentIndex(self._model_list[i].index(row, 0))

            row = (row - 1 + self._model_list[0].rowCount()) % self._model_list[0].rowCount()
            for i in range(self.n_view):
                self._mainwindow.treeview_list[i].setCurrentIndex(self._model_list[i].index(row, 0))
        except Exception as e:
            msg = "Error: Saving failed (%s)" % str(e)

        self.statusMessage.emit(msg)
        return success

    def gotoStampIndex(self, idx_stamp):
        step = 400
        row = idx_stamp * 400
        if row > self._model_list[0].rowCount():
            row = 0
        for i in range(self.n_view):
            self._mainwindow.treeview_list[i].setCurrentIndex(self._model_list[i].index(row, 0))
        self._cur_row = self._mainwindow.treeview_list[0].currentIndex().row()

    def gotoNextStamp(self):
        step = 400
        cur_row = self._mainwindow.treeview_list[0].currentIndex().row()
        row = (cur_row / 400 + 1) * 400
        if row > self._model_list[0].rowCount():
            row = 0
        for i in range(self.n_view):
            self._mainwindow.treeview_list[i].setCurrentIndex(self._model_list[i].index(row, 0))
        self._cur_row = self._mainwindow.treeview_list[0].currentIndex().row()

    def gotoPreviousStamp(self):
        step = 400
        cur_row = self._mainwindow.treeview_list[0].currentIndex().row()
        row = (cur_row - 1) / 400 * 400
        if row < 0:
            row = int(max(self._model_list[0].rowCount() - 1, 0))
            row = row / 400 * 400
        for i in range(self.n_view):
            self._mainwindow.treeview_list[i].setCurrentIndex(self._model_list[i].index(row, 0))
        self._cur_row = self._mainwindow.treeview_list[0].currentIndex().row()

    def saveAnnotations(self, fname):
        success = False
        try:
            # create new container if the filename is different
            if fname != self._container.filename():
                self._container = self._container_factory.create(fname)

            # Get annotations dict
            ann = self._model.root().getAnnotations()

            self._container.save(ann, fname)
            # self._model.writeback() # write back changes that are cached in the model itself, e.g. mask updates
            msg = "Successfully saved %s (%d files, %d annotations)" % \
                  (fname, self._model.root().numFiles(), self._model.root().numAnnotations())
            success = True
            self._model.setDirty(False)
        except Exception as e:
            msg = "Error: Saving failed (%s)" % str(e)

        self.statusMessage.emit(msg)
        return success

    def saveAnnotationList(self, filelist):
        success = False

        try:
            for i, fname in enumerate(filelist):
                # create new container if the filename is different
                if fname != self._container_list[i].filename():
                    self._container_list[i] = self._container_factory.create(fname)

                # Get annotations dict
                ann = self._model_list[i].root().getAnnotations()

                self._container_list[i].save(ann, fname)
                # self._model.writeback() # write back changes that are cached in the model itself, e.g. mask updates
                # msg = "Successfully saved %s (%d files, %d annotations)" % \
                #     (fname, self._model.root().numFiles(), self._model.root().numAnnotations())
                msg = "Successfully saved files."
                success = True
                self._model_list[i].setDirty(False)
        except Exception as e:
            msg = "Error: Saving failed (%s)" % str(e)

        self.statusMessage.emit(msg)
        return success

    def clearAnnotations(self):
        self._model = AnnotationModel([])
        # self._model.setBasedir("")
        self.statusMessage.emit('')
        self.annotationsLoaded.emit()

    def getCurrentFilename(self):
        return self._opened_file_name

    def getCurrentFilenameList(self):
        file_list = []
        for c in self._container_list:
            file_list.append(c.filename())
        return file_list

    ###########################################################################
    # Model stuff
    ###########################################################################

    def model(self):
        return self._model

    def modelList(self):
        return self._model_list

    def gotoIndexList(self, idx):
        next_image_list = []

        for i in range(self.n_view):
            if self._model_list[i] is None:
                return

            current = self._current_image_list[i]
            if current is None:
                current = next(self._model_list[i].iterator(ImageModelItem))

            next_image = current.getSibling(idx)
            if next_image is not None:
                next_image_list.append(next_image)

        if len(next_image_list) == self.n_view:
            self.setCurrentImageList(next_image_list)
        self._cur_row = self._mainwindow.treeview_list[0].currentIndex().row()

    def gotoNextList(self, step=1):
        next_image_list = []

        if not step:
            step = 1

        for i in range(self.n_view):
            if self._model_list[i] is not None:
                if self._current_image_list[i] is not None:
                    next_image = self._current_image_list[i].getNextSibling(step)
                else:
                    next_image = next(self._model_list[i].iterator(ImageModelItem))
                    if next_image is not None:
                        next_image = next_image.getNextSibling(step - 1)

                if next_image is not None:
                    next_image_list.append(next_image)

        if len(next_image_list) == self.n_view:
            self._keepAnnos = True
            self.setCurrentImageList(next_image_list)
            self._keepAnnos = False
        self._cur_row = self._mainwindow.treeview_list[0].currentIndex().row()

    def gotoPreviousList(self, step=1):
        prev_image_list = []

        if not step:
            step = 1

        for i in range(self.n_view):
            if self._model_list[i] is not None and self._current_image_list[i] is not None:
                prev_image = self._current_image_list[i].getPreviousSibling(step)

                if prev_image is not None:
                    prev_image_list.append(prev_image)

        if len(prev_image_list) == self.n_view:
            self.setCurrentImageList(prev_image_list)
        self._cur_row = self._mainwindow.treeview_list[0].currentIndex().row()

    def updateModified(self):
        """update all GUI elements which depend on the state of the model,
        e.g. whether it has been modified since the last save"""
        # self.ui.action_Add_Image.setEnabled(self._model is not None)
        # TODO also disable/enable other items
        # self.ui.actionSave.setEnabled(self.annotations.dirty())
        # self.setWindowModified(self.annotations.dirty())
        pass

    # def currentImage(self):
    #     return self._current_image

    def currentImageList(self):
        return self._current_image_list

    def confirmAll(self):
        for image in self._current_image_list:
            image.confirmAll()

    def setUnlabeled(self, flag=False):
        for image in self._current_image_list:
            image.setUnlabeled(flag)

    def setCurrentImageList(self, image_list):
        if isinstance(image_list, QModelIndex):
            row = image_list.row()
            column = image_list.column()
            image_list = []
            for model in self._model_list:
                index = model.index(row, column)
                item = model.itemFromIndex(index)
                image_list.append(item)

        for i in range(self.n_view):
            new_image = image_list[i]

            if isinstance(new_image, RootModelItem):
                return
            while (new_image is not None) and (not isinstance(new_image, ImageModelItem)):
                new_image = new_image.parent()
            if new_image is None:
                raise RuntimeError("Tried to set current image to item that has no Image or Frame as parent!")
            if new_image != self._current_image_list[i]:
                self._current_image_list[i] = new_image

        self.currentImageChanged.emit()

    def getImage(self, item):
        if item['class'] == 'frame':
            video = item.parent()
            return self._container.loadFrame(video['filename'], item['num'])
        else:
            return self._container.loadImage(item['filename'])

    def getImageList(self, item):
        for container in self._container_list:
            if item['class'] == 'frame':
                video = item.parent()
                return container.loadFrame(video['filename'], item['num'])
            else:
                return container.loadImage(item['filename'])

    def switchDisplayMode(self):
        views = self._mainwindow.view.scene_views
        active_view = self._mainwindow.view.getActiveSceneView()

        if self.mulcam_mode:
            active_view.show()
            for view in views:
                if view is not active_view:
                    view.hide()
            self.mulcam_mode = False
        else:
            for view in views:
                view.show()
            self.mulcam_mode = True

    def getAnnotationFilePatterns(self):
        return self._container_factory.patterns()

    def addImageFile(self, fname):
        fileitem = {
            'filename': fname,
            'class': 'image',
            'annotations': [],
        }
        return self._model._root.appendFileItem(fileitem)

    def addVideoFile(self, fname):
        fileitem = {
            'filename': fname,
            'class': 'video',
            'frames': [],
        }

        # FIXME: OKAPI should provide a method to get all timestamps at once
        # FIXME: Some dialog should be displayed, telling the user that the
        # video is being loaded/indexed and that this might take a while
        LOG.info("Importing frames from %s. This may take a while..." % fname)
        video = okv.createVideoSourceFromString(fname)
        video = okv.toRandomAccessVideoSource(video)

        # try to convert to iseq, getting all timestamps will be significantly faster
        iseq = okv.toImageSeqReader(video)
        if iseq is not None:
            timestamps = iseq.getTimestamps()
            LOG.debug("Adding %d frames" % len(timestamps))
            fileitem['frames'] = [{'annotations': [], 'num': i,
                                   'timestamp': ts, 'class': 'frame'}
                                  for i, ts in enumerate(timestamps)]
        else:
            i = 0
            while video.getNextFrame():
                LOG.debug("Adding frame %d" % i)
                ts = video.getTimestamp()
                frame = {'annotations': [],
                         'num': i,
                         'timestamp': ts,
                         'class': 'frame'
                         }
                fileitem['frames'].append(frame)
                i += 1

        self._model._root.appendFileItem(fileitem)

    # GUI functions
    def mainWindow(self):
        return self._mainwindow

    # PropertyEditor functions
    def propertyeditor(self):
        if self._mainwindow is None:
            return None
        else:
            return self._mainwindow.property_editor

    # Scene functions
    # def scene(self):
    #     if self._mainwindow is None:
    #         return None
    #     else:
    #         return self._mainwindow.scene

    # def view(self):
    #     if self._mainwindow is None:
    #         return None
    #     else:
    #         return self._mainwindow.view

    def fitInView(self):
        if self._mainwindow is None:
            return
        else:
            for view in self._mainwindow.view.scene_views:
                view.fitInView()

    def selectNextAnnotation(self):
        if self._mainwindow is not None:
            for scene in self._mainwindow.annotation_scenes:
                scene.selectNextItem()

    def selectPreviousAnnotation(self):
        if self._mainwindow is not None:
            for scene in self._mainwindow.annotation_scenes:
                scene.selectNextItem(reverse=True)

    def selectAllAnnotations(self):
        if self._mainwindow is not None:
            for scene in self._mainwindow.annotation_scenes:
                scene.selectAllItems()

    def deleteSelectedAnnotations(self):
        if self._mainwindow is not None:
            index = self._mainwindow.view.active_scene_view
            self._mainwindow.annotation_scenes[index].deleteSelectedItems()
            # for scene in self._mainwindow.annotation_scenes:
            #     scene.deleteSelectedItems()

    def deleteAllSelectedAnnotations(self):
        if self._mainwindow is not None:
            items = []
            for scene in self._mainwindow.annotation_scenes:
                for item in scene.selectedItems():
                    items.append(item)
            if len(items) > 0:
                for item in items:
                    for scene in self._mainwindow.annotation_scenes:
                        scene.deleteItemsByID(item.getID())

    def exitInsertMode(self):
        if self._mainwindow is not None:
            return self._mainwindow.property_editor.endInsertionMode()

    # TreeView functions
    def treeView(self):
        if self._mainwindow is None:
            return None
        else:
            return self._mainwindow.treeview

    def treeviewList(self):
        if self._mainwindow is None:
            return None
        else:
            return self._mainwindow.treeview_list
