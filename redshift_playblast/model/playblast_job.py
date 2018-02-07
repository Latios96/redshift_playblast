import logging
import os
import subprocess
import tempfile

from Qt import QtCore

from redshift_playblast.hooks import hooks

logger = logging.getLogger(__name__)

class Playblast_Job(QtCore.QObject):
    """
    Model class to represent a single playblast job
    """

    data_changed=QtCore.Signal()

    def __init__(self, file_path=None,start_frame=None,end_frame=None,width=None,height=None,frame_path=None, movie_path=None,camera=None,dof=None,motion_blur=None,quality=None, avaible_cameras=[], shader_override_type=0, local_mode=True):
        """
        :param file_path: path to the Maya file to open
        :type file_path: str
        :param start_frame: first frame of frame range
        :type start_frame: float
        :param end_frame: last frame of frame range
        :type end_frame: float
        :param width: width of resulting playblast
        :type width: int
        :param height: height of resulting playblast
        :type height: int
        :param frame_path: path where to put the temp frames
        :type frame_path: str
        :param movie_path: path where to put the final movie file
        :type movie_path: str
        :param camera: camera to playblast, expected to be a pymel transform
        :type camera: pymel.core.nodetypes.Transform
        :param dof: If True, playblast will contain dof
        :type dof: bool
        :param motion_blur: If True, playblast will contain motion_blur
        :type motion_blur: bool
        :param quality: quality of the playblast, valid values are low, med, high
        :type quality: str
        :param avaible_cameras: list of all avaible cameras in current scene
        :type avaible_cameras: list
        :param shader_override_type: type of Shader override applied when creating the playblast, see Shader_Override_Type
        :type shader_override_type: Shader_Override_Type
        :param local_mode: If True, playblast will be done in current maya session
        :type local_mode: bool
        """
        super(Playblast_Job, self).__init__()
        self.file_path=file_path
        self.start_frame=start_frame
        self.end_frame=end_frame
        self.width=width
        self.height=height
        self.frame_path=frame_path
        self.movie_path=movie_path
        self.camera=camera
        self.dof=dof
        self.motion_blur=motion_blur
        self.quality=quality
        self.shader_override_type = shader_override_type
        self.avaible_cameras=avaible_cameras
        self.local_mode=local_mode


    def ___str__(self):
        string=""
        string+="{0}={1}\n".format('file_path', self.file_path)
        string+="{0}={1}\n".format('start_frame', self.start_frame)
        string+="{0}={1}\n".format('end_frame', self.end_frame)
        string+="{0}={1}\n".format('width', self.width)
        string+="{0}={1}\n".format('height', self.height)
        string += "{0}={1}\n".format('frame_path', self.frame_path)
        string+="{0}={1}\n".format('movie_path', self.movie_path)
        string+="{0}={1}\n".format('camera', self.camera.name())
        string+="{0}={1}\n".format('dof', self.dof)
        string+="{0}={1}\n".format('motion_blur', self.motion_blur)
        string+="{0}={1}\n".format('quality', self.quality)
        string += "{0}={1}\n".format('shader_override_type', self.shader_override_type)
        string += "{0}={1}\n".format('local_mode', self.local_mode)
        return string

    def submit_to_deadline(self):
        """
        Submit job to deadline
        :return:
        """
        logger.info("submitting to deadline")
        PLUGIN_INFO_PATH=os.path.join(tempfile.gettempdir(), "redshift_playblast_pluginInfo.job")
        JOB_INFO_PATH = os.path.join(tempfile.gettempdir(), "redshift_playblast_jobInfo.job")

        #write plugin info
        logger.info('writing plugin info file to %s', PLUGIN_INFO_PATH)

        plugin_info_file = open(PLUGIN_INFO_PATH, 'w')

        plugin_info_file.write("{0}={1}\n".format('file_path', self.file_path))
        plugin_info_file.write("{0}={1}\n".format('start_frame', self.start_frame))
        plugin_info_file.write("{0}={1}\n".format('end_frame', self.end_frame))
        plugin_info_file.write("{0}={1}\n".format('width', self.width))
        plugin_info_file.write("{0}={1}\n".format('height', self.height))
        plugin_info_file.write("{0}={1}\n".format('movie_path', self.movie_path))
        plugin_info_file.write("{0}={1}\n".format('camera', self.camera.name()))
        plugin_info_file.write("{0}={1}\n".format('dof', self.dof))
        plugin_info_file.write("{0}={1}\n".format('motion_blur', self.motion_blur))
        plugin_info_file.write("{0}={1}\n".format('quality', self.quality))
        plugin_info_file.write("{0}={1}\n".format('shader_override_type', self.shader_override_type))

        logger.info("Executing hook deadline_plugin_info_file..")
        hooks.deadline_plugin_info_file(plugin_info_file)

        plugin_info_file.close()

        #write job info
        logger.info('writing job info file to %s', JOB_INFO_PATH)

        job_info_file=open(JOB_INFO_PATH, 'w')
        job_info_file.write("{0}={1}\n".format('Name', os.path.basename(self.file_path)))
        job_info_file.write("{0}={1}\n".format('Plugin', 'RedshiftPlayblast'))
        job_info_file.write("{0}={1}\n".format('Frames', self.start_frame))
        job_info_file.write("{0}={1}\n".format('OutputDirectory0', os.path.dirname(self.frame_path)))
        job_info_file.write("{0}={1}\n".format('OutputFilename0', os.path.basename(self.frame_path)))

        logger.info("Executing hook job_info_file..")
        hooks.deadline_job_info_file(job_info_file)

        job_info_file.close()

        cmd='"C:/Program Files/Thinkbox/Deadline10/bin/deadlinecommand.exe" {0} {1}'.format(JOB_INFO_PATH, PLUGIN_INFO_PATH)
        logger.info("starting submission...")
        logger.info(cmd)
        subprocess.check_output(cmd)
        logger.info("submission done")