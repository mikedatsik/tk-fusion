import os
import re
import sys
import sgtk
import BlackmagicFusion as bmd

fusion = bmd.scriptapp("Fusion")
comp = fusion.GetCurrentComp()

logger = sgtk.LogManager.get_logger(__name__)

logger.debug("Launching toolkit in classic mode.")
env_engine = os.environ.get("SGTK_ENGINE")
env_context = os.environ.get("SGTK_CONTEXT")
context = sgtk.context.deserialize(env_context)

try:
    path = comp.GetAttrs()['COMPS_FileName']
    tk = sgtk.sgtk_from_path(path)
    context = tk.context_from_path(path)
except:
    pass

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
        self.context_button.setStyleSheet("background-color: #4A586E")
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

        #######################################
        self.sg_saver_dpx_out = QtGui.QAction(self)
        self.sg_saver_dpx_out.setText("Dpx Output")
        self.sg_saver_dpx_out.activated.connect(lambda: self.__create_sg_saver('dpx'))

        self.sg_saver_exr16_out = QtGui.QAction(self)
        self.sg_saver_exr16_out.setText("Exr, 16 bit Output")
        self.sg_saver_exr16_out.activated.connect(lambda: self.__create_sg_saver('exr'))

        self.sg_saver_pngProxy_out = QtGui.QAction(self)
        self.sg_saver_pngProxy_out.setText("Png, Proxy with Alpha")
        self.sg_saver_pngProxy_out.activated.connect(lambda: self.__create_sg_saver('png'))

        self.sg_saver_review_out = QtGui.QAction(self)
        self.sg_saver_review_out.setText("Shotgun Quick Review")
        self.sg_saver_review_out.activated.connect(lambda: self.__create_sg_saver('mov'))

        self.shotgun_output_menu = QtGui.QMenu(self)
        self.shotgun_output_menu.addAction(self.sg_saver_dpx_out)
        self.shotgun_output_menu.addAction(self.sg_saver_exr16_out)
        self.shotgun_output_menu.addAction(self.sg_saver_pngProxy_out)
        self.shotgun_output_menu.addAction(self.sg_saver_review_out)

        self.sg_saver = QtGui.QPushButton("Create Output Node")
        self.sg_saver.setMenu(self.shotgun_output_menu)
        self.sg_saver.setStyleSheet("background-color: #810B44")

        self.sg_saver_update = QtGui.QPushButton("Update Output Nodes")
        self.sg_saver_update.clicked.connect(lambda: self.__update_sg_saver())
        self.sg_saver_update.setStyleSheet("background-color: #4A586E")
        #######################################

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

        self.line_tools = QtGui.QFrame()
        self.line_tools.setFrameShape(QtGui.QFrame.HLine)
        self.line_tools.setFrameShadow(QtGui.QFrame.Sunken)        
        qvbox.addWidget(self.line_tools)

        qvbox.addWidget(self.sg_saver)
        qvbox.addWidget(self.sg_saver_update)
        
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

    def __create_sg_saver(self, ext_type):
        comp = fusion.GetCurrentComp()
        path = comp.GetAttrs()['COMPS_FileName']

        task_type = engine.context.entity.get("type")
        work_template = engine.sgtk.template_from_path(path)
        fields = work_template.get_fields(path)

        comp_format = comp.GetPrefs().get('Comp').get('FrameFormat')
        fields['height'] = int(comp_format.get('Height'))
        fields['width'] = int(comp_format.get('Width'))
        fields['output'] = 'output'

        text, ok = QtGui.QInputDialog.getText(self, 'Input Name Dialog', 'Enter output name:')
        
        if text and ok:
            fields['output'] = text

        review_template = engine.get_template_by_name("fusion_%s_render_mono_%s" % (task_type.lower(), ext_type))
        output = review_template.apply_fields(fields)
        output = re.sub(r'%(\d+)d', '', output)

        comp.Lock()

        saver = comp.Saver({"Clip": output})
        saver.SetAttrs({"TOOLS_Name": "shotgun_%s" % ext_type})
        comp.Unlock()

    def __update_sg_saver(self):
        comp = fusion.GetCurrentComp()
        path = comp.GetAttrs()['COMPS_FileName']

        work_template = engine.sgtk.template_from_path(path)
        work_version = work_template.get_fields(path).get('version')
        
        savers = comp.GetToolList(False, "Saver").values()

        saver_names = []

        for saver in savers:
            path = saver.GetAttrs()['TOOLST_Clip_Name'].values()[0]
            template = engine.sgtk.template_from_path(path)
            if template:
                fields = template.get_fields(path)
                template_version = fields.get('version')
                if template_version is not work_version:
                    fields['version'] = work_version
                    saver.Clip = template.apply_fields(fields)
                    saver_names.append("<b>(%s)</b> form: v%03d to: v%03d<br>" % (saver.GetAttrs("TOOLS_Name"), template_version, work_version))
        if saver_names:
            QtGui.QMessageBox.information(self, "Shotgun Saver Updater",
                "%s Saver Nodes: <br><br>%s <br><br>"
                "Have been updated!" % (len(saver_names), "".join(saver_names))
                )
        else:
            QtGui.QMessageBox.information(self, "Shotgun Saver Updater",
                "No one node have been updated!")

app = QtGui.QApplication.instance()

wid = Window()
wid.run()

engine._qt_app.exec_()