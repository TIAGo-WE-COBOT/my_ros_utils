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
* Install [pdoc3](https://pdoc3.github.io/pdoc/) with 
```
pip3 install pdoc3 
```
* Run the [`update_doc.sh`](./docs/update_doc.sh) script in the `docs/` folder with
```
. <path_to_ws>/src/my_ros_utils/docs/update_docs.sh
```
