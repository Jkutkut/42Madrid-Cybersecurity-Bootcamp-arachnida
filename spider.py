#!/usr/bin/env python3

import sys
import urllib.request
from bs4 import BeautifulSoup

class Arachnida:

	DEF_PATH = "./idea/"
	DEF_DEPTH = 5

	def __init__(self, argc, argv):
		self.url = argv[argc]
		self.path = self.DEF_PATH
		self.depth = 0
		self.update(argc, argv)

	def update(self, argc, argv):
		i = 1
		while i < argc - 1:
			arg = sys.argv[i]
			if arg == '-r':
				if i < argc - 2:
					if sys.argv[i + 1] == '-l':
						if i < argc - 3 and sys.argv[i + 2].isdigit():
							recursive = int(sys.argv[i + 2])
						else:
							print("-l must be followed by a number")
							exit()
						i += 2
				else:
					recursive = self.DEF_DEPTH
			elif arg == '-p':
				if i < argc - 2:
					path = sys.argv[i + 1]
				else:
					print("-p must be followed by a path")
					exit()
				i += 1
			else:
				print("Flag not recognized")
				print(f'\t{arg}')
				exit()
			i += 1

	def run(self):
		Arachnida.spider(self.url, self.path, self.depth)

	def __str__(self) -> str:
		return f'Arachnida:\n\tURL: {self.url}\n\tPath: {self.path}\n\tDepth: {self.depth}'

	@staticmethod
	def spider(cls, url, recursive=0, path=None):
		if path is None:
			cls.DEF_PATH
		datos = urllib.request.urlopen(url).read().decode()
		soup =  BeautifulSoup(datos)
		tags = soup("img")
		for tag in tags:
			print(tag.get("src"))



if __name__ == '__main__':
	if len(sys.argv) == 1:
		print("Usage: ./spider [-rlpS] URL")
		exit()
	a = Arachnida(len(sys.argv) - 1, sys.argv)
	print(a)

