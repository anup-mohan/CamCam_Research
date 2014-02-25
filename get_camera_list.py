import MySQLdb

# database information
DB_SERVER = "bigdata.ecn.purdue.edu"
DB_USER_NAME = "readonly"
DB_PASSWORD = "dRT^#W$vdfg35"
DB_NAME = "camcam"


# conncect to the database, and get the connection cursor
connection = MySQLdb.connect(DB_SERVER, DB_USER_NAME, DB_PASSWORD, DB_NAME)
cursor = connection.cursor()

# get all active axis cameras
#cursor.execute("select * from ip_camera where brand_model_id=11 and camera_id in (select id from camera where is_active=1);")
cursor.execute("select * from ip_camera where brand_model_id=11;")
cameras = cursor.fetchall()

# Open a file to save the ip address
f=open("axis_camera_list_all.txt","wb")

# for each camera
for camera in cameras:
	# Save the ip address
	f.write(camera[3]+"\n")


# close the cursor
cursor.close()	
f.close
