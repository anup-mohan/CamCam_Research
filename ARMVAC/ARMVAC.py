import boto.ec2
import time
import sys
import os
from boto.manage.cmdshell import sshclient_from_instance


def upload_file(instance, key_file, username, local_filepath, remote_filepath):
    """
    Upload a file to a remote directory using SFTP. All parameters except
    for "instance" are strings. The instance parameter should be a
    boto.ec2.instance.Instance object.
 
    instance        An EC2 instance to upload the files to.
    key_file        The file path for a valid SSH key which can be used to
                    log in to the EC2 machine.
    username        The username to log in as.
    local_filepath  The path to the file to upload.
    remote_filepath The path where the file should be uploaded to.
    """
    ssh_client = sshclient_from_instance(
        instance,
        ssh_key_file=key_file,
        user_name=username
    )
    ssh_client.put_file(local_filepath, remote_filepath)
    
    
def download_file(instance, key_file, username, local_filepath, remote_filepath):
    """
    Download a file from a remote directory using SFTP. All parameters except
    for "instance" are strings. The instance parameter should be a
    boto.ec2.instance.Instance object.
 
    instance        An EC2 instance to upload the files to.
    key_file        The file path for a valid SSH key which can be used to
                    log in to the EC2 machine.
    username        The username to log in as.
    local_filepath  The path to the file to upload.
    remote_filepath The path where the file should be uploaded to.
    """
    ssh_client = sshclient_from_instance(
        instance,
        ssh_key_file=key_file,
        user_name=username
    )
    ssh_client.get_file(remote_filepath, local_filepath)
    


if __name__ == "__main__":

	###################### Read the inputs ##############################################
	
	N = int(sys.argv[1]) # Total number of cameras
	target_fps = sys.argv[2] # Target frame rate to be achieved on all cameras
	analysis_pgm = sys.argv[3] # Analysis program to be used
	ip_filename = sys.argv[4] # File containing the ip_addr of all cameras
	stream_time = sys.argv[5] # Time for which each camera has to be streamed
	total_time = sys.argv[6] # Total time for analysis
	
	################### Done Reading the inputs##########################################
	
	####################### Preparation for test phase ##################################
	
	print("Preparing for test phase")
	
	# Utilization result file name
	res_filename = "result_test_phase.txt" 
	
	# Connect to a Region in ec2
	ec2 = boto.ec2.connect_to_region('us-west-2',aws_access_key_id='AKIAIZHJ7ZRJNZQ37XMA',aws_secret_access_key='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')
	
	# Parameters to connect to instance
	key_file = 'Anup_Key.pem'
	keyname = 'Anup_Key'
	username = 'ubuntu'

	# Launch an instance from a image
	reservation = ec2.run_instances(image_id='ami-70c92c43',key_name=keyname,instance_type='m3.2xlarge',security_groups=['cam2'],monitoring_enabled=True)

	# Get instance handler
	instance = reservation.instances[0]

	# Wait till the instance is running
	status = instance.update()
	while status == 'pending':
		time.sleep(10)
		status = instance.update()

	# Add a name tag to the instance
	if status == 'running':
		instance.add_tag("Name","ARMVAC_test_phase")
	
	print("Launched the test instance")
		
	####### Copy the required files to the instance #######
	
	###### Copy executables ######
	# File to upload
	exec_fname = "test_phase.tar.gz"
	filepath = os.getcwd() + "/"
	filename = filepath + exec_fname
	remotefilepath = '/home/ubuntu/'
	remotefilename = remotefilepath + exec_fname
	
	# Upload the file
	upload_file(instance,key_file,username,filename,remotefilename)
	
	print("Copied executables")	
	##############################
	
	###### Copy analysis program ######
	# File to upload
	filename = analysis_pgm
	fname = filename.split("/")[-1]
	remotefilepath = '/home/ubuntu/'
	remotefilename = remotefilepath + fname
	
	# Upload the file
	upload_file(instance,key_file,username,filename,remotefilename)
	
	print("Copied analysis program")	
	###################################
	
	###### Copy ip address file #######
	# File to upload
	filename = ip_filename
	fname = filename.split("/")[-1]
	remotefilepath = '/home/ubuntu/'
	remotefilename = remotefilepath + fname
	
	# Upload the file
	upload_file(instance,key_file,username,filename,remotefilename)
	
	print("Copied ip file")
	###################################
	
	######## Done Copying the Required Files ################
	
	# Create an SSH client for the instance
	ssh_client = sshclient_from_instance(instance,ssh_key_file=key_file,user_name=username)
	
	# Unzip the executables
	ssh_client.run('tar --strip 1 -xvf '+exec_fname)
	
	print("unpacked executables")
	
	################### Done Preparing for the test phase ##############################################
	
	################### Enter the test phase ###########################################################
	
	print("Entering the test phase")
	
	# Run the test phase code
	ssh_client.run('python test_phase_code.py ' + analysis_pgm + " " + ip_filename + " " + res_filename + " " + target_fps + " " + stream_time)
	
	# Wait for result file to be written
	time.sleep(10)
	
	print("Finished execution, copying results")
	
	####### Copy the result back ############
	remotefilepath = '/home/ubuntu/'
	remotefilename = remotefilepath + res_filename
	localfilepath = os.getcwd() + "/"
	localfilename = localfilepath + res_filename
	
	download_file(instance,key_file,username,localfilename,remotefilename)
	####### Done Copying the result #########
	
	print("Finished the test phase")
	
	################### Exit the test phase ###########################################################
