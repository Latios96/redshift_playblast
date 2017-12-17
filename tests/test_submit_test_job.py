import unittest

import os

from ktrack_metadata import ktrack_metadata
from mock import patch

from redshift_playblast.logic import maya_manager

def get_resource(name):
    return os.path.join(os.path.dirname(__file__), 'resources', name)

class MyTestCase(unittest.TestCase):
    @patch('ktrack_metadata.from_scene')
    def test_submit(self,from_scene_mock):
        #Tests submission of simple file to deadline

        import pymel.core as pm

        from_scene_mock.return_value=ktrack_metadata.Ktrack_metadata(project_name='test_project',
                                        project_id=0,
                                        parent_id=0,
                                        parent_name='parent_name',
                                        parent_type='parent_type',
                                        task_name='task_name',
                                        task_id=0,
                                        version_name='version_name',
                                        version_id=0)


        #pm.openFile(get_resource('test_scene_cube_no_redshift.ma'), force=True)
        pm.openFile('M:/Projekte/2017/The_Cement_Mixer/Shots/shot050/shot050_Maya/shot050_Anim_v003_playblast_playground.mb', force=True)
        manager = maya_manager.Maya_Manager()
        manager.job.submit_to_deadline()


if __name__ == '__main__':
    unittest.main()
