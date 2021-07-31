from kivy.app import App                                    #importing kivy for the gui needs (which can be later developed to an app)
from kivy.uix.gridlayout import GridLayout              
from kivy.uix.label import Label                            #importing useful Kivy features
from kivy.uix.button import Button
from kivy.uix.image import Image

import pyttsx3                                              #pyttsx3- text to speech module
import speech_recognition as sr                             #speech to text module
import webbrowser                                           #module for accessing browsers
import pywhatkit as k                                       #for accessing a search engine for performing searches and stuff
import datetime                                             #for accessing current date and time
from datetime import date


eng=pyttsx3.init()                                          #initialising the pyttsx3 engine   
voices = eng.getProperty('voices')                          
eng.setProperty('voice', voices[1].id)                      #selecting the appropriate voice for engine

def speak(sentence):                                        #function for providing a verbal output
    
    eng.say(sentence)
    eng.runAndWait()

def listen():                                               #function for listening the verbal input
    
    r=sr.Recognizer()
    speak("Listening")
    
    with sr.Microphone() as source:
        audio=r.listen(source)
        
        try:
            statement=r.recognize_google(audio,language='en-in')                #realizing the input
        except Exception as e:
            statement='error'
    
    return statement

def google_search(item):                                     #function for performing a google search

    k.search(item)

def open_web(url):                                           #function for opening a website on your browser

    link = "https://www."+url+".com"
    webbrowser.open_new_tab(link)

def saydate():                                                #function to tell user the current date

    today = date.today()
    D = today.strftime("%B %d, %Y")
    
    speak("Today's Date:"+ D)
    
def saytime():                                                #function to tell user the current time
    
    now = datetime.datetime.now()
    h=now.hour
    m=now.minute
    s=now.second
    
    speak("Time is "+ str(h) +" hours "+ str(m) +" minutes and "+ str(s) + " seconds.")         #arranging time in a suitable format
 
class AIbot(App):                                                                               #the main app class                                                                                    
    
    def build(self):
        
        self.window = GridLayout()                                                              #initialising the gui window
        self.window.cols=1                                                                      
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5 , "center_y": 0.5}
        
        self.window.add_widget(Image(source='artificial-intelligence.jpg', size_hint=(8, 8), pos_hint={'center_x':.5, 'center_y':.5}))                 #adding a logo to the main screen

        self.button= Button( text="Speak", font_size=18, bold=True, background_color='#00FFCE' )                                       #construction of the button
        self.button.bind(on_press=self.callback)
        self.window.add_widget(self.button)
        
        self.reaction=Label(text='')
        self.window.add_widget(self.reaction)
        
        speak(" Hey there, I'm here to help you! For any help press the button and speak")
        
        return self.window

        

    def callback(self, instance) :                                                             # the fuction which will be called on the button press
        
        inp=listen()
        self.reaction.text=inp
        
        if inp!='error' :                                                                       # How the bot will encounter different situations
            
            if inp[0:4]=='open' :
                u=inp[5:]

                if 'www' not in inp:
                    open_web(u)
                    speak( "Opening " + u + " on browser" )
                else:
                    k="https://"+u
                    webbrowser.open_new_tab(k)
                    
            elif inp[0:6]=='search' :
                j=inp[7:]
                google_search(j)
                speak( "Searching for " + j + " on google")

            elif 'date' in inp :
                saydate()

            elif 'time' in inp :
                saytime()

            elif ( 'date' in inp ) and ( 'time' in inp ) :
                saydate()
                saytime()

            else:
                speak( "Here is what I found on Google" )
                google_search(inp)
            
            speak(" For any other help, Please press the button again.")

        else:
            speak( " Pardon me, unable to hear. Please press the button again ")


if __name__ == "__main__" :                                             #the app run
    AIbot().run()

