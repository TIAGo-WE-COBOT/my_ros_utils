# ROS `my_ros_utils` package

Provides utility functions to convert from ROS messages to Python datatypes.
Currently supported conversions:

- Image to NumPy array
- CompressedImage to NumPy array (for `compressed` topics)
- CompressedImage to NumPy array (for `compressedDepth` topics)
- PointCloud2 to NumPy arrays and NumPy arrays to Open3D PointCloud
- Open3D PointCloud to NumPy arrays and NumPy arrays to PointCloud2.

# Requirements

Listed in the `requirements.txt` file. Use `pip install -r requirements.txt` to (hopefully) install all the dependencies

- OpenCV
- Open3d
- [`ros_numpy`](https://github.com/eric-wieser/ros_numpy) package

# Use

The [documentation](https://tiago-we-cobot.github.io/my_ros_utils/) of the `my_ros_utils` module is provided via GitHub Pages. The source files are also available in the `docs` folder.

## Import

Import in your script using 

```
from my_ros_utils import image_conversion
from my_ros_utils import cloud_conversion
```

## Demo
After having sourced the environment and connected to the robot (or to its simulation), run the node implementing a demo usage of each submodule. 

### Images

```
rosrun my_ros_utils image_conversion.py
```

### Pointcloud

```
rosrun my_ros_utils cloud_converter.py
```

# Documentation

Full documentation of the package is available [here](https://tiago-we-cobot.github.io/my_ros_utils/).

To (re-)build the package documentation (e.g. if changing the docstrings, or adding new methods/submodules): 
0. Install [pdoc3](https://pdoc3.github.io/pdoc/) with 
```
pip3 install pdoc3 
```
1. Browse to the root folder of the package (e.g. with `cd ~/tiago_public_ws/src/my_ros_utils`).
2. Overwrite the existing documentation by running
```
pdoc --html --force --output-dir docs src/my_ros_utils
```
3. Move the `.html` files one folder up (i.e. in `docs/`)
```
cp -r docs/my_ros_utils/. docs
```
4. Optional. Remove the `docs/my_ros_utils` folder
```
rm -r docs/my_ros_utils/
```
