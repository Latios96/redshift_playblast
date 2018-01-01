# TODO
- Readme
- proper Deadline Plugin: tests, settings für ffmpeg path, maya path, playblast.py script
## install script
cmd line script:
- fragt nach Ordner im Maya [Script_Path oder PythonPath] und kopiert playblast module dahin 
- installiert Deadline Plugin, findet Repo Ordner mit: os.environ['DEADLINE_PATH'] deadlinecommand.exe GetRepositoryRoot
- kopiert playblast.py script in Deadline Ordner ODER setzt Pfad zu Maya Path
