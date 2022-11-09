from config import TOKEN, prefixes
from discord.ext.commands import Bot
from discord import *
from os import listdir
from assets.handler import handler
#from discord.gateway import DiscordWebSocket

#class MyDiscordWebSocket(DiscordWebSocket):

#    async def send_as_json(self, data):
#        if data.get('op') == self.IDENTIFY:
#            if data.get('d', {}).get('properties', {}).get('browser') is not None:
#                data['d']['properties']['browser'] = 'Discord Android'
#                data['d']['properties']['device'] = 'Discord Android'
#        await super().send_as_json(data)

#DiscordWebSocket.from_client = MyDiscordWebSocket.from_client

MY_GUILD = Object(id=809862945211285555)


class Jeanne(Bot):
    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
        #slash cogs
        for filename in listdir('./slash cogs'):
          if filename.endswith('.py'):
            await bot.load_extension(f'slash cogs.{filename[:-3]}')
            print(f"{filename} loaded")

          else:
            print(f'Unable to load {filename[:-3]}')

intents = Intents().all()
intents.presences = False
intents.webhooks = False
intents.voice_states = False
intents.reactions = False

bot = Jeanne(command_prefix="たいと", intents=intents,#the prefix is temporary
             allowed_mentions=AllowedMentions.all())
bot.remove_command('help')


#bot.load_extension('topgg.topgg_')

@bot.event
async def on_ready():
  print('Connected to bot: {}'.format(bot.user.name))
  print('Bot ID: {}'.format(bot.user.id))

bot.run(TOKEN, log_handler=handler())
