#!/usr/bin/env python3

import sys
from typing import Protocol
import urllib.request
from bs4 import BeautifulSoup

class Arachnida:

	DEF_PATH = "./"
	DEF_DEPTH = 5

	def __init__(self, argc, argv):
		# self.url = argv[argc]
		url = argv[argc]
		# Split the url between the domain and the path
		protocol = 'http://'
		if 'https://' in url:
			protocol = 'https://'
			url = url[8:] # Remove https://
		elif 'http://' in url:
			url = url[7:]
		
		url = url.split('/')
		self.url = protocol + url[0]
		self.path = "/".join(url[1:])

		self.depth = 0
		self.update(argc, argv)

	def update(self, argc, argv):
		i = 1
		while i < argc:
			arg = argv[i]
			if arg == '-r':
				if i < argc - 1:
					if argv[i + 1] == '-l':
						if i < argc - 2 and argv[i + 2].isdigit():
							self.depth = int(argv[i + 2])
						else:
							print(f'-r -l must be followed by a number, but {argv[i + 2]} was given')
							exit()
						i += 2
				else:
					self.depth = self.DEF_DEPTH
			elif arg == '-p': # TODO Check if path is valid
				if i < argc - 1:
					self.path = argv[i + 1]
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
		print(self.url + "/" + self.path)
		results = Arachnida.spider(self.url + "/" + self.path, self.depth)
		print(f'{len(results)} elements found')
		print(*[f'\t{e}' for e in results], sep='\n')

	def __str__(self) -> str:
		return f'Arachnida:\n\tURL: {self.url}\n\tPath: {self.path}\n\tDepth: {self.depth}'

	@classmethod
	def spider(cls, url, depth = 0, results=set()):
		data = urllib.request.urlopen(url).read().decode()
		soup = BeautifulSoup(data, 'html.parser')
		paths = cls.analyze(soup, results)
		print(f'{len(paths)} paths found')
		print(*[f'\t{p}' for p in paths], sep='\n')
		# if depth > 0:
		# 	for path in paths:
		# 		results = results | cls.spider(path, path, depth - 1, results)
		return results

	@classmethod
	def analyze(cls, soup, results):
		paths = set()
		for link in soup('a'):
			path = link.get('href')
			if len(path) > 2 and path[0] == '/':
				if path[-1] == '/':
					paths.add(path)
				else:
					results.add(path)
		return paths

	# @classmethod
	# def get_imgs(self, data, imgs, types=None):
	# 	if types is None:
	# 		types = Arachnida.DEF_IMG_TYPE
	# 	soup =  BeautifulSoup(data, "html.parser")
	# 	# soup =  BeautifulSoup(data, "lxml")
	# 	# soup =  BeautifulSoup(data, "lxml-xml")
	# 	# soup =  BeautifulSoup(data, "html5lib")
	# 	tags = soup("a")
	# 	for tag in tags:
	# 		# extension = tag.get('src').split('.')[-1]
	# 		# if extension in types:
	# 			# imgs.add(tag.get("src"))
	# 		imgs.add(tag.get("href"))


if __name__ == '__main__':
	if len(sys.argv) == 1:
		print("Usage: ./spider [-rlpS] URL")
		exit()
	a = Arachnida(len(sys.argv) - 1, sys.argv)
	print(a)
	a.run()
