class Shader_Override_Type(object):
    """
    Helpers class for shader override types, something like an enum
    """
    NO_OVERRIDE = 0 # no shading override is applied and the scene is playblasted with the current shading
    AMBIENT_OCCLUSION = 1 #an ambient occlusion shader is applied to all objects in scene
    GREYSCALE = 2 #a greyscale shader is applied to all objects in scene
    PRODUCTION_SHADER = 3 #the assign_production_shader hook will be called to assign your profuction shaders

    nice_names={NO_OVERRIDE: 'no override',
                 AMBIENT_OCCLUSION: 'Ambient Occlusion',
                 GREYSCALE: 'Greyscale',
                 PRODUCTION_SHADER: 'Production Shader'}

    @staticmethod
    def nice_name(value):
        return Shader_Override_Type.nice_names[value]

    @staticmethod
    def value(nice_name):
        for key, value in Shader_Override_Type.nice_names.iteritems():
            if nice_name==value:
                return key

