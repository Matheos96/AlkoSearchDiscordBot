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


client = MyClient()
client.run('NTY4ODE0NjAzMDAyMzE0NzU0.XLnj-A.rm_tMLP2oZ5sEVTHbmyPI4_Igw8')
