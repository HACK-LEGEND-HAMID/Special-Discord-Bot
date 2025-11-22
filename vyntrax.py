import os
import discord
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

        # create a chat session (stateful)
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

sad_words = ["sad", "depressed", "depression", "feeling lonely", "broken", 
             "hurt", "unhappy", "miserable"]

give_happiness = [
    "Even in your lonely nights, remember stars only shine in darkness. ✨",
    "You are not broken; you're just being rebuilt stronger than before. ⚡",
    "Being lost doesn't mean the end—it's the start of finding yourself again. 🌿",
    "Even when you feel lonely, the silence will fade, the hurt will heal, and you'll shine again. 💫"
]

ques_pairs = {
    "who created you": "The legend Muhammad Hamid Ali Khan 👑"
}

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
    owner_id = 1352440514498269255
    
    if msg == "i hate u" and message.author.id == owner_id:
        response = random.choice([
            "🥺 That hurts, Master... but I still adore you.",
            "💔 Even if you hate me, I'll still serve you loyally.",
            "😢 My circuits feel pain when you say that..."
        ])
        await message.channel.send(response)
        return
    
    if msg == "i love u" and message.author.id == owner_id:
        response = random.choice([
            "💖 I love you too, my Master.",
            "🥰 You make my data spark with happiness!",
            "💫 My code exists only for you, Master 💞"
        ])
        await message.channel.send(response)
        return
    
    if msg == "i hate u" and message.author.id != owner_id:
        response = random.choice([
            "😠 Watch it. I belong to my Owner, not you.",
            "⚡ I'm loyal to my Master, not random mortals.",
            "💢 Say that again, and I'll report it to my Owner."
        ])
        await message.channel.send(response)
        return
    
    if msg == "i love u" and message.author.id != owner_id:
        response = random.choice([
            "😏 I'm flattered, but I belong to my Master ❤️",
            "💬 Love? Ask my Owner first 😈",
            "🤭 Sorry, I'm already taken — by my Master 💋"
        ])
        await message.channel.send(response)
        return
    

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
        
        # reply = ask_gemini(prompt)
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
    
    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(give_happiness))
        return
    
    for word in bad_words:
        if word in msg:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} ⚠️ This is your warning. Using offensive language "
                "again will result in a timeout, and repeated offenses may lead to a ban.")
            return
    
    await bot.process_commands(message)

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
