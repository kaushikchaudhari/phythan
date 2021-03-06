import asyncio
import json
import os
import operator
import re

import discord
from discord.ext import commands
import tools.discordembed as dmbd




class WordDB:

    def __init__(self, bot):
        self.bot = bot

        if not os.path.exists('./json'):
            os.makedirs('./json')
        if not os.path.isfile('./json/wordDB.json'):
            with open('./json/wordDB.json', 'w',) as outfile:
                json.dump({}, outfile, indent=4)
        with open('./json/wordDB.json') as data_file:
            self.wordDB = json.load(data_file)
        if not os.path.isfile('./json/cmdDB.json'):
            with open('./json/cmdDB.json', 'w',) as outfile:
                json.dump({}, outfile, indent=4)
        with open('./json/cmdDB.json') as data_file:
            self.cmdDB = json.load(data_file)

        self.blacklist = ['the', 'and', 'for', 'are', 'but', 'not', 'you',
                          'all', 'any', 'can', 'her', 'was', 'one', 'our',
                          'out', 'day', 'get', 'has', 'him', 'his', 'how',
                          'man', 'new', 'now', 'old', 'see', 'two', 'way',
                          'who', 'boy', 'did', 'its', 'let', 'put', 'say',
                          'she', 'too', 'use', 'dad', 'mom']
    def cmdcount(self, name: str):
        if name in self.cmdDB:
            self.cmdDB[name] += 1
        else:
            self.cmdDB[name] = 1
        self.updatejsonfile()

    def updatejsonfile(self):
        """Update the json file"""
        with open('./json/wordDB.json', 'w',) as outfile:
            json.dump(self.wordDB, outfile, indent=4)
        with open('./json/cmdDB.json', 'w',) as outfile:
            json.dump(self.cmdDB, outfile, indent=4)

    async def on_message(self, message):
        if len(message.content) <= 2:
            return
        if message.author.bot:
            return
        if message.content.startswith(self.bot.command_prefix):
            return

        for x in re.compile('\w+').findall(message.content.replace('\n', ' ')):
            if len(x) <= 2:
                continue
            if x.startswith('http'):
                continue
            if x in self.blacklist:
                continue
            if x in self.wordDB:
                self.wordDB[str(x)] += 1
            else:
                self.wordDB[str(x)] = 1

        self.updatejsonfile()

    @commands.command(pass_context=True)
    async def topwords(self, ctx):
        """Top 10 words used in the server."""
        sorted_db = sorted(self.wordDB.items(), key=operator.itemgetter(1), reverse=True)

        digits = max(map(len, sorted_db))
        author = ctx.message.author
        title = "Top 10 Words Used"
        desc = "This is counted across all servers Rin is on."
        em = dmbd.newembed(author, title, desc)
        for i, x in zip(range(10), sorted_db):
            v = re.sub('[()\']', '', str(x))
            em.add_field(name="#" + str(i + 1), value=v.replace(",", ":"))

        await self.bot.say(embed=em)
        self.cmdcount('topwords')

    @commands.command(pass_context=True)
    async def wordused(self, ctx, word: str):
        """ Shows how many times a word has been used."""

        author = ctx.message.author
        num = 0
        title = ""
        if word in self.wordDB.keys():
            num = self.wordDB[word]
        if num == 1:
            title = "This word has been used only once."
        else:
            title = "This word has been used {} times.".format(num)

        desc = "This is counted across all servers Rin is on."
        em = dmbd.newembed(author, title, desc)

        await self.bot.say(embed=em)
        self.cmdcount('wordused')


    @commands.command()
    async def blackwords(self):
        """ Words that are not included in wordDB"""
        result = " ".join(self.blacklist)
        await self.bot.say("```\n" + result + "\nGrabbed from YourDictionary as the most common three letter words.\n```")
        self.cmdcount('blackwords')

    @commands.command(pass_context=True)
    async def topcmds(self, ctx):
        """ Top 10 cmds used."""
        sorted_db = sorted(self.cmdDB.items(), key=operator.itemgetter(1), reverse=True)
        digits = max(map(len, sorted_db))
        author = ctx.message.author
        title = "Top 10 Commands Used"
        desc = "This is counted across all servers Rin is on."
        em = dmbd.newembed(author, title, desc)
        for i, x in zip(range(10), sorted_db):
            v = re.sub('[()\']', '', str(x))
            em.add_field(name="#" + str(i + 1), value=str(self.bot.command_prefix) + v.replace(",", ":"))

        await self.bot.say(embed=em)
        self.cmdcount('topcmds')

    @commands.command(pass_context=True)
    async def cmdused(self, ctx, word: str):
        """ Shows how many times a cmd has been used."""

        author = ctx.message.author
        num = 0
        title = ""
        if word in self.cmdDB.keys():
            num = self.cmdDB[word]
        if num == 1:
            title = "This command has been used only once."
        else:
            title = "This command has been used {} times.".format(num)

        desc = "This is counted across all servers Rin is on."
        em = dmbd.newembed(author, title, desc)

        await self.bot.say(embed=em)
        self.cmdcount('cmdused')



def setup(bot):
    bot.add_cog(WordDB(bot))
