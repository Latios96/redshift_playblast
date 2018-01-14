import unittest
import pymel.core as pm

import os

from redshift_playblast.logic.edit_context import get_edit_context


def get_resource(name):
    return os.path.join(os.path.dirname(__file__), 'resources', name)

class MyTestCase(unittest.TestCase):

    def test_edit_context(self):
        """
        Tests edit context
        :return:
        """

        pm.openFile(get_resource('test_edit_context.ma'), force=True)

        old_translate=pm.ls('pCube1')[0].translateX.get()

        old_initial_shading_group=pm.ls('initialShadingGroup')[0]
        old_initial_shading_group_inputs=old_initial_shading_group.surfaceShader.inputs()
        with get_edit_context() as context:
            self.assertNotEqual(context, None)

            #test create node
            surface_shader=context.createNode('surfaceShader')

            self.assertEqual(len(pm.ls(type='surfaceShader')), 2)
            self.assertNotEqual(surface_shader, None)
            self.assertEqual(surface_shader.type(), u'surfaceShader')

            #test set attribute
            cube=pm.ls('pCube1')[0]
            context.setAttr(cube.translateX, 10.0)
            self.assertEqual(cube.translateX.get(),10.0)

            #test disconnect attribute
            context.disconnectAttr(old_initial_shading_group.surfaceShader)
            self.assertEqual(len(old_initial_shading_group.surfaceShader.inputs()),0)

            #test connect attribute
            cube2=pm.ls('pCube2')[0]
            print cube2.translate.inputs(p=True)
            context.connectAttr(cube.translate, cube2.translate)
            self.assertEqual(len(cube2.translate.inputs()), 1)

        #verify created surface shader was deleted
        self.assertEqual(len(pm.ls(type='surfaceShader')), 1)

        #verify attribute was set to old value
        self.assertEqual(cube.translateX.get(), old_translate)

        #verify disconnected attrs are connected back
        self.assertEqual(old_initial_shading_group.surfaceShader.inputs(), old_initial_shading_group_inputs)

        #verify attributes connected in context are restores
        cube2 = pm.ls('pCube2')[0]
        self.assertEqual(len(cube2.translate.inputs()), 0)

if __name__ == '__main__':
    unittest.main()
