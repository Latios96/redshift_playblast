# TODO

###todo
- documentation
- demo video
- Readme
- License
###done
- deadline plugin: parameter for maya location
- refractor module structure
- do local playblast in current maya scene
- check movie exists
- logging level: info
- ask for save???
- ffmpeg override file  
- restore render cam
- untitled file scene name
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


### ideas 

- support current render layer
- hooks oder OOP mit Dependecy Injection????
- customize: 
    - image/movie location
    - quality presets

- fix deadline progress
- support for different fps
- hook for image location
- exception when ffmpeg ist not found
- playblast_job: illegal_argument exceptions


- rewrite ui
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

