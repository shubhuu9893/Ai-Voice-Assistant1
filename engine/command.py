import win32com.client
import speech_recognition as sr
import eel
import time
import os

def speak(text):
    text = str(text)
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    voices = speaker.GetVoices()
    speaker.Voice = voices.Item(0)  # Use the second voice (index 1)
    speaker.Rate = -2  # Adjust rate (range is -10 to 10)
    eel.DisplayMessage(text)
    speaker.Speak(text)
    eel.receiverText(text)


def takecommand():
    r = sr.Recognizer()
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            with sr.Microphone() as source:
                print('listening....')
                eel.DisplayMessage('listening....')
                r.pause_threshold = 0.5
                r.adjust_for_ambient_noise(source, duration=0.5)
                r.energy_threshold = 200
                
                try:
                    audio = r.listen(source, timeout=10, phrase_time_limit=10)  # Increased timeout to 10 seconds
                    print('recognizing')
                    eel.DisplayMessage('recognizing....')
                    
                    try:
                        query = r.recognize_google(audio, language='en-IN')
                        print(f"user said: {query}")
                        eel.DisplayMessage(query)
                        return query.lower()
                    except sr.UnknownValueError:
                        print("Could not understand audio")
                        eel.DisplayMessage("Could not understand audio")
                        retry_count += 1
                        if retry_count < max_retries:
                            speak("I couldn't hear you clearly. Please try again.")
                            continue
                        else:
                            speak("Returning to main page due to no clear audio input.")
                            eel.returnToIndex()
                            return ""
                    except sr.RequestError as e:
                        print(f"Could not request results; {e}")
                        eel.DisplayMessage("Could not request results")
                        return ""
                except sr.WaitTimeoutError:
                    print("Listening timed out")
                    eel.DisplayMessage("Listening timed out")
                    speak("No speech detected. Returning to main page.")
                    eel.returnToIndex()
                    return ""
        except Exception as e:
            print(f"Error in takecommand: {e}")
            eel.DisplayMessage("Error in voice input")
            return ""
    
    return ""

@eel.expose
def allCommands(message=1):
    try:
        if message == 1:
            query = takecommand()
            if not query:
                speak("I couldn't hear you. Please try again.")
                return
            print(query)
            eel.senderText(query)
        else:
            query = message
            eel.senderText(query)

        if not query:
            return

        # Command handling
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "close" in query:
            from engine.features import closeCommand
            closeCommand(query)
        elif ("on youtube" in query or "play" in query) and "youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "send message" in query or "phone call" in query or "video call" in query:
            try:
                from engine.features import findContact, whatsApp, makeCall, sendMessage
                contact_no, name = findContact(query)
                if(contact_no != 0):
                    speak("Which mode you want to use whatsapp or mobile")
                    preferance = takecommand()
                    print(preferance)

                    if "mobile" in preferance:
                        if "send message" in query or "send sms" in query: 
                            speak("what message to send")
                            message = takecommand()
                            sendMessage(message, contact_no, name)
                        elif "phone call" in query:
                            makeCall(name, contact_no)
                        else:
                            speak("please try again")
                    elif "whatsapp" in preferance:
                        message = ""
                        if "send message" in query:
                            message = 'message'
                            speak("what message to send")
                            query = takecommand()
                                            
                        elif "phone call" in query:
                            message = 'call'
                        else:
                            message = 'video call'
                                            
                        whatsApp(contact_no, query, message, name)
            except ImportError:
                speak("I'm sorry, but messaging and calling features are not available at the moment.")
        else:
            from engine.features import chatBot
            chatBot(query)
    except Exception as e:
        print(f"Error in allCommands: {e}")
        speak("Sorry, I encountered an error. Please try again.")
    
    eel.ShowHood()





   