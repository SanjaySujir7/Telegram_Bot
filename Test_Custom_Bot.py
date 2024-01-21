from Custom_Bot import Tele_Bot,Update,END
from Handle_Response import Response
from random import choice
import requests
from Bot_Token import Weather_Api

TEST = 'test'
GENERATE_PASS = "generate_pass"
WEATHER_ASK = "weather_ask"

def Start(Update):
    
    Update.Reply_Text("Hi This is Chat Bot Created By Sanjay")
    
    
    
def Help_Message(Update):
    
    Update.Reply_Text(""" 
        Commands avalible : 
            /help : to get the help.
            /code : get the code of this bot.
            /voice : to generate text to speech.
            /qrcode : to generate qr code
            /search : to search query over internet.
            /weather : to get weather data by city name.
            /password : to generate random password.
    """)


def Custom_Messages (Update : Update):
    Text = Update.Text
    
    Update.Reply_Text(Response(Text=Text).Reply())
    

def Code_Message(update: Update):
    
    update.Send_File("Bot.py",caption="Here is the code! No external libs used. remember it does't include api token of this bot. also it does't include response logic.")
    
    
    
def Generate_Password (update : Update):
    text = update.Text.lower()

    if "/password" in text:
        update.Reply_Text("Enter the length of the password. i will generate a random password according to that length.")
        return GENERATE_PASS
    
    if not text.isdigit():
        update.Reply_Text("length should be in number not word. enter again.",Reply_To_Message_id=update.Message_Id)
        return GENERATE_PASS
    
    String = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%&*_+:;"
    text = int(text)
    
    Password = ""
    for _ in range(text):
        Password += choice(String)
    
    update.Reply_Text(f"pass: {Password}")
    return END


def Weather_Get (update : Update):
    city = update.Text.lower()
    
    if "/weather" in city:
        update.Reply_Text("Enter city name to find weather.")
        return WEATHER_ASK
    
    
    Generate_Text = update.Reply_Text("Getting data....",Reply_To_Message_id=update.Message_Id)
    
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
        update.Delete_Message(update.Chat_Id,Generate_Text)
        update.Reply_Text(Reply_Message)
        
        return END
    
    
    elif Response.status_code == 404:
        update.Delete_Message(update.Chat_Id,Generate_Text)
        update.Reply_Text("City not found! check spelling before enter.",Reply_To_Message_id=update.Message_Id)
        return END
    
    else:
        update.Delete_Message(update.Chat_Id,Generate_Text)
        update.Reply_Text("Something went wrong!")
        return END


Bot = Tele_Bot("Sanjay_Sujir_7","6750944019:AAG5R5h2sE4zyu-L6ZsxCOIEh6X25FqitRI",Polling_Time=20)

Bot.Add_Command_Handler('/start',Start)
Bot.Add_Command_Handler('/help',Help_Message)
Bot.Add_Custom_Message_Handler(Custom_Messages)


Bot.Add_Conversation_Handler(
    Entry=['/password',Generate_Password],
    States={
        GENERATE_PASS : Generate_Password
    }
)

Bot.Add_Conversation_Handler(
    Entry=['/weather',Weather_Get],
    States={
        WEATHER_ASK : Weather_Get
    }
)

print("Bot Started.")
Bot.Run()