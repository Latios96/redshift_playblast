import Deadline
from Deadline.Plugins import *

from System import *
from System.Diagnostics import *
from System.IO import *

from Deadline.Scripting import *

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
        self.frames_done=0

    ## Clean up the plugin.
    def Cleanup():
        del self.InitializeProcessCallback

    ## Called by Deadline to initialize the plugin.
    def InitializeProcess( self ):
        # Set the plugin specific settings.
        self.SingleFramesOnly = False
        self.PluginType = PluginType.Simple
        self.AddStdoutHandlerCallback( ".*Frame done - total time for frame.*" ).HandleCallback += self.do_progress

    #get render executable
    def RenderExecutable(self):
        maya_exe_list=self.GetConfigEntry( "MayaPyExecutable" )
        maya_exe = FileUtils.SearchFileList( maya_exe_list )
        if maya_exe == "":
            self.FailRender( "Maya mayapy executable was not found in the semicolon separated list \"" + maya_exe_list + "\". The path to the render executable can be configured from the Plugin Configuration in the Deadline Monitor." )

        return maya_exe

    def do_progress (self):
        self.total_frames=self.GetPluginInfoEntry('end_frame')-self.GetPluginInfoEntry('start_frame')
        self.frames_done+=1
        print "PROGRESS", self.frames_done*100/(self.total_frames+1)
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

        print "movie path"
        renderArguments+=' -movie_path "{0}"'.format(self.GetPluginInfoEntry('movie_path')) 

        print "getting camera"
        renderArguments+=' -camera {0}'.format(self.GetPluginInfoEntry('camera')) 

        print "getting dof"
        renderArguments+=' -dof {0}'.format(self.GetPluginInfoEntry('dof')) 

        print "getting motion_blur"
        renderArguments+=' -motion-blur {0}'.format(self.GetPluginInfoEntry('motion_blur')) 

        print "getting file path"
        renderArguments+=' -quality "{0}"'.format(self.GetPluginInfoEntry('quality')) 

        print "shader override type"
        renderArguments+=' -shader_override_type "{0}"'.format(self.GetPluginInfoEntry('shader_override_type')) 

        return renderArguments
