# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.
import sgtk
from sgtk import TankError
import BlackmagicFusion as bmd


__author__ = "Diego Garcia Huerta"
__email__ = "diegogh2000@gmail.com"


HookBaseClass = sgtk.get_hook_baseclass()


class FrameOperation(HookBaseClass):
    """
    Hook called to perform a frame operation with the 
    current scene
    """

    def execute(self, operation, head_in_frame=None, in_frame=None, out_frame=None, tail_out_frame=None, **kwargs):
        """
        Main hook entry point

        :operation: String
                    Frame operation to perform

        :in_frame: int
                    in_frame for the current context (e.g. the current shot, 
                                                      current asset etc)

        :out_frame: int
                    out_frame for the current context (e.g. the current shot, 
                                                      current asset etc)

        :returns:   Depends on operation:
                    'set_frame_range' - Returns if the operation was succesfull
                    'get_frame_range' - Returns the frame range in the form
                                        (in_frame, out_frame)
        """
        fusion = bmd.scriptapp("Fusion")
        comp = fusion.GetCurrentComp()

        if operation == "get_frame_range":
            current_in = int(comp.GetAttrs()["COMPN_GlobalStart"])
            current_out = int(comp.GetAttrs()["COMPN_GlobalEnd"])
            return (current_in, current_out)
 
        elif operation == "set_frame_range":
            # set frame ranges for plackback
            comp.SetAttrs({'COMPN_GlobalEnd' : out_frame})
            comp.SetAttrs({'COMPN_RenderEnd': tail_out_frame})
            comp.SetAttrs({'COMPN_GlobalStart' : in_frame})
            comp.SetAttrs({'COMPN_RenderStart': head_in_frame})
            return True
