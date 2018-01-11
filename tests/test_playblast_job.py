import unittest
import os

from mock import Mock, patch

from redshift_playblast.model import playblast_job
from redshift_playblast.logic import maya_manager

def get_resource(name):
    return os.path.join(os.path.dirname(__file__), 'resources', name)

class MyTestCase(unittest.TestCase):
    @patch('subprocess.check_output')
    def test_submit(self, subprocess_mock):
        job = playblast_job.Playblast_Job(file_path='test_file_path',
                                          start_frame=1000,
                                          end_frame=1100,
                                          width=1920,
                                          height=1080,
                                          frame_path='test_frame_path',
                                          movie_path='test_movie_path',
                                          camera=Mock(),
                                          dof=True,
                                          motion_blur=True,
                                          quality='med')
        job.submit_to_deadline()
        self.assertTrue(subprocess_mock.called)

    @patch('subprocess.check_output')
    def test_submit(self, check_output_mock):
        # Tests submission of simple file to deadline

        import pymel.core as pm

        pm.openFile(get_resource('test_scene_cube_no_redshift.ma'), force=True)
        # pm.openFile(r'M:\Projekte\2017\The_Cement_Mixer\Shots\shot010\shot010_Maya\shot010_Anim_v001.mb', force=True)
        manager = maya_manager.Maya_Manager()
        manager.job.submit_to_deadline()
        self.assertTrue(check_output_mock.assert_called)

if __name__ == '__main__':
    unittest.main()
