# Redshift Playblast

Tools to easily create Playblasts from Maya, but instead of OpenGL render them with Redshift for proper DOF, Motion Blur, lighting etc.

# Features
- a command line script to create the playblast
- a Deadline Plugin to create the playblast on the Render Farm
- a Maya Tool with settings to create the playblast

# Requirements
- ffmpeg is required to stitch the single rendered frames together
- mock is required to run the tests, Qt.py for GUI/Signals

# Installation
### Maya
- install Python Dependencies:
```sh
pip install -r requirements.txt --target <some folder in PYTHONPATH for Maya>
```
- install ffmpeg, download here: https://www.ffmpeg.org/download.html
- copy the folder "redshift_playblast" to some folder in PYTHONPATH for Maya

### Deadline
- the folder "RedshiftPlayblast" is the Deadline Plugin. Inside your Deadline Repository, copy the folder to <DEADLINE_REPOSITOY>/custom/plugins

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

