import logging
import os
import subprocess
import tempfile

from Qt import QtCore

logger = logging.getLogger(__name__)

class Playblast_Job(QtCore.QObject):

    data_changed=QtCore.Signal()

    def __init__(self, file_path=None,start_frame=None,end_frame=None,width=None,height=None,frame_path=None, movie_path=None,camera=None,dof=None,motion_blur=None,quality=None, context=None, avaible_cameras=[]):
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
        self.context=context
        self.avaible_cameras=avaible_cameras

    def ___str__(self):
        string=""
        string+="{0}={1}\n".format('file_path', self.file_path)
        string+="{0}={1}\n".format('start_frame', self.start_frame)
        string+="{0}={1}\n".format('end_frame', self.end_frame)
        string+="{0}={1}\n".format('width', self.width)
        string+="{0}={1}\n".format('height', self.height)
        string+="{0}={1}\n".format('movie_path', self.movie_path)
        string+="{0}={1}\n".format('camera', self.camera.name())
        string+="{0}={1}\n".format('dof', self.dof)
        string+="{0}={1}\n".format('motion_blur', self.motion_blur)
        string+="{0}={1}\n".format('quality', self.quality)
        return string

    def submit_to_deadline(self):
        """
        Submit job to deadline
        :return:
        """
        print "submitting to deadline"
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
        for key, value in self.context.iteritems():
            plugin_info_file.write("ktrack_{0}={1}\n".format(key, value))
        plugin_info_file.close()

        #write job info
        logger.info('writing job info file to %s', JOB_INFO_PATH)

        job_info_file=open(JOB_INFO_PATH, 'w')
        job_info_file.write("{0}={1}\n".format('Name', os.path.basename(self.file_path)))
        job_info_file.write("{0}={1}\n".format('Plugin', 'RedshiftPlayblast'))
        job_info_file.write("{0}={1}\n".format('Frames', self.start_frame))
        job_info_file.write("{0}={1}\n".format('OutputDirectory0', os.path.dirname(self.frame_path)))
        job_info_file.write("{0}={1}\n".format('OutputFilename0', os.path.basename(self.frame_path)))
        job_info_file.write("PostJobScript=M:/Projekte/z_pipeline/Deadline10/custom/scripts/Jobs/create_upload_playblast.py")

        job_info_file.close()

        cmd='"C:/Program Files/Thinkbox/Deadline10/bin/deadlinecommand.exe" {0} {1}'.format(JOB_INFO_PATH, PLUGIN_INFO_PATH)
        logger.info("starting submission...")
        logger.info(cmd)
        subprocess.check_output(cmd)
        logger.info("submission done")