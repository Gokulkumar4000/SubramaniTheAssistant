import webbrowser
from playsound import playsound
import os
import eel
from engine.command import speak
from engine.config import ASSISTANT_NAME
import regex as re
import pywhatkit as kit
from engine.db import cursor

@eel.expose
def playassistantsound():
    music_dir = os.path.abspath("www/assets/audio/music.mp3")
    playsound(music_dir)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower().strip()
    
    print(f"Processing command: '{query}'")  # Debugging

    if query:
        try:
            # Check sys_command table
            cursor.execute('SELECT path FROM sys_command WHERE name = ?', (query,))
            results = cursor.fetchall()
            print(f"Sys Command Results: {results}")  # Debugging

            if results:
                speak("Opening " + query)
                os.startfile(results[0][0])
            else:
                # Check web_command table
                cursor.execute('SELECT path FROM web_command WHERE name = ?', (query,))
                results = cursor.fetchall()
                print(f"Web Command Results: {results}")  # Debugging

                if results:
                    url = results[0][0]
                    # Ensure URL has the correct scheme
                    if not url.startswith(('http://', 'https://')):
                        url = 'http://' + url
                    speak("Opening " + query)
                    try:
                        print(f"Opening URL: {url}")  # Debugging
                        webbrowser.open(url)
                    except Exception as e:
                        speak("Could not open the webpage")
                        print(f"Webpage open error: {e}")  # Debugging
                else:
                    speak("Opening " + query)
                    try:
                        os.system('start ' + query)
                    except Exception as e:
                        speak("Not found")
                        print(f"Application open error: {e}")  # Debugging
        except Exception as e:
            speak("Something went wrong")
            print(f"Database query error: {e}")  # Debugging

def extract_yt_term(command):
    pattern = r"\b([\w\s]+)\s+(in|on)\s+youtube\b"
    match = re.search(pattern, command, re.IGNORECASE)
    if match:
        term = match.group(1).strip()
        print(f"Extracted YouTube Term: '{term}'")  # Debugging
        return term
    return None

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    if search_term:
        speak("Playing " + search_term + " on YouTube")
        kit.playonyt(search_term)
    else:
        speak("Could not extract search term for YouTube")
