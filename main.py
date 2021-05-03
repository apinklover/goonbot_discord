import discord
from discord.ext import commands, tasks
import random
from discord.utils import get
import urllib.parse, urllib.request, re
import youtube_dl

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = ';', intents = intents)
status = "monkaW"
client.remove_command('help')

@client.event # CONSOLE OUTPUT
async def on_ready():
    await client.change_presence(activity=discord.Game(status))
    print("GoonBot is up and working!")

@client.event # CONSOLE OUTPUT
async def on_member_join(member):
    print(f"{member} has just joined the server.")

@client.event # CONSOLE OUTPUT
async def on_member_remove(member):
    print(f"{member} has left the server.")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("Unknown command. Maybe try `;help`?")
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Enter all the required arguments.")
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.send("Make sure the argument passed in matches the required data type.")
    elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("You do not have sufficient permissions to execute that command.")

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! - {int(client.latency * 1000)}ms")

@client.command(aliases = ['8ball', 'eightball'])
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful."]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit = amount + 1)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason = reason)
    await ctx.send(f"Kicked {member.mention}")

@client.command()
@commands.has_permissions(kick_members=True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f"Banned {member.mention}")

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")

@client.command()
async def ppsize(ctx):
    size = ["ᵐᶦᶜʳᵒˢᶜᵒᵖᶦᶜ", "teeny", "smol", "meh", "larj", "huj", "MASSIVE", "**GIGANTIC**", "**H U M O N G O U S**"]
    await ctx.send(f"Your PP size: {random.choice(size)}")

@client.command()
async def howpog(ctx):
    pog_meter = random.randint(0, 100)
    if pog_meter < 26:
        await ctx.send(f"You are {pog_meter}% pog. :Sadge:")
    elif 25 < pog_meter < 69:
        await ctx.send(f"You are {pog_meter}% pog. :WeirdChamp:")
    elif pog_meter == 69:
        await ctx.send(f"You are {pog_meter}% pog. :Nice:")
    elif 69 < pog_meter < 100:
        await ctx.send(f"You are {pog_meter}% pog. :POGGERS:")
    else:
        await ctx.send(f"You are {pog_meter}% pog. :PogChamp:")

@client.command()
async def ytlink(ctx, *, search_query):
    query_string = urllib.parse.urlencode({"search_query": search_query})
    htm_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
    await ctx.send("Here is your YouTube video:")
    await ctx.send("http://www.youtube.com/watch?v=" + search_results[0])

@client.command()
async def help(ctx):
    await ctx.send(f"**These are the current bot commands. <required> [optional]**\n"
                   f"**BOT PREFIX =** `;`\n"
                   f"\n"
                   f"*Fun Commands*\n"
                   f"\n"
                   f"`ping` Reports latency in milliseconds.\n"
                   f"`8ball <string>` An 8-Ball. Aliases are `_8ball` and `eightball`.\n"
                   f"`ppsize` HOW BIG IS UR PP?\n"
                   f"`howpog` Determines your poggers status, represented as a percentage.\n"
                   f"`ytlink <string>` Gets first YouTube search result and sends its URL.\n"
                   f"\n"
                   f"*Administrative*\n"
                   f"\n"
                   f"`clear [int]` Delete specified amount of messages. If not specified, delete 5.\n"
                   f"`kick <@mention>` Kick specified member.\n"
                   f"`ban <@mention> [string]` Ban specified member with an optional reason.\n"
                   f"`unban <@mention> [string]` Unban specified member with an optional reason.")

client.run(" ENTER BOT ADDRESS HERE ")
