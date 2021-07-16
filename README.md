# Dynamic Background
> Generates seamless gifs of triangle meshes.



## Installation

*Python 3.8 required*

Required Python Dependencies:
- [PIL](https://pillow.readthedocs.io/en/stable/index.html)
- [numpy](https://numpy.org/doc/stable/)
- [opensimplex](https://pypi.org/project/opensimplex/)

Third Party Dependencies:
- [ImageMagick](https://imagemagick.org/script/download.php)

## Notes on Usage

The only file which needs to be modified in order to customize the gifs is `config.json`. However, if the file structure is changed there will be some issues in the source code (either `src/main.py` or `src/configs.py` depending on what is moved).

## File Structure

```
.
├── gifs
│   ├── 1
│   │   ├── config.json
│   │   └── gif1.gif
│   ├── 2
│   │   ├── config.json
│   │   └── gif2.gif
│   ├── 3
│   │   ├── config.json
│   │   └── gif3.gif
│   ├── 4
│   │   ├── config.json
│   │   └── gif4.gif
│   ├── 5
│   │   ├── config.json
│   │   └── gif5.gif
│   ├── 6
│   │   ├── config.json
│   │   └── gif6.gif
│   ├── 7
│   │   ├── config.json
│   │   └── gif7.gif
│   └── 8
│       ├── config.json
│       └── gif8.gif
├── src
│   ├── configs.py
│   ├── generate_points.py
│   ├── get_drawing_objects.py
│   ├── helpers.py
│   ├── line_drawing.py
│   ├── main.py
│   ├── point_drawing.py
│   ├── point.py
│   ├── triangle_coloring.py
│   └── triangulation.py
├── config.json
├── LICENSE
└── README.md
```
- `src/configs.py`: Houses all global variables needed for the project.
- `src/generate_points.py`: Methods for generating the initial points.
- `src/get_drawing_objects.py`: Methods for converting dictionary's into classes.
- `src/helpers.py`: Useful methods which exist outside of the other files.
- `src/line_drawing`: Classes for drawing the lines of the gif.
- `src/main.py`: The main function of the project. Creates and compiles frames into gifs.
- `src/point_drawing.py`: Classes for drawing the points of the gif.
- `src/point.py`: Classes for the different types of points in the gif.
- `src/triangle_coloring.py`: Classes for drawing the triangles of the gifs.
- `src/triangulation.py`: Houses the triangle class and has any methods needed to turn a list of points into a triangular mesh.
- `config.json`: Has all of the global variables needed for the project. More info in the next section.

## `config.json` Attribute Notes

Example config.json:
```
{
    "RANDOM_SEED": true,
    "SEED": 1625466190,
    "WIDTH": 1366,
    "HEIGHT": 768,
    "NUM_OF_FRAMES": 250,
    "BACKGROUND_COLOR": [0, 0, 0],
    "GIF_CONFIGS": {
        "NUM": 5,
        "MS_PER_FRAME": 11,
        "MARGIN": 150
    },
    "POINT_CONFIGS": {
        "AMPLITUDE": 0,
        "INTENSITY": 0,
        "SCALE": 0,
        "OFFSET_Y": 100,
        "NUM_OF_POINTS": 500,
        "SEPARATION_RADIUS": 40,
        "MAX_FAILS": 10000,
        "BORDER_CONFIGS": {
            "TOP": true,
            "BOTTOM": true,
            "LEFT": true,
            "RIGHT": true,
            "SEPARATION": 40
        },
        "DRIFTING_CONFIGS": {
            "PERCENTAGE": 1,
            "X_MIN": -1,
            "X_MAX": 1,
            "Y_MIN": 0,
            "Y_MAX": 0
        }
    },
    "TRIANGLE_COLORING_CONFIGS": {
        "TYPE": "ShadedGradient",
        "KWARGS": {
            "START_X": 150,
            "START_Y": 0,
            "END_X": 1516,
            "END_Y": 0,
            "START_COLOR": [235, 52, 52],
            "END_COLOR": [66, 224, 245],
            "ALPHA": 0.8,
            "AMBIENT_VECTOR": [1.0, 1.0, 0.5],
            "AMBIENT_GAIN": 55000,
            "AMBIENT_DEFINITION": 10
        }
    },
    "LINE_DRAWING_CONFIGS": {
        "DRAW_LINES": false,
        "TYPE": "SolidLine",
        "KWARGS": {
            "COLOR": [255, 255, 255],
            "WIDTH": 2
        }
    },
    "POINT_DRAWING_CONFIGS": {
        "DRAW_POINTS": false,
        "TYPE": "PlainPoint",
        "KWARGS": {
            "COLOR": [255, 255, 255],
            "WIDTH": 5
        }
    }
}
```

- `RANDOM_SEED` (boolean): Whether or not a random seed should be generated at runtime.
- `SEED` (int): The seed to be used to recreate a gif. This seed will be overwritten if `RANDOM_SEED` is set to true.
- `WIDTH` (int): The width of the final gif.
- `HEIGHT` (int): The height of the final gif.
- `NUM_OF_FRAMES` (int): The number of frames in the final gif.
- `BACKGROUND_COLOR` ([int]): The 0-255 RGB background color.
- `GIF_CONFIGS`: Configuration attributes for the final gif.
    * `NUM` (int): The folder where the final gif will be stored in.
    * `MS_PER_FRAME` (int): The number of milliseconds between frames.
    * `MARGIN` (int): The maximum distance past the edge of the screen that a point can move to.
- `POINT_CONFIGS`:
    * `AMPLITUDE` (float): How far points can travel compared tov initial position.
    * `INTENSITY` (float): How quickly points can change directions.
    * `SCALE` (float): How 'zoomed in' the noise should be (affects smoothness of motion).
    * `OFFSET_Y` (float): *There is almost no reason to modify this.* When the noise function is calculated it gives a scalar value based on the point's position. In order for the x-offset to not be equal to the y-offset the calculation for the y-offset must have a different position than the x-offset's calculation. This attribute moves the point's position for the y-offset calculation.
    * `NUM_OF_POINTS` (int): The maximum number of points in the gif.
    * `SEPARATION_RADIUS` (int): The minimum distance away initial points can be from each other.
    * `MAX_FAILS` (int): The maximum number of times the code will attempt to place a point before giving up.
    * `BORDER_CONFIGS`: Configuration attributes for drawing points on the border of the gif. Helpful for ensuring there are no gaps in the triangular mesh.
        - `TOP` (boolean): Whether or not the top border should be generated.
        - `BOTTOM` (boolean): Whether or not the bottom border should be generated.
        - `LEFT` (boolean): Whether or not the left border should be generated.
        - `RIGHT` (boolean): Whether or not the right border should be generated.
        - `SEPARATION` (int): How far apart border points should be.
    * `DRIFTING_CONFIGS`: Configuration attributes for points which continually drift in a specific direction.
        - `PERCENTAGE` (float): What percentage of points should be drifting (the rest will sway).
        - `X_MIN` (int): The minimum number of times a drifting point can drifting a full screen distance in the positive x-direction (will drift in the negative x-direction if negative).
        - `X_MAX` (int): The maximum number of times a drifting point can drifting a full screen distance in the positive x-direction (will drift in the negative x-direction if negative).
        - `Y_MIN` (int): The minimum number of times a drifting point can drifting a full screen distance in the positive y-direction (will drift in the negative y-direction if negative).
        - `Y_MAX` (int): The maximum number of times a drifting point can drifting a full screen distance in the positive y-direction (will drift in the negative y-direction if negative).
- `TRIANGLE_COLORING_CONFIGS`: The configuration attributes for coloring of the triangles (more detail in section [Triangle Coloring](#triangle-coloring)).
    * `TYPE` (string): Which triangle coloring object will be used to color the gif.
    * `KWARGS` (dict): The attributes needed to instantiate the triangle coloring object.
- `LINE_DRAWING_CONFIGS`: The configuration attributes for drawing the lines between points (more detail in section [Line Drawing](#line-drawing)).
    * `DRAW_LINES` (boolean): Whether or not the lines should be drawn.
    * `TYPE` (string): Which line drawing object will be used to color the gif.
    * `KWARGS` (dict): The attributes needed to instantiate the line drawing object.
- `POINT_DRAWING_CONFIGS`: The configuration attributes for drawing the points (more detail in section [Point Drawing](#point-drawing)).
    * `DRAW_POINTS`: Whether or not the points should be drawn.
    * `TYPE` (string): Which point drawing object will be used to color the gif.
    * `KWARGS` (dict): The attributes needed to instantiate the point drawing object.


## Triangle Coloring

`PlainColor`: Draws all triangles the same color.
```
    ...
    "TRIANGLE_COLORING_CONFIGS": {
        "TYPE": "PlainColor",
        "KWARGS": {
            "COLOR": [255, 255, 255]
        }
    },
    ...
```
- `COLOR` ([int]): 0-255 RGB color code for the color of the triangles.

`HSVLinearGradientContinuous`: Draws all triangles based off of a linear HSV color gradient. To define the direction of the gradient, two points are defined as the start and end of a line. Then the center of the triangle is used to find where the triangle is on the line and a linear interpolation is used to find the specific color. As the color gradient uses HSV colors, the gradient may create many intermediate colors.
```
    ...
    "TRIANGLE_COLORING_CONFIGS": {
        "TYPE": "HSVLinearGradientContinuous",
        "KWARGS": {
            "START_X": 0,
            "START_Y": 0,
            "END_X": 1366,
            "END_Y": 768,
            "START_COLOR": [255, 0, 0],
            "END_COLOR": [0, 0, 255]
        }
    },
    ...
```
- `START_X` (int): The x-value of the starting point for the gradient line.
- `START_Y` (int): The y-value of the starting point for the gradient line.
- `END_X` (int): The x-value of the ending point for the gradient line.
- `END_Y` (int): The y-value of the ending point for the gradient line.
- `START_COLOR` ([int]): A 0-255 RGB color code to be used as a starting color.
- `END_COLOR` ([int]): A 0-255 RGB color code to be used as a ending color.

`HSVExponentialGradientContinuous`: An extension of `HSVLinearGradientContinuous`, uses the same method for finding the gradient but instead of using a linear interpolation, the value is scaled by an exponential to squeeze toghether colors.
```
    ...
    "TRIANGLE_COLORING_CONFIGS": {
        "TYPE": "HSVExponentialGradientContinuous",
        "KWARGS": {
            "START_X": 0,
            "START_Y": 0,
            "END_X": 1366,
            "END_Y": 768,
            "START_COLOR": [255, 0, 0],
            "END_COLOR": [0, 0, 255],
            "ALPHA": 0.8
        }
    },
    ...
```
- `START_X` (int): The x-value of the starting point for the gradient line.
- `START_Y` (int): The y-value of the starting point for the gradient line.
- `END_X` (int): The x-value of the ending point for the gradient line.
- `END_Y` (int): The y-value of the ending point for the gradient line.
- `START_COLOR` ([int]): A 0-255 RGB color code to be used as a starting color.
- `END_COLOR` ([int]): A 0-255 RGB color code to be used as a ending color.
- `ALPHA` (float): The scale of the exponential function. **Fails when alpha is 0**.

`HSVLinearGradientDiscrete`: An extension of `HSVLinearGradientContinuous`, uses the same method for finding the gradient but will only use a set number of colors.
```
    ...
    "TRIANGLE_COLORING_CONFIGS": {
        "TYPE": "HSVLinearGradientDiscrete",
        "KWARGS": {
            "START_X": 0,
            "START_Y": 0,
            "END_X": 1366,
            "END_Y": 768,
            "START_COLOR": [255, 0, 0],
            "END_COLOR": [0, 0, 255],
            "NUM_OF_COLORS": 5
        }
    },
    ...
```
- `START_X` (int): The x-value of the starting point for the gradient line.
- `START_Y` (int): The y-value of the starting point for the gradient line.
- `END_X` (int): The x-value of the ending point for the gradient line.
- `END_Y` (int): The y-value of the ending point for the gradient line.
- `START_COLOR` ([int]): A 0-255 RGB color code to be used as a starting color.
- `END_COLOR` ([int]): A 0-255 RGB color code to be used as a ending color.
- `NUM_OF_COLORS` (int): The number of colors the gradient should have.

`AmbientShader`: Uses a simple shading approach to shade the gif. This does not create accurate shadows and instead uses how closely the triangle is facing the 'light source' to find how bright the triangle should be.
```
    ...
    "TRIANGLE_COLORING_CONFIGS": {
        "TYPE": "AmbientShader",
        "KWARGS": {
            "AMBIENT_COLOR": [98, 182, 227],
            "AMBIENT_VECTOR": [1.0, 1.0, 1.0],
            "AMBIENT_GAIN": 50000,
            "AMBIENT_DEFINITION": 20
        }
    },
    ...
```
- `AMBIENT_COLOR` ([int]): A 0-255 RGB color code for the brightest color of the gif.
- `AMBIENT_VECTOR` ([float]): The vector which points in the direction of the 'light source'.
- `AMBIENT_GAIN` (float): How bright the ambient light is.
- `AMBIENT_DEFINITION` (int): How defined the light is.

`MultiLightShader`: An extension of the `AmbientShader`, this includes extra point light sources.
```
    ...
    "TRIANGLE_COLORING_CONFIGS": {
        "TYPE": "MultiLightShader",
        "KWARGS": {
            "AMBIENT_COLOR": [156, 47, 11],
            "AMBIENT_VECTOR": [0, 1.0, 0.2],
            "AMBIENT_GAIN": 3000000,
            "AMBIENT_DEFINITION": 10,
            "GAIN": 1000,
            "LIGHTS": [
                {
                    "POS": [703, 0, 1000],
                    "INTENSITY": 500,
                    "COLOR": [255, 0, 81]
                },
                {
                    "POS": [1406, 808, 1000],
                    "INTENSITY": 200,
                    "COLOR": [255, 247, 0]
                }
            ]
        }
    },
    ...
```
- `AMBIENT_COLOR` ([int]): A 0-255 RGB color code for the brightest color of the gif.
- `AMBIENT_VECTOR` ([float]): The vector which points in the direction of the 'light source'.
- `AMBIENT_GAIN` (float): How bright the ambient light is.
- `AMBIENT_DEFINITION` (int): How defined the light is.
- `GAIN` (float): How bright the light sources are.
- `LIGHTS` ([dict]): The variables for the point sources of light.
    * `POS` ([int]): The point of light's position.
    * `INTENSITY` (float): The point of light's intensity.
    * `COLOR` ([int]): A 0-255 RGB color code for the color of the point of light.

`ShadedGradient` an extension of the `AmbientShader`. Instead of using a single color, this uses another triangle coloring object.
```
    ...
    "TRIANGLE_COLORING_CONFIGS": {
        "TYPE": "ShadedGradient",
        "KWARGS": {
            "GRADIENT": {
                "TYPE": "HSVExponentialGradientContinuous",
                "KWARGS": {
                    "START_X": 150,
                    "START_Y": 150,
                    "END_X": 1516,
                    "END_Y": 918,
                    "START_COLOR": [235, 52, 52],
                    "END_COLOR": [66, 224, 245],
                    "ALPHA": 0.8
                }
            },
            "AMBIENT_VECTOR": [1.0, 1.0, 0.5],
            "AMBIENT_GAIN": 55000,
            "AMBIENT_DEFINITION": 10
        }
    },
    ...
```
- `GRADIENT` (dict): The triangle coloring object which is used as the base color.
    * `TYPE` (string): The type of triangle coloring object.
    * `KWARGS` (dict): The inputs to the triangle coloring object.
- `AMBIENT_VECTOR` ([float]): The vector which points in the direction of the 'light source'.
- `AMBIENT_GAIN` (float): How bright the ambient light is.
- `AMBIENT_DEFINITION` (int): How defined the light is.

## Line Drawing
`SolidLine`: Draws all lines with a set color and width.
```
    ...
    "LINE_DRAWING_CONFIGS": {
        "DRAW_LINES": true,
        "TYPE": "SolidLine",
        "KWARGS": {
            "COLOR": [255, 255, 255],
            "WIDTH": 2
        }
    },
    ...
```
- `COLOR`([int]): The 0-255 RGB color the lines will be.
- `WIDTH` (int): The width the lines will be.

`FadingLine`: A way of coloring the lines based off of how long they are. **The color of the line will be linearly interpolated when the length of the line is between `MIN_DIST` and `MAX_DIST`.** 
```
    ...
    "LINE_DRAWING_CONFIGS": {
        "DRAW_LINES": true,
        "TYPE": "FadingLine",
        "KWARGS": {
            "START_COLOR": [255, 255, 255],
            "END_COLOR": [0, 0, 0],
            "MIN_DIST": 20,
            "MAX_DIST": 250,
            "WIDTH": 5
        }
    },
    ...
```
- `START_COLOR` ([int]): The 0-255 RGB color code for when the line's length is <= `MIN_DIST`.
- `END_COLOR` ([int]): The 0-255 RGB color code for when the length is >= `MAX_DIST`.
- `MIN_DIST` (float): The minimum length the line can be .
- `MAX_DIST` (float): The maximum length the line can be.
- `WIDTH` (int): The width of the line.

## Point Drawing
`PlainPoint`: Draws all points with a specific thickness and color.
```
    ...
    "POINT_DRAWING_CONFIGS": {
        "DRAW_POINTS": true,
        "TYPE": "PlainPoint",
        "KWARGS": {
            "COLOR": [255, 255, 255],
            "WIDTH": 5
        }
    }
    ...
```
- `COLOR` ([int]): A 0-255 RGB color code for the color of the points.
- `WIDTH` (int): The width of the points. 

## Contributing

I have tried to make it fairly simple to add options to this project. If you have any ideas for different ways to color the triangles, lines, or points you can suggest them with an issue marked as an `idea` or you can create the function by creating a new class which extends one of the following abstract classes:
```
class TriangleColorer(ABC):
    @abstractmethod
    def get_color(self, triangle):
        pass
```

```
class LineDrawer(ABC):
    @abstractmethod
    def get_color(self, edge):
        pass

    @abstractmethod
    def get_width(self, edge):
        pass
```

```
class PointDrawer(ABC):
    @abstractmethod
    def get_color(self, x, y):
        pass

    @abstractmethod
    def get_width(self, x, y):
        pass
```
If you have an idea for other functionality, add an issue marked `idea` or you can clone the repository and try it out for yourself.

## Future Work

I would like the ability to change how the OpenSimplex oscillates. I could do this by changing the circle that the OpenSimplex function takes to instead be a different, smooth, continuous shape. Perhaps randomly generated or a set shape. A potential shape could be a sort of infinity symbol. Additionally, I would like to make a gui which would make it easier to create and preview gifs before commiting to generating and compiling. Finally, I would like to add some more options for coloring the triangles, one option would be to take a noise map to create a sort of tie-dye pattern or a gradient which extends radially as opposed to linearly.
