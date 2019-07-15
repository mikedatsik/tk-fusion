# ------------------------------------------------------------------------------
# Copyright (C) 2018 Diego Garcia Huerta - All Rights Reserved
#
# CONFIDENTIAL AND PROPRIETARY
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Diego Garcia Huerta <diegogh2000@gmail.com>. October 2018
# ------------------------------------------------------------------------------
import os
import sgtk
from sgtk.platform.qt import QtGui

import BlackmagicFusion as bmd
fusion = bmd.scriptapp("Fusion")


__author__ = "Diego Garcia Huerta"
__email__ = "diegogh2000@gmail.com"


HookClass = sgtk.get_hook_baseclass()


class SceneOperation(HookClass):
    """
    Hook called to perform an operation with the
    current scene
    """

    def execute(self, operation, file_path, context, parent_action,
                file_version, read_only, **kwargs):
        """
        Main hook entry point

        :param operation:       String
                                Scene operation to perform

        :param file_path:       String
                                File path to use if the operation
                                requires it (e.g. open)

        :param context:         Context
                                The context the file operation is being
                                performed in.

        :param parent_action:   This is the action that this scene operation is
                                being executed for.  This can be one of:
                                - open_file
                                - new_file
                                - save_file_as
                                - version_up

        :param file_version:    The version/revision of the file to be opened.  If this is 'None'
                                then the latest version should be opened.

        :param read_only:       Specifies if the file should be opened read-only or not

        :returns:               Depends on operation:
                                'current_path' - Return the current scene
                                                 file path as a String
                                'reset'        - True if scene was reset to an empty
                                                 state, otherwise False
                                all others     - None
        """
        app = self.parent

        app.log_debug("-"*50)
        app.log_debug('operation: %s' % operation)
        app.log_debug('file_path: %s' % file_path)
        app.log_debug('context: %s' % context)
        app.log_debug('parent_action: %s' % parent_action)
        app.log_debug('file_version: %s' % file_version)
        app.log_debug('read_only: %s' % read_only)

        comp = fusion.GetCurrentComp()

        if operation == "current_path":
            return comp.GetAttrs()['COMPS_FileName']

        elif operation == "open":
            fusion.LoadComp(file_path)

        elif operation == "save":
            comp.Save(file_path)
        elif operation == "save_as":
            comp.Save(file_path)
        elif operation == "reset":
            comp.Save(file_path)
            return True
