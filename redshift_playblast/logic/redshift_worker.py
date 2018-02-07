import glob
import logging
import subprocess

import os
import webbrowser

import pymel.core as pm
import maya.mel as mel

from redshift_playblast.hooks import hooks
from redshift_playblast.logic.edit_context import get_edit_context
from redshift_playblast.model.shader_override_types import Shader_Override_Type

FFMEG_EXE = 'ffmpeg.exe'

MOVIE_EXTENSION = ".mov"

FRAME_EXTENSION = ".png"

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
            'max_samples': 128,
            'threshold': 0.005
            },
}

class Redshift_Worker(object):
    """
    Class responable for executing a Playblast_Job
    """

    def __init__(self, job):
        self.job=job

        #load alembic plugin, can lead to problems with referenced alembics
        pm.loadPlugin('AbcImport')

        #load file
        if not job.local_mode:
            pm.openFile(self.job.file_path, force=True)

        # load redshift plugin
        pm.loadPlugin('redshift4maya')
        if len(pm.ls('redshiftOptions'))==0:
            pm.createNode('RedshiftOptions')


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

    def set_start_end_frame(self, context, start_frame, end_frame):
        self.start_frame=start_frame
        self.end_frame = end_frame

        logger.info("settings start and end frame to %s, %s", start_frame, end_frame)

    def set_resolution(self, context, width, height):
        logger.info("set resolution to %s x %s", width, height)

        default_resolution=self._get_object_by_name('defaultResolution')
        context.setAttr(default_resolution.width, width)
        context.setAttr(default_resolution.height, height)

    def set_frame_path(self, context, frame_path):
        self.frame_path=frame_path
        logger.info("set frame path to %s", frame_path)
        logger.info("replaced path to %s", frame_path.replace("_####.png", ""))
        #context.setAttr(self._get_object_by_name('defaultRenderGlobals').imageFilePrefix, frame_path.replace(".####.png", ""))
        context.setAttr(self._get_object_by_name('defaultRenderGlobals').imageFilePrefix, frame_path.replace(".####.png", ""))

    def set_camera(self, context, camera):
        logger.info("set camera to %s", camera)
        self.camera=self._get_object_by_name(camera)
        context.set_render_cam(camera)

    def set_dof(self, context, dof_enabled):
        logger.info("set dof enabled: %s", dof_enabled)
        context.setAttr(self.camera.depthOfField, 1 if dof_enabled else 0)

    def set_motion_blur(self, context, motion_blur):
        logger.info("set motion_blur enabled: %s", motion_blur)
        context.setAttr(self._get_object_by_name("redshiftOptions").motionBlurEnable, motion_blur)
        context.setAttr(self._get_object_by_name("redshiftOptions").motionBlurDeformationEnable, motion_blur)

    def set_quality(self, context, quality):
        logger.info("set quality to: %s", quality)
        context.setAttr(self._get_object_by_name("redshiftOptions").unifiedMinSamples, QUALITY_PRESETS[quality.lower()]['min_samples'])
        context.setAttr(self._get_object_by_name("redshiftOptions").unifiedMaxSamples, QUALITY_PRESETS[quality.lower()]['max_samples'])
        context.setAttr(self._get_object_by_name("redshiftOptions").unifiedAdaptiveErrorThreshold, QUALITY_PRESETS[quality.lower()]['threshold'])


    def create_playblast(self):
        """
        Renders all frames and creates Quicktime after that. Will remove rendered images
        :return: path to created Quicktime
        """
        try:
            with get_edit_context() as context:

                #disable parallel evaluation
                context.disable_parallel_evaluation()

                # change renderer
                context.setAttr(self._get_object_by_name("defaultRenderGlobals").currentRenderer, 'redshift')

                # set file format and other render setting stuff
                context.setAttr(self._get_object_by_name("redshiftOptions").imageFormat,2)

                context.setAttr(self._get_object_by_name("defaultRenderGlobals").animation, 1)
                context.setAttr(self._get_object_by_name("defaultRenderGlobals").extensionPadding,4)

                self.set_start_end_frame(context, self.job.start_frame, self.job.end_frame)

                self.set_resolution(context, self.job.width, self.job.height)

                self.set_frame_path(context, self.job.frame_path)

                self.set_camera(context, self.job.camera)

                self.set_dof(context, self.job.dof)

                self.set_motion_blur(context, self.job.motion_blur)

                self.set_quality(context, self.job.quality)

                #create shader overrides
                self.create_shader_override(context, self.job.shader_override_type)

                logger.info("Rendering range %s-%s", int(self.start_frame), int(self.end_frame))

                context.setAttr(self._get_object_by_name("defaultRenderGlobals").startFrame, self.start_frame)
                context.setAttr(self._get_object_by_name("defaultRenderGlobals").endFrame, self.end_frame)
                mel.eval('mayaBatchRenderProcedure(0, "", "' + str('') + '", "' + 'redshift' + '", "")')

        except Exception as e:
            logger.error(e)


        #path to created quicktime
        quicktime=self._create_quicktime()

        #if local mode, we open the quicktime afterwards
        if self.job.local_mode:
            webbrowser.open(quicktime)

        return quicktime

    def _create_quicktime(self):
        #todo add information about Quicktime to docs
        """
        Uses ffmpeg to create Quicktime from rendered images. Images will be deleted after Quicktime creation.
        :return: path to created Quicktime
        """
        start_frame=str(self.start_frame)
        input_path=self.frame_path.replace('####', '%04d')
        output_file=self.job.movie_path

        if os.path.exists(output_file):
            os.remove(output_file)

        ffmpeg_folder=hooks.get_ffmpeg_folder()

        ffmpeg_path=os.path.join(ffmpeg_folder, FFMEG_EXE)

        if not os.path.exists(ffmpeg_path):
            raise FFmpegNotFound("ffmpeg not found!!1")

        convert_command = '{0} -apply_trc iec61966_2_1 -r 24 -start_number {1} -i "{2}" -vcodec libx264 -pix_fmt yuv420p -profile:v high -level 4.0 -preset medium -bf 0 "{3}"'.format(ffmpeg_path, start_frame, input_path, output_file)

        logger.info("generating quicktime...")
        logger.info(convert_command)

        subprocess.call(convert_command)

        logger.info("Quicktime was created")

        logger.info("deleting pngs...")
        for image_path in glob.glob(input_path.replace('%04d', '*')):
            os.remove(image_path)

        logger.info("pngs deleted")

        return output_file

    def create_shader_override(self, context, shader_type=Shader_Override_Type.AMBIENT_OCCLUSION):
        #AMBIENT_OCCLUSION
        if shader_type==Shader_Override_Type.AMBIENT_OCCLUSION:
            logger.info("creating shader override %s", Shader_Override_Type.AMBIENT_OCCLUSION)

            surfaceShader = context.createNode('surfaceShader')

            ao_shader = context.createNode('RedshiftAmbientOcclusion')

            context.connectAttr(ao_shader.outColor, surfaceShader.outColor)

            for shadingGroup in pm.ls(type='shadingEngine'):
                context.disconnectAttr(shadingGroup.surfaceShader)
                context.connectAttr(surfaceShader.outColor, shadingGroup.surfaceShader)

        #GREYSCALE
        elif shader_type==Shader_Override_Type.GREYSCALE:
            redshift_material = context.createNode('RedshiftMaterial')
            redshift_material.refl_weight.set(0)
            redshift_material.refl_color.set((0, 0, 0))

            for shadingGroup in pm.ls(type='shadingEngine'):
                context.disconnectAttr(shadingGroup.surfaceShader)
                context.connectAttr(redshift_material.outColor,shadingGroup.surfaceShader)

        #PRODUCTION_SHADER
        elif shader_type==Shader_Override_Type.PRODUCTION_SHADER:
            logger.info("creating shader override %s", Shader_Override_Type.PRODUCTION_SHADER)
            hooks.assign_production_shader(context)

        #NO_OVERRIDE
        else:
            logger.info("creating shader override %s", Shader_Override_Type.NO_OVERRIDE)

class ObjectNotExistsError(Exception):
    """
    Exception thrown when there is no object with the given name, for example persp_ysdf
    """
    pass

class FFmpegNotFound(Exception):
    """
    Exception thrown when ffmpeg.exe could not be found
    """

    def __init__(self, ffmpeg_path):
        error="FFmpeg could not be found at location {}. Please install ffmpeg to this location or customize hook get_ffmpeg_folder"
        super(FFmpegNotFound, self).__init__(error)