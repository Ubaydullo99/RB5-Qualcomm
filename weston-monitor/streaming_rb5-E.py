# RB5 weston terminal:

# in monitor: from z90x drone camera 
gst-launch-1.0 rtspsrc location=rtsp://223.171.57.239:554/live ! decodebin ! videoconvert ! qtimlesnpe config=/data/misc/camera/yolo/mle_snpeyolov5m_quant_hta.config postprocessing=yolov5detection ! qtioverlay bbox-color=0xFF0000FF ! videoconvert ! waylandsink width=1920 height=1080 async=true sync=false enable-last-sample=false
# When you run this command, GStreamer constructs a pipeline with the specified elements and configurations. It captures video frames from the QMMF source, applies a neural network inference using the SNPE plugin, performs post-processing for object detection, adds bounding box overlays, and displays the processed video on the screen using Wayland.

# gst-launch-1.0: This command launches the GStreamer command-line tool, version 1.0, which is a framework for constructing multimedia pipelines in Unix-like systems.
## qtiqmmfsrc: This is a GStreamer element used to capture video frames from Qualcomm's QMMF (Qualcomm Multimedia Framework) source. It represents the video source for the pipeline.
# !: The exclamation mark symbol is used in GStreamer pipelines to separate elements and connect them together.
# video/x-raw(memory:GBM): This is the format specifier for the input video frames in the pipeline. It indicates that the frames are in raw video format, stored in a GBM (Generic Buffer Manager) memory buffer.
## format=NV12: This specifies the pixel format of the video frames as NV12, which is a common YUV format used in video encoding and decoding.
## framerate=30/1: This sets the framerate of the video to 30 frames per second.
# queue: This element is used to introduce buffering between elements in the pipeline. It helps smooth out any variations in data flow and prevents blocking.
# qtimlesnpe: This element represents the QTI (Qualcomm Technologies, Inc.) MLE (Machine Learning Extension) SNPE (Snapdragon Neural Processing Engine) plugin. It is responsible for executing neural network inference using the SNPE framework.
## config=/data/misc/camera/yolo/mle_snpeyolov5m_quant_hta.config: This specifies the path to the configuration file used by the QTI MLE SNPE plugin. The configuration file contains settings and parameters for the neural network model.
## postprocessing=yolov5detection: This enables post-processing of the SNPE output. In this case, it performs object detection using the YOLOv5 algorithm.
# qtioverlay: This element adds an overlay to the video frames, such as bounding boxes around detected objects.
## bbox-color=0xFF0000FF: This sets the color of the bounding boxes to blue (0xFF0000FF in RGBA format).
# waylandsink: This element is used to display the video frames using the Wayland display protocol. It renders the frames on the screen.
## async=true: This enables asynchronous processing in the pipeline, allowing elements to operate independently.
## sync=false: This disables synchronization between the different elements in the pipeline.
## enable-last-sample=false: This disables the saving of the last sample processed by the pipeline.



# in weston monitor: from video file crack-detection:
gst-launch-1.0 filesrc location=/root/crackvideos/crackvideos/YUN_0001.MP4 ! decodebin ! videoconvert ! qtimlesnpe config=/data/misc/camera/yolo/mle_snpeyolov5m_quant_hta.config postprocessing=yolov5detection ! qtioverlay bbox-color=0xFF0000FF ! waylandsink width=1920 height=1080 async=true sync=false enable-last-sample=false
# When you run this command, GStreamer constructs a pipeline with the specified elements and configurations. It reads the video data from the file YUN_0001.MP4, decodes the video stream, converts the frames to a compatible format, performs neural network inference using the SNPE plugin with YOLOv5 post-processing for object detection, adds bounding box overlays, and displays the processed video on the screen using Wayland.

# filesrc location=/root/crackvideos/crackvideos/YUN_0001.MP4: This is a GStreamer element used to read video data from a file. It specifies the location of the input video file to be processed. In this case, the file is located at /root/crackvideos/crackvideos/YUN_0001.MP4
# decodebin: This element automatically selects the appropriate decoder for the input video file. It dynamically detects and decodes the video stream.
# videoconvert: This element converts the video frames to a format compatible with the subsequent elements in the pipeline. It ensures that the video frames are in a standard format for further processing.



# in monitor: from z90x drone camera 
gst-launch-1.0 rtspsrc location=rtsp://223.171.57.239:554/live ! decodebin ! videoconvert ! qtimlesnpe config=/data/misc/camera/yolo/mle_snpeyolov5m_quant_hta.config postprocessing=yolov5detection ! qtioverlay bbox-color=0xFF0000FF ! videoconvert ! queue ! waylandsink width=1920 height=1080 sync=true enable-last-sample=false
# When you run this command, GStreamer constructs a pipeline with the specified elements and configurations. It receives the video stream from the RTSP source, decodes the video stream, converts the frames to a compatible format, performs neural network inference using the SNPE plugin with YOLOv5 post-processing for object detection, adds bounding box overlays, converts the frames to a format compatible with Wayland, and displays the processed video on the screen using Wayland.

# rtspsrc location=rtsp://223.171.57.239:554/live: This is a GStreamer element used to receive video data from an RTSP (Real-Time Streaming Protocol) source. It specifies the location of the RTSP stream to be captured. In this case, the RTSP stream is located at rtsp://223.171.57.239:554/live.

