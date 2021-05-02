import re
import argparse

parser = argparse.ArgumentParser(description='Show unused and repeated imports.')
parser.add_argument('filesPath', type=str, nargs='+',
                    help='files to clean')

programArgs = parser.parse_args()

for filePath in programArgs.filesPath:
	print(filePath)
	with open(filePath, 'r') as browsedFile:
		for line in browsedFile:
			#print(line)
			#print(type(line))
			if line == '\n':
				continue
			print(line, end='')
	

#print(programArgs)

#for file in programArgs:
#	print(file)
