from redshift_playblast import playblast_job
import pymel.core as pm
import ktrack_metadata


class Maya_Manager(object):

    def __init__(self):
        self.job=playblast_job.Playblast_Job(file_path=pm.sceneName(),
                                             start_frame=pm.playbackOptions(minTime=True),
                                             end_frame=pm.playbackOptions(maxTime=True),
                                             width=1920,
                                             height=1080,
                                             frame_path=self.get_frame_path(),
                                             movie_path=self.get_movie_path(),
                                             camera=self.get_camera_information()[0],
                                             dof=self.get_camera_information()[1],
                                             motion_blur=True,
                                             quality='med',
                                             context=ktrack_metadata.from_scene())

    def get_frame_path(self):
        return "{project_location}/movies/{scene_name}_####.exr".format(project_location=pm.workspace.path, scene_name=pm.sceneName())

    def get_movie_path(self):
        return "{project_location}/movies/{scene_name}.mov".format(project_location=pm.workspace.path, scene_name=pm.sceneName())

    def get_camera_information(self):

        if len(pm.ls('render_cam'))>0:
            camera=pm.ls('render_cam')[0]
        else:
            camera=pm.ls('persp')[0]

        return camera, camera.depthOfField.get()

    def submit(self):
        self.job.submit_to_deadline()

