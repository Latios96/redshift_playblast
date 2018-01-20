import unittest

import os

from mock import patch, Mock

from redshift_playblast.logic import maya_manager

def get_resource(name):
    return os.path.join(os.path.dirname(__file__), 'resources', name)

class Redshift_Playblast_Test(unittest.TestCase):

    def test_create(self):
        """
        Tests the creation of a new maya manager
        """

        manager=maya_manager.Maya_Manager()

        self.assertNotEqual(manager, None)

        self.assertNotEqual(manager.job.file_path, None)
        self.assertNotEqual(manager.job.start_frame, None)
        self.assertNotEqual(manager.job.end_frame, None)
        self.assertNotEqual(manager.job.width, None)
        self.assertNotEqual(manager.job.height, None)
        self.assertNotEqual(manager.job.frame_path, None)
        self.assertNotEqual(manager.job.movie_path, None)
        self.assertNotEqual(manager.job.camera, None)
        self.assertNotEqual(manager.job.dof, None)
        self.assertNotEqual(manager.job.motion_blur, None)
        self.assertNotEqual(manager.job.quality, None)

    def test_frame_end_minimal_frame_start(self):
        """
        End frame can not be less that start frame.
        """
        manager = maya_manager.Maya_Manager()

        manager.set_job_value('start_frame', 10)
        manager.set_job_value('end_frame', 20)

        old_end_frame = manager.job.end_frame

        manager.set_job_value('start_frame', 100)

        self.assertNotEqual(old_end_frame, manager.job.end_frame)
        self.assertEqual(manager.job.end_frame, 100)

    def test_set_job_value(self):
        """
        Tests if the values are correctly set to the job
        :return:
        """

        manager = maya_manager.Maya_Manager()

        #start frame
        manager.set_job_value('start_frame', 111)
        self.assertEqual(manager.job.start_frame, 111)

        #end frame
        manager.set_job_value('end_frame', 112)
        self.assertEqual(manager.job.end_frame, 112)

        #width
        manager.set_job_value('width', 2560)
        self.assertEqual(manager.job.width, 2560)

        #height
        manager.set_job_value('height', 1440)
        self.assertEqual(manager.job.height, 1440)

        #camera
        manager.set_job_value('camera', 'persp')
        self.assertEqual(manager.job.camera, 'persp')

        #dof
        manager.set_job_value('dof', True)
        self.assertEqual(manager.job.dof, True)
        manager.set_job_value('dof', False)
        self.assertEqual(manager.job.dof, False)

        #motion blur
        manager.set_job_value('motion_blur', True)
        self.assertEqual(manager.job.motion_blur, True)
        manager.set_job_value('motion_blur', False)
        self.assertEqual(manager.job.motion_blur, False)

        #quality
        manager.set_job_value('quality', 'low')
        self.assertEqual(manager.job.quality, 'low')

        #shader_override_type
        manager.set_job_value('shader_override_type', 4)
        self.assertEqual(manager.job.shader_override_type, 4)

        #unsupported parameter
        with self.assertRaises(Exception):
            manager.set_job_value('asdfas', 1440)

    def test_get_scene_name(self):
        """Check that a untitled file is also named untitled"""
        import pymel.core as pm
        pm.newFile(force=True)

        manager = maya_manager.Maya_Manager()
        self.assertTrue('untitled' in manager.get_scene_name())




