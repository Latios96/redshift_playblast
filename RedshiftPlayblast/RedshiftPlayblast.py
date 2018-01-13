import Deadline
print Deadline.__file__
from Deadline.Plugins import *
import os
######################################################################
## This is the function that Deadline calls to get an instance of the
## main DeadlinePlugin class.
######################################################################
def GetDeadlinePlugin():
    return RedshiftPlayblastPlugin()

######################################################################
## This is the function that Deadline calls when the plugin is no
## longer in use so that it can get cleaned up.
######################################################################
def CleanupDeadlinePlugin( deadlinePlugin ):
    deadlinePlugin.Cleanup()

######################################################################
## This is the main DeadlinePlugin class for MyPlugin.
######################################################################
class RedshiftPlayblastPlugin (DeadlinePlugin):

    ## Hook up the callbacks in the constructor.
    def __init__( self ):
        self.InitializeProcessCallback += self.InitializeProcess
        self.RenderExecutableCallback += self.RenderExecutable
        self.RenderArgumentCallback += self.RenderArgument
        self.AddStdoutHandlerCallback( "[Redshift] Frame done - total time for frame" ).HandleCallback += self.HandleProgress 
        self.frames_done=0

    ## Clean up the plugin.
    def Cleanup():
        del self.InitializeProcessCallback

    ## Called by Deadline to initialize the plugin.
    def InitializeProcess( self ):
        # Set the plugin specific settings.
        self.SingleFramesOnly = False
        self.PluginType = PluginType.Simple

    #get render executable
    def RenderExecutable(self):
        return r"C:\Program Files\Autodesk\Maya2017\bin\mayapy.exe"

    def HandleProgress (self):
        self.total_frames=self.GetPluginInfoEntry('end_frame')-self.GetPluginInfoEntry('start_frame')
        self.frames_done+=1
        self.SetProgress(self.frames_done*100/(self.total_frames+1))

    def RenderArgument(self):
        renderArguments= r"M:\workspace\redshift_playblast\redshift_playblast\playblast.py"
        print "getting file path"
        renderArguments+=' -file_path "{0}"'.format(self.GetPluginInfoEntry('file_path')) 

        print "getting start_frame"
        renderArguments+=' -start_frame {0}'.format(self.GetPluginInfoEntry('start_frame')) 

        print "getting end_frame"
        renderArguments+=' -end_frame {0}'.format(self.GetPluginInfoEntry('end_frame')) 

        print "getting width"
        renderArguments+=' -width {0}'.format(self.GetPluginInfoEntry('width')) 

        print "getting height"
        renderArguments+=' -height {0}'.format(self.GetPluginInfoEntry('height')) 

        print "getting  frame_path" 
        job=self.GetJob()
        print job.GetJobInfoKeyValue('OutputDirectory0')
        print job.GetJobInfoKeyValue('OutputFilename0')
        renderArguments+=' -frame_path "{0}"'.format(os.path.join(job.GetJobInfoKeyValue('OutputDirectory0'), job.GetJobInfoKeyValue('OutputFilename0')))

        print "getting camera"
        renderArguments+=' -camera {0}'.format(self.GetPluginInfoEntry('camera')) 

        print "getting dof"
        renderArguments+=' -dof {0}'.format(self.GetPluginInfoEntry('dof')) 

        print "getting motion_blur"
        renderArguments+=' -motion-blur {0}'.format(self.GetPluginInfoEntry('motion_blur')) 

        print "getting file path"
        renderArguments+=' -quality "{0}"'.format(self.GetPluginInfoEntry('quality')) 

        return renderArguments
