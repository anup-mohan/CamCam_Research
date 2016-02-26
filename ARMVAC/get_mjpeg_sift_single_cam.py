########################################################################################################################
# Script to calculate and save the frame rate of a given camera.
# The streams from the camera will be analyzed for 5 minutes and average fps will be computed
# The results would be saved in "ip_address_of_camera".txt file
# The sift extraction code from OpenCV is used to extract SIFT features on each frame
########################################################################################################################

import urllib
import sys
import time
import signal
import cv2
import numpy as np

def timeout_handler(signum, frame):
    """ This function handles the timeout for downloading an image.
        """
    raise Exception()

# register the timeout handler
signal.signal(signal.SIGALRM, timeout_handler)

def get_MJPEG_stream(ip_addr,trial,des_fps,fps_method,STREAM_TIME):
    
    # Timeout for single image
    DOWNLOAD_IMAGE_TIMEOUT = 10

    # Timeout for a minute of download
    DOWNLOAD_IMAGE_TIMEOUT2 = int(STREAM_TIME) + 10

    # File to save the results
    filename = ip_addr + ".txt"
    resfile = open(filename, "a")

    # Image file name prefix
    image_name = "feat_" + str(ip_addr) + "_" + str(trial) + "_"

    # Reset Error Flag
    error_flag = 0

    # Flag to see if stream_mjpeg opened succesfully
    flag_stream_mjpeg = 0

    # index for video frame
    cnt = 0

    # Start the download timer
    signal.alarm(DOWNLOAD_IMAGE_TIMEOUT)
    
    # Desired frame rate through axis command
    if (int(fps_method) == 1):
    	options = "?des_fps="+str(des_fps)
    else:
    	options = ""
    	
    # Total number of frames
    num_frames = int(des_fps) * int(STREAM_TIME)

    try:
        # the url of the MJPEG stream"
        stream_mjpeg = urllib.urlopen("http://" + ip_addr + "/axis-cgi/mjpg/video.cgi"+ options)
        flag_stream_mjpeg = 1

    except (ValueError, IOError, Exception):
        print("Error at 1 in IP: %s" % ip_addr)
        flag_stream_mjpeg = 0
        signal.alarm(0)


    # Reset the timer
    signal.alarm(0)

    # Timeout value set to stream time
    timeout = time.time() + int(STREAM_TIME)

    # Stream data for the specified time
    while time.time() < timeout:
    
        fps_cnt = 0

    	start_time = time.time()

	while time.time() < start_time + 1:

    	    # Stream and analyze data till the required frame rate is achieved or till timeout
    	    if (fps_cnt < int(des_fps)):
		        if stream_mjpeg.readline().startswith("--myboundary"):
		            # The second line is useless
			    stream_mjpeg.readline()

                            img_size = int(stream_mjpeg.readline().lstrip("Content-Length: "))
	                    # Read in the empty line and binary image data
	                    data = stream_mjpeg.read(img_size + 2)
				
	                    img_array = np.asarray(bytearray(data[2:]),dtype=np.uint8)
	                    img = cv2.imdecode(img_array,-1)
	                    gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	                    sift = cv2.SIFT()
	                    kp, des = sift.detectAndCompute(gray,None)
	
	
			    cnt += 1
                            fps_cnt += 1
		
            else:
	                rem_time = 1 - (time.time() - start_time)
                        if (rem_time > 0):
                            time.sleep(rem_time)


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
    # Get Desired FPS
    des_fps = sys.argv[3]
    # Select method of ensuring frame rate
    fps_method = sys.argv[4] # 0-delay, 1 -through command
    # Duration of stream
    STREAM_TIME = sys.argv[5]
    
    get_MJPEG_stream(ip_addr,trial,des_fps,fps_method,STREAM_TIME)
