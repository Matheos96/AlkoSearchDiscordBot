import discord
from alko_search import search as a_s


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

