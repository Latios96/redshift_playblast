class Shader_Override_Type(object):
    NO_OVERRIDE = 0
    AMBIENT_OCCLUSION = 1
    GREYSCALE = 2
    PRODUCTION_SHADER = 3

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

