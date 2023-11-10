import discord
from discord.ext import commands, tasks
from utils.functions import process
from itertools import cycle
import time
import utils.messages
from classes.resource import Resource
from classes.github import GitHub

res = Resource()
gh = GitHub()


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        widgets = res.get_all_widgets()
        widgets = [wid + "e" if wid.endswith("x") else wid for wid in widgets ]
        self.activities = cycle([f"with {wid}s" for wid in widgets])
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} has logged in")

        self.guild = self.bot.get_guild(utils.messages.GUILD_ID)
        self.check_new_members.start()
        self.add_offline_roles.start()
        self.presence.start()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.content == "F":
            await message.channel.send("Respekts :3")

        if gh.validate_link(message.content):
            if "`" in message.content or "```" in message.content:
                return

            code_info = gh.get_code_block(message.content)
            code_block = "\n".join(code_info[0])
            info_str = code_info[1][0]
            lang = code_info[1][1]
            reference = message.reference

            if code_block:
                code_msg = "> {}\n{}\n```{}\n{}```"
                await message.channel.send(
                    code_msg.format(message.content, info_str, lang, code_block),
                    suppress_embeds=True,
                    reference=reference,
                )

                await message.delete()

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        img = process(member.name, member.display_avatar.url)
        time.sleep(2)

        role = discord.utils.get(member.guild.roles, name="New Member")
        await member.send(
            f"Hope you enjoy your stay, make sure to read the <#840634593790132243> channel and follow the rules!"
        )
        await member.send(file=discord.File(fp=img, filename="welcome.png"))

        await member.add_roles(role)
        await member.send(
            f"You have been promoted to the role of a @New Member in {self.guild.name}"
        )

    @tasks.loop(hours=2)
    async def check_new_members(self):
        new_member_role = discord.utils.get(self.guild.roles, name="New Member")
        member_role = discord.utils.get(self.guild.roles, name="Member")
        members = new_member_role.members

        for member in members:
            dt_joined = member.joined_at
            dt_now = discord.utils.utcnow()

            days = (dt_now - dt_joined).days
            is_bot = member.bot

            if days >= 3 and not is_bot:
                await member.add_roles(member_role, reason="Member for >= 3 days")
                await member.remove_roles(
                    new_member_role, reason="Member for >= 3 days"
                )
                await member.send(
                    f"Congratulations, you have been promoted to the role of a @Member in {self.guild.name}"
                )

    @tasks.loop(hours=1)
    async def add_offline_roles(self):
        everyone = discord.utils.get(self.guild.roles, name="@everyone")
        new_mem = discord.utils.get(self.guild.roles, name="New Member")
        all_mem = everyone.members

        for member in all_mem:
            dt_joined = member.joined_at
            dt_now = discord.utils.utcnow()
            days = (dt_now - dt_joined).days
            is_bot = member.bot

            if days < 3 and member not in new_mem.members and not is_bot:
                await member.add_roles(
                    new_mem,
                    reason="Could not give the role due to bot maintanence, so now given.",
                )
                await member.send(
                    f"Sorry, we could not give you this role earlier but you now have been promoted to the role of a @New Member in {self.guild.name}"
                )

    @tasks.loop(seconds=20)
    async def presence(self):
        task = next(self.activities)
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.playing, name=task)
        )


async def setup(bot):
    await bot.add_cog(Events(bot))
