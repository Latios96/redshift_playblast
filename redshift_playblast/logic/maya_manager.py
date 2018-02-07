import logging
import os

from redshift_playblast.logic.redshift_worker import Redshift_Worker

logger = logging.getLogger(__name__)

import pymel.core as pm
import maya.cmds as cmds
from Qt import QtCore, QtWidgets

from redshift_playblast.model import playblast_job
from redshift_playblast.view import popups_questions
from redshift_playblast.hooks import hooks

class Maya_Manager(object):
    """
    Class responsable for doing all the Maya Logic
    """

    def __init__(self):
        self.job= playblast_job.Playblast_Job(file_path=pm.sceneName(),
                                              start_frame=int(pm.playbackOptions(minTime=True, query=True)),
                                              end_frame=int(pm.playbackOptions(maxTime=True, query=True)),
                                              width=1920,
                                              height=1080,
                                              frame_path=self.get_frame_path(),
                                              movie_path=self.get_movie_path(),
                                              camera=self.get_camera_information()[0],
                                              dof=self.get_camera_information()[1],
                                              motion_blur=True,
                                              quality='med',
                                              avaible_cameras=self.get_avaible_cameras())

    def get_frame_path(self):
        return hooks.frame_path(self.get_scene_name())

    def get_movie_path(self):
        return hooks.movie_path(self.get_scene_name())

    def get_scene_name(self):
        scene_name=os.path.splitext(os.path.basename(pm.sceneName()))[0]
        if len(scene_name)==0:
            return "untitled"
        else:
            return scene_name

    def get_camera_information(self):
        """
        Returns information about current camera
        :return: tupel of current camera (pymel node) and depthOfField enabled (bool)
        """

        if len(pm.ls('render_cam'))>0:
            camera=pm.ls('render_cam')[0]
        else:
            camera=pm.ls('persp')[0]

        return camera, camera.depthOfField.get()

    def get_avaible_cameras(self):
        return [x.parent(0) for x in pm.ls(type='camera')]

    def create_playblast(self):
        if os.path.exists(self.job.movie_path):
            result=popups_questions.movie_exists()
            if not result:
                return
        if self.job.local_mode:
            worker=Redshift_Worker(self.job)
            worker.create_playblast()
        else:
            #check for unsaved changes
            if cmds.file(q=True, modified=True):
                result = popups_questions.unsaved_changes()
                if result:
                    pm.saveFile()
            self.job.submit_to_deadline()

    def apply_scene_range(self):
        self.set_job_value('start_frame', int(pm.playbackOptions(minTime=True, query=True)))
        self.set_job_value('end_frame', int(pm.playbackOptions(maxTime=True, query=True)))

    def apply_render_settings_resolution(self):
        default_resolution = pm.ls('defaultResolution')[0]
        self.set_job_value('width', default_resolution.width.get())
        self.set_job_value('height', default_resolution.height.get())

    def set_job_value(self, value_name, value):
        """
        Gets the raw UI value and sets it to the job
        :param value_name:
        :param value:
        :return:
        """
        if value_name=='start_frame':
            if value=="":
                self.job.start_frame=0
            else:
                self.job.start_frame=int(value)

                #make sure that start frame cant be bigger than end frame
                if self.job.start_frame>self.job.end_frame:
                    self.job.end_frame=self.job.start_frame

                self.job.data_changed.emit()

        elif value_name=='end_frame':
            if value == "":
                self.job.end_frame =0
            else:
                self.job.end_frame=int(value)
                self.job.data_changed.emit()

        elif value_name=='width':
            if value == "":
                self.job.width=0
            else:
                self.job.width=int(value)
                self.job.data_changed.emit()

        elif value_name=='height':
            if value == "":
                self.job.height =0
            else:
                self.job.height=int(value)
                self.job.data_changed.emit()

        elif value_name=='camera':
            if len(pm.ls(value))>0:
                self.job.camera=pm.ls(value)[0]
            #self.job.data_changed.emit()

        elif value_name=='dof':
            self.job.dof=value
            self.job.data_changed.emit()

        elif value_name=='motion_blur':
            self.job.motion_blur=value
            self.job.data_changed.emit()

        elif value_name=='quality':
            self.job.quality=value
            #self.job.data_changed.emit()

        elif value_name=='shader_override_type':
            self.job.shader_override_type=value
            #self.job.data_changed.emit()
        elif value_name=='local_mode':
            self.job.local_mode=value
            self.job.data_changed.emit()
        else:
            error="Unsupported Parameter: "+value_name
            raise Exception(error)
        logger.debug(self.job.___str__())









