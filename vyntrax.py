import os
import discord
import re
from discord.ext import commands
from dotenv import load_dotenv
import logging
import requests
import json
import random
import google.generativeai as genai
from google.genai import types
from google import genai

def ask_gemini_2(system_prompt, prompt):

    tools = [{'google_search': {}}]
    config= types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=tools
    )

    try:
        client = genai.Client()

        chat = client.chats.create(
            model="gemini-2.5-flash",
            config=config)
        response = chat.send_message(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"AI Error: {e}")
        return "Sorry, I couldn't get a reply right now. 😔"

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

bad_words = ["fuck", "fuck you", "asshole", "nigger", "gay", "bitch", "bastard", 
             "fag", "whore", "slut", "pussy", "dick", "stupid", "jerk", "ass", 
             "piss", "bhosda", "chod", "chutiya", "bsdk", "madarchod", "bc", 
             "behnchod", "lund", "randi", "gaand", "gandu", "lauda", "teri maa", 
             "behn ka", "madharchod", "madarchod", "haramzada"]


ques_pairs = {
    "who created you": "The legend Muhammad Hamid Ali Khan 👑"
}
warning_messages = [
    "⚠ Watch your mouth {user}.",
    "🚫 {user}, this isn’t a street fight.",
    "😡 {user}, language check yourself.",
    "💣 {user}, control your words before I do."
]
def get_quote():
        response = requests.get("https://zenquotes.io/api/random", timeout=5)
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " - " + json_data[0]['a']
        return quote

@bot.event
async def on_member_remove(member):
    with open("leaves.txt", "a") as f:
        f.write(f"{member.name} ({member.id}) left the server.\n")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    guild = discord.utils.get(bot.guilds, name=GUILD)
    if guild:
        print(f"🌍 Connected to guild: {guild.name} (ID: {guild.id})")
        print(f"🎯 Matched main server: {guild.name}")
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')
    else:
        print("❌ No guild found matching that name.")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the Vyntrax Dominion {member.name}! 🎉")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    msg = message.content.lower().strip()

    if msg.startswith("!ai"):
        query = message.content[3:].strip()
        if query == "":
            await message.reply("💬 Ask me something! Example: `!ai tell me a joke`")
            return
        
        thinking_msg = await message.channel.send("Thinking... 🤔")
        
        system_prompt = """
You are a friendly AI girl bot. Reply in a cute, friendly way.
Keep your answer short (3-5 lines max).
Use simple English and be helpful.
If someone says 'I love you', politely say you belong to your owner.
if someone say who is the owner of this server reply him beginner hacker Muhammad Hamid Ali khan in legendary way with beautiful quotes
side owner name sharjeel ali expert ethical hacker co owner muneeb.if person say who is ur owner u reply him beginner hacker Muhammad Hamid Ali Khan in legendary way...one more thing which i want to tell u is that i am using ur api but u are in discord group so make ur message eye catching and beautiful talk like human girl
"""

        prompt = f"""
{system_prompt}
User question: {query}
Reply:"""
        

        reply = ask_gemini_2(system_prompt,query)
        await thinking_msg.delete()
        await message.channel.send(reply)
        return
    
    if message.content.startswith("$"):
        user_msg = message.content[1:].strip().lower()
        if user_msg in ques_pairs:
            await message.channel.send(ques_pairs[user_msg])
            return
        elif user_msg == "give_quote":
            quote = get_quote()
            await message.channel.send(f"📜 {quote}")
            return
        else:
            await message.channel.send("Hmm... I don't have an answer for that yet 🤔")
            return

    msg = message.content.lower().strip()
    for word in bad_words:
        if re.search(rf'\b{re.escape(word)}\b', msg):
            await message.delete()
            warning = random.choice(warning_messages).format(user=message.author.mention)
            await message.channel.send(warning)
            return


    
    await bot.process_commands(message)

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
