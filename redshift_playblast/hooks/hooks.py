import logging
logger = logging.getLogger(__name__)


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
    """
    Returns the path to the folder containing the ffmpeg executable
    :return:
    """
    return 'C:/ffmpeg/bin'

def assign_production_shader():
    """
    Called when Shader override type is set to PRODUCTION_SHADER. Place your logic to get production shaders and assignment here
    :return:
    """
    logger.info("Assigning production shaders...")