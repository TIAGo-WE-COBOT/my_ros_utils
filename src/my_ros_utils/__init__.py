"""A set of utility functions to convert back and forth ROS messages related to the vision stack, and handy Python datatypes.
    
    * `image_conversion.py`: A set of conversion tools to convert images from the ROS message format to an OpenCV-compatible format. The module relies on NumPy.
    * `cloud_conversions.py`: A set of conversion tools to convert point clouds from the ROS message format to the Open3D format. The module relies on `ros_numpy`, and also the intermediate conversions (from/to ROS or Open3D to/from NumPy) are made available as public methods.
    * `bag_conversion.py`: A set of conversion tools to convert audio and video streams from ROS message bags. The tools allow to convert image stream to `.mp4` video, and audio stream to `.mp3` or `.wav` file. Video and audio can be converted into separated files or merged into a single `.mp4` file. The module relies on OpenCV and the `cv_bridge` package.
"""