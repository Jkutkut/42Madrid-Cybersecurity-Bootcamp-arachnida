#!/usr/bin/env python3

import sys
import urllib.request
from bs4 import BeautifulSoup

DEFAULT_PATH = "./idea/"
DEFAULT_RECURSIVE = 5

def spider(url, recursive=0, path=DEFAULT_PATH):
	datos = urllib.request.urlopen(url).read().decode()
	soup =  BeautifulSoup(datos)
	tags = soup("img")
	for tag in tags:
		print(tag.get("src"))


if __name__ == '__main__':
	if len(sys.argv) == 1:
		print("Usage: ./spider [-rlpS] URL")
		exit()
	i = 1
	recursive=0
	path=DEFAULT_PATH
	while i < len(sys.argv) - 1:
		arg = sys.argv[i]
		if arg == '-r':
			if i < len(sys.argv) - 2:
				if sys.argv[i + 1] == '-l':
					if i < len(sys.argv) - 3 and sys.argv[i + 2].isdigit():
						recursive = int(sys.argv[i + 2])
					else:
						print("-l must be followed by a number")
						exit()
					i += 2
			else:
				recursive = DEFAULT_RECURSIVE
		elif arg == '-p':
			if i < len(sys.argv) - 2:
				path = sys.argv[i + 1]
			else:
				print("-p must be followed by a path")
				exit()
			i += 1
		else:
			print("Flag not recognized")
			print(f'flag: {arg}')
			print(f'Recursive: {recursive}')
			print(f'Path: {path}')
			exit()
		i += 1

	url = "https://github.com/jkutkut" # TODO Debug
	# url = sys.argv[i]

	# spider(url)

	print(f'Recursive: {recursive}')
	print(f'Path: {path}')
	print(f'URL: {url}')

