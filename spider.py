#!/usr/bin/env python3

import sys
import os
# from typing import Protocol
import urllib.request
from bs4 import BeautifulSoup

class Arachnida:

	DEF_STORE_PATH = "./results/"
	DEF_DEPTH = 4

	def __init__(self, argc, argv):
		url = argv[argc]
		# Split the url between the domain and the path
		self.protocol = 'http://'
		if 'https://' in url:
			self.protocol = 'https://'
			url = url[8:] # Remove https://
		elif 'http://' in url:
			url = url[7:]
		
		url = url.split('/')
		self.url = self.protocol + url[0] + '/'
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
		results = Arachnida.spider(self.url, self.path, self.depth)
		self.save(results)

	def __str__(self) -> str:
		return f'Arachnida:\n\tURL: {self.url}\n\tPath: {self.path}\n\tDepth: {self.depth}'

	@classmethod
	def spider(cls, url, path, depth = 0, results=set()):
		print(f'Spidering {url} at {path}, depth {depth}')
		data = urllib.request.urlopen(url + path).read().decode()
		soup = BeautifulSoup(data, 'html.parser')
		paths = cls.analyze(soup, results)
		if depth > 0:
			for p in paths:
				if len(p) > len(path):
					if p[0] == '/':
						p = p[1:]
					results = results | cls.spider(url, p, depth - 1, results)
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

	def save(self, results):
		# Create a folder for the results
		# dir = self.DEF_STORE_PATH + self.url.replace(self.protocol, '') + "/"
		dir = self.DEF_STORE_PATH + self.url.replace(self.protocol, '')[:-1]
		os.makedirs(dir, exist_ok=True)
		print("Storing results in " + dir)

		# Download the results
		for result in results:
			# file = result.split('/')[-1]
			# print(f'\t{file}')
			# urllib.request.urlretrieve(self.url + result, dir + file)
			print(f'\t{result}')
			file_dir = '/'.join(result.split('/')[:-1])
			os.makedirs(dir + file_dir, exist_ok=True)
			urllib.request.urlretrieve(self.url + result, dir + result)


if __name__ == '__main__':
	if len(sys.argv) == 1:
		print("Usage: ./spider [-rlpS] URL")
		exit()
	a = Arachnida(len(sys.argv) - 1, sys.argv)
	print(a)
	a.run()
