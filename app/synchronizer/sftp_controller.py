import pysftp

#function that get username in input and synchronize local models in folder: 'models/username/' to RPI folder 'models/'
def synchronizeUser(user, sensitivity=.5, drive_s=.5, simple=False):

	#Create setting csv
	ofile  = open('toRPI/settings.csv', "w")
	ofile.write( str(sensitivity) + ' ' )
	ofile.write( str(drive_s) + ' ' )
	ofile.write( str(simple) )
	ofile.close()
	status = False
	try:
		srv = pysftp.Connection(host="rasby", 
								username="pi",
								password="raspberry")

		modelsDir = 'models/'

		with srv.cd( 'Desktop/Rally-Project/userdata' ):
			
			srv.put( modelsDir+user+'/left1.pmdl' )
			srv.put( modelsDir+user+'/left2.pmdl' )	
			srv.put( modelsDir+user+'/left3.pmdl' )
			srv.put( modelsDir+user+'/right1.pmdl' )	
			srv.put( modelsDir+user+'/right2.pmdl' )
			srv.put( modelsDir+user+'/right3.pmdl' )
			srv.put( modelsDir+user+'/stop.pmdl' )
			srv.put( modelsDir+user+'/start.pmdl' )

			srv.put( 'toRPI/settings.csv' )
			print ( srv.listdir() )
			srv.close()
			status = True
	except:
		print('non connesso')	
	return status