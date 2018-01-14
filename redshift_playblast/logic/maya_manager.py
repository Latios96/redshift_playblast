import logging
import os
logger = logging.getLogger(__name__)

import pymel.core as pm
from Qt import QtCore

from redshift_playblast.model import playblast_job


class Maya_Manager(object):

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
        return "{project_location}/movies/{scene_name}.####.png".format(project_location=pm.workspace.path, scene_name=os.path.splitext(os.path.basename(pm.sceneName()))[0])

    def get_movie_path(self):
        return "{project_location}/movies/{scene_name}.mov".format(project_location=pm.workspace.path, scene_name=os.path.splitext(os.path.basename(pm.sceneName()))[0])

    def get_camera_information(self):

        if len(pm.ls('render_cam'))>0:
            camera=pm.ls('render_cam')[0]
        else:
            camera=pm.ls('persp')[0]

        return camera, camera.depthOfField.get()

    def get_avaible_cameras(self):
        return [x.parent(0) for x in pm.ls(type='camera')]

    def submit(self):
        self.job.submit_to_deadline()

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
            print value
            self.job.camera=pm.ls(value)[0]
            #self.job.data_changed.emit()

        elif value_name=='dof':
            self.job.dof=value
            self.job.data_changed.emit()

        elif value_name=='motion_blur':
            self.job.motion_blur=value
            self.job.data_changed.emit()

        elif value_name=='quality':
            print value
            self.job.quality=value
            #self.job.data_changed.emit()

        elif value_name=='shader_override_type':
            self.job.shader_override_type=value
            #self.job.data_changed.emit()

        else:
            error="Unsupported Parameter: "+value_name
            raise Exception(error)
        logger.debug(self.job.___str__())









