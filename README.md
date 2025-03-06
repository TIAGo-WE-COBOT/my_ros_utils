# ROS `my_ros_utils` package

Provides utility functions to convert from ROS messages to Python datatypes.
Currently supported conversions, sorted by ROS datatype:

* [`sensor_msgs/Image`](https://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/Image.html) and [`sensor_msgs/CompressedImage`](https://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/CompressedImage.html)
    - `Image` msg to `numpy` array
    - `CompressedImage` msg to `numpy` array (for `compressed` topics)
    - `CompressedImage` msg to `numpy` array (for `compressedDepth` topics)
* [`sensor_msgs/PointCloud2`](https://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/PointCloud2.html)
    - `PointCloud2` msg to `numpy` array and `numpy` array to [`Open3D.geometry.PointCloud`](https://www.open3d.org/docs/release/python_api/open3d.geometry.PointCloud.html)
    - `Open3D.geometry.PointCloud` to `numpy` arrays and `numpy` arrays to  `PointCloud2` msg.
* [ROS bags](https://wiki.ros.org/rosbag)
    - `Image` and `CompressedImage` msg from ROS bag to `mp4` file.
    - `Audio` and `AudioStamped` msg from ROS bag to `mp3` or `wav` file.
    - `mp4` and `mp3`/`wav` files from above processes to `mp4` with audio and video.

# Requirements

Listed in the `requirements.txt` file. Use `pip install -r requirements.txt` to (hopefully) install all the dependencies

- OpenCV
- Open3d
- [`ros_numpy`](https://github.com/eric-wieser/ros_numpy) package


# Documentation

The [documentation](https://tiago-we-cobot.github.io/my_ros_utils/) of the `my_ros_utils` module is provided via GitHub Pages. 

The source files of the documentation are available in the [`docs`](./docs) folder.
To (re-)build the package documentation (e.g. if changing the docstrings, or adding new methods/submodules): 
* Install [pdoc3](https://pdoc3.github.io/pdoc/) with 
```
pip3 install pdoc3 
```
* Run the [`update_doc.sh`](./docs/update_doc.sh) script in the `docs/` folder with
```
. <path_to_ws>/src/my_ros_utils/docs/update_docs.sh
```


## Example usage

Import in your script using 

```
from my_ros_utils import image_conversion
from my_ros_utils import cloud_conversion
from my_ros_utils import bag_conversion
```

Find example usage in the [scripts](scripts/) folder.