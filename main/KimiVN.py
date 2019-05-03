from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os
from gtts import gTTS
from playsound import playsound

# import pyttsx3;

# engine = pyttsx3.init();
#
# # set propertie voice
# engine.setProperty('rate', 150)
# voices = engine.getProperty('voices')
#
# engine.setProperty('voice', voices[1].id)
# Bot cũ version 1 = Bot
# Bot version 2 = Kimi1.0
bot1 = ChatBot('KimiVN',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch',
        'main.logic.time_adapter.TimeLogicAdapterVN'
    ],
   database_uri='sqlite:///database.sqlite3')
trainer = ChatterBotCorpusTrainer(bot1)

training_vietnames = 'vietnamese/'

for file in os.listdir(training_vietnames):
    trainer.train(training_vietnames + file)
count = 0
while True:
    count += 1
    message = input('You: ')
    if message.strip() == 'Bye':
        print('Kimi : Bye')
        break
    else:
        reply = bot1.get_response(message)
        print('Kimi: ', reply)
        tts = gTTS(text=str(reply), lang='vi')
        tts.save("good"+str(count)+".mp3")
        playsound("good"+str(count)+".mp3")
        os.remove("good"+str(count)+".mp3")
