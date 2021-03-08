import urllib.parse
from string import ascii_uppercase

from bs4 import BeautifulSoup
import lxml
from pprint import pprint

import requests
import aiohttp
from discord.ext.commands import Cog

url = "https://docs.python.org/3/genindex-all.html"
alphabet = '_' + ascii_uppercase

response = requests.get(url)

content = response.text

soup = BeautifulSoup(content, 'lxml')

# print(soup.prettify())

lis = list(set(soup.find_all("li")))
a = [a for a in list(set(soup.find_all("li")))]
print(len(a))
print(a)
