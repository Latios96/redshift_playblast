import unittest

import sys
from PySide2 import QtTest
from Qt import QtWidgets

import os

from mock import patch, Mock

from redshift_playblast.view import redshift_playblast_view

def get_resource(name):
    return os.path.join(os.path.dirname(__file__), 'resources', name)

class Redshift_Playblast_View_Test(unittest.TestCase):

    def test_creation(self):
        import pymel.core as pm

        pm.openFile(get_resource('test_scene_cube_no_redshift.ma'), force=True)
        view=redshift_playblast_view.Redshift_Playblast_View()
        #todo implement UI tests

def main():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(Redshift_Playblast_View_Test)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main()
