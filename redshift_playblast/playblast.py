import argparse
# we have to import pymel here, because otherwise maya does not setup the PYTHONPATH from maya.env
import pymel.core as pm

from redshift_playblast.logic import redshift_worker
from redshift_playblast.model.playblast_job import Playblast_Job


class PlayblastQualityError(Exception):
    """
    Exception thrown when a non-valid quality settings was supplied
    """
    pass


def main():
    """
    Takes command line arguments and constructs a playblast job from it.
    Executes the job using a Redshift Worker
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-file_path', help='File to  playblast')
    parser.add_argument('-start_frame', help='Starting frame for playblast')
    parser.add_argument('-end_frame', help='Ending frame for playblast')
    parser.add_argument('-width', help='width for playblast')
    parser.add_argument('-height', help='width for playblast')
    parser.add_argument('-frame_path', help='Path where to place the rendered images')
    parser.add_argument('-movie_path', help='Path where to place the movie file')
    parser.add_argument('-camera', help='camera to use')
    parser.add_argument('-dof', help='Use DOF or not')
    parser.add_argument('-motion-blur', help='Use Motion Blur or not')
    parser.add_argument('-quality', help='Quality, LOW, MED or HIGH')
    parser.add_argument('-shader_override_type', help='shader override')

    args = parser.parse_args()

    # validate args
    if args.quality.lower() not in ['low', 'med', 'high', 'medium']:
        error = "Unsupported quality settings: " + args.quality + ". Supported are LOW, MED or HIGH"
        raise PlayblastQualityError(error)

    # create job and convert args to correct data types

    job = Playblast_Job(file_path=args.file_path,
                        start_frame=float(args.start_frame),
                        end_frame=float(args.end_frame),
                        width=int(args.width),
                        height=int(args.height),
                        frame_path=args.frame_path,
                        movie_path=args.movie_path,
                        camera=args.camera,
                        dof=True if 'True' in args.dof else False,
                        motion_blur=True if 'True' in args.motion_blur else False,
                        quality=args.quality,
                        avaible_cameras=[],
                        shader_override_type=int(args.shader_override_type),
                        local_mode=False)

    print job

    renderer = redshift_worker.Redshift_Worker(job)

    renderer.create_playblast()


if __name__ == '__main__':
    main()
