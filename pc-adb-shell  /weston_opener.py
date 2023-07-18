# PC cmd: 
# To create weston terminal: after installing adb - platform-tools file inside the c folder

export SNPE_TARGET_ARCH=aarch64-ubuntu-gcc7.5
export LD_LIBRARY_PATH=/data/local/tmp/snpeexample/$SNPE_TARGET_ARCH/lib
export PATH=$PATH:/data/local/tmp/snpeexample/$SNPE_TARGET_ARCH/bin
export ADSP_LIBRARY_PATH="/data/local/tmp/snpeexample/dsp/lib;/system/lib/rfsa/adsp;/system/vendor/lib/rfsa/adsp;/dsp"
 
export XDG_RUNTIME_DIR="/usr/bin/weston_socket"
mkdir -p $XDG_RUNTIME_DIR
chmod 0700 $XDG_RUNTIME_DIR
/usr/bin/weston --tty=1 --connector=29 &


# in weston monitor: streaming
gst-launch-1.0 qtiqmmfsrc ! video/x-raw\(memory:GBM\), format=NV12, width=1280, height=720, framerate=30/1 ! queue ! qtimlesnpe config=/data/misc/camera/yolo/mle_snpeyolov5m_quant_hta.config  postprocessing=yolov5detection !  queue ! qtioverlay bbox-color=0xFF0000FF ! waylandsink  width=1920 height=1080 async=true sync=false enable-last-sample=false

# in weston monitor: from video file crack-detection:
gst-launch-1.0 filesrc location=/root/crackvideos/crackvideos/YUN_0001.MP4 ! decodebin ! qtimlesnpe config=/data/misc/camera/yolo/mle_snpeyolov5m_quant_hta.config postprocessing=yolov5detection ! videoconvert ! qtioverlay bbox-color=0xFF0000FF ! waylandsink width=1920 height=1080 async=true sync=false enable-last-sample=false
