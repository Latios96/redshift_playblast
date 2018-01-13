# TODO
- Readme
- hooks
- support ffmpeg not in path
- proper Deadline Plugin: tests, settings für ffmpeg path, maya path, playblast.py script, ffmpeg settings
- option to remove temp png images
- do local playblast in current maya scene
- QC Renders for Alembics and VDBs
## install script
cmd line script:
- fragt nach Ordner im Maya [Script_Path oder PythonPath] und kopiert playblast module dahin 
- installiert Deadline Plugin, findet Repo Ordner mit: os.environ['DEADLINE_PATH'] deadlinecommand.exe GetRepositoryRoot
- kopiert playblast.py script in Deadline Ordner ODER setzt Pfad zu Maya Path
- fragt nach, ob es ffmpeg downloaden soll, fragt nach Ordner
- alles auch einmal mit cmd options configurierbar
- writes install.bat with current settings

