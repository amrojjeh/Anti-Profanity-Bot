import discord

CLIENT = discord.Client()

@CLIENT.event
async def on_ready():
    """ Print when the bot is ready """
    print('Logged in as')
    print(CLIENT.user.name)
    print(CLIENT.user.id)
    print(CLIENT.user.display_name)
    print('------')

@CLIENT.event
async def on_message(message):
    await RemoveProfanity(message)
    await innapropriateMessage(message)
    await AddProfanity(message)
    
async def innapropriateMessage(message):
    """ Profainity Filter, it runs when a new message gets sent """
    ProfanityList = []
    with open("ProfanityList.txt", "r") as myfile:
        ProfanityList = myfile.read().split("\n")
    newSentence = message.content # The sentence that is gonna replace the innapropriate message
    for word in range(0, len(ProfanityList)):
        if((message.content.lower().find(ProfanityList[word].lower())) != -1 \
                   and not message.author.bot and ProfanityList[word] != ""): # Profanity word comes from ProfanityList.txt
            newWord = "" # New Profanity word to match casing
            for letter in range(0, len(ProfanityList[word])):
                messageLetter = message.content.lower().find(ProfanityList[word][letter]) # index of bad word and letter
                if (message.content[messageLetter].isupper()):
                    newWord += ProfanityList[word][letter].upper()
                else:
                    newWord += ProfanityList[word][letter].lower()
            newSentence = newSentence.replace(newWord, "|BADWORD|")
    if newSentence != message.content and not message.author.bot:
        await CLIENT.delete_message(message)
        await CLIENT.send_message(message.channel, "**{}** {}".format(message.author.display_name, newSentence))
        newSentence = ""
                    
async def AddProfanity(message):
    """ Add profanities from the list """
    if message.content.lower().startswith("!addprofanity") and not message.author.bot \
            and isModerator(message): # If true, it will append to a file called ProfanityList.txt
        if isProfanity(message.content.lower().replace("!addprofanity ", "")) != 1:
            with open("ProfanityList.txt", "a") as myfile:
                myfile.write(message.content.lower().replace("!addprofanity ", "") + "\n")
        else:
            CLIENT.send_message(message.channel, "Profanity already exists.")

async def RemoveProfanity(message):
    """ Remove profanities from the list """
    if  message.content.lower().startswith("!removeprofanity") and not message.author.bot \
            and isModerator(message): # If true, it will append to a file called ProfanityList.txt
        ProfanityList = []
        with open("ProfanityList.txt", "r") as myfile:
            ProfanityList = myfile.read().split("\n")
        for i in range(len(ProfanityList)):
            if ProfanityList[i] == message.content.lower().replace("!removeprofanity ", ""):
                ProfanityList[i] = ""
        with open("ProfanityList.txt", "w") as myfile:
            for i in range(len(ProfanityList)):
                if ProfanityList[i] != "":
                    myfile.write(ProfanityList[i] + "\n")

def isModerator(message):
    for i in range(0, len(message.author.roles)):
        if str(message.author.roles[i]).lower() == "moderator" or str(message.author.roles[i]).lower() == "admin":
            return True
    return False

def isProfanity(profanity):
    ProfanityList = []
    with open("ProfanityList.txt", "r") as myfile:
        ProfanityList = myfile.read().split("\n")
    for i in range(0, len(ProfanityList)):
        if ProfanityList[i] == profanity:
            return 1
    return 0

CLIENT.run("INSERT TOKEN HERE")
