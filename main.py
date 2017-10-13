import os
import discord
import asyncio
import random

client = discord.Client()

@client.event
async def on_ready():
    """ Print when the bot is ready """
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print(client.user.display_name)
    print('------')

@client.event
async def on_message(message):
    """When a new message has arrived"""
    await RemoveProfanity(message)
    await innapropriateMessage(message)
    await AddProfanity(message)
    
async def innapropriateMessage(message):
    """ Profainity Filter, it runs when a new message gets sent """
    ProfanityList = []
    try:
        with open("ProfanityList.txt", "r") as myfile:
            ProfanityList = myfile.read().split("\n")
    except FileNotFoundError:
        myfile = open("ProfanityList.txt", "w+")
        myfile.close()
        print("File has just been created")
        return
    for word in range(0, len(ProfanityList)):
        if((message.content.lower().find(ProfanityList[word].lower())) != -1 and str(message.author) != "TEST TEST TEST#5653" and ProfanityList[word] != ""): # Profanity word comes from ProfanityList.txt
            await client.delete_message(message)
            newWord = "" # New Profanity word to match casing
            for letter in range(len(ProfanityList[word])):
                messageLetter = message.content.find(ProfanityList[word][letter])
                if (message.content[messageLetter].isupper()):
                    newWord += ProfanityList[word][letter].upper()
                else:
                    newWord += ProfanityList[word][letter].lower()
            await client.send_message(message.channel, "**{}** {}".format(message.author.display_name, message.content.replace(newWord, "|BADWORD|")))
            break
                    
async def AddProfanity(message):
    """ Add profanities from the list """
    if (message.content.lower().startswith("!addprofanity") and str(message.author) != "TEST TEST TEST#5653"): # If true, it will append to a file called ProfanityList.txt
        try:
            with open("ProfanityList.txt", "a") as myfile:
                myfile.write(message.content.lower().replace("!addprofanity ", "") + "\n")
        except FileNotFoundError:
            myfile = open("ProfanityList.txt", "w+")
            myfile.write(message.content.lower().replace("!addprofanity ", "") + "\n")
            myfile.close()
            print("File has just been created")

async def RemoveProfanity(message):
    """ Remove profanities from the list """
    if (message.content.lower().startswith("!removeprofanity") and str(message.author) != "TEST TEST TEST#5653"): # If true, it will append to a file called ProfanityList.txt
        ProfanityList = []
        try:
            with open("ProfanityList.txt", "r") as myfile:
                ProfanityList = myfile.read().split("\n")
        except FileNotFoundError:
            myfile = open("ProfanityList.txt", "w+")
            myfile.close()
            print("File has just been created, could not remove profanity.")
            return
        for i in range(len(ProfanityList)):
            if (ProfanityList[i] == message.content.lower().replace("!removeprofanity ", "")):
                ProfanityList[i] = ""
        with open("ProfanityList.txt", "w") as myfile:
            myfile.write("\n".join(ProfanityList))

client.run("INSERT BOT TOKEN HERE")
