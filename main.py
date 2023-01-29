#Cole Smith
#Date last updated: 01,20,2021
#Discord Bot

#libraries that were used
import discord
import random
import datetime
#this library is for the timezone conversion
import pytz

#importing other files
from ban import bannable
from auth_token import auth_token
from quotes import quotes

#here is the discord.py documentation that was used to create almost all of this discord bot
#https://discordpy.readthedocs.io/en/stable/

#these set up the bot and give it proper administrator privilages
intents = discord.Intents.default()
ban_members = True
intents.members = True
client = discord.Client(intents=intents)

print('Link Start')
#just tells the termimal that the bot is running
@client.event
async def on_ready():
  print("Authorized")
  print('We have logged in as {0.user}\n'.format(client))

#new member welcoming system
@client.event
async def on_member_join(member):
  guild = member.guild
  if guild.system_channel is not None:
    to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
    await guild.system_channel.send(to_send)

#these lines of code will trigger everytime there is a new message  
@client.event
async def on_message(message):

  #makes sure the bot is not responding to its previous message
  if message.author == client.user:
    return

  if message.content == '$help':
    await message.channel.send("LIST OF FEATURES AND COMMAND\n1. $rand\t| Prints a random number between 1 and a number you select\n2. $help\t| Well you clearly figured out how this one works\n3. $Hello\t| Use this command to say hello to the bot\n4. $quote\t| Use this command for me to send you a random quote. All of these quotes were found on random peoples discord profile\n\nBe warned that you cannot enter swearwords, for more information on what these are please send me a direct message '$bannable''")

  #checks the messsage for any words in the blacklist, checks to see if each word in the message is any of the words in the blacklist
  #the try statement is their just in case the user enters something unexpected so the terminal doesn't get clogged with error messages
  try:
    for bannable_word in bannable:
      if bannable_word in message.content:
        #deletes the message if it has a bad word
        await message.delete()
        await message.channel.send("Please don't enter a blacklisted word again")
  except:
    return


#https://discordpy.readthedocs.io/en/latest/api.html#discord.ChannelType  #this checks to see if a mesage was typing in the private channel also known as a direct message. If the user enters the command $bannable in a dm to the bot the bot will print the list of bannable words in the server. It only works in a dm, this is because people could abuse this command to have it look like the bot is swearing in the server.
  if str(message.channel.type) == "private":
    if message.content == "$bannable":
      await message.channel.send(bannable)

  
  #checks to see if the message the user typed is hello, if it is then the bot will say hello back to the user.
  if message.content.startswith('$Hello'):
    await message.channel.send(f'Hello {message.author}!')
  
  #Prints out every message that has been happened since the bot started running, this is so the program can keep a rough record of all message that occured, this is for secuity reasons.
  print(f"{message.author}   {message.content}")


  #This command will just print out a random edgy quote from a list inside quotes.py
 #This command wasn't made for any actual reason, it was made just as a fun little joke for me and my friends.
  if message.content == "$quote":
    await message.channel.send(random.choice(quotes))
    

  #this if statement will trigger if the user inputs '$rand' the bot will then ask for the random number how high the random number should go up to(starting at one). For example the user then types 720, the program will then print out a random number between 1-720
  try:
    if message.content == "$rand":
        await message.channel.send("What do you want your random integer to go up to, starting from 1. eg,if you want your number to be between 1-100 please enter 100\n\nPlease enter a POSITIVE INTEGER GREATER than 1")
      #borrowed some code from https://github.com/Rapptz/discord.py/blob/master/examples/guessing_game.py
        def check(m):
          print(f"{m.content.isdigit()}, and thats all")
          return m.author == message.author and m.content.isdigit()
        rand_int = await client.wait_for('message')
        #the rand_int variable needs
        rand_int.content=int(rand_int.content)
        print(rand_int.content)
      
        #calculates a random between 1 and the number the user entered
        random_ = random.randint(1, rand_int.content)
        #send the message in the chat with the randomized number
        await message.channel.send(random_)
        
        rand_int.content = str(rand_int.content)
  except:
    await message.channel.send("Next time please enter an a positive integer value. :)")


  #these few lines below take the users message and store it in a text file next to the message author.
  #https://stackoverflow.com/a/62947906
  dt_today = datetime.datetime.today()   
  dt_Eastern = dt_today.astimezone(pytz.timezone('Canada/Eastern')) 
  current_time = (dt_Eastern.strftime("%c"))
  txt = message.content

  with open("save_to_log.txt",'a') as save_to_log:
    save_to_log.write(f"{message.author}||{current_time}:\t{txt}\n")
  
  
#runs the bot with the authenication key provide for my specific bot via discord
client.run(auth_token)