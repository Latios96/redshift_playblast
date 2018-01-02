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
- write:
    ```sh
    import ktrack_metadata
    ktrack_metadata.write_to_scene(meta)
    ```
    meta needs to be an instance of ktrack_metadata.Ktrack_metadata. 
- read
     ```sh
    import ktrack_metadata
    meta=ktrack_metadata.from_scene()
    ```
    from_scene will return a ktrack_metadata.Ktrack_metadata instance.
- create a ktrack_metadata.Ktrack_metadata instance
     ```sh
        import ktrack_metadata
        meta=ktrack_metadata.Ktrack_metadata(parameters)
        meta=ktrack_metadata.Ktrack_metadata.from_dict(your_dict)
    ```
# Limitations
- only Deadline is supported as a Render Manager
- the script renders single images and stitches them together to a Quicktime using ffmpeg. These single images are rendered as .png files instead of .exr,
because ffmpeg has problems with exrs from Redshift

