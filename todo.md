# TODO
- - do local playblast in current maya scene
    ###todo
    - ask for save???
    - open output folder
    - redshift worker should use movie path of job
    - untitled file sc
    ###done
    - edit context for everything in redshift worker. also motion blur and depth of field
    - rename worker.render_frames() to create_playblast
    - add check for DG Evaluation Mode
    - add check if file already exists
    - call redshift worker in current session
    - edit context to restore old state: createNode, setAttr, connectAttr, disconnectAttr
    - rename "submit" button and methods to "Create Playblast"
    - add "local" or "renderfarm" radio button to UI
    - add local or renderfarm to playblast job
    - tooltips for maya buttons
    - UI: Buttons for 'from scene range' for frame range and 'from render settings' for resolution

- ffmpeg override file    
- support unsaved file
- support current render layer
- Readme
- hooks oder OOP?
- hook for image location
- exception when ffmpeg ist not found
- playblast_job: illegal_argument exceptions

- fix deadline progress
- proper Deadline Plugin: tests, maya path, playblast.py script
- documentation

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

