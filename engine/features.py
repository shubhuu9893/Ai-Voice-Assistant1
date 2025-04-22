import os
from shlex import quote
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound
import eel
import pyaudio
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME
# Playing assiatnt sound function
import pywhatkit as kit
import pvporcupine
import psutil
import importlib

from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat

# Try importing optional modules
try:
    import pywhatkit as kit
    PYWHATKIT_AVAILABLE = True
except Exception:
    PYWHATKIT_AVAILABLE = False

try:
    from engine.ai_config import model
    GEMINI_AVAILABLE = True
except Exception:
    GEMINI_AVAILABLE = False

try:
    import pvporcupine
    PORCUPINE_AVAILABLE = True
except Exception:
    PORCUPINE_AVAILABLE = False

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

    
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

       

def PlayYoutube(query):
    if not PYWHATKIT_AVAILABLE:
        speak("I'm sorry, but YouTube playback is not available at the moment. Please check your internet connection.")
        return
    
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    try:
        kit.playonyt(search_term)
    except Exception as e:
        print(f"Error playing YouTube: {e}")
        speak("I'm sorry, but I couldn't play that on YouTube. Please check your internet connection.")


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()



# find contacts
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):
    

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

def closeCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("close", "")
    app_name = query.strip().lower()

    if app_name != "":
        try:
            # First try to find the application in the database
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                # Get the process name from the path
                process_name = os.path.basename(results[0][0])
                # Try to close the application
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'].lower() == process_name.lower():
                        proc.kill()
                        speak(f"Closed {app_name}")
                        return
            
            # If not found in database, try to close by the given name
            for proc in psutil.process_iter(['name']):
                if app_name in proc.info['name'].lower():
                    proc.kill()
                    speak(f"Closed {app_name}")
                    return
            
            speak(f"Could not find {app_name} running")
        except Exception as e:
            print(f"Error closing application: {e}")
            speak("Could not close the application")

def get_ai_response(query):
    # Try Gemini first
    if GEMINI_AVAILABLE:
        try:
            # Add context to the query for better responses
            enhanced_query = f"Please provide a clear and concise response to: {query}"
            
            # Generate response from Gemini
            response = model.generate_content(enhanced_query)
            
            if response.text:
                # Clean and format the response
                cleaned_response = response.text.strip()
                # Remove asterisks from the response
                cleaned_response = cleaned_response.replace('*', '')
                # Limit response length if too long
                if len(cleaned_response) > 500:
                    cleaned_response = cleaned_response[:497] + "..."
                return cleaned_response
        except Exception as e:
            print(f"Error with Gemini AI: {e}")
            # Continue to fallback if Gemini fails
    
    # Fallback to HugChat
    try:
        chatbot = hugchat.ChatBot()
        response = chatbot.chat(query)
        if response:
            # Clean and format the response
            cleaned_response = str(response).strip()
            # Remove asterisks from the response
            cleaned_response = cleaned_response.replace('*', '')
            # Limit response length if too long
            if len(cleaned_response) > 500:
                cleaned_response = cleaned_response[:497] + "..."
            return cleaned_response
    except Exception as e:
        print(f"Error with HugChat: {e}")
        return "I apologize, but I'm having trouble accessing AI services at the moment. Please try again later."

# chat bot 
def chatBot(query):
    user_input = query.lower()
    try:
        # Basic commands
        if "hello" in user_input or "hi" in user_input:
            response = "Hello! How can I help you today?"
        elif "how are you" in user_input:
            response = "I'm doing well, thank you for asking! How can I assist you?"
        elif "what can you do" in user_input:
            response = "I can help you with various tasks like:\n1. Opening and closing applications\n2. Playing YouTube videos\n3. Sending messages and making calls\n4. Answering questions about any topic\n5. Providing information from the internet"
        elif "thank you" in user_input:
            response = "You're welcome! Is there anything else I can help you with?"
        elif "bye" in user_input or "goodbye" in user_input:
            response = "Goodbye! Have a great day!"
        else:
            response = get_ai_response(user_input)
        
        print(response)
        speak(response)
        return response
    except Exception as e:
        error_msg = "I apologize, but I encountered an error. Could you please try again?"
        print(f"Error in chatBot: {e}")
        speak(error_msg)
        return error_msg

# android automation

def makeCall(name, mobileNo):
    mobileNo = mobileNo.replace(" ", "")
    speak("Calling "+name)
    try:
        command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
        os.system(command)
    except Exception as e:
        print(f"Error making call: {e}")
        speak("Could not make call. ADB might not be installed or the device might not be connected.")


# to send message
def sendMessage(message, mobileNo, name):
    try:
        from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
        message = replace_spaces_with_percent_s(message)
        mobileNo = replace_spaces_with_percent_s(mobileNo)
        speak("sending message")
        goback(4)
        time.sleep(1)
        keyEvent(3)
        # open sms app
        tapEvents(136, 2220)
        #start chat
        tapEvents(819, 2192)
        # search mobile no
        adbInput(mobileNo)
        #tap on name
        tapEvents(601, 574)
        # tap on input
        tapEvents(390, 2270)
        #message
        adbInput(message)
        #send
        tapEvents(957, 1397)
        speak("message send successfully to "+name)
    except Exception as e:
        print(f"Error sending message: {e}")
        speak("Could not send message. ADB might not be installed or the device might not be connected.")