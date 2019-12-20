#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import datetime


# noinspection PyInterpreter
def main():
	console_prefix = "$ "
	channel_name = "whatsapp"
	description = "Transform exported whatsapp discussions into ready-for-import slack.com threads."
	
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument("input", type=argparse.FileType('r'), help="Input filename")
	parser.add_argument("-c", "--channel", default=channel_name, help="Slack.com channel name, default: "+channel_name)
	parser.add_argument("-o", "--output", type=argparse.FileType('w'), help="Output filename")	
	# parser.print_help()
	
	args = parser.parse_args()
	
	# Print description in case of parse success
	print("\n 🚀  {0}: {1}\n".format(os.path.basename(sys.argv[0]), description))

	input_file = args.input
	output_file = open("Slack Import "+args.input.name, 'w') if args.output is None else args.output
	
	print("{0}input filename:     '{1}'".format(console_prefix, input_file.name))
	print("{0}output filename:    '{1}'".format(console_prefix, output_file.name))
	print("{0}slack channel name: '{1}'".format(console_prefix, channel_name))
	
	print("{0}Reading input file...".format(console_prefix))
	input_lines = input_file.readlines()
	usernames_mapping = {}
	
	# Looping through raw lines to group combine lines
	output_line = None
	output_elements = {}
	
	with open(output_file.name, 'w') as outfile:	
	
		for line in input_lines:
			try:
				dt = datetime.datetime.strptime(line.split('-')[0].strip(), "%m/%d/%y, %H:%M %p")
			except ValueError:
				# We cannot find a date, it's a continuation of a line, most probably...
				if ("content" in output_elements.keys()):
					output_elements["content"] += "\n"+line.strip()
				else:
					print("bad line")
					print(line)
			else:
				if output_elements.get("content", None) is not None:
					new_line = '"{0}","{1}","{2}","{3}"'.format(int(output_elements["date"].timestamp()), channel_name,
																output_elements["username"],
																output_elements["content"].replace('"', "'"))
					# print(new_line)
					outfile.write(new_line+"\n")
					output_elements = {}
	
				# We can find a date at start of line, it's a new line
				output_line = line.strip()
				output_elements["date"] = dt
				
				# Make sure to change all double quotes to standard ones
				for quote in ['"', '‟', '″', '˝', '“']:
					output_line = output_line.replace(quote, '\"')
	
				# Oh, by the way, look for a username. The presence of a username followed by a colon is the only fkag we can use.
				input_username = line.strip().split('-')[1].strip().split(':')[0].strip()
				if input_username not in usernames_mapping.keys():
					output_username = input("\n{0}Unknown username '{1}'. Enter corresponding Slack.com username (<Enter>=identical): ".format(console_prefix, input_username))
					if len(output_username.strip()) > 0:
						usernames_mapping[input_username] = output_username.strip()
					
				output_username = usernames_mapping.get(input_username, None)
				if output_username is not None:
					output_elements["username"] = output_username
					output_elements["content"] = ':'.join('-'.join(line.strip().split('-')[1:]).strip().split(':')[1:]).strip()


		# We need this to get the last line...			
		if output_elements.get("content", None) is not None:
			new_line = '"{0}","{1}","{2}","{3}"'.format(int(output_elements["date"].timestamp()), channel_name,
														output_elements["username"], output_elements["content"].replace('"', "'"))
			# print(new_line)
			outfile.write(new_line+"\n")
			output_elements = {}

			
	print("\n  🌖 {0}Done. Enjoy!\n".format(console_prefix))

if __name__ == "__main__":
	main()


