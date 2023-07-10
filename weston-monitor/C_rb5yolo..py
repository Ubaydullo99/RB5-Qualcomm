#  For starting Weston:   

export SNPE_TARGET_ARCH=aarch64-ubuntu-gcc7.5 
&& export LD_LIBRARY_PATH=/data/local/tmp/snpeexample/$SNPE_TARGET_ARCH/lib 
&& export PATH=$PATH:/data/local/tmp/snpeexample/$SNPE_TARGET_ARCH/bin && export ADSP_LIBRARY_PATH="/data/local/tmp/snpeexample/dsp/lib;/system/lib/rfsa/adsp;/system/vendor/lib/rfsa/adsp;/dsp"


export XDG_RUNTIME_DIR="/usr/bin/weston_socket"
mkdir -p $XDG_RUNTIME_DIR
chmod 0700 $XDG_RUNTIME_DIR
/usr/bin/weston --tty=1 --connector=29 &


# or :
./start_weston.sh       # (only on 1 rb5)


# in monitor: from rb5 camera 
gst-launch-1.0 qtiqmmfsrc ! video/x-raw\(memory:GBM\), format=NV12, width=1280, height=720, framerate=30/1 ! queue ! qtimlesnpe config=/data/misc/camera/yolo/mle_snpeyolov5m_quant_hta.config  postprocessing=yolov5detection !  queue ! qtioverlay bbox-color=0xFF0000FF ! waylandsink  width=1920 height=1080 async=true sync=false enable-last-sample=false


# in monitor: from usb video file crack-detection:
gst-launch-1.0 filesrc location=/root/crackvideos/crackvideos/YUN_0001.MP4 ! decodebin ! videoconvert ! qtimlesnpe config=/data/misc/camera/yolo/mle_snpeyolov5m_quant_hta.config postprocessing=yolov5detection ! qtioverlay bbox-color=0xFF0000FF ! videoconvert ! waylandsink width=1920 height=1080 async=true sync=false enable-last-sample=false


# in monitor: from z90x drone camera 
gst-launch-1.0 rtspsrc location=rtsp://223.171.57.239:554/live ! decodebin ! videoconvert ! qtimlesnpe config=/data/misc/camera/yolo/mle_snpeyolov5m_quant_hta.config postprocessing=yolov5detection ! qtioverlay bbox-color=0xFF0000FF ! videoconvert ! waylandsink width=1920 height=1080 async=true sync=false enable-last-sample=false






# VLC access (video, rb5 camera streaming, drone camera streaming)

# rb5 video file: 

# in monitor: 
gst-launch-1.0 filesrc location=/data/misc/camera/yolo/crack_video.mp4 ! qtdemux name=demux demux. ! queue ! h264parse ! qtivdec ! video/x-raw\(memory:GBM\)! qtimlesnpe config=/data/misc/camera/yolo/mle_snpeyolov5m_quant_hta.config  postprocessing=yolov5detection !  queue ! qtioverlay bbox-color=0x00FFFFFF ! queue ! omxh264enc periodicity-idr=1 interval-intraframes=8 target-bitrate=750000 control-rate=2 ! queue ! h264parse config-interval=-1 ! rtph264pay pt=96 ! udpsink host=127.0.0.1 port=8554

# pc: 
adb forward tcp:8554 tcp:8554
adb root
adb shell

gst-rtsp-server -p 8554 -m /live "( udpsrc name=pay0 port=8554 caps=\"application/x-rtp,media=video,clock-rate=90000,encoding-name=H264,payload=96\" )"

# vlc: 
rtsp://127.0.0.1:8554/live



# rb5 drone camera 
# in monitor: 
gst-launch-1.0 rtspsrc location=rtsp://223.171.57.239:554/live ! decodebin ! videoconvert ! queue ! qtimlesnpe config=/data/misc/camera/yolo/mle_snpeyolov5m_quant_hta.config postprocessing=yolov5detection ! videoconvert ! x264enc tune=zerolatency speed-preset=veryfast key-int-max=30 bitrate=2000 ! video/x-h264, profile=baseline ! h264parse ! matroskamux ! tcpserversink host=0.0.0.0 port=8900

# pc: 
adb forward tcp:8900 tcp:8900
adb root

# vlc: 
tcp://192.168.0.3:8900





