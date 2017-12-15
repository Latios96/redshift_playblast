import os
import subprocess

class Playblast_Job(object):

    def __init__(self, file_path=None,start_frame=None,end_frame=None,width=None,height=None,frame_path=None, movie_path=None,camera=None,dof=None,motion_blur=None,quality=None, context=None):
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

    def submit_to_deadline(self):
        """
        Submit job to deadline
        :return:
        """
        print "submitting to deadline"
        PLUGIN_INFO_PATH="M:/redshift_playblast_pluginInfo.job"
        JOB_INFO_PATH = "M:/redshift_playblast_jobInfo.job"
        #job info: OutputDirectory0

        #alles andere: plugin
        plugin_info_file = open(PLUGIN_INFO_PATH, 'w')

        plugin_info_file.write("{0}={1}\n".format('file_path', self.file_path))
        plugin_info_file.write("{0}={1}\n".format('start_frame', self.end_frame))
        plugin_info_file.write("{0}={1}\n".format('width', self.width))
        plugin_info_file.write("{0}={1}\n".format('height', self.height))
        plugin_info_file.write("{0}={1}\n".format('frame_path', self.frame_path))
        plugin_info_file.write("{0}={1}\n".format('movie_path', self.movie_path))
        plugin_info_file.write("{0}={1}\n".format('camera', self.camera.name()))
        plugin_info_file.write("{0}={1}\n".format('dof', self.dof))
        plugin_info_file.write("{0}={1}\n".format('motion_blur', self.motion_blur))
        plugin_info_file.write("{0}={1}\n".format('quality', self.quality))
        for key, value in self.context.iteritems():
            plugin_info_file.write("ktrack_{0}={1}\n".format(key, value))
        plugin_info_file.close()

        job_info_file=open(JOB_INFO_PATH, 'w')
        job_info_file.write("{0}={1}\n".format('Name', os.path.basename(self.file_path)))
        job_info_file.write("{0}={1}\n".format('Plugin', 'RedshiftPlayblast'))

        job_info_file.close()

        cmd='"C:/Program Files/Thinkbox/Deadline10/bin/deadlinecommand.exe" {0} {1}'.format(JOB_INFO_PATH, PLUGIN_INFO_PATH)
        print cmd
        subprocess.check_output(cmd)