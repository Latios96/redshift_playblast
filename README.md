# Redshift Playblast

Tools to easily create Playblasts from Maya, but instead of OpenGL render them with Redshift for proper DOF, Motion Blur, lighting etc.

# Features
- a command line script to create the playblast
- a Deadline Plugin to create the playblast on the Render Farm
- a Maya Tool with settings to create the playblast

# Requirements
- ffmpeg is required to stitch the single rendered frames together

# Installation
Use install script. This will guide you through the installation
```sh
pip install git+ssh://git@github.com/Latios96/ktrack_metadata.git
```

# Usage
Run inside Maya 
```sh
from redshift_playblast.view import redshift_playblast_view
redshift_playblast_view.run_maya()
```
# Limitations
- only tested under Windows
- only Deadline is supported as a Render Manager
- the script renders single images and stitches them together to a Quicktime using ffmpeg. These single images are rendered as .png files instead of .exr,
because ffmpeg has problems with exrs from Redshift

