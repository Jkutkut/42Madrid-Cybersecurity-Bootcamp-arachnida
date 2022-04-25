#!/usr/bin/env python3

import sys
import urllib.request
from bs4 import BeautifulSoup

DEFAULT_PATH="./idea/"
DEFAULT_RECURSIVE=5

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
	while i < len(sys.argv):
		arg = sys.argv[i]
		print(f'{str(i)} {str(len(sys.argv) - 2)} {arg}')
		if arg == '-r':
			recursive = DEFAULT_RECURSIVE
		i += 1

	url = "https://github.com/jkutkut" # TODO Debug
	# url = sys.argv[i]

	# spider(url)
