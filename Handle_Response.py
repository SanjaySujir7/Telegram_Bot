from random import choice


Response_Dictionary = {
    'nothing' : [
        "ok."
    ],
    "no" : ["ok."],
    'hi' :[
        "hi! How can i help today ?",
        "hi Iam simple chat bot how can i help today ?",
    ],
    'hello' : [
        "hi! How can i help today ?",
        "hi Iam simple chat bot how can i help today ?",
    ],
    "hey" : [
        "hi! How can i help today ?",
        "hi Iam simple chat bot how can i help today ?",
    ],
    "good morning" : [
        "Good Morning!",
        "Good Morning! How can i help you ?",
        "Good Morning dear user!"
    ],
    "good afternoon" :[
        "Good After noon!",
        "Good After noon! How can i help you ?",
        "Good After noon dear user!"
    ],
    "good night" : [
        "Good Night!",
        "Good Night! How can i help you ?",
        "Good Night dear user!"
    ],
    "good evening" : [
        "Good Evening!",
        "Good Evening! How can i help you ?",
        "Good Evening dear user!"
    ],
    "thank you" : [
        "Your Welcome!",
        "Its ok! Your welcome.",
        "Your Welcome! No need to thank me!.",
    ],
    "thanks" :[
        "Your Welcome!",
        "Its ok! Your welcome.",
        "Your Welcome! No need to thank me!."
    ],
    "/creater" : [
        "Sanjay sujir.",
    ],
    "ok" : [
        "Ha",
        "Ha anything else ?"
    ],
    "/cancel" : [
        "Nothing to cancel."
    ],
    "good" : [
        "Thank you.",
        "Its my pleasure.",
        "Glad to see."
    ],
    "bye" : [
        "Ok Bye dear user!",
        "Ok Bye.",
        "Ok Bye let's meet again."
    ]
}

Else_Replies = [
    "I do not understand your language!",
    "Sorry i could not understand your text! Enter /help to get more information.",
    "Sorry i did't understand.",
    "Sorry iam not an ai bot to understand everything. i have limitation!"
]

class Response :
    
    def __init__ (self,Text):
        self.Text = Text.lower()
        
    def Reply(self):
        for key in Response_Dictionary:
            if key in self.Text:
                
                return choice(Response_Dictionary[key])
            
        return choice(Else_Replies)