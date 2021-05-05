import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


client = discord.Client() #create a client instance
#connection to discord

sad_words = ["sad", "depressed", "tired", "exhausted", "unhappy", "miserable", "unhappy", "worried", "anxious", "depressing", "angry"]

starter_encouragements = [
  "Every problem is temporary, but you are not. They will pass. So cheer up!",
  "Hang in there, you've got this!",
  "Fear not, as you are being divinely guided!",
  "You are a strong and great person!"
  ]

if "responding" not in db.keys():
  db["responding"] = True

#helper funcion to return a quote from the API
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

#helper function where users can add more encouraging messages to the list
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

#helper function to delete encouraging message from list
def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


#event: bot is working and ready to be used
@client.event #register the event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

#event: bot receives a message
@client.event
async def on_message(message):#takes message argument
  if message.author == client.user:
     return #ignore messages from the bot itself

  msg = message.content
  
  #$inspire feature: returns a random inspiring quote upon query
  if msg.startswith('$inspire'): 
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    #displaying both starter and user added encouragements 
    options = starter_encouragements
    if "encouragements" in db.keys():
      #options = options + db["encouragements"]
      options = options.extend(db["encouragements"])
    
    #respond with encouraging words upon sad word detection feature
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(starter_encouragements))
      #ISSUE HERE: The above line gives error if I add (options) instead of (starter_encouragements)

  #$new: user adds an encouraging message
  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  #$del: user deletes an encouragement
  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  #$list: display the list of all present encouragements 
  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  #$responding: turn the robot's sad message responding on/off
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

keep_alive()
client.run(os.getenv('TOKEN')) 
