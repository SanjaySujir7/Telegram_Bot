import requests


END = "END_OF_CONVERSATION"


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
        
        message = self.User_Messages['result']
        
        for messages in message:
            if not 'text' in messages['message']:
                self.Reply_Text("This is text Bot")
                continue
            
            self.Off_Set = messages['update_id'] + 1
            self.Chat_Id = messages['message']['chat']['id']
            Text = messages['message']['text'].lower()
            self.Text = Text
            self.Message_Id = messages['message']["message_id"]
            print(Text)
            
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
         
        
       
    def Run(self):
        Check_Existence = self.Check_Existence()
        
        if not Check_Existence:
            if not self.Name == self.Bot_Info['result']['username']:
                return "Bot name is incorrect!"
            
        while True:
            Updates = self.Get_Update()
            
            if Updates['res']:
                if Updates['data']['result']:

                    self.User_Messages = Updates['data']
                    self.Reply_Message()
                    
            else:
                return Updates['data']
                    
                
        
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