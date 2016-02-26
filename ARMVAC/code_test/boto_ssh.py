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




# Connect to a Region in ec2
ec2 = boto.ec2.connect_to_region('us-west-2',aws_access_key_id='AKIAIZHJ7ZRJNZQ37XMA',aws_secret_access_key='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')

# Get the required instance handler
reservation = ec2.get_all_instances(instance_ids='i-54fa849d')[0]
instance = reservation.instances[0]

# Parameters to connect to instance
key_file = 'Anup_Key.pem'
username = 'ubuntu'

# File to upload
filepath = '/home/anupmohan/Documents/Research/camcam/CamCam_Research/Journal_Spring2016/boto/'
filename = filepath + sys.argv[1]
remotefilepath = '/home/ubuntu/'
remotefilename = remotefilepath + sys.argv[1]

# Copy file to EC2 instance
#upload_file(instance,key_file,username,filename,remotefilename)

# Copy file from EC2 instance
#download_file(instance,key_file,username,filename,remotefilename)

###### Copy executables ######
# File to upload
exec_fname = "test_phase.tar.gz"
filepath = os.getcwd() + "/"
filename = filepath + exec_fname
remotefilepath = '/home/ubuntu/'
remotefilename = remotefilepath + exec_fname

# Upload the file
upload_file(instance,key_file,username,filename,remotefilename)

# Create an SSH client for the instance
ssh_client = sshclient_from_instance(instance,ssh_key_file=key_file,user_name=username)
	
# Unzip the executables
ssh_client.run('tar --strip 1 -xvf '+exec_fname)                           


