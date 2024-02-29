# Create a new file called cog_example.py
# Import the necessary modules
import typing
import discord
from discord.ext import commands
from discord import app_commands
import traceback
# Create a class for your cog
import asyncio
import gspread
import requests


class Tours(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.sheet_key = '1E8fmroZgGrTYWs4kIdzLFd5y-k5P14dRWLQ13xYz7Rw'
    sheet_credential = gspread.service_account('keys.json')
    self.spreadsheet = sheet_credential.open_by_key(self.sheet_key)
    worksheet = self.spreadsheet.worksheet('team_info')
    self.playing_teams = worksheet.col_values(1)
    print(self.playing_teams)

  @commands.hybrid_command(name='refresh',
                           description="Refresh the team info data")
  async def refresh(self, ctx):
    await ctx.defer()
    self.sheet_key = '1E8fmroZgGrTYWs4kIdzLFd5y-k5P14dRWLQ13xYz7Rw'
    sheet_credential = gspread.service_account('keys.json')
    self.spreadsheet = sheet_credential.open_by_key(self.sheet_key)
    worksheet = self.spreadsheet.worksheet('team_info')
    self.playing_teams = worksheet.col_values(1)
    print(self.playing_teams)
    await ctx.send("Data Refreshed ! ")

  @commands.hybrid_command(name="member_info",description="returns players discord id")
  async def member_info(self,ctx,member:discord.Member=None):
        if member == None:
          embed = discord.Embed(title=f"**{ctx.guild.name}**",description="member info",colour = discord.Colour.gold())
          embed.add_field(name="``Member      :``",value = f"{ctx.author.mention}",inline=True)
          embed.add_field(name="``Discord tag :``",value = f"**{ctx.author.name}**",inline=True)
          embed.add_field(name="``Discord Id  :``",value = f"**{ctx.author.id}**",inline=True)
          embed.set_footer(text="Created and managed by CEA")
          await ctx.send(f"{ctx.author.mention} ID : {ctx.author.id}",embed=embed)
        else:
          embed = discord.Embed(title=f"**{ctx.guild.name}**",description="member info",colour = discord.Colour.gold())
          embed.add_field(name="``Member      :``",value = f"{member.mention}",inline=True)
          embed.add_field(name="``Discord tag :``",value = f"**{member.name}**",inline=True)
          embed.add_field(name="``Discord Id  :``",value = f"**{member.id}**",inline=True)
          embed.set_footer(text="Created and managed by CEA")
          await ctx.send(f"{member.mention} ID : {member.id}",embed=embed)
          
  
  @commands.command()
  async def syncs(self, ctx):
    self.bot.tree.copy_global_to(guild=ctx.guild)
    await self.bot.tree.sync()
    await self.bot.tree.sync(guild=ctx.guild)
    await ctx.reply("```Commands synced to the server ! ```")

  async def team_detail_autocompletion(
      self, ctx: commands.Context,
      current: str) -> typing.List[app_commands.Choice[str]]:
    data = [
        app_commands.Choice(name=team, value=team)
        for team in self.playing_teams
        if team.lower().startswith(current.lower())
    ]
    data = data[:24]
    return data

  @commands.hybrid_command(name="team_info",
                           description="Load the tour player info")
  @app_commands.autocomplete(team_name=team_detail_autocompletion)
  async def challonge_tournament(self, ctx, team_name: str):
    await ctx.defer()
    worksheet = self.spreadsheet.worksheet('team_info')
    k = worksheet.find(team_name)
    s = worksheet.row_values(int(k.row))
    col_name = worksheet.row_values(1)
    embed = discord.Embed(
        title=f"**{team_name}**",
        description=f"Here you can see all the info of the **{team_name}** team"
    )
    for i, j in enumerate(s):
      if i > 1:
        if j.isnumeric():
          j = discord.utils.get(ctx.guild.members, id=int(j))
          if j == None:
            embed.add_field(name=f"{col_name[i]}", value=f"**{j}**")
          else:
            embed.add_field(name=f"{col_name[i]}",
                            value=f"{j.name} - {j.mention}")
        else:
          embed.add_field(name=f"{col_name[i]}", value=f"**{j}**")
    file = discord.File('logo.png')
    embed.set_thumbnail(url="attachment://logo.png")
    embed.set_footer(text="Created & Managed by **CEA**")
    await ctx.send(embed=embed)


async def setup(bot):
  await bot.add_cog(Tours(bot))
