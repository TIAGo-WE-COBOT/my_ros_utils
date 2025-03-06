import os
import subprocess
import wave

import cv2

import rosbag
from cv_bridge import CvBridge

from audio_common_msgs.msg import AudioData, AudioDataStamped
from sensor_msgs.msg import Image, CompressedImage

def parse_audio_format(format_str):
    """
    Parse an audio format string (e.g., S16LE) and return:
    - sample width (in bytes)
    - byteorder ('little' or 'big')
    - range of values (min, max)

    Args:
        format_str (str): Audio format string. Must start with 'S' or 'U' to indicate signed or unsigned format, respectively. The format string should also include the sample width in bits (e.g., 'S16LE' for signed 16-bit little-endian).
    Return:
        dict: A dictionary containing the sample width, byteorder, and range of values (min, max).
    """
    # Determine if the format is signed or unsigned
    if format_str.startswith('S'):
        is_signed = True
    elif format_str.startswith('U'):
        is_signed = False
    else:
        raise ValueError(f"Invalid format string: {format_str}. Must start with 'S' or 'U'.")

    # Extract the sample width (in bits)
    sample_width_bits = int(''.join(filter(str.isdigit, format_str)))
    sample_width_bytes = sample_width_bits // 8  # Convert bits to bytes

    # Determine byteorder
    if 'LE' in format_str:
        byteorder = 'little'
    elif 'BE' in format_str:
        byteorder = 'big'
    else:
        byteorder = 'little'  # Default to little endian if not specified

    # Calculate the range of values
    if is_signed:
        min_value = -(2 ** (sample_width_bits - 1))
        max_value = (2 ** (sample_width_bits - 1)) - 1
    else:
        min_value = 0
        max_value = (2 ** sample_width_bits) - 1

    return {
        'sample_width': sample_width_bytes,
        'byteorder': byteorder,
        'range': (min_value, max_value)
    }


def bag2video(bag_file, image_topic, output_dir=None):
    """Reads a ROS1 bag file and extracts the images from a given image topic.
    Adapted from [munzz11 on GitHub Gist](https://gist.github.com/munzz11/1131f18b4134094a70db4e451040e08f).

    Args:
        bag_file (str): Path to the bag file.
        image_topic (str): Name of the image topic to extract from the bag. The messages published on this topic must be of type `sensor_msgs/Image` or `sensor_msgs/CompressedImage`.
        output_dir (str, optional): Destination directory for output files. If set to `None`, the output file will be saved in the same directory of the input bag. Defaults to `None`.
    """
    # Define the output filepaths
    if output_dir is None:
        output_dir = os.path.dirname(bag_file)
    output_video = os.path.join(output_dir, 
                                os.path.basename(bag_file).replace('.bag', 
                                                                   '.mp4'))
    
    # Open and inspect the bag file
    bag = rosbag.Bag(bag_file, 'r')
    topics_dict = bag.get_type_and_topic_info().topics

    # Create the CV bridge to convert ROS messages to OpenCV images
    bridge = CvBridge()

    # Define the codec and video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_frame_rate = topics_dict[image_topic].frequency
    video_frame_size = None  # Will be determined from the first frame
    video_writer = None

    for topic, msg, t in bag.read_messages(topics=[image_topic]):
        # Convert the ROS image message to OpenCV image
        if msg._type == Image._type:
            frame = bridge.imgmsg_to_cv2(msg, "bgr8")
        elif msg._type == CompressedImage._type:
            frame = bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
        else:
            raise ValueError("Invalid image message type. Supported types are `Image` and `CompressedImage`.")
        
        # Initialize the video writer on first non-empty frame
        if video_frame_size is None:
            video_frame_size = (frame.shape[1], frame.shape[0])
            video_writer = cv2.VideoWriter(output_video, 
                                            fourcc,
                                            video_frame_rate, video_frame_size
                                            )

        video_writer.write(frame)
        
    bag.close()
    
    if video_writer is not None:
        video_writer.release()
        print(f"Video saved as {output_video}")


def bag2audio(bag_file, audio_topic, audio_info_topic=None, output_dir=None):
    """Reads a ROS1 bag file and extracts the audio from a given audio topic.

    Args:
        bag_file (str): Path to the bag file.
        audio_topic (str): Name of the audio topic to extract from the bag. The messages published on this topic must be of type `audio_common_msgs/AudioData` or `audio_common_msgs/AudioDataStamped`.
        audio_info_topic (str, optional): Name of the topic to extract info on audio stream. The messages published on this topic must be of type `audio_common_msgs/AudioInfo`. If not specified, default values in `audio_common/audio_capture/launch/capture_wave.launch` are used. Defaults to None.
        output_dir (str, optional): Destination directory for output files. If set to `None`, the output file will be saved in the same directory of the input bag. Defaults to `None`.
    """
    # Open and inspect the bag file
    bag = rosbag.Bag(bag_file, 'r')

    # Get info on the audio stream
    is_audio_info_msg_received = False
    if audio_info_topic:
        for topic, msg, t in bag.read_messages(topics=[audio_info_topic]):
            channels = msg.channels
            sample_rate = msg.sample_rate
            sample_format = msg.sample_format
            coding_format = msg.coding_format
            is_audio_info_msg_received = True
            break # only read the first message
    if not is_audio_info_msg_received: 
        # If the bag does not provide AudioInfo messages, revert to default values of `audio_common/audio_capture/launch/capture_wave.launch`.
        # See: https://github.com/ros-drivers/audio_common
        channels=1
        sample_rate=16000
        sample_format="S16LE"
        coding_format="wav"
    sample_format_dict = parse_audio_format(sample_format)
    #byteorder = sample_format_dict['byteorder']
    sample_width = sample_format_dict['sample_width']

    # Check if the requested coding format is supported
    ALLOWED_CODING_FMT = ["wav", "mp3"]
    if coding_format in ALLOWED_CODING_FMT:
        fext = '.' + coding_format
    else:
        raise ValueError("Invalid coding format. Supported formats are {}".format(ALLOWED_CODING_FMT))
    # Define the output filepaths
    if output_dir is None:
        output_dir = os.path.dirname(bag_file)
    output_audio = os.path.join(output_dir, 
                                os.path.basename(bag_file).replace('.bag', 
                                                                   fext))
    
    # Initialize audio data buffer
    audio_data = []

    for topic, msg, t in bag.read_messages(topics=[audio_topic]):
        if msg._type == AudioData._type:
            audio_msg_data = msg.data
        elif msg._type == AudioDataStamped._type:
            audio_msg_data = msg.audio.data
        else:
            raise ValueError("Invalid audio message type. Supported types are `AudioData` and `AudioDataStamped`.")
        audio_data.extend(audio_msg_data)
    
    if audio_data: # if valid audio data is received
        with wave.open(output_audio, "w") as f:
            f.setnchannels(channels)
            f.setframerate(sample_rate)
            f.setsampwidth(sample_width)
            f.writeframes(bytes(audio_data))
            print(f"Audio saved as {output_audio}")


def combine_video_audio(video_file, audio_file, output_file=None):
    """Combine video and audio files into a single MP4 file.

    Args:
        video_file (str): Path to the video file.
        audio_file (str): Path to the audio file.
        output_file (str, optional): Output video file. If set to `None`, the output file will be saved in the same directory of the input video file. Defaults to None.
    """
    if output_file:
        output_dir = os.path.dirname(output_file)
        output_filename = os.path.basename(output_file)
    else:
        output_dir = os.path.dirname(video_file)
        output_filename = os.path.basename(video_file).replace('.mp4', 
                                                               '_with_audio.mp4')
    output_file = os.path.join(output_dir, output_filename)
    command = [
        'ffmpeg', '-i', video_file, '-i', audio_file,
        '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_file
    ]
    subprocess.run(command, 
                   stdout=subprocess.DEVNULL, 
                   stderr=subprocess.STDOUT
                   )
    print(f"Video merged with audio at {output_file}")