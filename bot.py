import os
import discord
from discord.ext import commands 
from dotenv import load_dotenv
from openai import OpenAI
import logging


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
OPEN_ROUTER_KEY = os.getenv('OPEN_ROUTER')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.moderation = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def LLM_response(messages):
    """Send messages to OpenRouter LLM and get response"""
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPEN_ROUTER_KEY,
        )
        
        if isinstance(messages, list):
            if not any(msg.get("role") == "system" for msg in messages):
                messages = [{"role": "system", "content": "You are a helpful AI assistant. Keep responses concise and under 1000 characters. Be direct and to the point."}] + messages
        else:
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant. Keep responses concise and under 1000 characters. Be direct and to the point."},
                messages
            ]
        
        completion = client.chat.completions.create(
                model="deepseek/deepseek-r1:free",
                messages=messages,
                max_tokens=600,  
                temperature=0.7
            )  
        
        
        response = completion.choices[0].message.content
        
        # Truncate response if too long for Discord (1900 chars to be safe)
        if len(response) > 1900:
            response = response[:1900] + "...\n\n*Response truncated due to length limit*"
        
        return response
        
    except Exception as e:
        print(f"Error in LLM_response: {e}")
        return f"Sorry, I encountered an error: {str(e)}"

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')

@bot.event
async def on_message(message):
    print(f"Received a message from {message.author} in {type(message.channel)}: {message.content}")  # Debug print

    if message.author == bot.user:
        return 

    if "@ai" in message.content.lower():
        question = message.content.replace("@ai", "").strip()
        if not question:
            await message.channel.send("Please provide a question after @ai")
            return

        print(f"Processing AI request: {question}")

        # Server text channel: create thread
        if isinstance(message.channel, discord.TextChannel):
            try:
                # Create a thread on the message
                thread = await message.create_thread(
                    name=f"AI Thread: {question[:20]}",
                    auto_archive_duration=60
                )
                
                thinking_msg = await thread.send("🤔 Thinking...")
                
                reply = await LLM_response({"role": "user", "content": question})
                
                # Update thinking message
                await thinking_msg.edit(content=reply)
                
            except Exception as e:
                print(f"Error creating thread: {e}")
                await message.channel.send(f"Error creating thread: {str(e)}")

        # Thread in server
        elif isinstance(message.channel, discord.Thread):
            try:
                thread = message.channel
                
                
                thinking_msg = await thread.send("🤔 Thinking...")
                
                # Collect all messages in thread + Current message
                messages = []
                async for msg in thread.history(limit=50, oldest_first=True):
                    if msg.author != bot.user and not msg.content.startswith("🤔"):
                        messages.append({
                            "role": "user" if not msg.author.bot else "assistant", 
                            "content": msg.content
                        })
                
              
                messages.append({"role": "user", "content": question})
                
                reply = await LLM_response(messages)
                
                # Update thinking message 
                await thinking_msg.edit(content=reply)
                
            except Exception as e:
                print(f"Error in thread: {e}")
                await message.channel.send(f"Error processing request: {str(e)}")


        # DM with the bot , which is not quite working thanks to discord
        elif isinstance(message.channel, discord.DMChannel):
            try:
                print(f"Received DM or Group DM from {message.author}: {message.content}")
                
                thinking_msg = await message.channel.send("🤔 Thinking...")
                
                messages = []
                async for msg in message.channel.history(limit=50, oldest_first=True):
                    if msg.author != bot.user and not msg.content.startswith("🤔"):
                        if "@ai" in msg.content.lower():
                            question_content = msg.content.replace("@ai", "").strip()
                            if question_content:
                                messages.append({
                                    "role": "user", 
                                    "content": question_content
                                })
                
                messages.append({"role": "user", "content": question})
                
                reply = await LLM_response(messages)
                
                await thinking_msg.edit(content=reply)
                
            except Exception as e:
                print(f"Error in DM or Group DM: {e}")
                await message.channel.send(f"Error processing request: {str(e)}")
    
    # Process remaining commands too
    await bot.process_commands(message)

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)