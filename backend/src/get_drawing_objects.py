from configs import TRIANGLE_COLORING_CONFIGS, LINE_DRAWING_CONFIGS, POINT_DRAWING_CONFIGS
from triangle_coloring import *
from line_drawing import *
from point_drawing import *

def get_triangle_coloring_object(configs=TRIANGLE_COLORING_CONFIGS):
    if configs["TYPE"] == 'PlainColor':
        return PlainColor(**configs["KWARGS"])
    elif configs["TYPE"] == 'RGBGradient':
        return RGBGradient(**configs["KWARGS"])
    elif configs["TYPE"] == 'HSVLinearGradientContinuous':
        return HSVLinearGradientContinuous(**configs["KWARGS"])
    elif configs["TYPE"] == 'HSVLinearGradientDiscrete':
        return HSVLinearGradientDiscrete(**configs["KWARGS"])
    elif configs["TYPE"] == 'HSVExponentialGradientContinuous':
        return HSVExponentialGradientContinuous(**configs["KWARGS"])
    elif configs["TYPE"] == 'AmbientShader':
        return AmbientShader(**configs["KWARGS"])
    elif configs["TYPE"] == 'MultiLightShader':
        return MultiLightShader(**configs["KWARGS"])
    elif configs["TYPE"] == 'ShadedGradient':
        return ShadedGradient(**configs["KWARGS"])
    elif configs["TYPE"] == 'StaticNoise':
        return StaticNoise(**configs["KWARGS"])
    elif configs["TYPE"] == 'TieDyeSwirl':
        return TieDyeSwirl(**configs["KWARGS"])
    elif configs["TYPE"] == 'ColorShifting':
        return ColorShifting(**configs["KWARGS"])
    else:
        raise RuntimeError(f"Incorrect configs attribute 'TYPE': {configs['TYPE']}")

def get_line_drawing_object(configs=LINE_DRAWING_CONFIGS):
    if not configs["DRAW_LINES"]:
        return None
    if configs["TYPE"] == 'SolidLine':
        return SolidLine(**configs["KWARGS"])
    elif configs["TYPE"] == 'FadingLine':
        return FadingLine(**configs["KWARGS"])
    raise RuntimeError(f"Incorrect configs attribute 'TYPE': {configs['TYPE']}")

def get_point_drawing_object(configs=POINT_DRAWING_CONFIGS):
    if not configs["DRAW_POINTS"]:
        return None
    if configs["TYPE"] == 'PlainPoint':
        return PlainPoint(**configs["KWARGS"])
    raise RuntimeError(f"Incorrect configs attribute 'TYPE': {configs['TYPE']}")
