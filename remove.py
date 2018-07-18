import os
import shutil

for file in os.listdir('./images/'):
	if not int(file[-2:])<90:
		shutil.rmtree('./images/'+file)