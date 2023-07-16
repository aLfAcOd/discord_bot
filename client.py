import random as r
import sys
import time as tm

from colorama import init

init()
from colorama import Fore

import discord
from discord import app_commands
from discord.ext import commands as com, tasks

import disTools as tools

TOKEN = None

client = com.Bot(command_prefix="  ", intents=discord.Intents.all())
client.remove_command('help')

@client.event
async def on_ready():
    print(Fore.YELLOW+f'We have logged in as {client.user}')
    change_present.start()
    try:
        synced = await client.tree.sync()
        print(Fore.RED+f'Synced with {len(synced)} command(s)')
    except: return

rich_present_current_index = 0
@tasks.loop(seconds=5)
async def change_present():
    global rich_present_current_index
    if rich_present_current_index == 0:
        await client.change_presence(activity=discord.Activity(name="/help", type=discord.ActivityType.listening), status=discord.Status.idle)
    elif rich_present_current_index == 1:
        members = []
        for mem in client.get_all_members():
            if mem.get_role(1093607341187944518) is not None:
                members.append(mem)
        await client.change_presence(activity=discord.Activity(name=f"{len(members)} learner", type=discord.ActivityType.watching), status=discord.Status.idle)

    rich_present_current_index += 1
    if rich_present_current_index > 1: rich_present_current_index = 0

@client.tree.command(name="spam", description="Spam random texts in channel")
@app_commands.describe(count="Spam message range")
async def spam(interaction: discord.Interaction, count: int):
    if not tools.hasRole(interaction.user, 1129627160492134430): return
    await interaction.response.defer()
    for i in range(count):
        s = ""
        for q in range(2000):
            s += str(chr(r.randint(97, 122)))
        await interaction.channel.send((s + "\n") * 1)

@client.tree.command(name="clear", description="Clear channel's messages")
@app_commands.describe(count="How many messages should delete")
async def clear(interaction: discord.Interaction, count: str = "all"):
    if not tools.hasRole(interaction.user, 1129629644962926716): return
    if count == "all":
        await interaction.response.defer()
        await interaction.channel.purge()
        await interaction.channel.send(embed = discord.Embed(description='همه ی پیام ها حذف شدند', colour=0x374642), delete_after=2)
    else:
        await interaction.response.defer()
        await interaction.channel.purge(limit=int(count))
        if int(count) > 1:
            await interaction.channel.send(embed = discord.Embed(description=count + ' پیام حذف شدند', colour=0x283654), delete_after=2)
        else:
            await interaction.channel.send(embed = discord.Embed(description='یک پیام حذف شد', colour=0x275642), delete_after=2)

@client.tree.command(name="post", description="Post something into channel")
@app_commands.describe(title="Title of post", thumb="Url of image of post", image="Bigger image of post", text="Content of your post")
async def post(interaction: discord.Interaction, title: str, thumb: str = None, image: str = None, *, text: str):
    if not tools.hasRole(interaction.user, 1129629974580711464): return
    await interaction.response.defer()
    emb = discord.Embed(
        title='>>> '+title,
        description=text,
        colour= r.choice([0xff0000, 0x66ff66,0x0000ff])
    )
    if thumb != 'no':
        emb.set_thumbnail(url= thumb)
    if image != 'no':
       emb.set_image(url= image)
    await interaction.channel.send(embed=emb)

@client.tree.command(name="code", description="Send code for someone")
@app_commands.describe(lang="Target language that code for", code="Target code")
async def code(interaction: discord.Interaction, lang: str = 'python', *, code: str):
    await interaction.response.defer(thinking=False, ephemeral=True)
    lang = lang.lower()
    lan = lang
    if lang.startswith("py"): lan = "py"
    if lang == "c#": lan = "cs"

    if not ["cs", "java", "c++", "cpp", "dart", "py", "ruby", "go", "arduino", "plain", "js", "html", "css", "c", "php", "r", "matlab"].__contains__(lan): lan = "plain"
    lang = {"cs": "C#", "java": "Java", "c++": "C++", "cpp": "C++", "dart": "Dart", "py": "Python", "ruby": "Ruby", "go": "Go", "arduino": "Arduino", "plain": "Plain", "js": "JavaScript", "html": "HTML", "css": "CSS", "c": "C", "php": "PHP", "r": "R", "matlab": "Matlab" }.get(lan, "plain")
    icon = {"cs": "csharp", "java": "java", "c++": "cplusplus", "cpp": "cplusplus", "dart": "dart", "py": "python", "ruby": "ruby", "go": "go", "arduino": "arduino", "plain": "travis", "js": "javascript", "html": "html", "css": "css", "c": "c", "php": "php", "r": "r", "matlab": "matlab" }.get(lan, "travis")
    membed = discord.Embed(
        title= lang,
        description=f'```{lan}\n{code}```',
        colour=0x0000ff
    ).set_thumbnail(url=f"https://cdn.jsdelivr.net/gh/devicons/devicon/icons/{icon}/{icon}-original.svg")\
        .set_footer(text="By " + interaction.user.display_name,icon_url='https://s27.picofile.com/file/8459782442/m.png')
    await interaction.channel.send(embed=membed)

@client.tree.command(name="support", description="Had into a problem?? Use command & Will help you")
@app_commands.describe(message="Your problem")
async def support(interaction: discord.Interaction, *, message: str):
    await discord.Guild.get_channel(interaction.guild, 1129420151348015136).send(
        content="||"+discord.Guild.get_role(interaction.guild, 1093609257166983208).mention + "||",
        embed=discord.Embed(
            title=interaction.user.display_name + " به کمک نیاز دارد!",
            description=message,
            colour=0xff0000
        ).set_thumbnail(url=interaction.user.display_avatar.url),
        silent=False
    )
    await interaction.response.send_message(embed=
        discord.Embed(
            description='با موفقیت ارسال شد',
            colour=0x758834
        ),
        ephemeral=True
    )

@client.tree.command(name="javab", description="Answer someone's support request")
@app_commands.describe(cont="Target user", message="Your answer for question")
async def javab(interaction: discord.Interaction, cont: discord.User, *, message: str):
    if not tools.hasRole(interaction.user, 1129630151924273213): return
    await cont.send(
        embed=discord.Embed(
            title='پیام از طرف پشتیبانی',
            description=message,
            colour= 0xff0000
        )
    )
    await interaction.response.send_message(embed=
        discord.Embed(
            title=':)',
            description='با موفقیت ارسال شد',
            colour= 0x0000ff
        ),
        ephemeral=True
    )

@client.tree.command(name="help", description="Help command")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(embed=
        discord.Embed(
            title='>>> لیست کامند ها',
            description="""**/clear** جلوش تعداد پیام هایی رو که میخواین مینویسین اونم پاک میکنه
            فقط باید دقت کنید که تو چنر عمومی باشه
            ------------------------
            **/code** 
           اینم باید توچنل عمومی استفاده کنید 
            باید کامند رو بنویسید بعد زبان کد و بعد  کد رو پیست کنید
            ------------------------
            **/support**
            اگر کاری با پشتیبان داشتید این کامند رو بنویسید و بعد پیامتون روبنویسید
            """
            ,
            colour=  0x66ff66,
    ).set_footer(text='code assistant bot', icon_url='https://s27.picofile.com/file/8459782442/m.png').set_author(name='help'),
                                            ephemeral=True)

@client.tree.command(name="stop", description="stop the bot from working")
async def stop(interaction: discord.Interaction):
    if interaction.user.id == 952960349152366663 or interaction.user.id == 818719435673042964:
        await interaction.response.send_message(embed = discord.Embed(title= "هویت ادمین تایید شد", description='ربات در 10 ثانیه دیگر خاموش میشود', colour= 0x534786), ephemeral=True)
        await client.change_presence(status=discord.Status.invisible, activity=discord.Game(name= 'turned off', type = 3))
        tm.sleep(10)
        sys.exit()
    else:
        await interaction.response.send_message('هویت شما برای خاموش کردن ربات تایید نشد', ephemeral=True)

@client.tree.command(name="announce", description="Announce news")
@app_commands.describe(message="Content of your announcement")
async def announce(interaction: discord.Interaction, *, message: str):
    if not tools.hasRole(interaction.user, 1129630537330479144): return
    await client.get_channel(1101905616638849104).send(message)

client.run(TOKEN)
