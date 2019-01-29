import discord
from discord.ext import commands
from discord import Server
from discord.ext.commands import has_permissions

TOKEN = 'NTM5ODc2Nzg1ODUzMTY5NjY2.DzIv4A.lg1tScbUXOkn-tkucBp63YTG-LQ'

commandPrefix = ":"
warnlog = "warn-log"
banlog = "ban-log"
muterole = "Muted"

client = commands.Bot(command_prefix=commandPrefix)
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="use "+ commandPrefix + "help"))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.author.bot:
        return;
    print("A user has sent a message.")
    await client.process_commands(message)


@client.command()
@has_permissions(administrator=True)
async def setwarnlog(loginput="log"):
    global warnlog
    warnlog = loginput


@client.command()
@has_permissions(administrator=True)
async def setbanlog(loginput="log"):
    global banlog
    banlog = loginput


@client.command()
@has_permissions(administrator=True)
async def setmuterole(roleinput="Muted"):
    global muterole
    muterole = roleinput


@client.command(pass_context=True)
async def help(ctx):
    channel = ctx.message.channel

    embed = discord.Embed(
        title="Help\a",
        description=" ",
        colour=discord.Colour.gold()
    )

    embed.add_field(name="\a", value="\a", inline=False)
    embed.add_field(name="Setup Commands:", value="\a", inline=False)
    embed.add_field(name=commandPrefix + "setmuterole [role name]", value="Sets the muted role.", inline=False)
    embed.add_field(name=commandPrefix + "setwarnlog [channel name]", value="Sets the warn log channel.", inline=False)
    embed.add_field(name=commandPrefix + "setbanlog [channel name]", value="Sets the warn log channel.\a\a", inline=False)
    embed.add_field(name="\a", value="\a", inline=False)
    embed.add_field(name="Moderation Commands:", value="\a", inline=False)
    embed.add_field(name=commandPrefix + "warn [user] [reason]", value="Warns a user for breaking a rule.", inline=False)
    embed.add_field(name=commandPrefix + "mute [user] [reason]", value="Mutes a user for breaking a rule.", inline=False)
    embed.add_field(name=commandPrefix + "unmute [user] [reason]", value="Unmutes a user.", inline=False)
    embed.add_field(name=commandPrefix + "ban [user] [reason]", value="Bans a user for breaking a rule.", inline=False)
    embed.add_field(name=commandPrefix + "unban [user] [reason]", value="Unbans a user.", inline=False)
    embed.add_field(name=commandPrefix + "clear [amount]", value="Clears all previous messages up to a certain amount.\a\a", inline=False)
    embed.add_field(name=commandPrefix + "banlist", value="Lists all banned users.", inline=False)

    await client.send_message(channel, embed=embed)


@client.command(pass_context=True)
@has_permissions(kick_members=True, ban_members=True, administrator=True)
async def warn(ctx, user: discord.Member, *infractions):
    try:
        if ctx.message.author.top_role > user.top_role:
            channel = ctx.message.channel
            logchannel = discord.utils.get(ctx.message.server.channels, name=warnlog)
            embed = discord.Embed(
                title="Warning",
                description="_ _",
                colour=discord.Colour.orange()
            )

            if len(infractions) > 0:
                output = ""
                for word in infractions:
                    output += word
                    output += " "
                embed.set_footer(text="Moderator - " + ctx.message.author.name)
                embed.add_field(name="User warned:", value="{}".format(user), inline=True)
                embed.add_field(name="Reason:", value=output, inline=True)

                await client.send_message(channel, embed=embed)
                await client.send_message(logchannel, embed=embed)
            else:
                embed.set_footer(text="Moderator - " + ctx.message.author.name)
                embed.add_field(name="User warned:", value="{}".format(user), inline=True)
                embed.add_field(name="Reason:", value="Unspecified.", inline=True)

                await client.send_message(channel, embed=embed)
                await client.send_message(logchannel, embed=embed)
        else:
            await client.say("That user has a role higher in the hierarchy than you, I can't do that.")
    except discord.ext.commands.CheckFailure:
        await client.say("That user has a role higher in the hierarchy than you, I can't do that.")


@client.command(pass_context=True)
@has_permissions(ban_members=True, administrator=True)
async def ban(ctx, user: discord.Member, *infractions):
    try:
        if ctx.message.author.top_role > user.top_role:
            channel = ctx.message.channel
            logchannel = discord.utils.get(ctx.message.server.channels, name=banlog)
            embed = discord.Embed(
                title="Ban",
                description="_ _",
                colour=discord.Colour.red()
            )

            if len(infractions) > 0:
                output = ""
                for word in infractions:
                    output += word
                    output += " "
                embed.set_footer(text="Moderator - " + ctx.message.author.name)
                embed.add_field(name="User warned:", value="{}".format(user), inline=True)
                embed.add_field(name="Reason:", value=output, inline=True)

                await client.ban(user)
                await client.send_message(channel, embed=embed)
                await client.send_message(logchannel, embed=embed)
            else:
                embed.set_footer(text="Moderator - " + ctx.message.author.name)
                embed.add_field(name="User warned:", value="{}".format(user), inline=True)
                embed.add_field(name="Reason:", value="Unspecified.", inline=True)

                await client.ban(user)
                await client.send_message(channel, embed=embed)
                await client.send_message(logchannel, embed=embed)
        else:
            await client.say("That user has a role higher in the hierarchy than you, I can't do that.")
    except discord.ext.commands.CheckFailure:
        await client.say("That user has a role higher in the hierarchy than you, I can't do that.")


@client.command(pass_context = True)
@has_permissions(kick_members=True, ban_members=True, administrator=True)
async def mute(ctx, member: discord.Member, *infractions):
    try:
        if ctx.message.author.top_role > member.top_role:
            role = discord.utils.get(member.server.roles, name='Muted')
            await client.add_roles(member, role)
            embed=discord.Embed(
                title="Mute",
                description="_ _",
                color=discord.Colour.dark_gold()
            )
            output = ""
            if len(infractions) > 0:
                for word in infractions:
                    output += word
                    output += " "
                embed.add_field(name="User muted:", value="{}".format(member), inline=True)
                embed.add_field(name="Reason:", value=output, inline=True)
                embed.set_footer(text="Moderator - " + ctx.message.author.name)
                await client.say(embed=embed)
            else:
                embed.add_field(name="User muted:", value="{}".format(member), inline=True)
                embed.add_field(name="Reason:", value="Unspecified.", inline=True)
                embed.set_footer(text="Moderator - " + ctx.message.author.name)
                await client.say(embed=embed)
        else:
            await client.say("That user has a role higher in the hierarchy than you, I can't do that.")
    except discord.ext.commands.CheckFailure:
        await client.say("That user has a role higher in the hierarchy than you, I can't do that.")

@client.command(pass_context = True)
@has_permissions(kick_members=True, ban_members=True, administrator=True)
async def unmute(ctx, member: discord.Member, *infractions):
    try:
        if ctx.message.author.top_role > member.top_role:
            role = discord.utils.get(member.server.roles, name='Muted')
            await client.remove_roles(member, role)
            embed=discord.Embed(
                title="Unmute",
                description="",
                color=discord.Colour.teal()
            )
            if len(infractions) > 0:
                output = ""
                for word in infractions:
                    output += word
                    output += " "
                embed.add_field(name="User unmuted:", value="{}".format(member), inline=True)
                embed.add_field(name="Reason:", value=output, inline=True)
                embed.set_footer(text="Moderator - " + ctx.message.author.name)
                await client.say(embed=embed)
            else:
                output = ""
                for word in infractions:
                    output += word
                    output += " "
                embed.add_field(name="User unmuted:", value="{}".format(member), inline=True)
                embed.add_field(name="Reason:", value="Unspecified", inline=True)
                embed.set_footer(text="Moderator - " + ctx.message.author.name)
                await client.say(embed=embed)
        else:
            await client.say("That user has a role higher in the hierarchy than you, I can't do that.")
    except discord.ext.commands.CheckFailure:
        await client.say("That user has a role higher in the hierarchy than you, I can't do that.")

@client.command(pass_context=True)
@has_permissions(kick_members=True, ban_members=True, administrator=True)
async def banlist(ctx):
    logchannel = discord.utils.get(ctx.message.server.channels, name=banlog)
    embed = discord.Embed(
        title="Ban List",
        description="_ _",
        colour=discord.Colour.red()
    )
    embed.set_footer(text="Moderator - " + ctx.message.author.name)
    bannedUsers = await client.get_bans(ctx.message.server)
    if len(bannedUsers) > 0:
        user_number = 0;
        for user in bannedUsers:
            user_number = user_number + 1
            embed.add_field(name="Banned user #" + str(user_number) + ":", value="{}".format(user), inline=True)
        await client.send_message(ctx.message.channel, embed=embed)
        await client.send_message(logchannel, embed=embed)
    else:
        await client.send_message(ctx.message.channel, "No bans!")


@client.command(pass_context=True)
@has_permissions(ban_members=True, administrator=True)
async def unban(ctx, user_name, *infractions):
    for member in ctx.message.server.members:
        try:
            if ctx.message.author.top_role > member.top_role:
                channel = ctx.message.channel
                logchannel = discord.utils.get(ctx.message.server.channels, name=banlog)
                embed = discord.Embed(
                    title="Unban",
                    description="_ _",
                    colour=discord.Colour.green()
                )

                bannedUsers = await client.get_bans(ctx.message.server)
                for user in bannedUsers:
                    if user.display_name == user_name:
                        break;

                if len(infractions) > 0:
                    output = ""
                    for word in infractions:
                        output += word
                        output += " "


                    embed.set_footer(text="Moderator - " + ctx.message.author.name)
                    embed.add_field(name="User unbanned:", value="{}".format(user), inline=True)
                    embed.add_field(name="Reason:", value=output, inline=True)

                    await client.unban(ctx.message.server, user)
                    await client.send_message(channel, embed=embed)
                    await client.send_message(logchannel, embed=embed)

                    break;
                else:
                    embed.set_footer(text="Moderator - " + ctx.message.author.name)
                    embed.add_field(name="User unbanned:", value="{}".format(user), inline=True)
                    embed.add_field(name="Reason:", value="Unspecified.", inline=True)

                    await client.unban(ctx.message.server, user)
                    await client.send_message(channel, embed=embed)
                    await client.send_message(logchannel, embed=embed)

                    break;
            else:
                await client.say("That user has a role higher in the hierarchy than you, I can't do that.")
        except discord.ext.commands.CheckFailure:
            await client.say("That user has a role higher in the hierarchy than you, I can't do that.")


@client.command(pass_context=True)
@has_permissions(kick_members=True, ban_members=True, administrator=True)
async def clear(ctx, amount=1000000):
    if ctx.message.author.server_permissions.manage_messages:
        channel = ctx.message.channel
        messages = []
        amount = amount + 1
        async for message in client.logs_from(channel, limit = int(amount)):
            messages.append(message)
        await client.delete_messages(messages)
        await client.say("Messages deleted.")



client.run(TOKEN)