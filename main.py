import discord
from discord.ext import commands
import asyncio
import os
import keep_alive
import json

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix="!", intent=intents, case_insensitive=True)

filter_words = ["dick", "fuck", "arse", "bitch", "boob"]

#start
@client.event
async def on_ready():
    print("The bot is ready to go!")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))

#ping command
@client.command()
async def ping(ctx):
	await ctx.send(f'Pong! :ping_pong:  `{round(client.latency * 1000)}ms`')

#clear command
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int =None):
    if amount == None:
        await ctx.send("Please specify the amount of messages to be cleared next time!")
        return
    
    if amount > 100:
        await ctx.send("The the limit of the messages to be cleared is till `100`")
        return

    if amount <= 0:
        await ctx.send("The amount of messages to be cleared can't be 0 or less than 0!")
        return

    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"Succesfully purged {amount} messages", delete_after=3)

#clear error
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permissions to use this command!")
        return
    
    else:
        await ctx.send(error)
        return

#mute command
@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member = None, mute_time = None, *, reason = "No reason provided"):
    if member == None:
        await ctx.send("Who do you want me to mute?! Please mention someone next time")
        return

    if member == ctx.author:
        await ctx.send("You can't mute yourself!")
        return

    if member.top_role >= ctx.author.top_role:
        await ctx.send("You can't mute that user cause that user is same or higher than you!")
        return

    if member.id == 810911479964368906:
        await ctx.send("You can't mute me?! I am immortal!")
        return

    if member.id == 791016386200862730:
        await ctx.send("You can't mute the owner of the server!")
        return

    if mute_time == None:
        mute_time = "permenantely"

    if mute_time[-1] != 's' and mute_time[-1] != 'm' and mute_time[-1] != 'h' and mute_time[-1] != 'd' and mute_time != "permenantely":
        await ctx.send("You need to have your last digit as `s/m/h/d` for example 5h")
        return

    role = discord.utils.get(ctx.guild.roles, name="Muted")

    if member.bot == True:
        await member.add_roles(role)
        await ctx.send(f"Successfully done!\n\n\nMuted <@!{member.id}>\n\nMute Time : {mute_time}\n\nReason : {reason}")

        if mute_time != "permenantely":
            if mute_time[-1] == 's':
                e = int(mute_time[:-1])
                await asyncio.sleep(e)
                await member.remove_roles(role)
                await ctx.send(f"Unmuted {member.mention} because time is up")

            elif mute_time[-1] == 'm':
                i = int(mute_time[:-1]) * 60
                await asyncio.sleep(i)
                await member.remove_roles(role)
                await ctx.send(f"Unmuted {member.mention} because time is up")

            elif mute_time[-1] == 'h':
                p = int(mute_time[:-1]) * 3600
                await asyncio.sleep(p)
                await member.remove_roles(role)
                await ctx.send(f"Unmuted {member.mention} because time is up")

            elif mute_time[-1] == 'd':
                n = int(mute_time[:-1]) * 86400
                await asyncio.sleep(n)
                await member.remove_roles(role)
                await ctx.send(f"Unmuted {member.mention} because time is up")

    else:
        await member.add_roles(role)
        await ctx.send(f"Successfully done!\n\n\nMuted <@!{member.id}>\n\nMute Time : {mute_time}\n\nReason : {reason}\n\nMuted by : <@!{ctx.author.id}>")
        await member.send(f"You have been muted in {ctx.guild.name}\n\nMuted by : <@!{ctx.author.id}>\n\nMute Time : {mute_time}\n\nReason : {reason}")

        if mute_time != "permenantely":
            if mute_time[-1] == 's':
                e = int(mute_time[:-1])
                await asyncio.sleep(e)
                await member.remove_roles(role)
                await ctx.send(f"Unmuted {member.mention} because time is up")

            elif mute_time[-1] == 'm':
                i = int(mute_time[:-1]) * 60
                await asyncio.sleep(i)
                await member.remove_roles(role)
                await ctx.send(f"Unmuted {member.mention} because time is up")

            elif mute_time[-1] == 'h':
                p = int(mute_time[:-1]) * 3600
                await asyncio.sleep(p)
                await member.remove_roles(role)
                await ctx.send(f"Unmuted {member.mention} because time is up")

            elif mute_time[-1] == 'd':
                n = int(mute_time[:-1]) * 86400
                await asyncio.sleep(n)
                await member.remove_roles(role)
                await ctx.send(f"Unmuted {member.mention} because time is up")

#mute error
@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permissions to use this command!")
        return

    if isinstance(error, commands.MemberNotFound):
        await ctx.send("That's not a valid user?!")
        return

    else:
        await ctx.send(error)
        return    

#kick command
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None, *, reason = "No reason provided"):
    if member == None:
        await ctx.send("Please provide a member to be kicked next time!")
        return
    
    if member.id == ctx.author.id:
        await ctx.send("You can't kick yourself?!")
        return

    if member.id == 791016386200862730:
        await ctx.send("You can't kick the owner of the server?!")
        return
    
    if member.id == 810911479964368906:
        await ctx.send("You can't kick me! I am immortal!")
        return

    if member.top_role >= ctx.author.top_role:
        await ctx.send("You can't kick that user cause that user is higher or equal rank as you!")
        return

    if member.bot == True:
        await member.kick(reason=reason)
        await ctx.send(f"Succesfully kicked {member} from the server for {reason}")
        return

    await member.kick(reason=reason)
    await ctx.send(f"Succesfully kicked {member} from the server for {reason}")
    await member.send(f"You have been kicked from {ctx.guild.name} by {ctx.author} for {reason}")

#kick error
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permissions to use this command!")
        return

    if isinstance(error, commands.MemberNotFound):
        await ctx.send("That's not a valid user!")
        return

    else:
        await ctx.send(error)
        return

#unban command
@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, member=None):
    if member == None:
        await ctx.send("Who do you want to unban?! Please fulfil this requirement next time!")
        return

    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Successfully unbanned {user.name}#{user.discriminator}")
            return

    await ctx.send("That user is not banned!")

#unban error
@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permsissions to use this command!")
        return

    else:
        await ctx.send("Thats not a valid user!")
        return

#ban command
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None, *, reason="No reason provided"):
    if member == None:
        await ctx.send("Please mention someone next time you want to ban!")
        return

    else:
        if member.top_role >= ctx.author.top_role:
            await ctx.send("You can't ban that user cause that user is higher than or equal as you!")
            return

        elif member == ctx.author:
            await ctx.send("You can't ban yourself?!")
            return

        elif member.id == 791016386200862730:
            await ctx.send("You can't ban the owner of the server!")
            return

        elif member.id == 810911479964368906:
            await ctx.send("You can't ban me! I am immortal!")
            return

        else:
            await ctx.send(f"Successfully banned {member} from the server for {reason}")
            if member.bot == True:
                await member.ban(reason=reason)

            else:
                await member.send(f"You have been banned from the server {ctx.guild.name} by {ctx.author} for {reason}")
                await member.ban(reason=reason)

#ban error
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permissions to use that command!")
        return

    if isinstance(error, commands.MemberNotFound):
        await ctx.send("Thats not a valid user!")
        return

    else:
        await ctx.send(error)

#get_modmail_data function
async def get_modmail_data():
    with open("id.json","r") as f:
        users = json.load(f)

    return users

#get_accept_data function
async def get_accept_data():
    with open("accept.json","r") as f:
        users = json.load(f)

    return users

#open_accept function
async def open_accept(id_, user):
    users = await get_accept_data()

    if str(id_) in users:
        return False
    else:
        users[str(id_)] = {}
        users[str(id_)]["user"] = user.id

    with open("accept.json","w") as f:
        json.dump(users,f,indent=4)
    return True

#modmail command
@client.command()
async def modmail(ctx):
    await ctx.send("Please see your DM!")
    await ctx.author.send("What is your report for the server?")
    
    try:
        msg = await client.wait_for(
            "message",
            timeout = 300,
            check = lambda message: message.author == ctx.author
                            and message.channel == message.channel
            )

        if msg:
            channel = client.get_channel(811213147821834270)
            users = await get_modmail_data()
            number = users["id"]["number"]
            users["id"]["number"] += 1
            em = discord.Embed(title=f"ModMail from {ctx.author}\n\n", description=f"Report: {msg.content}\n\n", color=ctx.author.color)
            em.add_field(name="id", value=f"`{number}`")
            await channel.send(embed=em)
            await ctx.author.send(f"Successfully sent a ModMail to the staff with id: `{number}`. The staff will notify you soon about your modmail soon as possible!")
            with open("id.json", "w") as f:
                json.dump(users, f)
            await open_accept(number, ctx.author)

    except asyncio.TimeoutError:
        await ctx.author.send('You were late to response')

#accept command
@client.command(aliases=["ac"])
@commands.has_permissions(manage_roles=True)
async def accept(ctx, _id = None, *, response = None):
    if _id == None:
        await ctx.send("Please provide the id next time!")
        return

    if response == None:
        await ctx.send("Please provide a response next time!")
        return

    users = await get_accept_data()
    user = users[_id]["user"]
    member = await ctx.guild.fetch_member(int(user))
    await member.send(f"Your modmail with id: {_id} has been accepted! The response from the staff is: {response}. If you have any doubts, please DM {ctx.author}")
    del users[_id]

    with open('accept.json','w') as f:
        json.dump(users,f,indent=4)

    await ctx.send(f"Successfully given the response to <@!{user}>")

#accept error
@accept.error
async def accept_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permissions to use that!")
        return

    else:
        await ctx.send("Coudn't find a modmail with that id!")
        return

#cancel command
@client.command(aliases=["ca"])
@commands.has_permissions(manage_roles=True)
async def cancel(ctx, _id = None, *, response = None):
    if _id == None:
        await ctx.send("Please provide the id next time!")
        return

    if response == None:
        await ctx.send("Please provide a response next time!")
        return

    users = await get_accept_data()
    user = users[_id]["user"]
    member = await ctx.guild.fetch_member(int(user))
    await member.send(f"Your modmail with id: `{_id}` has been rejected for the following reason: {response}. If you have any doubt please DM {ctx.author} about it.")
    del users[_id]

    with open('accept.json','w') as f:
        json.dump(users,f,indent=4)

    await ctx.send(f"Successfully given the response to <@!{user}> with reason {response}")

#cancel error
@cancel.error
async def cancel_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permissions to use that command!")
        return

    else:
        await ctx.send("Coudn't find a modmail with that id!")
        return

#reaction_role event
@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 811178043732393985:
        for word in filter_words:
            if word in payload.member.name:
                await payload.member.edit(nick=payload.member.id)
                await payload.member.send("I have changed your nickname in this server to your id cause you name had inappropriate material")
                await payload.member.add_roles(client.get_guild(payload.guild_id).get_role(811179944004681818))
                await payload.member.remove_roles(client.get_guild(payload.guild_id).get_role(811229521495588914))
                return

        await payload.member.add_roles(client.get_guild(payload.guild_id).get_role(811179944004681818))
        await payload.member.remove_roles(client.get_guild(payload.guild_id).get_role(811229521495588914))
        return

#nick command
@client.command()
async def nick(ctx,*, nick=None):
    if nick == None:
        await ctx.send("Please specify the nickname argument next time!")
        return

    for word in filter_words:
        if word in nick:
            await ctx.message.delete()
            await ctx.send("Sorry I can't change your nickname to that cause that nickname has inappropriate words")
            return

    await ctx.author.edit(nick=nick)
    await ctx.send(f"Successfully changed your nickname to {nick}")

#restart command
@client.command()
@commands.has_permissions(administrator=True)
async def restart(ctx):
    users = await get_modmail_data()
    users["id"]["number"] = 1
    with open("id.json", "w") as f:
        json.dump(users,f,indent=4)

    await ctx.send("Succesfully restarted the bot!")

#run area
keep_alive.keep_alive()
token=os.environ.get('Token')
client.run(token)