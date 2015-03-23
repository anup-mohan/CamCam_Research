########################################################################################################################
# Script to calculate and save the frame rate, CPU and Memory utilization of a given camera.
# The streams from the camera will be analyzed for a minute and average fps and cpu/mem utilization will be computed
# The script will call the bash script get_cpu_mem_util.sh to calculate the cpu/mem utilization
# The results would be saved in "ip_address_of_camera".txt file
# Change the path of the result file according to the system being used
########################################################################################################################

import urllib
import sys
import time
import subprocess
import os
import signal

# Timeout for single image
DOWNLOAD_IMAGE_TIMEOUT = 10

# Timeout for a minute of download
DOWNLOAD_IMAGE_TIMEOUT2 = 70

# Duration of stream
STREAM_TIME = 60


def timeout_handler(signum, frame):
    """ This function handles the timeout for downloading an image.
        """
    raise Exception()

# register the timout handler
signal.signal(signal.SIGALRM, timeout_handler)

def get_MJPEG_stream(ip_addr,trial):

    # File to save the results
    filename = ip_addr + ".txt"
    resfile = open(filename, "a")

    # Reset Error Flag
    error_flag = 0

    # Flag to see if stream_mjpeg opened succesfully
    flag_stream_mjpeg = 0

    # index for video frame
    cnt = 0

    # Start the download timer
    signal.alarm(DOWNLOAD_IMAGE_TIMEOUT)

    try:
        # the url of the MJPEG stream"
        stream_mjpeg = urllib.urlopen("http://" + ip_addr + "/axis-cgi/mjpg/video.cgi")
        flag_stream_mjpeg = 1

    except (ValueError, IOError, Exception):
        print("Error at 1 in IP: %s" % ip_addr)
        flag_stream_mjpeg = 0
        signal.alarm(0)


    # Reset the timer
    signal.alarm(0)

    # Timeout value to be 60 seconds
    timeout = time.time() + STREAM_TIME

    # Start the download timer
    signal.alarm(DOWNLOAD_IMAGE_TIMEOUT2)

    try:
        # Stream data for 60 seconds
        while time.time() < timeout:
            if stream_mjpeg.readline().startswith("--myboundary"):
                # The second line is useless
                stream_mjpeg.readline()

                try:
                    # Get frame size
                    img_size = int(stream_mjpeg.readline().lstrip("Content-Length: "))
                    # Read in the empty line and binary image data
                    data = stream_mjpeg.read(img_size + 2)

                # f = open(name+repr(cnt)+".jpg","wb")
                # Empty line takes 2 bytes(<CR> <LF>),thus start to record from byte 3
                # f.write(data[2:])
                # f.close()

                except (ValueError, IOError, Exception):
                    print("Error at 2 in IP: %s" % ip_addr)
                    error_flag = 1
                    break

                cnt += 1

    except (ValueError, IOError, Exception):
        print("Error at 3 in IP at pt3: %s" % ip_addr)
        error_flag = 1

    # Reset the timer
    signal.alarm(0)

    if error_flag == 0:
        # fps = no:of frames/time(seconds)
        fps = cnt / float(STREAM_TIME)

        # To prevent Divide by Zero Error
        if cnt == 0:
            cnt = 1

        # Save FPS information
        resfile.write("trial: %s fps: %f" % (trial, fps))
        resfile.write("\n")

    # Close the MJPEG stream
    if flag_stream_mjpeg:
        stream_mjpeg.close()

    # Close the file
    resfile.close()


if __name__ == '__main__':

    # Get IP of the camera
    ip_addr = sys.argv[1]
    # Get trial number
    trial = sys.argv[2]

    get_MJPEG_stream(ip_addr,trial)