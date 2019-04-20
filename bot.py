import discord
from alko_search import search as a_s
from alko_search import set_sorting


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!alkohelp'):
            await message.channel.send('Search: !alkosearch product name\n\n'
                                       'Change sorting of search results: !alkosort [1-4]\n'
                                       '1. Alphabetical Order A-Ö (default)\n'
                                       '2. Alphabetical Order Ö-A'
                                       '\n3. By Price, lowest first\n'
                                       '4. By Price, highest first'.format(message))

        if message.content.startswith('!alkosort'):
            sorting = message.content.replace("!alkosort", "").strip()
            if set_sorting(sorting):
                await message.channel.send('Sorting method changed!'.format(message))
            else:
                await message.channel.send('Failed to change sorting method. Make sure you entered a number between'
                                           ' 1 and 4'.format(message))

        if message.content.startswith('!alkosearch'):
            search_term = message.content.replace("!alkosearch", "").strip()
            await message.channel.send('Searching Alko for ' + search_term + '...'.format(message))
            result_array = a_s(search_term)
            for line in result_array:
                line = line.replace("{n}", "\n")
                await message.channel.send(line.format(message))


try:
    f = open("token.txt", "r")
    token = f.read().strip()
    f.close()
    client = MyClient()
    client.run(token)
except FileNotFoundError:
    print("You have to create a file in the same folder as bot.py called 'token.txt' and paste your token into it.")

