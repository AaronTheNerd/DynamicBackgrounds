# Dynamic Background
> Generates seamless gifs of triangle meshes.



## Installation

*`Python3.10` and `pipenv` required*

Installing Python dependencies with
```
pipenv install
```
in the root directory of the project.

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
├── config.json
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md
└── src
    ├── configs.py
    ├── main.py
    ├── bowyer_watson.py
    ├── triangle_math.py
    ├── triangle.py
    ├── coloring
    │   ├── ABCs.py
    │   ├── color.py
    │   ├── gradient.py
    │   ├── point_translator.py
    │   ├── line
    │   │   ├── ABCs.py
    │   │   ├── color.py
    │   │   ├── line.py
    │   │   └── width.py
    │   ├── point
    │   │   ├── ABCs.py
    │   │   ├── color.py
    │   │   ├── point.py
    │   │   └── width.py
    │   ├── range
    │   │   ├── ABCs.py
    │   │   ├── line_range.py
    │   │   ├── position_range.py
    │   │   ├── range.py
    │   │   └── reflective_range.py
    │   └── triangle
    │       ├── ABCs.py
    │       ├── color.py
    │       ├── shader.py
    │       └── triangle.py
    ├── point
    │   ├── ABCs.py
    │   ├── point.py
    │   ├── state.py
    │   ├── generator
    │   │   ├── ABCs.py
    │   │   ├── generate.py
    │   │   ├── mover_generator.py
    │   │   └── zmover_generator.py
    │   ├── mover
    │   │   ├── ABCs.py
    │   │   ├── mover.py
    │   │   └── zmover.py
    │   └── random
    │       ├── ABCs.py
    │       ├── float.py
    │       ├── int.py
    └── utils
        ├── concrete_inheritors.py
        ├── interpolate.py
        ├── progress_bar.py
        └── vector3d.py
```

## `config.json` Attribute Notes

Example config.json:
```
{
  "generate_seed": true,
  "seed": 1626244211,
  "gif_configs": {
    "width": 1366,
    "height": 768,
    "num": 5,
    "background_color": [0, 0, 0],
    "margin": 150,
    "ms_per_frame": 11,
    "num_of_frames": 250
  },
  "point_generation_configs": {
    "num_of_points": 500,
    "separation_radius": 40,
    "max_fails": 10000,
    "border_configs": {
      "top": false,
      "bottom": false,
      "left": false,
      "right": false,
      "separation": 50
    }
  },
  "point_movement_configs": {
    "x_movers": [
      {
        "type": "Drift",
        "kwargs": {
          "frequency": {
            "type": "Integer",
            "kwargs": {
              "value": 1
            }
          }
        }
      },
      {
        "type": "Sway",
        "kwargs": {
          "amplitude": 60,
          "intensity": 1,
          "x_scale": 0.004,
          "y_scale": 0.01,
          "x_offset": 0,
          "y_offset": 0
        }
      }
    ],
    "y_movers": [
      {
        "type": "Sway",
        "kwargs": {
          "amplitude": 30,
          "intensity": 1,
          "x_scale": 0.004,
          "y_scale": 0.01,
          "x_offset": 100,
          "y_offset": 100
        }
      }
    ],
    "z_movers": [
      {
        "type": "NoiseMap",
        "kwargs": {
          "amplitude": 3,
          "x_scale": 0.004,
          "y_scale": 0.004,
          "x_offset": 0,
          "y_offset": 0
        }
      },
      {
        "type": "Sway",
        "kwargs": {
          "amplitude": 0.5,
          "intensity": 0.005,
          "x_scale": 50,
          "y_scale": 50,
          "x_offset": 100,
          "y_offset": 0
        }
      },
      {
        "type": "Wave",
        "kwargs": {
          "amplitude": 1,
          "speed": -5,
          "wavelength": 5
        }
      }
    ]
  },
  "triangle_coloring": {
    "type": "TriangleDrawer",
    "kwargs": {
      "gradient": {
        "type": "GradientHSV",
        "kwargs": {
          "start_color": {
            "type": "PlainHSV",
            "kwargs": {
              "color": [235, 52, 52]
            }
          },
          "end_color": {
            "type": "PlainHSV",
            "kwargs": {
              "color": [66, 224, 245]
            }
          },
          "range": {
            "type": "Linear",
            "kwargs": {
              "start": {
                "type": "Circle",
                "kwargs": {
                  "start": [150, 150],
                  "center": [833, 534]
                }
              },
              "end": {
                "type": "Circle",
                "kwargs": {
                  "start": [1516, 918],
                  "center": [833, 534]
                }
              },
              "range": {
                "type": "EaseInOut"
              }
            }
          }
        }
      },
      "shader": {
        "type": "AmbientShader",
        "kwargs": {
          "ambient_vector": [1.0, 1.0, 0.5],
          "ambient_gain": 110000,
          "ambient_definition": 11
        }
      }
    }
  }
}
```

- `random_seed` (boolean): Whether or not a random seed should be generated at runtime.
- `seed` (int): The seed to be used to recreate a GIF. This seed will be overwritten if `random_seed` is set to true.
- `gif_configs`
    * `width` (int): The width of the final GIF.
    * `height` (int): The height of the final GIF.
    * `num` (int): The folder where the final GIF will be stored in.
    * `background_color` (int[]): The 0-255 RGB background color.
    * `margin` (int): The maximum distance past the edge of the screen that a point can move to.
    * `ms_per_frame` (int): The number of milliseconds between frames.
    * `num_of_frames` (int): The number of frames in the final GIF.
- `point_generation_configs`
    * `num_of_points` (int): The maximum number of points to be added to the GIF.
    * `separation_radius` (int): The minimum distance away initial points can be from each other.
    * `max_fails` (int): The maximum number of times the code will attempt to place a point before giving up.
    * `border_configs`: Configuration attributes for drawing points on the border of the gif. Helpful for ensuring there are no gaps in the triangular mesh.
        - `top` (boolean): Whether or not the top border should be generated.
        - `bottom` (boolean): Whether or not the bottom border should be generated.
        - `left` (boolean): Whether or not the left border should be generated.
        - `right` (boolean): Whether or not the right border should be generated.
        - `separation` (int): How far apart border points should be.
- `point_movement_configs`:
    * `x_movers` (dict[]): TBD
    * `y_movers` (dict[]): TBD
    * `z_movers` (dict[]): TBD
- `triangle_coloring`: Optional configuration attributes for coloring of the triangles (more detail in section [Triangle Coloring](#triangle-coloring)).
- `line_coloring`: Optional configuration attributes for drawing the lines between points (more detail in section [Line Drawing](#line-drawing)).
- `point_coloring`: Optional configuration attributes for drawing the points (more detail in section [Point Drawing](#point-drawing)).

## Triangle Coloring
TBD

## Line Drawing
TBD

## Point Drawing
TBD

## Contributing

I have tried to make it fairly simple to add options to this project. If you have any ideas for new ways to implement an abstract base class (found in the files named `ABCs.py`) you can suggest them with an issue marked as an `idea` or you can create the functionality by creating a new class which extends one of the following abstract classes in the same folder at `ABCs.py`:

## Future Work

1. The most pressing issue at this point is the amount of time it takes for the triangulation algorithm to run with >100 points. I would like to spend some times looking into new algorithms and potentially add some multiprocessing to significantly reduce the overall runtime of the program.
2. In an attempt to allow for a higher variety of GIFs generated from the project, I have made it fairly tedious to manually write the configurations for a GIF. Because of this, I would like to write up a GUI for this project to simplify this task.
3. Add a more complex shading system to enhance the look of shaded GIFs.
