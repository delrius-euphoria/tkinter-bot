import discord
import os
from utils.keep_alive import keep_alive
from dotenv import load_dotenv
from discord.ext import commands
from utils.paths import COGS_DIR

load_dotenv()
TOKEN = os.getenv("TOKEN")


class TkBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        intents = discord.Intents.all()

        super().__init__(*args, intents=intents, **kwargs)

    async def setup_hook(self):
        for filename in os.listdir(COGS_DIR):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")

        await self.tree.sync()


bot = TkBot(command_prefix="!")


def main():
    bot.run(TOKEN)


if __name__ == "__main__":
    keep_alive()
    main()
