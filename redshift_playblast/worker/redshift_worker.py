import logging

import pymel.core as pm
import maya.mel as mel

logger = logging.getLogger(__name__)


QUALITY_PRESETS={
    'low': {
            'min_samples': 2,
            'max_samples': 16,
            'threshold': 0.25,
            },
    'med': {
            'min_samples': 2,
            'max_samples': 32,
            'threshold': 0.05,
            },
    'medium': {
            'min_samples': 2,
            'max_samples': 32,
            'threshold': 0.05,
            },
    'high': {
            'min_samples': 2,
            'max_samples': 64,
            'threshold': 0.01
            },
}

class Redshift_Worker(object):

    def __init__(self, args):
        #TODO validate args
        #TODO restore original values before job, needed to run job inside maya
        self.args=args

        #load file
        if pm.sceneName is not self.args.file_path:
            pm.openFile(self.args.file_path, force=True)

        # load redshift plugin
        pm.loadPlugin('redshift4maya')
        if len(pm.ls('redshiftOptions'))==0:
            pm.createNode('RedshiftOptions')

        #change renderer
        self._get_object_by_name("defaultRenderGlobals").currentRenderer.set('redshift')
        #set file format and other render setting stuff
        self._get_object_by_name("redshiftOptions").imageFormat.set(2)

        self._get_object_by_name("defaultRenderGlobals").animation.set(1)
        self._get_object_by_name("defaultRenderGlobals").extensionPadding.set(4)

        self.set_start_end_frame(self.args.start_frame, self.args.end_frame)

        self.set_resolution(self.args.width, self.args.height)

        self.set_frame_path(self.args.frame_path)

        self.set_camera(self.args.camera)

        self.set_dof(self.args.dof)

        self.set_motion_blur(self.args.motion_blur)

        self.set_quality(self.args.quality)

    def _get_object_by_name(self, name):
        """
        Returns a PyMel object by its name
        :param name:
        :return:
        """
        candidates=pm.ls(name)
        if len(candidates)==1:
            return candidates[0]
        else:
            error="Object with name {0} does not exists".format(name)
            logger.error(error)
            raise ObjectNotExistsError(error)

    def set_start_end_frame(self, start_frame, end_frame):
        logger.info("settings start and end frame to %s, %s", start_frame, end_frame)
        self._get_object_by_name("defaultRenderGlobals").startFrame.set(start_frame)
        self._get_object_by_name("defaultRenderGlobals").endFrame.set(end_frame)

    def set_resolution(self, width, height):
        logger.info("set resolution to %s x %s", width, height)
        default_resolution=self._get_object_by_name('defaultResolution')
        default_resolution.width.set(width)
        default_resolution.height.set(height)

    def set_frame_path(self, frame_path):
        logger.info("set frame path to %s", frame_path)
        logger.info("replaced path to %s", frame_path.replace("_####.png", ""))
        self._get_object_by_name('defaultRenderGlobals').imageFilePrefix.set(frame_path.replace(".####.png", ""))

    def set_camera(self, camera):
        logger.info("set camera to %s", camera)
        self.camera=self._get_object_by_name(camera)
        mel.eval('makeCameraRenderable("{0}")'.format(camera))

    def set_dof(self, dof_enabled):
        logger.info("set dof enabled: %s", dof_enabled)
        self.camera.depthOfField.set(1 if dof_enabled else 0)

    def set_motion_blur(self, motion_blur):
        logger.info("set motion_blur enabled: %s", motion_blur)
        self._get_object_by_name("redshiftOptions").motionBlurEnable.set(motion_blur)
        self._get_object_by_name("redshiftOptions").motionBlurDeformationEnable.set(motion_blur)

    def set_quality(self, quality):
        logger.info("set quality to: %s", quality)
        self._get_object_by_name("redshiftOptions").unifiedMinSamples.set(QUALITY_PRESETS[quality.lower()]['min_samples'])
        self._get_object_by_name("redshiftOptions").unifiedMaxSamples.set(QUALITY_PRESETS[quality.lower()]['max_samples'])
        self._get_object_by_name("redshiftOptions").unifiedAdaptiveErrorThreshold.set(QUALITY_PRESETS[quality.lower()]['threshold'])

    def render_frame(self, frame_number):
        """
        renders frame with given number
        :return:
        """
        old_start=self._get_object_by_name("defaultRenderGlobals").startFrame.get()
        old_end = self._get_object_by_name("defaultRenderGlobals").endFrame.get()
        self._get_object_by_name("defaultRenderGlobals").startFrame.set(frame_number)
        self._get_object_by_name("defaultRenderGlobals").endFrame.set(frame_number)
        mel.eval('mayaBatchRenderProcedure(0, "", "' + str('') + '", "' + 'redshift' + '", "")')
        self._get_object_by_name("defaultRenderGlobals").startFrame.set(old_start)
        self._get_object_by_name("defaultRenderGlobals").endFrame.set(old_end)

    def render_frames(self):
        """
        renders frame with given number
        :return:
        """
        mel.eval('mayaBatchRenderProcedure(0, "", "' + str('') + '", "' + 'redshift' + '", "")')


class ObjectNotExistsError(Exception):
    """
    Exception thrown when there is no object with the given name, for example persp_ysdf
    """
    pass