from flask import Flask
from threading import Thread
#Flask: Web Server to keep the bot running
#server concurrently running with bot


app = Flask('')

@app.route('/')
def home():
  return "Hello, I am alive!"
  #returns to anyone who visits the server

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start() 