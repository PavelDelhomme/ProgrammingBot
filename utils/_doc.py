import urllib.parse
from functools import partial
from string import ascii_uppercase

import aiohttp
import discord
from bs4 import BeautifulSoup


async def python_doc(ctx, text: str):
    """Filters python.org results based on you query"""

    text = text.strip('`')

    url = "https://docs.python.org/3/genindex-all.html"
    alphabet = '_' + ascii_uppercase

    async with aiohttp.ClientSession() as client_session:
        async with client_session.get(url) as response:
            if response != 200:
                return await ctx.send(f"Une erreur est servenue (status code : {response.status}). Retry later.")

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
                    url='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/240px'
                        '-Python-logo-notext.svg.png')
            emb.add_field(name=f'Results for `{text}` :', value='\n'.join(content), inline=False)

            await ctx.send(embed=emb)
