# Dynamic Background
> Generates seamless gifs of triangle meshes.



## Installation

*`Python3.10` and `pipenv` required*

Install Python dependencies with
```
pipenv install
```
in the root directory of the project.

Third Party Dependencies:
- [ImageMagick](https://imagemagick.org/script/download.php)

## Notes on Usage

The only file which needs to be modified in order to customize the gifs is `config.json`. However, if the file structure is changed there will be some issues in the source code (either `src/main.py` or `src/configs.py` depending on what is moved).

## Contributing

I have tried to make it fairly simple to add options to this project. If you have any ideas for new ways to implement an abstract base class (found in the files named `ABCs.py`) you can suggest them with an issue marked as an `idea` or you can create the functionality by creating a new class which extends one of the following abstract classes in the same folder at `ABCs.py`:

## Future Work

1. The most pressing issue at this point is the amount of time it takes for the triangulation algorithm to run with >100 points. I would like to spend some times looking into new algorithms and potentially add some multiprocessing to significantly reduce the overall runtime of the program.
2. In an attempt to allow for a higher variety of GIFs generated from the project, I have made it fairly tedious to manually write the configurations for a GIF. Because of this, I would like to write up a GUI for this project to simplify this task.
3. Add a more complex shading system to enhance the look of shaded GIFs.
