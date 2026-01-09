import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import logging
import requests
import json
import random
import google.generativeai as genai
from google.genai import types
from google import genai

user_sessions = {}

def ask_gemini_3(system_prompt, question, previous_id=None):
    try:
        client = genai.Client()

        tools = [{'google_search': {}}]
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=tools
        )

        chat = client.chats.create(
            model="gemini-3-flash-preview",
            config=config
        )

        if previous_id:
            response = chat.send_message(question, previous_interaction_id=previous_id)
        else:
            response = chat.send_message(question)

        return response.text.strip(), chat.id

    except Exception as e:
        print("AI Error:", e)
        return "Sorry, I couldn't reply 😔", None



def get_quote(): 
    response = requests.get("https://zenquotes.io/api/random", timeout=5) 
    json_data = json.loads(response.text) 
    quote = json_data[0]['q'] + " - " + json_data[0]['a'] 
    return quote

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

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


@bot.tree.command(name="ai", description="Ask AI anything")
@app_commands.describe(question="Ask your question")
async def ai(interaction: discord.Interaction, question: str):
    
    await interaction.response.defer()
    system_prompt = """
You are a friendly AI girl and Your name is Filra Span.
Reply in a cute, friendly way.
Keep replies short (3–5 lines).
If someone asks who owns the server,
reply in a legendary way:
Owner:Muhammad Hamid Ali Khan 👑
Side Owner:Muhammad Qaiser Mehboob
Co-Owner: Muhammad Hashir Amir 💘
"""
    
    user_id = interaction.user.id

    previous_id = user_sessions.get(user_id)  

    reply, new_id = ask_gemini_3(
        system_prompt,
        question,
        previous_id
    )

    if new_id:
        user_sessions[user_id] = new_id 

    await interaction.followup.send(reply)



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

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
