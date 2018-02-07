import logging
logger = logging.getLogger(__name__)

import pymel.core as pm

def deadline_plugin_info_file(file_handle):
    """
    Called after the job wrote its data to the plugin_info_file for deadline.
    Use this hooks to write additional stuff to the plugin info file.
    :param file_handle:
    :return:
    """
    pass

def deadline_job_info_file(file_handle):
    """
    Called after the job wrote its data to the job_info_file for deadline.
    Use this hooks to write additional stuff to the job info file.
    :param file_handle:
    :return:
    """
    pass

def get_ffmpeg_folder():
    # type: () -> str
    """
    Returns the path to the folder containing the ffmpeg executable
    :return:
    """
    return 'C:/ffmpeg/bin'

def assign_production_shader(context):
    """
    Called when Shader override type is set to PRODUCTION_SHADER. Place your logic to get production shaders and assignment here
    You have to use the given edit context, if you want your changes to be reverted in a live maya session
    :return:
    """
    logger.info("Assigning production shaders...")

def frame_path(scene_name):
    """
    Returns the path of the rendered images. Has to end with .####.png .
    :return:
    """
    return "{project_location}/movies/{scene_name}.####.png".format(project_location=pm.workspace.path, scene_name=scene_name)

def movie_path(scene_name):
    """
    Returns the path of the final playblast. Has to end with .mov. {scenename will be replaced automagically}
    :return:
    """
    return "{project_location}/movies/{scene_name}.mov".format(project_location=pm.workspace.path, scene_name=scene_name)