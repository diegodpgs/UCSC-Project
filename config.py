import os

def detectOS():
	if os.sep == '/':
		return 'Unix'

	return 'Windows'

def findMainFolder(mainfolder='MD'):
	actual_directory = os.getcwd().split(os.sep)


	index = len(actual_directory)-1

	while index >= 0 and actual_directory[index] != mainfolder:
		index -= 1

	if index >= 0:
		return os.sep.join(actual_directory[0:index + 1]) + os.sep

	return None

def isLibrariesInstalled(path):
	folders = os.listdir(path)

	if 'bash_run_xml_thru_realpro.sh' not in folders or 'run_xml_thru_realpro.sh' not in folders:
		print folders
		print 'is missing some of the following files in the directory %s' % path
		print 'bash_run_xml_thru_realpro.sh\nrun_xml_thru_realpro.sh'
		return False

	return True

def writeConfig():
	config_file = open('config_MD.py','w')
	path = findMainFolder()
	run_file = open(path+'run_all.sh','w')
	PATH_TREE = path+'tree_structure#v0.6#'.replace('#',os.sep)

	if isLibrariesInstalled(path):
		config_file.write('PATH="%s"\n' % path)
		config_file.write('PATH_TREE="%s"' % (PATH_TREE))
		
		
		run_file.write('python %s%s\n' % (PATH_TREE,'contentplanner.py'))
		if detectOS() == 'Unix':
			run_file.write('run_xml_thru_realpro.sh')
		else:
			run_file.write('bash_run_xml_thru_realpro.sh')
		

		config_file.close()
		run_file.close()

writeConfig()





