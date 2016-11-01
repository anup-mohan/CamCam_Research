import boto.ec2
import time
import sys
import os
import find_Nimax
import predict_Nimax
import VSBPP
import logging
from multiprocessing import Process
from boto.manage.cmdshell import sshclient_from_instance

# GLOBAL CONSTANTS
MAX_CORES = 8 # Maximum cores in an instance
WAIT_TIME = 10 # wait time in seconds
INST_LAUNCH_WAIT = 60 # Time to wait after launching an instance
TEST_PHASE_FILES = "test_phase.tar.gz" # Neccessary files for test phase
EXEC_PHASE_FILES = "execute_phase.tar.gz" # Neccessary files for execute phase

# Parameters to connect to instance. Modify accordingly to connect to your account
KEY_FILE = 'Anup_Key.pem' # Modify to use your key file
KEYNAME = 'Anup_Key' # Modify to use your key file
USERNAME = 'ubuntu'
REGIONS = ['us-west-2']
AWS_ACCESS_KEY = "" # Add your AWS access key here
AWS_SECRET_KEY = "" # Add your AWS secret key here
AMI_ID = 'ami-a8f419c8'
REMOTEFILEPATH = '/home/ubuntu/'

# Launch one EC2 instance
def launch_instance(ec2, amiId, instType, keyname, instName):
	
	# Launch an instance from a image
	reservation = ec2.run_instances(image_id=amiId,key_name=keyname,instance_type=instType,security_groups=['cam2'],monitoring_enabled=True)

	# Get instance handler
	instance = reservation.instances[0]
	
	# Wait till the instance is running
	status = instance.update()
	while status == 'pending':
		time.sleep(WAIT_TIME)
		status = instance.update()

	# Add a name tag to the instance
	if status == 'running':
		instance.add_tag("Name",instName)
	
	return instance

# Terminate EC2 Instances
def terminate_instances(conn_handler,instance_id_list):
	
	conn_handler.terminate_instances(instance_ids = instance_id_list)
	

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
    local_filepath  The path where the file should be downloaded to.
    remote_filepath The path to the file to download.
    """
    ssh_client = sshclient_from_instance(
        instance,
        ssh_key_file=key_file,
        user_name=username
    )
    ssh_client.get_file(remote_filepath, local_filepath)
    

def download_all_files(instance, key_file, username, local_filepath, remote_filepath):
	
	# Create an SSH client for the instance
    ssh_client = sshclient_from_instance(
        instance,
        ssh_key_file=key_file,
        user_name=username
    )
    
    # Get all file names in the remote path
    filenames = ssh_client.listdir(remote_filepath)
    
    # Download only text files
    for fname in filenames:
    	if (ssh_client.isdir(remote_filepath + fname) == False):
			
			remotefilename = remote_filepath + fname
			localfilename = local_filepath + fname
			
			ssh_client.get_file(remotefilename, localfilename)

# Copy the required files
def copy_files(instance,executable_files,analysis_pgm,ip_filename):

	
	###### Copy executables ######
	# File to upload
	exec_fname = executable_files
	filepath = os.getcwd() + "/"
	filename = filepath + exec_fname
	remotefilename = REMOTEFILEPATH + exec_fname
	
	# Upload the file
	upload_file(instance,KEY_FILE,USERNAME,filename,remotefilename)
	
	print("Copied executables")	
	##############################
	
	###### Copy analysis program ######
	# File to upload
	filename = analysis_pgm
	fname = filename.split("/")[-1]
	remotefilename = REMOTEFILEPATH + fname
	
	# Upload the file
	upload_file(instance,KEY_FILE,USERNAME,filename,remotefilename)
	
	print("Copied analysis program")	
	###################################
	
	###### Copy ip address file #######
	# File to upload
	filename = ip_filename
	fname = filename.split("/")[-1]
	remotefilename = REMOTEFILEPATH + fname
	
	# Upload the file
	upload_file(instance,KEY_FILE,USERNAME,filename,remotefilename)
	
	print("Copied ip file")
	###################################


# Process to run the execute phase commands
def run_execute_phase(inst_handle, analysis_pgm, ip_filename, res_filename,num_cams,target_fps,stream_time,total_time,ip_ptr):

	print("Analyzing cameras from ip_start_ptr: %d" %(ip_ptr))
	
	# Create an SSH client for the instance
	ssh_client = sshclient_from_instance(inst_handle,ssh_key_file=KEY_FILE,user_name=USERNAME)

	# Unzip the executables
	ssh_client.run('tar --strip 1 -xvf '+EXEC_PHASE_FILES)

	# Run the test phase code
	ssh_client.run('python execute_phase_code.py ' + analysis_pgm + " " + ip_filename + " " + res_filename + " " + str(target_fps) + " " + str(num_cams) + " " + str(stream_time) + " " + str(total_time) + " " + str(ip_ptr))
	




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
	
	# Connect to a Region in ec2
	ec2 = boto.ec2.connect_to_region(REGIONS[0],aws_access_key_id=AWS_ACCESS_KEY,aws_secret_access_key=AWS_SECRET_KEY)
	
	# SSH client need to send the log files
	logging.basicConfig()

	
	# Launch an instance from a image and get instance handler
	instName = "ARMVAC_test_phase"
	instType = "m3.2xlarge"
	instance = launch_instance(ec2, AMI_ID, instType, KEYNAME,instName)
	
	print("Launched the test instance")
		
	####### Copy the required files to the instance #######
	
	copy_files(instance,TEST_PHASE_FILES,analysis_pgm,ip_filename)
	
	######## Done Copying the Required Files ################
	
	# Create an SSH client for the instance
	ssh_client = sshclient_from_instance(instance,ssh_key_file=KEY_FILE,user_name=USERNAME)
	
	# Unzip the executables
	ssh_client.run('tar --strip 1 -xvf '+TEST_PHASE_FILES)
	
	print("unpacked executables")
	
	################### Done Preparing for the test phase ##############################################
	
	################### Enter the test phase ###########################################################
	
	print("Entering the test phase")
	
	# Utilization result file name
	res_filename = "result_test_phase_" + instance.id + ".txt"
	
	# Run the test phase code
	ssh_client.run('python test_phase_code.py ' + analysis_pgm + " " + ip_filename + " " + res_filename + " " + target_fps + " " + stream_time)
	
	# Wait for result file to be written
	time.sleep(10)
	
	print("Finished execution, copying results")
	
	####### Copy the result back ############
	remotefilename = REMOTEFILEPATH + res_filename
	localfilepath = os.getcwd() + "/"
	localfilename = localfilepath + res_filename
	
	download_file(instance,KEY_FILE,USERNAME,localfilename,remotefilename)
	####### Done Copying the result #########
	
	# Terminate the test phase instance
	instance_id_list = []
	instance_id_list.append(instance.id)
	terminate_instances(ec2,instance_id_list)
	
	print("Finished the test phase")
	
	################### Exit the test phase ###########################################################

	################### Find Heuristic Solution #######################################################

	################### Find NiMax ####################################################################

	# Read the utilization file
	util_file = open(localfilename,'r')

	# Calculate the NiMax value
	NiMax = find_Nimax.calc_NiMax(util_file)

	################### Done Finding  NiMax ###########################################################
	
	################### Predict NiMax for other instances #############################################

	# Known value of Nmax
	Nmax_in = NiMax

	# Known value of no: of cores
	cores_in = MAX_CORES

	# Predict Nmax values for all instance types
	result = predict_Nimax.pred_Nimax(Nmax_in,cores_in)
	
	print result

	################### Done Prediction ###############################################################

	################### Apply heuristic algorithm #####################################################

	# Size array with NiMax value for each type of cloud instance
	Nmax_array = result[:,1]

	# Find the heuristic solution
	result_obj, total_cost = VSBPP.apply_heuristic_solution(N,Nmax_array)

	################### Applied Heuristic algorithm ###################################################

	print "The solution: 'Instance Type, Number of instances, Cameras per instance' is as follows"

	# Print Results
	for item in result_obj:
		print item.name, item.count, item.ncams		
	print total_cost

	################### Done Finding Heuristic Solution ###############################################
	
	################### Preparing for the execute phase ###############################################
	
	print("Preparing for the execute phase")
	
	# List of instance handlers
	inst_handler = []
	# List of instance ids for termination
	instance_id_list = []
	
	# Initialize Counters
	count = 0
	ip_ptr = 0
	
	# Initialize the list for process synchronization
	procs = []
	
	# Launch instances as given by solution and perform analysis
	for item in result_obj:
				
			for i in range(item.count):
			
				# Increment instance count
				count += 1

				# Launch an instance from a image and get instance handler
				instName = "ARMVAC_execute_" + str(count)
				inst_handle = launch_instance(ec2, AMI_ID, item.name, KEYNAME,instName)
				inst_handler.append(inst_handle)
				instance_id_list.append(inst_handle.id)
				
				# Wait for the instance to be launched
				time.sleep(INST_LAUNCH_WAIT)
				
				try:
					# Copy the required files to the instance
					copy_files(inst_handle,EXEC_PHASE_FILES,analysis_pgm,ip_filename)
				except:
					time.sleep(INST_LAUNCH_WAIT)
					
					# Copy the required files again
					copy_files(inst_handle,EXEC_PHASE_FILES,analysis_pgm,ip_filename)
				
				# Intialize the processes to execute the analysis program
				inst_process = Process(target=run_execute_phase, args=(inst_handle, analysis_pgm, ip_filename, res_filename, item.ncams, target_fps,stream_time,total_time,ip_ptr))
				procs.append(inst_process)				
				
				# Increment the ip_ptr to allocate different cameras to the next instance
				ip_ptr = ip_ptr + int(item.ncams)
				
				print("Launched instance: %s" %(instName))
				
	print("Done preparing for the execute phase")

	################### Done preparing for the execute phase ############################################
				
	################### Starting the execute phase ######################################################

	print("Starting the execute phase")
	
	# Start all the processes
	for pr in procs:
		pr.start()
	
	# Waiting for all processes to start
	time.sleep(WAIT_TIME)
	
	# Make sure all processes have finished execution
	for k in procs:
		k.join()

	# Waiting before copying the results
	time.sleep(WAIT_TIME)

	# Copy the results from the instances
	for instance in inst_handler:
		# Create a directory for the results
		localdir = os.getcwd() + "/" + "Results_inst_" + instance.id
		os.makedirs(localdir)
		localfilepath = localdir + "/"
		
		remotefilepath = '/home/ubuntu/'
		
		# Download the result files
		download_all_files(instance,KEY_FILE,USERNAME,localfilepath,remotefilepath)
 
 	# Terminate the execute phase instances
	terminate_instances(ec2,instance_id_list)
	
	print("Finished the execute phase")
	
	################### Finished the execute phase ######################################################

