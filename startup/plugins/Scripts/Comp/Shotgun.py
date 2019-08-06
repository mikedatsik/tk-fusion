import os
import sys
import sgtk

logger = sgtk.LogManager.get_logger(__name__)

logger.debug("Launching toolkit in classic mode.")
env_engine = os.environ.get("SGTK_ENGINE")
env_context = os.environ.get("SGTK_CONTEXT")
context = sgtk.context.deserialize(env_context)

engine = sgtk.platform.start_engine(env_engine, context.sgtk, context)

from sgtk.platform.qt import QtGui, QtCore

class Window(QtGui.QWidget):
    """Simple Test"""
    
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 300, 300)
        self.setWindowTitle("Shotgun: Manu Pannel")
        self.mainlayout()
        
    def mainlayout(self):
        #######################################
        self.jump_to_sg = QtGui.QAction(self)
        self.jump_to_sg.setText("Jump to Shotgun")
        self.jump_to_sg.activated.connect(lambda: self._jump_to_sg())

        self.jump_to_fs = QtGui.QAction(self)
        self.jump_to_fs.setText("Jump to File System")
        self.jump_to_fs.activated.connect(lambda: self._jump_to_fs())

        self.jump_to_rv = QtGui.QAction(self)
        self.jump_to_rv.setText("Jump to Screening Room in RV")
        self.jump_to_rv.activated.connect(lambda: self.callMenu('Jump to Screening Room in RV'))

        self.jump_to_wp = QtGui.QAction(self)
        self.jump_to_wp.setText("Jump to Screening Room Web Player")
        self.jump_to_wp.activated.connect(lambda: self.callMenu('Jump to Screening Room Web Player'))

        self.work_aria_info = QtGui.QAction(self)
        self.work_aria_info.setText("Work Area Info...")
        self.work_aria_info.activated.connect(lambda: self.callMenu('Work Area Info...'))

        self.context_menu = QtGui.QMenu(self)
        self.context_menu.addAction(self.jump_to_sg)
        self.context_menu.addAction(self.jump_to_fs)
        self.context_menu.addSeparator()
        self.context_menu.addAction(self.jump_to_rv)
        self.context_menu.addAction(self.jump_to_wp)
        self.context_menu.addAction(self.work_aria_info)

        self.context_button = QtGui.QPushButton(str(engine.context))
        self.context_button.setMenu(self.context_menu)
        #######################################

        self.open = QtGui.QPushButton("File Open...")
        self.open.clicked.connect(lambda: self.callMenu('File Open...'))

        self.save = QtGui.QPushButton("File Save...")
        self.save.clicked.connect(lambda: self.callMenu('File Save...'))

        self.snapshot = QtGui.QPushButton("Snapshot...")
        self.snapshot.clicked.connect(lambda: self.callMenu('Snapshot...'))

        self.publish = QtGui.QPushButton("Publish...")
        self.publish.clicked.connect(lambda: self.callMenu('Publish...'))

        self.load = QtGui.QPushButton("Load...")
        self.load.clicked.connect(lambda: self.callMenu('Load...'))

        self.breakdown = QtGui.QPushButton("Scene Breakdown...")
        self.breakdown.clicked.connect(lambda: self.callMenu('Scene Breakdown...'))


        #######################################
        self.snapshot_menu_history = QtGui.QAction(self)
        self.snapshot_menu_history.setText("Snapshot History...")
        self.snapshot_menu_history.activated.connect(lambda: self.callMenu('Snapshot History...'))

        self.snapshot_menu_snapshot = QtGui.QAction(self)
        self.snapshot_menu_snapshot.setText("Snapshot...")
        self.snapshot_menu_snapshot.activated.connect(lambda: self.callMenu('Snapshot...'))        

        self.snapshot_menu = QtGui.QMenu(self)
        self.snapshot_menu.addAction(self.snapshot_menu_history)
        self.snapshot_menu.addAction(self.snapshot_menu_snapshot)

        self.snapshot_button = QtGui.QPushButton("Scene Snapshot")
        self.snapshot_button.setMenu(self.snapshot_menu)
        #######################################


        self.pannel = QtGui.QPushButton("Shotgun Panel...")
        self.pannel.clicked.connect(lambda: self.callMenu('Shotgun Panel...'))

        #######################################
        self.shotgun_workfiles_menu_open = QtGui.QAction(self)
        self.shotgun_workfiles_menu_open.setText("File Open...")
        self.shotgun_workfiles_menu_open.activated.connect(lambda: self.callMenu('File Open...'))

        self.shotgun_workfiles_menu_save = QtGui.QAction(self)
        self.shotgun_workfiles_menu_save.setText("File Save...")
        self.shotgun_workfiles_menu_save.activated.connect(lambda: self.callMenu('File Save...'))

        self.shotgun_workfiles_menu = QtGui.QMenu(self)
        self.shotgun_workfiles_menu.addAction(self.shotgun_workfiles_menu_open)
        self.shotgun_workfiles_menu.addAction(self.shotgun_workfiles_menu_save)

        self.shotgun_workfiles = QtGui.QPushButton("Shotgun Workfiles")
        self.shotgun_workfiles.setMenu(self.shotgun_workfiles_menu)
        #######################################

        self.syncFr = QtGui.QPushButton("Sync Frame Range with Shotgun")
        self.syncFr.clicked.connect(lambda: self.callMenu('Sync Frame Range with Shotgun'))

        qvbox = QtGui.QVBoxLayout()

        qvbox.addWidget(self.context_button)

        self.line_context = QtGui.QFrame()
        self.line_context.setFrameShape(QtGui.QFrame.HLine)
        self.line_context.setFrameShadow(QtGui.QFrame.Sunken)        
        qvbox.addWidget(self.line_context)

        qvbox.addWidget(self.open)
        qvbox.addWidget(self.snapshot)
        qvbox.addWidget(self.save)
        qvbox.addWidget(self.publish)

        self.line_open = QtGui.QFrame()
        self.line_open.setFrameShape(QtGui.QFrame.HLine)
        self.line_open.setFrameShadow(QtGui.QFrame.Sunken)
        qvbox.addWidget(self.line_open)

        qvbox.addWidget(self.load)
        qvbox.addWidget(self.breakdown)
        
        qvbox.addWidget(self.snapshot_button)
        
        qvbox.addWidget(self.pannel)

        qvbox.addWidget(self.shotgun_workfiles)

        qvbox.addWidget(self.syncFr)

        # qvbox.insertStretch(2)
        self.setLayout(qvbox)
                    
    def run(self):
        self.show()
    
    def callMenu(self, name):
        for item in engine.commands.items():
            if name in item[0]:
                item[1].get('callback').__call__()
        
        if name in ["File Open...", "File Save..."]:
            self.context_button.setText(str(engine.context))

    def _jump_to_sg(self):
        """
        Jump to shotgun, launch web browser
        """
        url = engine.context.shotgun_url
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

    def _jump_to_fs(self):
        """
        Jump from context to FS
        """
        # launch one window for each location on disk
        paths = engine.context.filesystem_locations
        for disk_location in paths:

            # get the setting
            system = sys.platform

            # run the app
            if system == "linux2":
                cmd = 'xdg-open "%s"' % disk_location
            elif system == "darwin":
                cmd = 'open "%s"' % disk_location
            elif system == "win32":
                cmd = 'cmd.exe /C start "Folder" "%s"' % disk_location
            else:
                raise Exception("Platform '%s' is not supported." % system)

            exit_code = os.system(cmd)
            if exit_code != 0:
                engine.logger.error("Failed to launch '%s'!", cmd)

app = QtGui.QApplication.instance()

wid = Window()
wid.run()

engine._qt_app.exec_()