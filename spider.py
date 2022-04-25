import sys
import urllib.request
from bs4 import BeautifulSoup



def spider(url):
	datos = urllib.request.urlopen(url).read().decode()
	soup =  BeautifulSoup(datos)
	tags = soup("img")
	for tag in tags:
		print(tag.get("src"))


if __name__ == '__main__':
	if len(sys.argv) == 1:
		print("Usage: ./spider [-rlpS] URL")
		exit()
	i = 0
	while i < len(sys.argv) - 1:
		arg = sys.argv[i]
		i += 1

	url = "https://github.com/jkutkut" # TODO Debug
	# url = sys.argv[i]

