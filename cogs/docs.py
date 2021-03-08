import discord
from discord.ext.commands import command, Cog, MissingRequiredArgument
from discord.mentions import default

import urllib.parse
from functools import partial
from string import ascii_uppercase

import aiohttp
import discord
from bs4 import BeautifulSoup
import lxml

from pprint import pprint


class PythonDocs(Cog):
    """
    Search something in the python documentation
    """
    def __init__(self, bot):
        self.bot = bot

    @command(name="python",
             usage="\\{text}\\",
             description="Filters python.org results based on your query",
             brief="Search docs on python.org")
    async def python_doc(self, ctx, text: str):
        """Filters python.org results based on your query"""

        text = text.strip('\\')
        # todo have an number of pages... to not have to many results per pages...
        url = "https://docs.python.org/3/genindex-all.html"
        alphabet = '_' + ascii_uppercase

        try:
            async with aiohttp.ClientSession() as client_session:
                async with client_session.get(url) as response:
                    if response.status != 200:
                        return await ctx.send('An error occurred (status code: {response.status}). Retry later.')

                    soup = BeautifulSoup(str(await response.text()), 'lxml')

                    def soup_match(tag):
                        return all(string in tag.text for string in text.strip().split()) and tag.name == 'li'

                    elements = soup.find_all(soup_match, limit=10)
                    links = [tag.select_one("li > a") for tag in elements]
                    links = [link for link in links if link is not None]

                    if not links:
                        return await ctx.send("No results")

                    content = [f"[{a.string}](https://docs.python.org/3/{a.get('href')})" for a in links]

                    emb = discord.Embed(title="Python 3 docs")
                    emb.set_thumbnail(
                        url='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/240px-Python-logo-notext.svg.png')
                    emb.add_field(name=f'Results for `{text}` :', value='\n'.join(content), inline=False)
                    if len(emb) > 1024:
                        async with aiohttp.ClientSession() as client_session:
                            async with client_session.get(url) as response:
                                if response.status != 200:
                                    return await ctx.send(
                                        'An error occurred (status code: {response.status}). Retry later.')

                                soup = BeautifulSoup(str(await response.text()), 'lxml')

                                def soup_match(tag):
                                    return all(
                                        string in tag.text for string in text.strip().split()) and tag.name == 'li'

                                elements = soup.find_all(soup_match, limit=1)
                                links = [tag.select_one("li > a") for tag in elements]
                                links = [link for link in links if link is not None]

                                if not links:
                                    return await ctx.send("No results")

                                content = [f"[{a.string}](https://docs.python.org/3/{a.get('href')})" for a in links]

                                emb = discord.Embed(title="Python 3 docs")
                                emb.set_thumbnail(
                                    url='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/240px-Python-logo-notext.svg.png')
                                emb.add_field(name=f'Results for `{text}` :', value='\n'.join(content), inline=False)
                    try:
                        await ctx.send(embed=emb)
                    except discord.HTTPException as e:
                        await ctx.send("An error as occured")
                        await ctx.send(e)
        except MissingRequiredArgument as e:
            await ctx.send("An argument is missing")
            await ctx.send(e)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("PythonDocs")


class CppDocs(Cog):
    """
    Search something in the C++ documentation

    """
    def __init__(self, bot):
        self.bot = bot

    @command(name="cpp",
             usage="cpp \{text}\\",
             description="Search something on cppreference",
             brief="Search docs on cppreference.org")
    async def _cppreference(language, ctx, text: str):
        """Search something on cppreference"""

        text = text.strip('\\')


        base_url = 'https://cppreference.com/w/cpp/index.php?title=Special:Search&search=' + text
        url = urllib.parse.quote_plus(base_url, safe=';/?:@&=$,><-[]')
        try:
            async with aiohttp.ClientSession() as client_session:
                async with client_session.get(url) as response:
                    if response.status != 200:
                        return await ctx.send(f'An error occurred (status code: {response.status}). Retry later.')

                    soup = BeautifulSoup(await response.text(), 'lxml')

                    uls = soup.find_all('ul', class_='mw-search-results')

                    if not len(uls):
                        return await ctx.send('No results')

                    if language == 'C':
                        wanted = 'w/c/'
                        url = 'https://wikiprogramming.org/wp-content/uploads/2015/05/c-logo-150x150.png'
                    else:
                        wanted = 'w/cpp/'
                        url = 'https://isocpp.org/files/img/cpp_logo.png'

                    for elem in uls:
                        if wanted in elem.select_one("a").get('href'):
                            links = elem.find_all('a', limit=10)
                            break

                    content = [f"[{a.string}](https://en.cppreference.com/{a.get('href')})" for a in links]
                    emb = discord.Embed(title=f"{language} docs")
                    emb.set_thumbnail(url=url)
                    emb.add_field(name=f'Results for `{text}` :', value='\n'.join(content), inline=False)

                    await ctx.send(embed=emb)
        except MissingRequiredArgument as e:
            await ctx.send("An argument is missing")
            await ctx.send(e)

    c_doc = partial(_cppreference, 'C')
    cpp_doc = partial(_cppreference, 'C++')

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("CppDocs")


class JavaDocs(Cog):
    """
    Search something in the Java documentation
    """
    def __init__(self, bot):
        self.bot = bot

    @command(name="javadoc",
             usage="javado \\{text}\\",
             description="",
             brief="")
    async def _javareference(self, ctx, text: str):
        """Search something on javareference"""
        self.all = text.split(".")
        self.classes = self.all[0]
        self.module = self.all[1]
        text = text.strip('\\')
        text = text.strip(' ')

        base_url = f"https://docs.oracle.com/en/java/javase/11/docs/api/java.desktop/javax/swing/text/{self.classes}.{self.module}.html"
        url = urllib.parse.quote_plus(base_url, safe=';/?:@&=$,><-[]')
        try:
            async with aiohttp.ClientSession() as client_session:
                async with client_session.get(url) as response:
                    if response.status != 200:
                        return await ctx.send(f'An error occured (status code: {response.status}). Retry later.')

                    soup = BeautifulSoup(await response.text(), 'lxml')

        except Exception as e:
            await ctx.send("An error was occured : ")
            await ctx.send(e)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("JavaDocs")

class HtmlDocs(Cog):
    """
    Search something in the html documentation
    """
    def __init__(self, bot):
        self.bot = bot

    @command(name="html",
             usage="\\text\\",
             brief="Search docs about html")
    async def html_doc(self, ctx, text: str):
        """Filters html results based on your query"""

        text = text.strip('\\')
        url = f"https://www.w3schools.com/tags/tag_{text}.asp"

        try:
            async with aiohttp.ClientSession() as client_session:
                async with client_session.get(url) as response:
                    if response.status != 200:
                        return await ctx.send(f"An error occured (startus code: {response.status}). Retry later.")

                    soup = BeautifulSoup(await response.text(), 'lxml')
                    return await ctx.send(soup)
        except Exception as e:
            await ctx.send("An error occured : ")
            await ctx.send(e)

# todo : html
# todo : css
# todo : bs4
# todo : java
# todo : pygame
# todo : pyglet
# todo : pymunk
# todo : matplotlib
# todo : discord.py
# todo : matematics
# todo : NeuralNet
# todo : numpy
# todo : java android
# todo : android
# todo : nginx
# todo : receuil d'exercice en python
# todo : actualité / mysql / sap / sécurité / tensorflow / sckitik learn
# todo : developpez.net
# todo : faire des recherches par catégorie et mot clef


def setup(bot):
    bot.add_cog(PythonDocs(bot))
    bot.add_cog(CppDocs(bot))
    bot.add_cog(JavaDocs(bot))
