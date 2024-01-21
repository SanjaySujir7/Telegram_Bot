from Handle_Response import Response
from random import choice
import requests
from Bot_Token import Weather_Api
from gtts import gTTS


TEST = 'test'
GENERATE_PASS = "generate_pass"
WEATHER_ASK = "weather_ask"
END = "END_OF_CONVERSATION"
VOICE_GENERATION = "Voice_generation"

class InvalidTokenError(Exception):
    def __init__(self, message="Your Token is Incorrect!"):
        self.message = message
        super().__init__(self.message)
        
class NetworkError(Exception):
    def __init__(self, message="Check Your Internet Connection!"):
        self.message = message
        super().__init__(self.message)
       
       
class Update:
    def __init__(self):
        self.Text = None
        self.Chat_Id = None
        self.Message_id = None
        self.Bot_Message
        
    def Reply_Text(self,text,Reply_To_Message_id = None):
        pass
    
    def Send_Photo(self,Path,caption = None,Reply_To_Message_id = None):
        pass
    
    def Send_File(self,Path,caption,Reply_To_Message_id = None):
        pass
    
    def Send_Audio(self,Path,caption,Reply_To_Message_id = None):
        pass
    
    def Delete_Message(self,Chat_Id,Message_id):
        pass

        
class Tele_Bot:
    
    def __init__(self,Name,Api_Key,Polling_Time = 10):
        self.Name = Name
        self.Api_key = Api_Key
        self.Bot_Info = None
        self.User_Messages = None
        self.Off_Set = None
        self.Commands = {}
        self.Custom_Messages = None
        self.Is_Conversation_Started = False
        self.Conversation_Handlers = []
        self.Last_Conversation_Return = None
        self.Last_Conversation_Index = None
        self.Polling_Time = Polling_Time
        
            
    def Add_Conversation_Handler(self,Entry,States):
        
        self.Conversation_Handlers.append({'Entry' : {Entry[0] : Entry[1]},'states' : States})
        
        
    def Check_Existence(self):
       try:
            Result = requests.get(f'https://api.telegram.org/bot{self.Api_key}/getMe')
            Data = Result.json()
            
            if Result.status_code == 200 and Data['ok']:
                self.Bot_Info = Data
                
                return True
            
            else:
                raise InvalidTokenError
            
       except:
           raise NetworkError('Something Went Wrong! check your Internet Connection.')
       
       
    def Get_Update(self):
        try:
            params = {'offset':self.Off_Set,'timeout' : self.Polling_Time}
        
            Result = requests.get(f'https://api.telegram.org/bot{self.Api_key}/getUpdates',params=params)
            
            Data = Result.json()
        
            return {'res' : True, 'data' : Data}
            
            
        except:
            return {'res' : False,'data':"Something Went Wrong!"}
        
    
    def Reply_Message(self):
        
        message = self.User_Messages
        
        if not 'text' in message['message']:
            self.Reply_Text("This is text Bot")
            return
        
        self.Off_Set = message['update_id'] + 1
        self.Chat_Id = message['message']['chat']['id']
        Text = message['message']['text'].lower()
        self.Text = Text
        self.Message_Id = message['message']["message_id"]
    
        
        if self.Is_Conversation_Started:
            handler = self.Conversation_Handlers[self.Last_Conversation_Index]
            
            if not self.Last_Conversation_Return =='END_OF_CONVERSATION':
                Return = handler['states'][self.Last_Conversation_Return](self)
                self.Last_Conversation_Return = Return
                return
            
            else:

                self.Is_Conversation_Started = False
                self.Last_Conversation_Index = None
                self.Last_Conversation_Return = None
        

        for index,all in enumerate(self.Conversation_Handlers):
            if Text in all['Entry']:
                Return = all['Entry'][Text](self)
                self.Is_Conversation_Started = True
                self.Last_Conversation_Index = index
                self.Last_Conversation_Return = Return
                return
            
        if Text in self.Commands:
            self.Commands[Text](self)
            
        else:
            self.Custom_Messages(self)
         
        
       
    def Run(self,Data):
    
        self.User_Messages = Data
        self.Reply_Message()
                    
                
        
    def Add_Command_Handler(self,Command,Function):
        self.Commands[Command] = Function
        
        
    def Add_Custom_Message_Handler(self,Function):
        self.Custom_Messages = Function
        
    def Reply_Text(self,text,Reply_To_Message_id = None):

        params = {'chat_id' : self.Chat_Id,'text' :text}
        
        if Reply_To_Message_id:
            params["reply_to_message_id"] = Reply_To_Message_id
                    
        Res = requests.post(f'https://api.telegram.org/bot6750944019:AAG5R5h2sE4zyu-L6ZsxCOIEh6X25FqitRI/sendMessage',params=params)
        
        return Res.json()["result"]['message_id']
        
        
    def Send_Photo(self,Path,caption = None, Reply_To_Message_id = None):
        
        params = {"chat_id": self.Chat_Id, "caption": caption}
        
        if Reply_To_Message_id:
            params["reply_to_message_id"] = Reply_To_Message_id
            
        with open(Path,'rb') as file:
            files = {'photo' : file}
            
            requests.post(f"https://api.telegram.org/bot6750944019:AAG5R5h2sE4zyu-L6ZsxCOIEh6X25FqitRI/sendPhoto",params=params,files=files)
            
            
    def Send_Audio(self,Path,caption,Reply_To_Message_id = None):
        params = {"chat_id": self.Chat_Id, "caption": caption}
        
        if Reply_To_Message_id:
            params["reply_to_message_id"] = Reply_To_Message_id
        
        with open(Path,'rb') as file:
            files = {'audio' : file}
            
            requests.post(f"https://api.telegram.org/bot6750944019:AAG5R5h2sE4zyu-L6ZsxCOIEh6X25FqitRI/sendAudio",params=params,files=files)
            
            
    def Send_File(self,Path,caption,Reply_To_Message_id = None):
    
        params = {"chat_id": self.Chat_Id, "caption": caption}
        
        if Reply_To_Message_id:
            params["reply_to_message_id"] = Reply_To_Message_id
        
        with open(Path,'rb') as file:
            files = {'document' : file}
            
            requests.post(f"https://api.telegram.org/bot6750944019:AAG5R5h2sE4zyu-L6ZsxCOIEh6X25FqitRI/sendDocument",params=params,files=files)
            
            
    def Delete_Message(self,chat_id,Message_id):
        
        params = {
        "chat_id": chat_id,
        "message_id": Message_id
        }
        
        Res = requests.post(f"https://api.telegram.org/bot6750944019:AAG5R5h2sE4zyu-L6ZsxCOIEh6X25FqitRI/deleteMessage",params=params)




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
    
    
    
def Voice_Generation_Ask (update : Update):
    
    update.Reply_Text("Enter any text to generate voice.")
    return VOICE_GENERATION
    
    
    
def Voice_Generation (update : Update):
    text = update.Text
    
    if "/cancel" in text:
        update.Reply_Text("Operation canceld.")
        return END

    
    if not text:
        update.Reply_Text("Please enter text to generate voice.")
        return VOICE_GENERATION
    
    Generating_Text = update.Reply_Text("Generating audio...",Reply_To_Message_id=update.Message_id)
    tts = gTTS(text,lang="en-IN")
    
    tts.save("voice.mp3")
    
    update.Delete_Message(update.Chat_Id, Generating_Text)
    update.Send_Audio("voice.mp3")
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
