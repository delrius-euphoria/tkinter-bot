import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
import utils.messages
from discord.utils import format_dt
from classes.resource import Resource

res = Resource()


class Commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="describe",
        description="Provide a basic introduction to the constructor call and link to more info",
    )
    @app_commands.choices(
        widget=[Choice(name=wid, value=wid) for wid in res.get_all_widgets()]
    )
    @app_commands.describe(widget="The widget to which you want the information about")
    # @app_commands.autocomplete(widget=wid_autocomplete)
    async def describe(self, interaction: discord.Interaction, widget: Choice[str]):
        await interaction.response.defer()

        res.reload_resource()

        wid = widget.value
        color = interaction.user.roles[-1].color

        desc = res.get_desc(wid)
        code = res.get_code(wid)
        link = res.get_link(wid)

        embed = discord.Embed(title=f"`{wid}`", color=color)
        embed.description = desc
        embed.add_field(name="Usage:", value=f"```py\n{code}```")
        embed.add_field(
            name="URL:", value=f"[Jump to the documentation]({link})", inline=False
        )

        await interaction.followup.send(embed=embed)

    @app_commands.command(
        name="docs", description="Provide link to good tkinter documentations"
    )
    async def docs(self, interaction: discord.Interaction):
        res.reload_resource()

        color = interaction.user.roles[-1].color
        embed = discord.Embed(
            title="Documentations",
            description="The 3 documentations that we have found useful are:",
            color=color,
        )
        embed.add_field(
            name="NMT docs(Anzel's version)", value=utils.messages.DOCS_ANZEL
        )
        embed.add_field(name="TkDocs", value=utils.messages.DOCS_TK, inline=False)
        embed.add_field(
            name="tkinterbook(Effbot)", value=utils.messages.DOCS_EFFBOT, inline=False
        )
        embed.add_field(
            name="Found more quality docs?",
            value=f"If you found a good documentation and would like to share with us, feel free to post it in the <#873683336118300713> channel for review",
            inline=False,
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="code", description="Guideline for pasting code in discord"
    )
    @app_commands.describe(member="Member to tag, if any")
    async def code(
        self, interaction: discord.Interaction, member: discord.Member = None
    ):
        color = interaction.user.roles[-1].color
        embed = discord.Embed(description=utils.messages.code_block, color=color)
        if member:
            return await interaction.response.send_message(
                f"<@{member.id}>", embed=embed
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="subscribe", description="Command to subscribe to optionalannouncements"
    )
    @app_commands.choices(
        role=[
            Choice(name=val, value=val)
            for val in ["Bot Announcements", "Challenge Announcements"]
        ]
    )
    @app_commands.describe(role="The announcement you want to subscribe to")
    @app_commands.guild_only()
    async def subscribe(self, interaction: discord.Interaction, role: Choice[str]):
        await interaction.response.defer(ephemeral=True)

        needed_role = discord.utils.get(interaction.guild.roles, name=role.value)
        await interaction.user.add_roles(needed_role)

        color = interaction.user.roles[-1].color
        embed = discord.Embed(
            description=f"Successfully subscribed to {role.value.lower()}", color=color
        )

        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(
        name="unsubscribe",
        description="Command to unsubscribe to optionalannouncements",
    )
    @app_commands.choices(
        role=[
            Choice(name=val, value=val)
            for val in ["Bot Announcements", "Challenge Announcements"]
        ]
    )
    @app_commands.describe(role="The announcement you want to subscribe to")
    @app_commands.guild_only()
    async def unsubscribe(self, interaction: discord.Interaction, role: Choice[str]):
        await interaction.response.defer(ephemeral=True)

        uneeded_role = discord.utils.get(interaction.guild.roles, name=role.value)
        await interaction.user.remove_roles(uneeded_role)

        color = interaction.user.roles[-1].color
        embed = discord.Embed(
            description=f"Successfully unsubscribed to {role.value.lower()}",
            color=color,
        )

        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(
        name="paste", description="Guideline for pasting long lines of code in discord"
    )
    @app_commands.describe(member="Member to tag, if any")
    async def paste(
        self, interaction: discord.Interaction, member: discord.Member = None
    ):
        color = interaction.user.roles[-1].color

        embed = discord.Embed(description=utils.messages.long_code, color=color)
        if member:
            return await interaction.response.send_message(
                f"<@{member.id}>", embed=embed
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="age",
        description="Command to see how long you have been in the server for",
    )
    @app_commands.describe(member="Member you want to see the age of, if any")
    @app_commands.guild_only()
    async def age(
        self, interaction: discord.Interaction, member: discord.Member = None
    ):
        color = interaction.user.roles[-1].color
        if member is None:
            member = interaction.user

        dt_joined = format_dt(member.joined_at, "R")

        embed = discord.Embed(
            description=f"<@{member.id}> joined {dt_joined}", color=color
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="count", description="Command to see the count of server members"
    )
    @app_commands.guild_only()
    async def count(self, interaction: discord.Interaction):
        await interaction.response.defer()
        member_count = len(
            [
                member
                async for member in interaction.guild.fetch_members()
                if not member.bot
            ]
        )
        
        color = interaction.user.roles[-1].color
        count_embed = discord.Embed(
            description=f"Member Count: **{member_count}**", color=color
        )
        await interaction.followup.send(embed=count_embed)

    @app_commands.command(name="faq", description="Command to show FAQs on tkinter")
    @app_commands.choices(
        question=[Choice(name=q, value=q) for q in utils.messages.FAQ.keys()]
    )
    @app_commands.describe(
        question="Question to provide the link for", member="Member to tag, if any"
    )
    async def faq(
        self,
        interaction: discord.Interaction,
        question: Choice[str] = "",
        member: discord.Member = None,
    ):
        color = interaction.user.roles[-1].color
        embed = discord.Embed(color=color)

        if question:
            embed.title = question.value
            link = utils.messages.FAQ[question.value]
            embed.description = f"[Link to the post]({link})"
            if member:
                return await interaction.response.send_message(
                    f"<@{member.id}>", embed=embed
                )

            return await interaction.response.send_message(embed=embed)

        embed.title = "FAQs on tkinter"
        for q, link in utils.messages.FAQ.items():
            embed.add_field(name=q, value=f"[Link to the post]({link})", inline=False)
        else:
            embed.add_field(
                name="Are we missing some FAQs?",
                value="If we missed an FAQ and you would like to share with us, feel free to post it in the <#873683336118300713> channel for review",
                inline=False,
            )

        if member:
            return await interaction.response.send_message(
                f"<@{member.id}>", embed=embed
            )

        return await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Commands(bot))
