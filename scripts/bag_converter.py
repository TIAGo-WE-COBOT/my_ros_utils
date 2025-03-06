import os
import argparse
import glob

from my_ros_utils.bag_conversion import bag2video, bag2audio, combine_video_audio

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert ROS1 bag image topic to MP4 video")
    parser.add_argument("bag_files", 
                        nargs="+", # multiple arguments 
                        help="Paths to the ROS1 bag files (supports wildcards like *.bag)")
    parser.add_argument("-i", "--image_topic",
                        nargs="?",  # 0 or 1 arguments
                        const=None,
                        help="Image or CompressedImage topic to extract from the bag file")
    parser.add_argument("-a", "--audio_topic",
                        nargs="?",  # 0 or 1 arguments
                        const=None,
                        help="AudioData or AudioDataStamped topic to extract from the bag file")
    parser.add_argument("--audio_info_topic",
                        nargs="?",  # 0 or 1 arguments
                        const=None,
                        help="AudioInfo topic to get the audio info from the bag file")
    parser.add_argument("-o", "--output_dir",
                        nargs="?",  # 0 or 1 arguments
                        const=None,
                        help="Directory to save the output MP4 videos (and MP3 audio, if audio is processed)")
    parser.add_argument("-m", "--merge",
                        action="store_true",
                        help="Merge the audio and video files into a single MP4 file")
    parser.add_argument("-c", "--clean",
                        action="store_true",
                        help="Delete the intermediate video and audio files after merging")
    args = parser.parse_args()
    for i, bag_file in enumerate(args.bag_files):
        print("Processing file {}/{}".format(i+1, len(args.bag_files)))
        bag_paths = glob.glob(bag_file)
        for path in bag_paths:
            bag_filename = os.path.basename(path)
            bag_dir = os.path.dirname(path)
            output_dir = args.output_dir if args.output_dir else bag_dir
            if args.image_topic:
                # Process the bag file to create a video from images
                bag2video(path, 
                        image_topic=args.image_topic,
                        output_dir=output_dir)
            else:
                args.merge = False  # if no video topic is provided,
                                    # there is nothing to merge
            if args.audio_topic:
                # Process the bag file to create audio from audio chuncks
                bag2audio(path,
                          audio_topic=args.audio_topic,
                          audio_info_topic=args.audio_info_topic,
                          output_dir=output_dir)
            else:
                args.merge = False  # if no audio topic is provided, 
                                    # there is nothing to merge    
            if args.merge:
                # Merge the video and audio files
                combine_video_audio(os.path.join(output_dir, 
                                                 bag_filename.replace('.bag', 
                                                                      '.mp4')),
                                    os.path.join(output_dir,   
                                                bag_filename.replace('.bag', 
                                                                     '.wav')),
                                    )
            else:
                args.clean = False  # if no merge is done, 
                                    # there is audio and/or video are 
                                    # the final output of the script
            if args.clean:
                # Remove intermediate video and audio files
                try:
                    os.remove(os.path.join(output_dir, 
                                        bag_filename.replace('.bag', 
                                                             '.mp4')))
                except:
                    pass
                try:
                    os.remove(os.path.join(output_dir, 
                                        bag_filename.replace('.bag', 
                                                             '.wav')))
                except:
                    pass
