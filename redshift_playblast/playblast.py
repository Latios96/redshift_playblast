import argparse
#we have to import pymel here, because otherwise maya does not setup the PYTHONPATH from maya.env
import pymel.core as pm

from redshift_playblast.worker import redshift_worker


class PlayblastQualityError(Exception):
    """
    Exception thrown when a non-valid quality settings was supplied
    """
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-file_path', help='File to  playblast')
    parser.add_argument('-start_frame', help='Starting frame for playblast')
    parser.add_argument('-end_frame', help='Ending frame for playblast')
    parser.add_argument('-width', help='width for playblast')
    parser.add_argument('-height', help='width for playblast')
    parser.add_argument('-frame_path', help='Path where to place the rendered images')
    parser.add_argument('-camera', help='camera to use')
    parser.add_argument('-dof', help='Use DOF or not')
    parser.add_argument('-motion-blur', help='Use Motion Blur or not')
    parser.add_argument('-quality', help='Quality, LOW, MED or HIGH')

    args = parser.parse_args()

    #validate args
    if args.quality.lower() not in ['low', 'med', 'high', 'medium']:
        error="Unsupported quality settings: "+args.quality+". Supported are LOW, MED or HIGH"
        raise PlayblastQualityError(error)

    #convert args to correct data types
    args.start_frame=float(args.start_frame)
    args.end_frame = float(args.end_frame)
    args.width=int(args.width)
    args.height = int(args.height)
    args.motion_blur=True if 'True' in args.motion_blur else False
    args.dof = True if 'True' in args.dof else False


    renderer=redshift_worker.Redshift_Worker(args)

    renderer.render_frames()

if __name__ == '__main__':
    main()