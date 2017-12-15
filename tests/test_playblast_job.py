import unittest

from ktrack_metadata import ktrack_metadata
from mock import Mock, patch

from redshift_playblast import playblast_job

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
                                          quality='med',
                                          context=ktrack_metadata.Ktrack_metadata(  project_name='test_project',
                                                                                    project_id=0,
                                                                                    parent_id=0,
                                                                                    parent_name='parent_name',
                                                                                    parent_type='parent_type',
                                                                                    task_name='task_name',
                                                                                    task_id=0,
                                                                                    version_name='version_name',
                                                                                    version_id=0))
        job.submit_to_deadline()
        self.assertTrue(subprocess_mock.called)

if __name__ == '__main__':
    unittest.main()
