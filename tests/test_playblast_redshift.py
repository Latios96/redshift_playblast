import os
import unittest
import uuid

from mock import patch, Mock

from redshift_playblast import playblast
from redshift_playblast.logic import redshift_worker


def get_resource(name):
    return os.path.join(os.path.dirname(__file__), 'resources', name)

def construct_args_mock_cli(**kwargs):
    args_mock=Mock()
    args_mock.start_frame = 1
    args_mock.end_frame = 2
    args_mock.width=1920
    args_mock.height = 1080
    args_mock.frame_path=get_resource('playblast_test.####.png')
    args_mock.file_path=get_resource('test_scene_cube.ma')
    args_mock.camera='camera1'
    args_mock.dof = 'True'
    args_mock.motion_blur='True'
    args_mock.quality='low'
    args_mock.shader_override_type = 0

    for key, value in kwargs.iteritems():
        setattr(args_mock, key, value)

    return args_mock

def construct_job_mock(**kwargs):
    args_mock=Mock()
    args_mock.start_frame = 1
    args_mock.end_frame = 2
    args_mock.width=1920
    args_mock.height = 1080
    args_mock.frame_path=get_resource('playblast_test.####.png')
    args_mock.file_path=get_resource('test_scene_cube.ma')
    args_mock.camera='camera1'
    args_mock.dof = True
    args_mock.motion_blur=True
    args_mock.quality='low'
    args_mock.shader_override_type=0

    for key, value in kwargs.iteritems():
        setattr(args_mock, key, value)

    return args_mock


class Redshift_Playblast_Test(unittest.TestCase):

    @patch('argparse.ArgumentParser.parse_args')
    def test_wrong_quality(self, argparse_mock):
        """
        Tests when the playblast script is called with a wrong quality
        :param argparse_mock:
        :return:
        """
        #constructing result fakce
        my_mock=construct_args_mock_cli(quality='ert')
        argparse_mock.return_value=my_mock

        #now parse the args
        with self.assertRaises(playblast.PlayblastQualityError):
            playblast.main()

    @patch('redshift_playblast.logic.redshift_worker.Redshift_Worker')
    @patch('argparse.ArgumentParser.parse_args')
    def test_spelling_robustness(self, argparse_mock,redshift_mock):
        """
        Tests when the playblast script is called with a correct quality in non-upper-case, like low, lOw, or loW
        :param argparse_mock:
        :return:
        """
        for spelling in ['low', 'loW', 'Low','high', 'HigH','med']:
            # constructing result fakce
            my_mock=construct_args_mock_cli(quality=spelling)
            argparse_mock.return_value = my_mock

            # now parse the args
            playblast.main()

    def test_get_object_by_name(self):
        """
        Tests getting a pymel object by name
        :return:
        """

        argparse_mock = Mock()
        my_mock = construct_job_mock()

        redshift = redshift_worker.Redshift_Worker(my_mock)

        # test existing obj
        self.assertFalse(redshift._get_object_by_name('persp')==None)

        # test non existing obj
        with self.assertRaises(redshift_worker.ObjectNotExistsError):
            redshift._get_object_by_name('persptrgft')

    def test_redshift_setter_correctness(self):
        """
        Tests if the redshift setters work correctly
        :return:
        """
        argparse_mock=Mock()
        my_mock = construct_job_mock()
        redshift = redshift_worker.Redshift_Worker(my_mock)

        #now check correctness of values

    def test_render_frames_no_redshift_config(self):
        """
        Tests rendering a file which didnt hat redshift loaded before
        :return:
        """
        argparse_mock = Mock()
        frames=get_resource('test_render_{0}.####.png'.format(str(uuid.uuid4()).split('-')[0]))
        my_mock = construct_job_mock(file_path=get_resource('test_scene_cube_no_redshift.ma'),
                                      start_frame=1,
                                      end_frame=3,
                                      frame_path=frames,
                                      camera='render_cam',
                                      )

        redshift = redshift_worker.Redshift_Worker(my_mock)
        quicktime_path=redshift.create_playblast()

        self.assertTrue(os.path.exists(quicktime_path))

        os.remove(quicktime_path)







if __name__ == '__main__':
    unittest.main()
