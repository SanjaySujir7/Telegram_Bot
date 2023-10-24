from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, Application,ConversationHandler,CallbackContext
from random import choice
from Bot_Token import Token,Weather_Api,Bot_Name
from Handle_Response import Response
from gtts import gTTS
import qrcode
import wikipediaapi
import requests


Api_Token = Token

#Coversation Handler Variables

VOICE_GENERATION = "voice_generation"
QRCODE_GENEARTION = "qrcode"
SEARCH_WIKI = "search_wiki"
WEATHER_ASK = "weather_ask"
GENERATE_PASS = "Generate_Password"

async def Start_Message(update: Update, context: ContextTypes.DEFAULT_TYPE):

  await update.message.reply_text("Hello! I am a simple chat bot created by Sanjay. you can chat with me.\ntype /help for more information.")
  


async def Help_Message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text(""" 
        Commands avalible : 
            /help : to get the help.
            /code : get the code of this bot.
            /voice : to generate text to speech.
            /qrcode : to generate qr code
            /search : to search query over internet.
            /weather : to get weather data by city name.
            /password : to generate random password.
    """)
    
    

async def Code_Message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_document("Bot.py",caption="Here is the code! remember it does't include api token of this bot. also it does't include response logic.")
    
    
    
async def Message_Handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  
    print(f"User : {update.message.chat.first_name}, message :{update.message.text}")
    
    message_type = update.message.chat.type
    message = update.message.text

    if message_type == "group":
        pass
    
    else:
        
        response = Response(message) # here add your response logic
        await update.message.reply_text(response.Reply())
        


async def Error_Handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

  print(f"Update {update} caused error {context.error}")
  await update.message.reply_text("Something went wrong!")
  
  
  
async def Voice_Generation_Ask (update : Update, context : CallbackContext):
    
    await update.message.reply_text("Enter any text to generate voice.")
    return VOICE_GENERATION
    
    
    
async def Voice_Generation (update : Update, context : CallbackContext):
    text = update.message.text
    
    if "/cancel" in text:
        await update.message.reply_text("Operation canceld.")
        return

    
    print(f"User : {update.message.chat.first_name}, Voice : {text}")
    
    if not text:
        await update.message.reply_text("Please enter text to generate voice. example : /voice Hi iam simple chatbot")
        return
    
    Generating_Text = await update.message.reply_text("Generating audio...", reply_to_message_id=update.message.message_id)
    tts = gTTS(text,lang="en-IN")
    
    tts.save("voice.mp3")
    
    await context.bot.delete_message(update.message.chat.id, Generating_Text.message_id)
    await update.message.reply_audio("voice.mp3")
    return ConversationHandler.END



async def Cancel_Operation(update: Update, context: CallbackContext):
    await update.message.reply_text("Operation canceled.")
    
    
async def QrCode_Generation (update: Update, context: CallbackContext):
    text = update.message.text
    print(f"User : {update.message.chat.first_name}, QRcode_text :{text}")
    
    if "/qrcode" in text:
        await update.message.reply_text("Enter any text to convert it to qrcode.")
        
        return QRCODE_GENEARTION
    
    Generate_Text = await update.message.reply_text("Generating qrcode....",reply_to_message_id=update.message.message_id)
    
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qr_code.png")
    
    await context.bot.delete_message(update.message.chat.id, Generate_Text.message_id)
    await update.message.reply_photo("qr_code.png",caption=f"Here is the qrcode for text '{text}'.")
    
    return ConversationHandler.END
    

async def Search_Wikepedia (update : Update, context : CallbackContext):
    
    wiki_wiki = wikipediaapi.Wikipedia("english/us")

    text = update.message.text
    print(f"User : {update.message.chat.first_name}, search : {text}")
    
    if '/search' in text:
        await update.message.reply_text("What is your query to search ?")
        return SEARCH_WIKI
        
    page = wiki_wiki.page(text)

    if page.exists():
        
        await update.message.reply_text(f"Summary: {page.text[:300]}")
        
    else:
        await update.message.reply_text("Content not found!")
        
    return ConversationHandler.END



async def Weather_Get (update : Update, context : CallbackContext):
    city = update.message.text.lower()
    
    if "/weather" in city:
        await update.message.reply_text("Enter city name to find weather.")
        return WEATHER_ASK
    
    print(f"User : {update.message.chat.first_name}, Weather : {city}")
    Generate_Text = await update.message.reply_text("Getting data....",reply_to_message_id=update.message.message_id)
    
    Response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={Weather_Api}&units=metric")

    if Response.status_code == 200:
        
        data = Response.json()
        City_Name = data['name']
        Lon = data['coord']['lon']
        Lat = data['coord']['lat']
        Temp = data['main']['temp']
        Mini_Temp = data['main']['temp_min']
        Max_Temp = data['main']['temp_max']
        Pressure = data['main']['pressure']
        Humidity = data['main']['humidity']
        Wind = f"speed : {data['wind']['speed']}, deg : {data['wind']['deg']}"


        Reply_Message = f"""
            City_Name = {City_Name}.
        Longitude : {Lon}, Latitude = {Lat}.
            
        Temperature : {Temp} °C,
        Minimum_Temperature : {Mini_Temp} °C,
        Maximum_Temperature : {Max_Temp} °C,
        Pressure : {Pressure},
        Humidity : {Humidity},
        {Wind}   
        """
        await context.bot.delete_message(update.message.chat.id,Generate_Text.id)
        await update.message.reply_text(Reply_Message)
        
        return ConversationHandler.END
    
    
    elif Response.status_code == 404:
        await context.bot.delete_message(update.message.chat.id,Generate_Text.id)
        await update.message.reply_text("City not found! check spelling before enter.")
        return ConversationHandler.END
    
    else:
        await context.bot.delete_message(update.message.chat.id,Generate_Text.id)
        await update.message.reply_text("Something went wrong!")
        return ConversationHandler.END
    
    
async def Generate_Password (update : Update, context : CallbackContext):
    text = update.message.text.lower()

    if "/password" in text:
        await update.message.reply_text("Enter the length of the password. i will generate a random password according to that length.")
        return GENERATE_PASS
    
    if not text.isdigit():
        await update.message.reply_text("length should be in number not word. enter again.",reply_to_message_id=update.message.message_id)
        return GENERATE_PASS
        
        
    String = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%&*_+:;"
    text = int(text)
    
    Password = ""
    for _ in range(text):
        Password += choice(String)
    
    await update.message.reply_text(f"pass: {Password}")
    return ConversationHandler.END
    

# Conversation Handler
conv_handler_voice = ConversationHandler(
    entry_points=[CommandHandler("voice", Voice_Generation_Ask)],
    states={
        VOICE_GENERATION: [MessageHandler(filters.TEXT, Voice_Generation)],
        
    },
    fallbacks=[CommandHandler("cancel", Cancel_Operation)],
)


Qr_code_Handler = ConversationHandler(
    entry_points=[CommandHandler("qrcode", QrCode_Generation)],
    states={
        QRCODE_GENEARTION: [MessageHandler(filters.TEXT, QrCode_Generation)],
        
    },
    fallbacks=[CommandHandler("cancel", Cancel_Operation)],
)

Weather_Conv_Handler = ConversationHandler(
    entry_points=[CommandHandler("weather", Weather_Get)],
    states={
        WEATHER_ASK: [MessageHandler(filters.TEXT, Weather_Get)],
        
    },
    fallbacks=[CommandHandler("cancel", Cancel_Operation)],
)


Search_Conv_Handler = ConversationHandler(
    entry_points=[CommandHandler("search", Search_Wikepedia)],
    states={
        SEARCH_WIKI: [MessageHandler(filters.TEXT, Search_Wikepedia)],
        
    },
    fallbacks=[CommandHandler("cancel", Cancel_Operation)],
)


Password_Conv_Handler = ConversationHandler(
    entry_points=[CommandHandler("password", Generate_Password)],
    states={
        GENERATE_PASS: [MessageHandler(filters.TEXT, Generate_Password)],
        
    },
    fallbacks=[CommandHandler("cancel", Cancel_Operation)],
)

def Main ():
    
    print("Starting bot...")

    app = Application.builder().token(Api_Token).build()

    app.add_handler(CommandHandler('start', Start_Message))
    app.add_handler(CommandHandler('help', Help_Message))
    app.add_handler(CommandHandler('code', Code_Message))
    app.add_handler(conv_handler_voice)
    app.add_handler(Qr_code_Handler)
    app.add_handler(Search_Conv_Handler)
    app.add_handler(Weather_Conv_Handler)
    app.add_handler(Password_Conv_Handler)
    
    app.add_handler(MessageHandler(filters.TEXT, Message_Handler))

    app.add_error_handler(Error_Handler)

    print("bot is live...")
    app.run_polling(poll_interval=10)
    
    
if __name__ == "__main__":
    Main()