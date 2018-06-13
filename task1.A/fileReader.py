from sys import argv, exit, version_info
from os import path, stat

if version_info[0] <3:
	import consoleSize
else:
	from shutil import get_terminal_size

def is_num(var):

	try:
		int(float(var))
		return True
	except:
		return False


def param_validator():
	'''Parameter validation'''

	#checks if supplied filename exists
	if not path.isfile(argv[1]):
		print("File {} does not exist.".format(argv[1]))
		exit(2)

	#checks if line width is a number
	if not is_num(argv[2]):
		print("line_width should be a whole number or deciamal.")
		print("NOTE: Decimals will be rounded to their nearest whole numbers.")
		exit(0)

	#checks if supplied break type is a number and the correct numbers are supplied
	if not is_num(argv[3]) or int(float(argv[3])) not in [0,1]:
		print("break_type should be with 0 or 1")
		exit(0)


	alignment = str(argv[4]).lower()

	#checks if the supplied alignment matches available alignments
	if alignment not in ["l", "c", "r"]:
		print("Incorrent allignment type.")
		print("Available alignment types:\n\tl for left, c for center and r for right.\n")
		exit(0)


def help():
	'''Displayes help message for application usage'''

	print("Uage: python fileReader.py <filename> <line_width> <break_type> <alighment>\n")
	print("Parameter description:")
	print("filename: The name of the file to be read. The full file path should be supplied if the desired file is in a deffering directory from this application.")
	print("line_width: A limit on the number of characters that can be put on one line.\n")
	print("break_type: A Boolean value (0 for word or 1 for character) indicating whether the application should break on words or characters.\n")
	print("alignment: How the characters on each line should be aligned i.e. left-,center- or right-aligned.")
	print("This is inicated be l for left, c for center and r for right.\n")

	print("Options:")
	print("-h - displays help message.")

def rd_ln_brk_on_char(line_width, stream):

	try:
		line = stream.read(line_width)
		nc = stream.read(1)

		if nc != " " and line[-1] != " " and nc != "":
			line += "-"

		stream.seek(-1, 1)

		return line

	except Exception as e:
		print (e)
		exit(0)

def rd_ln_brk_on_word(line_width, stream):

	try:
		line = stream.read(line_width)
		nc = stream.read(1)

		if nc != " " and len(line + nc) > line_width:
			line+= nc

			char = stream.read(1)
			while char != "" and char !=" ":
				line+=char
				char = stream.read(1)

			return line

		if nc != " " and line[-1] != " " and nc != "":
			line_arr = line.split(" ")
			
			rewind = len(line_arr[-1])+1
			stream.seek((rewind * -1), 1)

			line_arr.pop()

			line = " ".join(line_arr)

		elif line[-1] == " ":
			stream.seek(-1, 1)
		

		return line

	except Exception as e:
		print (e)
		exit(0)

def main():

	if len(argv) < 5 or '-h' in argv:
		help()
		exit(0)

	param_validator()

	filename = argv[1]
	line_width = int(float(argv[2]))
	break_type = int(float(argv[3]))
	align_type = argv[4]

	try:
		with open(filename, 'r') as stream:
			EOF = stat(filename).st_size
			cp = 0

			if version_info[0] < 3:
				console_width = consoleSize.get_terminal_size()[0]
			else:
				console_width = get_terminal_size().columns

			indent = 0

			if align_type == "c":
				indent = (console_width/2) + (line_width/2)
				print (indent)
			elif align_type == "r":
				indent = console_width

			while cp < EOF-1 :
				
				if break_type == 1:
					line = rd_ln_brk_on_char(line_width, stream)
				else:
					line = rd_ln_brk_on_word(line_width, stream)

				cp = stream.tell()

				print("{0:>{1}}".format(line, indent))
				
	except Exception as e:
		print (e)
		exit(0)


if __name__ == "__main__":
	main()