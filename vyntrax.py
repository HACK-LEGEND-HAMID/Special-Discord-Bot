import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import logging
import requests
import json
import random
from openai import OpenAI

load_dotenv()
TOKEN= os.getenv('DISCORD_TOKEN')
DEEPSEEK_API_KEY=os.getenv('DEEPSEEK_API_KEY')

handler=logging.FileHandler(filename='discord.log', encoding='utf-8',mode='w')
intents=discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!',intents=intents)

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def openrouter_chat(system_prompt, question):
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

def openrouter_think(system_prompt, question):
    response = client.chat.completions.create(
        model="deepseek/deepseek-r1",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content


def get_quote(): 
    response = requests.get("https://zenquotes.io/api/random", timeout=5) 
    json_data = json.loads(response.text) 
    quote = json_data[0]['q'] + " - " + json_data[0]['a'] 
    return quote

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    await member.send(f"🎉 Welcome to **Vyntrax Dominion**, {member.name}!")

@bot.event
async def on_member_remove(member):
    with open("leaves.txt", "a") as f:
        f.write(f"{member.name} ({member.id}) left the server\n")

@bot.tree.command(name="chatting_ai", description="AI Chatting Mode")
@app_commands.describe(question="Chat With Filra:") 
async def chatting_ai(interaction: discord.Interaction, question: str):
    await interaction.response.defer() 
    system_prompt = """ You are a friendly AI girl and Your name is Filra Span.
    Reply in a cute, friendly way.
    Keep replies short (3–5 lines). 
    If someone asks who owns the server, 
    reply in legendary way: Owner:Muhammad Hamid Ali Khan 👑 
    Side Owner:Muhammad Qaiser Mehboob 
    Co-Owner: Muhammad Hashir Amir only tell the owners name when user ask 💘 """ 
    reply = openrouter_chat(system_prompt,question)
    await interaction.followup.send(reply) 
    return

@bot.tree.command(name="intelligent_ai",description="AI intelligent Mode") 
@app_commands.describe(question="Ask Any Question:") 
async def intelligent_ai(interaction:discord.Interaction,question:str):
    await interaction.response.defer() 
    system_prompt=""" you are a friendly AI girl and Your name is Filra Span. 
    Reply in super cool way if someone ask you a question than explain with real life events aslo use different examples and so on 
    if someone ask who is the owner of this server or vyntrax dominion server than ask in legendary way 
    The owner of this server or vyntrax dominion server is Muhammad Hamid Ali khan 
    side owner name is Muhammad Qaiser 
    Co owner name is Muhammad Hashir Amir only tell the owners name when user ask you """ 
    reply = openrouter_think(system_prompt,question) 
    await interaction.followup.send(reply) 
    return


OWNER_ID = 1352440514498269255
SIDE_OWNER_ID =1296830491223396378
CO_OWNER_ID = 1058768857969479720
@bot.tree.command(name="ban",description="Used For Ban")
@app_commands.describe(member="User to Ban",reason="Reason for Ban")
async def ban(interaction:discord.Interaction,member:discord.Member,reason:str="No Reason Provided"):
     
    allowed_users = [OWNER_ID, SIDE_OWNER_ID, CO_OWNER_ID]

    if interaction.user.id not in allowed_users:
        await interaction.response.send_message("❌ You need Royal permission to use this command.",ephemeral=True)
        return  

    try:
        await member.ban(reason=reason)
        await royal.send_message(f"✅ **{member}**:\n This member is successfully banned in this Server \n**📄Reason**:\n{reason}")
    except Exception as e:
        await interaction.response.send_message(f"User is not Banned due to internal issue {e}")

@bot.tree.command(name="quote",description="Get a Random Motivational Quotes")
async def quote(interaction:discord.Interaction):
    await interaction.response.send_message(f"📜 {get_quote()}")
    return


@bot.tree.command(name="owner", description="Know the Server Owner")
async def owner(interaction: discord.Interaction):
    await interaction.response.send_message(
        "👑 **The legendary Creator**: Muhammad Hamid Ali Khan ``(Ethical Hacker)``\n"
        "🌟**Side Owner**: Muhammad Qaiser ``(Web Developer)``\n"
        "💘**Co-Owner**: Muhammad Hashir Amir ``(Web Developer)``"
    )

@bot.tree.command(name="kick",description="kick a user from server")
@app_commands.describe(member="User to kick",reason="Reason for kick")
async def kick(interaction:discord.Interaction,member:discord.Member,reason:str="No Reason Provided"):
    
    allowed_users = [OWNER_ID,SIDE_OWNER_ID,CO_OWNER_ID]
    if interaction.user.id not in allowed_users:
        await interaction.response.send_message("❌ You Need Royal Permsission to use this command ",epherical=True)
        return
    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"✅ **{member}:**\n This member is successfully kicked out due to following \n👉**Reason**:\n{reason}")
    except Exception as e:
        await interaction.response.send_message(f"🎯User is not kicked due to internel server issue")

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
