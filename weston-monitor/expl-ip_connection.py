# VLC access (video, rb5 camera streaming, drone camera streaming)
           
                # rb5 video file: 
# in a monitor: 
gst-launch-1.0 filesrc location=/data/misc/camera/yolo/crack_video.mp4 ! qtdemux name=demux demux. ! queue ! h264parse ! qtivdec ! video/x-raw\(memory:GBM\)! qtimlesnpe config=/data/misc/camera/yolo/mle_snpeyolov5m_quant_hta.config  postprocessing=yolov5detection !  queue ! qtioverlay bbox-color=0x00FFFFFF ! queue ! omxh264enc periodicity-idr=1 interval-intraframes=8 target-bitrate=750000 control-rate=2 ! queue ! h264parse config-interval=-1 ! rtph264pay pt=96 ! udpsink host=127.0.0.1 port=8554

# Overall, this pipeline reads a video file, performs YOLOv5 object detection on the video frames, overlays bounding boxes on the detected objects, encodes the video stream using H.264, and streams the encoded video over UDP.

# qtdemux name=demux: The qtdemux element demultiplexes the input multimedia file, separating the audio and video streams.
# demux. ! queue ! h264parse ! qtivdec ! video/x-raw(memory:GBM): This section processes the video stream. It includes a queue element to manage the data flow, h264parse for parsing H.264 video streams, and qtivdec for decoding the video stream. The resulting video is in GBM memory format.
# qtimlesnpe config=/data/misc/camera/yolo/mle_snpeyolov5m_quant_hta.config postprocessing=yolov5detection: This part uses the qtimlesnpe element to perform inference on the video frames using a YOLOv5 model. It takes a configuration file and applies postprocessing for object detection using YOLOv5.
# queue ! qtioverlay bbox-color=0x00FFFFFF: After the inference, this section adds an overlay on the video frames with bounding boxes around the detected objects. The overlay's bounding box color is set to white.
# queue ! omxh264enc periodicity-idr=1 interval-intraframes=8 target-bitrate=750000 control-rate=2: This part encodes the video frames using the omxh264enc element with specific encoding parameters such as periodic IDR (Instantaneous Decoder Refresh) frames, interval between intra frames, target bitrate, and control rate.
# queue ! h264parse config-interval=-1: The encoded H.264 video stream is then parsed using h264parse, which sets the config interval to -1, indicating that the configuration data is included in every keyframe.
# rtph264pay pt=96: The h264 video stream is packed into RTP packets for transmission over the network. The payload type (pt) is set to 96.
# udpsink host=127.0.0.1 port=8554: The RTP packets are sent over UDP to the specified destination IP address (127.0.0.1) and port number (8554).

# pc: 
adb forward tcp:8554 tcp:8554
# adb forward tcp:8554 tcp:8554: This command forwards the TCP port 8554 on your Android device to the same port on your local machine. This allows the RTSP server running on the Android device to be accessible from your computer.
adb root
# adb root: This command requests temporary access to your Android device. It is necessary to run some commands with elevated privileges.
adb shell


gst-rtsp-server -p 8554 -m /live "( udpsrc name=pay0 port=8554 caps=\"application/x-rtp,media=video,clock-rate=90000,encoding-name=H264,payload=96\" )"
# The combination of the UDP source (udpsrc) element and the specified caps provides the input for the RTSP server. It receives RTP packets over UDP on port 8554 and provides the video stream through the RTSP server.

# gst-rtsp-server: RTSP (Real-Time Streaming Protocol) server using GStreamer's gst-rtsp-server tool and stream video over RTSP. This command starts the gst-rtsp-server tool on the Android device, which sets up the RTSP server.
# -p 8554: Specifies the port number for the RTSP server to listen on. In this case, it is set to 8554. By combining the -p and -m options, the RTSP server will listen on the specified port (8554 in this case) and make the video stream available at the /live path
# -m /live: Sets the mount point for the RTSP stream. In this case, the stream is available at the /live path.
# "(...) ": This section specifies the pipeline elements that handle the source of the RTSP stream. It uses GStreamer's pipeline syntax.
## udpsrc name=pay0: This is the source element responsible for receiving the RTP packets over UDP. It listens on a specific port (port=8554 in this case) for incoming RTP packets.
# caps="...": This parameter sets the capabilities (caps) of the incoming RTP stream. It describes the properties and characteristics of the video stream. Here's a breakdown of the caps specified:
## application/x-rtp: This specifies the RTP protocol used for streaming.
## media=video: Indicates that the stream is a video stream.
## clock-rate=90000: Specifies the video stream's clock rate, typically 90,000 Hz for most video codecs.
## encoding-name=H264: Indicates that the video stream is encoded using the H.264 codec.
## payload=96: Specifies the payload type identifier for the H.264 video packets. This is necessary for correct interpretation and decoding of the video stream.

# vlc: 
rtsp://127.0.0.1:8554/live

# Clients can connect to the RTSP server using a URL like rtsp://<server_ip>:8554/live and request the video stream. The server will then transmit the video stream to the clients over RTSP.



              # drone camera streaming
# rb5 drone camera 
# in a monitor: (output is 50 seconds delay and video stopping and lags)
gst-launch-1.0 rtspsrc location=rtsp://223.171.57.239:554/live ! decodebin ! videoconvert ! queue ! qtimlesnpe config=/data/misc/camera/yolo/mle_snpeyolov5m_quant_hta.config postprocessing=yolov5detection ! videoconvert ! x264enc tune=zerolatency speed-preset=veryfast key-int-max=30 bitrate=2000 ! video/x-h264, profile=baseline ! h264parse ! matroskamux ! tcpserversink host=0.0.0.0 port=8900
# The pipeline takes the RTSP stream as input, decodes it, performs object detection using YOLOv5, encodes it with x264, and finally serves the processed video over TCP using the Matroska container format.

# gst-launch-1.0: This command starts the GStreamer pipeline.
## rtspsrc location=rtsp://223.171.57.239:554/live: The rtspsrc element is used to receive an RTSP stream. It connects to the given RTSP URL (rtsp://223.171.57.239:554/live in this case) to fetch the stream.
# decodebin: This element dynamically selects the appropriate decoder based on the input stream's format and decodes the compressed video stream.
# videoconvert: This element converts the video format, ensuring compatibility with downstream elements.
# qtimlesnpe config=/data/misc/camera/yolo/mle_snpeyolov5m_quant_hta.config postprocessing=yolov5detection: This section performs inference on the video frames using a YOLOv5 model using the qtimlesnpe element. It takes a configuration file (/data/misc/camera/yolo/mle_snpeyolov5m_quant_hta.config) and applies post-processing for object detection using YOLOv5.
# videoconvert: Another videoconvert element ensures format compatibility for the following elements.
# x264enc tune=zerolatency speed-preset=veryfast key-int-max=30 bitrate=2000: This section encodes the video stream using the x264 encoder. It specifies the tune parameter as zerolatency for low-latency encoding, sets the speed-preset to veryfast for fast encoding, key-int-max to 30 to limit the maximum interval between keyframes, and bitrate to 2000 (kbps) for the target bitrate.
# video/x-h264, profile=baseline: This element sets the video format as H.264 with the baseline profile.
# h264parse: This element parses the encoded H.264 stream.
# matroskamux: This element is responsible for multiplexing the parsed H.264 video stream into the Matroska container format.
# tcpserversink host=0.0.0.0 port=8900: The tcpserversink element sets up a TCP server that listens on all network interfaces (0.0.0.0) and the specified port (8900). It serves the processed video stream over TCP to any connected client.

# pc: 
adb forward tcp:8900 tcp:8900
adb root

# Vlc: 
tcp://192.168.0.3:8900


# 2nd method - output video stopping and laggings are fixed and 20-30 delays
gst-launch-1.0 rtspsrc location=rtsp://223.171.57.239:554/live latency=0 ! decodebin ! videoconvert ! qtimlesnpe config=/data/misc/camera/yolo/mle_snpeyolov5m_quant_hta.config postprocessing=yolov5detection ! qtioverlay bbox-color=0xFF0000FF ! videoconvert ! queue max-size-buffers=1 max-size-bytes=0 max-size-time=0 ! x264enc tune=zerolatency bitrate=750 speed-preset=superfast key-int-max=30 ! video/x-h264, profile=baseline ! h264parse config-interval=-1 ! mpegtsmux ! udpsink host=192.168.0.61 port=8900 sync=true enable-last-sample=false
# rtsp://223.171.57.239:554/live - source drone camera ip address , 192.168.0.61 - ip of pc receiving stream with vlc
# Overall, this GStreamer pipeline fetches an RTSP video stream, decodes it, performs object detection using YOLOv5 with AIMET, overlays bounding boxes, encodes the processed video stream using x264, and sends it over UDP to a specified destination.

# queue max-size-buffers=1 max-size-bytes=0 max-size-time=0: This element adds a queue to limit the pipeline's buffering. It sets the maximum size of the queue to 1 buffer, which means it will hold at most one frame in memory.
# x264enc tune=zerolatency bitrate=750 speed-preset=superfast key-int-max=30: This element encodes the video stream using the x264 encoder with specific settings. The tune=zerolatency option optimizes the encoding for low latency, bitrate=750 sets the target bitrate to 750 kbps, speed-preset=superfast selects the encoding speed preset, and key-int-max=30 specifies the maximum number of frames between keyframes.
# video/x-h264, profile=baseline: This sets the output format of the encoded video stream to H.264 with the baseline profile.
# h264parse config-interval=-1: This element inserts SPS (Sequence Parameter Set) and PPS (Picture Parameter Set) headers into the H.264 stream. The config-interval=-1 option indicates that these headers should be inserted whenever necessary.
# mpegtsmux: This element muxes the encoded video stream into an MPEG-TS (Transport Stream) container.
# udpsink host=192.168.0.61 port=8900 sync=true enable-last-sample=false: This element sends the MPEG-TS stream over UDP to a specific host and port. The host parameter specifies the destination IP address, and port specifies the destination port number. The sync=true option enables synchronization, and enable-last-sample=false indicates that the last sample should not be sent

#in pc cmd:
adb forward tcp:8900 tcp:8900
adb root

VLC link:
udp://@:8900

# Reference 
http://jhub.argosdyne.com/cb/wiki/222550

