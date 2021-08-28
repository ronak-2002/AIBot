#importing the required modules and packages
from kivy.app import App
from kivy.uix.gridlayout import GridLayout          
from kivy.uix.label import Label                           #Kivy for GUI
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.image import Image

import pyttsx3                                             # pyttsx3 for text-to-speech output
import speech_recognition as sr                            # Speech_recognition for voice input
import webbrowser                                          # for accesing web
import pywhatkit as k                                      # for accesing google services
import datetime                                            # current date and time according to the system
from datetime import date
import time                                                # for producing delays in the code

# Coding begins.....

eng=pyttsx3.init()                                         # initializing speech engine                                     
voices = eng.getProperty('voices')                         
eng.setProperty('voice', voices[1].id)

def speak(sentence):                                        # function for voice output
    
    eng.say(sentence)
    eng.runAndWait()

def listen():                                               # function for voice input
    
    r=sr.Recognizer()
    speak("Listening")
    
    with sr.Microphone() as source:
        audio=r.listen(source)
        
        try:
            statement=r.recognize_google(audio,language='en-in')        # accessing google voice input api with indian english
        except Exception as e:
            statement='error'
    
    return statement

def google_search(item):                                        # function to perform google search

    k.search(item)

def open_web(url):                                              # function for accessing a website

    link = "https://www."+url+".com"
    webbrowser.open_new_tab(link)

def saydate():                                                   # function for accessing the current date from the system

    today = date.today()
    D = today.strftime("%B %d, %Y")
    
    speak("Today's Date:"+ D)
    
def saytime():                                                   # function for accessing the current time from the system

    now = datetime.datetime.now()
    h=now.hour
    m=now.minute
    s=now.second
    
    # setting output in a meaningful form
    speak("Time is "+ str(h) +" hours "+ str(m) +" minutes and "+ str(s) + " seconds.")  

def arithmetics():                                                 # function for performing some simple arithmetics
    speak( " Which operation would you like to perform? " )
    op = listen()
    if op!='error':
        speak( " Say the numbers with and in between " )
        no = listen()
        l=[]
        for i in no:
            try:
                l.append(int(i))
            except:
                continue
                        
        if 'add' in op:
            s=0
            for i in l:
                s=s+l
            speak( "The sum is" + str(s))
            
        elif 'multiplication' in op:
            s=1
            for i in l:
                s=s*l
            speak( "The product is" + str(s))
            
        elif 'division' in op:
            s=l[0]//l[1]
            r=l[0]%l[1]
            speak( "The quotient is" + str(s)+ "and the remainder is" + str(r))
            
        elif 'subtract' in op:
            s=max(l)
            for i in l:
                s=s-l
            speak( "The answer is" + str(s))

        else:
            speak( "Wrong Input")
    else:
        speak( "Wrong Input")

# GUI design begins....
class AIbot(App):
    
    def build(self):
        self.window = GridLayout()                                      # SELECTING KIVY'S DEFALULT GRID LAYOUT
        self.window.cols=1                                              # SETTING NO. OF COLUMNS
        
        self.window.size_hint = (0.6, 0.7)                              # SETTING UP THE SIZE RATIOS OF THE GUI WINDOW
        self.window.pos_hint = {"center_x": 0.5 , "center_y": 0.5}
        
        # SETTING UP A LOGO
        self.window.add_widget(Image(source='artificial-intelligence.jpg', size_hint=(4, 4), pos_hint={'center_x':.5, 'center_y':.5}))

        # ADDING THE'Speak' BUTTON
        self.button= Button( text="Speak", font_size=18, bold=True, background_color='#00FFCE' ,size_hint =(2, 2), pos_hint={'center_x':.5, 'center_y':.9})
        self.button.bind(on_press=self.callback)
        self.window.add_widget(self.button)
        
        # ADDING THE 'Set Speech rate' BUTTON
        self.button2= Button( text="Set Speech rate", font_size=18, bold=True, background_color='#0000FF' ,size_hint =(2, 2), pos_hint={'center_x':.9, 'center_y':.2})
        self.button2.bind(on_press=self.callback2)
        self.window.add_widget(self.button2)
        
        # ADDING A LABEL THAT WILL PRINT WHATEVER USER INPUTS TO THE SCRIPT
        self.reaction=Label(text='')
        self.window.add_widget(self.reaction)
        
        # INTRO WHILE STARTING
        speak(" Hey there, I'm here to help you! For any help press the button and speak")
        
        return self.window
    
    # FUNCTION WHICH WILL BE CALLED WHEN THE NEW RATE IS SET ON THE SLIDER
    def on_value_change(self, instance, value):
        rate = value
        eng.setProperty('rate', 178+rate)               # SETTING THE ENGINE'S SPEECH RATE     
        time.sleep(1)
        self.window.remove_widget(self.slide)           # MAKING THE SLIDER DISAPPEAR ONCE THE NEW SPEECH RATE IS SET
        
    # FUNCTION WHICH WILL BE CALLED WHEN THE SPEAK BUTTON IS PRESSED
    def callback(self, instance) :
        
        # CALLING THE PREVIOUSLY DEFINED FUNCTIONS A/C TO USERS' INPUT
        inp=listen()
        self.reaction.text=inp
        
        if inp!='error' :
            
            if inp[0:4]=='open' :
                u=inp[5:]
                open_web(u)
                speak( "Opening " + u + " on browser" )
        
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
            
            elif ('arithmetic' in inp) or (inp== 'math') or (inp == 'calculation') or ( inp in ['add', 'divide' , 'subtract', 'multiply', 'sum', 'product']):
               arithmetics()
                
            else:
                speak( "Here is what I found on Google" )
                google_search(inp)
            
            speak(" For any other help, Please press the button again.")


        else:
            speak( " Pardon me, unable to hear. Please press the button again ")

    # FUNCTION WHICH WILL BE CALLED WHEN THE SET SPEECH RATE BUTTON IS PRESSED
    def callback2(self, instance):
        
        # ADDING THE SLIDER
        self.slide = Slider(min=-100, max=100, value=25, orientation = 'horizontal', size_hint =(5, 5), pos_hint={'center_x':.5, 'center_y':.9})
        self.window.add_widget(self.slide)
        self.slide.bind(value = self.on_value_change)
           
        
if __name__ == "__main__" :                         # Running the main GUI
    AIbot().run()

