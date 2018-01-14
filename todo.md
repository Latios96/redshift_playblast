# TODO
- Readme
- hooks
- hook for image location
- exception when ffmpeg ist not found
- playblast_job: illegal_argument exceptions
- edit context to restore old state: createNode, setAttr, connectAttr, disconnectAttr
- UI: Buttons for 'from scene range' for frame range and 'from render settings' for resolution
- proper Deadline Plugin: tests, maya path, playblast.py script
- documentation
- do local playblast in current maya scene
- QC Renders for Alembics and VDBs
- demo video
## install script
cmd line script:
- fragt nach Ordner im Maya [Script_Path oder PythonPath] und kopiert playblast module dahin 
- installiert Deadline Plugin, findet Repo Ordner mit: os.environ['DEADLINE_PATH'] deadlinecommand.exe GetRepositoryRoot
- kopiert playblast.py script in Deadline Ordner ODER setzt Pfad zu Maya Path
- fragt nach, ob es ffmpeg downloaden soll, fragt nach Ordner
- alles auch einmal mit cmd options configurierbar
- writes install.bat with current settings

