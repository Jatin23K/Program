import speech_recognition as sr
import pyttsx3
import datetime
import os
import time
import webbrowser
import subprocess
import requests
import json
from urllib.parse import quote
import pyautogui
import pickle
from pytube import Search


class AIAssistant:
    def __init__(self):
        self.name = "David"
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init(driverName='sapi5')
        self.engine.setProperty('rate', 180)
        
        # Wake words and deactivation words
        self.wake_words = ["hey david", "hello david","david","Hey Dude"]
        self.deactivate_words = ["goodbye","goodbye david", "bye david"]
        self.is_active = False

        # Initialize VLC player
        self.player = None
        self.is_playing = False
        
        # YouTube API key - Replace with your actual API key
        self.youtube_api_key = "Your_API_Key"
 
        # Memory system
        self.memory_file = "assistant_memory.pkl"
        self.memory = self.load_memory()
        
        # Conversation history
        self.conversation_history = []
        
        # Task list
        self.tasks = []
        
        # Application paths
        self.app_paths = {
            'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'firefox': r'C:\Program Files\Mozilla Firefox\firefox.exe',
            'edge': r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            'pycharm': r'C:\Program Files\JetBrains\PyCharm Community Edition\bin\pycharm64.exe',
            'visual studio code': r'C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe',
            'vs code': r'C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe',
            'vscode': r'C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe',
            'idle': r'C:\Users\Shadow\AppData\Local\Programs\Python\Python313\pythonw.exe',
            'word': r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE',
            'excel': r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE',
            'outlook': r'C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE',
            'powerpoint': r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE',
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'cmd': 'cmd.exe',
            'command prompt': 'cmd.exe',
            'powershell': 'powershell.exe',
            'control panel': 'control.exe',
            'task manager': 'taskmgr.exe',
            'microsoft store': 'ms-windows-store:',
            'power bi': r'C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe',
            'powerbi': r'C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe',
            'tableau': r'C:\Program Files\Tableau\Tableau\bin\tableau.exe',
            'notion': r'C:\Users\%USERNAME%\AppData\Local\Programs\Notion\Notion.exe',
            'chatgpt': 'https://chat.openai.com'
        }

        # Process names for closing applications
        self.app_processes = {
            'chrome': 'chrome.exe',
            'firefox': 'firefox.exe',
            'edge': 'msedge.exe',
            'pycharm': 'pycharm64.exe',
            'visual studio code': 'Code.exe',
            'vs code': 'Code.exe',
            'vscode': 'Code.exe',
            'idle': 'pythonw.exe',
            'word': 'WINWORD.EXE',
            'excel': 'EXCEL.EXE',
            'outlook': 'OUTLOOK.EXE',
            'powerpoint': 'POWERPNT.EXE',
            'notepad': 'notepad.exe',
            'calculator': 'CalculatorApp.exe',
            'cmd': 'cmd.exe',
            'command prompt': 'cmd.exe',
            'powershell': 'powershell.exe',
            'power bi': 'PBIDesktop.exe',
            'powerbi': 'PBIDesktop.exe',
            'tableau': 'tableau.exe',
            'notion': 'Notion.exe',
            'task manager': 'Taskmgr.exe'
        }

                # System controls
        self.system_controls = {
            'volume up': self.volume_up,
            'volume down': self.volume_down,
            'mute': self.mute_audio,
            'unmute': self.unmute_audio,
            'sleep': 'rundll32.exe powrprof.dll,SetSuspendState 0,1,0',
            'shutdown': 'shutdown /s /t 60',
            'restart': 'shutdown /r /t 60',
            'cancel shutdown': 'shutdown /a'
        }

    def load_memory(self):
        """Load memory from file"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'rb') as f:
                    return pickle.load(f)
            return {
                'user_preferences': {},
                'conversation_history': [],
                'important_dates': {},
                'notes': [],
                'last_interaction': None,
                'favorite_apps': [],
                'volume_level': 50,
                'muted': False,
                'last_played_song': None,
                'reminders': []
            }
        except Exception as e:
            print(f"Error loading memory: {e}")
            return {
                'user_preferences': {},
                'conversation_history': [],
                'important_dates': {},
                'notes': [],
                'last_interaction': None,
                'favorite_apps': [],
                'volume_level': 50,
                'muted': False,
                'last_played_song': None,
                'reminders': []
            }

    def save_memory(self):
        """Save memory to file"""
        try:
            with open(self.memory_file, 'wb') as f:
                pickle.dump(self.memory, f)
        except Exception as e:
            print(f"Error saving memory: {e}")

    def remember(self, category, key, value):
        """Store information in memory"""
        if category not in self.memory:
            self.memory[category] = {}
        self.memory[category][key] = value
        self.save_memory()
        return f"I'll remember that {key} is {value}"

    def recall(self, category, key):
        """Recall information from memory"""
        if category in self.memory and key in self.memory[category]:
            return f"Your {key} is {self.memory[category][key]}"
        return None

    def add_to_history(self, user_input, assistant_response):
        """Add interaction to conversation history"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conversation_history.append({
            'timestamp': timestamp,
            'user': user_input,
            'assistant': assistant_response
        })
        self.save_memory()

    def add_note(self, note=None):
        """Add a note to memory"""
        if note is None:
            self.speak("What would you like to add to your notes?")
            note = self.listen()
            if not note:
                self.speak("I didn't catch that. Please try again.")
                return None
            
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.memory['notes'].append({
            'timestamp': timestamp,
            'content': note
        })
        self.save_memory()
        return f"I've added a note: {note}"

    def list_notes(self):
        """List all notes"""
        if not self.memory['notes']:
            return "You don't have any notes."
        
        # Display notes in console
        print("\nYour Notes:")
        for i, note in enumerate(self.memory['notes'], 1):
            print(f"{i}. [{note['timestamp']}] {note['content']}")
        
        # Speak each note
        for note in self.memory['notes']:
            self.speak(f"Note: {note['content']}")
        
        return f"You have {len(self.memory['notes'])} notes."

    def edit_note_by_name(self, note_name):
        """Edit a note by its name/content"""
        if not self.memory['notes']:
            self.speak("You don't have any notes to edit.")
            return None

        # Find the note
        for i, note in enumerate(self.memory['notes']):
            if note_name.lower() in note['content'].lower():
                self.speak(f"I found the note: {note['content']}")
                self.speak("What would you like to change it to?")
                new_content = self.listen()
                if new_content:
                    # Update the note
                    self.memory['notes'][i]['content'] = new_content
                    self.memory['notes'][i]['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.save_memory()
                    return f"I've updated the note to: {new_content}"
                else:
                    self.speak("I didn't catch that. Please try again.")
                    return None
        
        self.speak(f"I couldn't find a note containing '{note_name}'")
        return None

    def delete_note_by_name(self, note_name):
        """Delete a note by its name/content"""
        if not self.memory['notes']:
            self.speak("You don't have any notes to delete.")
            return None

        # Find and delete the note
        for i, note in enumerate(self.memory['notes']):
            if note_name.lower() in note['content'].lower():
                deleted_content = note['content']
                del self.memory['notes'][i]
                self.save_memory()
                return f"I've deleted the note: {deleted_content}"
        
        return f"I couldn't find a note containing '{note_name}'"

    def add_important_date(self, event, date):
        """Add an important date to memory"""
        self.memory['important_dates'][event] = date
        self.save_memory()
        return f"I'll remember that {event} is on {date}"

    def get_important_date(self, event):
        """Get an important date from memory"""
        if event in self.memory['important_dates']:
            return f"{event} is on {self.memory['important_dates'][event]}"
        return f"I don't have any information about {event}"

    def list_important_dates(self):
        """List all important dates"""
        if not self.memory['important_dates']:
            return "You don't have any important dates saved."
        result = "Here are your important dates:\n"
        for event, date in self.memory['important_dates'].items():
            result += f"- {event}: {date}\n"
        return result

    def add_favorite_app(self, app_name):
        """Add an app to favorites"""
        if app_name not in self.memory['favorite_apps']:
            self.memory['favorite_apps'].append(app_name)
            self.save_memory()
            return f"I've added {app_name} to your favorite apps."
        return f"{app_name} is already in your favorite apps."

    def list_favorite_apps(self):
        """List all favorite apps"""
        if not self.memory['favorite_apps']:
            return "You don't have any favorite apps saved."
        result = "Here are your favorite apps:\n"
        for i, app in enumerate(self.memory['favorite_apps'], 1):
            result += f"{i}. {app}\n"
        return result

    def clear_memory(self, category=None):
        """Clear memory or a specific category"""
        if category:
            if category in self.memory:
                self.memory[category] = {}
                self.save_memory()
                return f"I've cleared your {category} memory."
            return f"I don't have a {category} category in my memory."
        else:
            self.memory = {
                'user_preferences': {},
                'conversation_history': [],
                'important_dates': {},
                'notes': [],
                'last_interaction': None,
                'favorite_apps': [],
                'volume_level': 50,
                'muted': False,
                'last_played_song': None,
                'reminders': []
            }
            self.save_memory()
            return "I've cleared all my memory."

    def take_screenshot(self):
        """Take a screenshot"""
        try:
            screenshots_dir = os.path.join(os.path.expanduser("~"), "OneDrive", "Pictures", "Screenshots")
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(screenshots_dir, f"screenshot_{timestamp}.png")
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            if os.path.exists(filename):
                return f"Screenshot saved as {filename}"
            return "Screenshot was taken but couldn't be saved."
        except Exception as e:
            return f"Sorry, I couldn't take a screenshot: {str(e)}"

    def volume_up(self, level=5):
        """Increase system volume"""
        for _ in range(level):
            pyautogui.press('volumeup')
            time.sleep(0.1)
        self.memory['volume_level'] = min(100, self.memory['volume_level'] + level)
        self.save_memory()

    def volume_down(self, level=5):
        """Decrease system volume"""
        for _ in range(level):
            pyautogui.press('volumedown')
            time.sleep(0.1)
        self.memory['volume_level'] = max(0, self.memory['volume_level'] - level)
        self.save_memory()

    def mute_audio(self):
        """Mute system audio"""
        pyautogui.press('volumemute')
        self.memory['muted'] = True
        self.save_memory()

    def unmute_audio(self):
        """Unmute system audio"""
        pyautogui.press('volumemute')
        self.memory['muted'] = False
        self.save_memory()

    def get_weather(self):
        """Get current weather"""
        return "Weather functionality requires an API key. Please add your OpenWeatherMap API key to use this feature."

    def speak(self, text):
        print(f"[ASSISTANT] {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"[ERROR] Text-to-speech failed: {e}")

    def listen(self) -> str:
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = self.recognizer.recognize_google(audio, language='en-US').lower()
            print(f"[DEBUG] Heard: {command}")
            return command
        except sr.WaitTimeoutError:
            print("[DEBUG] Listen error: Timeout waiting for phrase")
        except sr.UnknownValueError:
            print("[DEBUG] Listen error: Could not understand audio")
        except sr.RequestError as e:
            print(f"[DEBUG] Listen error: Could not request results; {e}")
        except Exception as e:
            print(f"[DEBUG] Listen error: {e}")
        return ""

    def get_identity(self):
        return f"I am {self.name}, your AI assistant."

    def get_time(self):
        return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}"

    def open_application(self, app_name):
        app_name = app_name.lower()
        if app_name in self.app_paths:
            path = self.app_paths[app_name].replace('%USERNAME%', os.getenv('USERNAME'))
            try:
                if path.startswith('http'):
                    os.system(f'start {path}')
                else:
                    subprocess.Popen(path)
                self.speak(f"Opening {app_name}")
            except Exception as e:
                self.speak(f"Failed to open {app_name}: {e}")
        else:
            self.speak(f"I don't know how to open {app_name}.")

    def close_application(self, app_name):
        app_name = app_name.lower()
        if app_name in self.app_processes:
            process = self.app_processes[app_name]
            os.system(f"taskkill /f /im {process}")
            self.speak(f"Closing {app_name}")
        else:
            self.speak(f"I don't know how to close {app_name}.")

    def get_capabilities(self):
        """Get a list of all assistant capabilities"""
        capabilities = [
            "1. Basic Commands:",
            "   - Time, date, and day information",
            "   - Greetings and basic conversation",
            "",
            "2. Application Control:",
            "   - Open applications",
            "   - Close applications",
            "",
            "3. System Controls:",
            "   - Volume control (up/down)",
            "   - Mute/unmute audio",
            "   - Take screenshots",
            "",
            "4. Memory System:",
            "   - Remember information",
            "   - Recall information",
            "   - Clear memory",
            "",
            "5. Notes and Dates:",
            "   - Add notes",
            "   - List notes",
            "   - Edit notes",
            "   - Delete notes",
            "   - Add important dates",
            "   - Check important dates",
            "",
            "6. Reminders:",
            "   - Add reminders",
            "   - List reminders",
            "   - Edit reminders",
            "   - Delete reminders",
            "",
            "7. Favorite Apps:",
            "   - Add favorite apps",
            "   - List favorite apps",
            "",
            "8. Weather Information:",
            "   - Get current weather (requires API key)",
            "",
            "9. Conversation:",
            "   - Maintains conversation history",
            "   - Responds to greetings",
            "   - Provides information about itself"
        ]
        return "\n".join(capabilities)

    def add_reminder(self):
        """Add a reminder"""
        self.speak("What is the reminder?")
        reminder_name = self.listen()
        if not reminder_name:
            self.speak("I didn't catch that. Please try again.")
            return None

        self.speak("What's the time of the reminder?")
        reminder_time = self.listen()
        if not reminder_time:
            self.speak("I didn't catch that. Please try again.")
            return None

        self.speak("What's the repeat rate? It can be everyday, weekdays, or once.")
        repeat_rate = self.listen()
        if not repeat_rate:
            self.speak("I didn't catch that. Please try again.")
            return None

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.memory['reminders'].append({
            'timestamp': timestamp,
            'name': reminder_name,
            'time': reminder_time,
            'repeat': repeat_rate
        })
        self.save_memory()
        return f"I've added a reminder: {reminder_name} at {reminder_time} repeating {repeat_rate}."

    def list_reminders(self):
        """List all reminders"""
        if not self.memory['reminders']:
            return "You don't have any reminders."
        
        # Display reminders in console
        print("\nYour Reminders:")
        for i, reminder in enumerate(self.memory['reminders'], 1):
            print(f"{i}. [{reminder['timestamp']}] {reminder['name']} at {reminder['time']} repeating {reminder['repeat']}")
        
        # Speak each reminder
        for reminder in self.memory['reminders']:
            self.speak(f"Reminder: {reminder['name']} at {reminder['time']} repeating {reminder['repeat']}")
        
        return f"You have {len(self.memory['reminders'])} reminders."

    def edit_reminder_by_name(self, reminder_name):
        """Edit a reminder by its name"""
        if not self.memory['reminders']:
            self.speak("You don't have any reminders to edit.")
            return None

        # Find the reminder
        for i, reminder in enumerate(self.memory['reminders']):
            if reminder_name.lower() in reminder['name'].lower():
                self.speak(f"I found the reminder: {reminder['name']} at {reminder['time']} repeating {reminder['repeat']}")
                self.speak("What would you like to change it to?")
                new_name = self.listen()
                if new_name:
                    self.speak("What's the new time of the reminder?")
                    new_time = self.listen()
                    if new_time:
                        self.speak("What's the new repeat rate? It can be everyday, weekdays, or once.")
                        new_repeat = self.listen()
                        if new_repeat:
                            # Update the reminder
                            self.memory['reminders'][i]['name'] = new_name
                            self.memory['reminders'][i]['time'] = new_time
                            self.memory['reminders'][i]['repeat'] = new_repeat
                            self.memory['reminders'][i]['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            self.save_memory()
                            return f"I've updated the reminder to: {new_name} at {new_time} repeating {new_repeat}"
                        else:
                            self.speak("I didn't catch that. Please try again.")
                            return None
                    else:
                        self.speak("I didn't catch that. Please try again.")
                        return None
                else:
                    self.speak("I didn't catch that. Please try again.")
                    return None
        
        self.speak(f"I couldn't find a reminder containing '{reminder_name}'")
        return None

    def delete_reminder_by_name(self, reminder_name):
        """Delete a reminder by its name"""
        if not self.memory['reminders']:
            self.speak("You don't have any reminders to delete.")
            return None

        # Find and delete the reminder
        for i, reminder in enumerate(self.memory['reminders']):
            if reminder_name.lower() in reminder['name'].lower():
                deleted_name = reminder['name']
                del self.memory['reminders'][i]
                self.save_memory()
                return f"I've deleted the reminder: {deleted_name}"
        
        return f"I couldn't find a reminder containing '{reminder_name}'"

    def volume_up(self, level: int = 5) -> None:
        """Increase system volume by specified level"""
        for _ in range(level):
            pyautogui.press('volumeup')
            time.sleep(0.1)
        # Update memory
        self.memory['volume_level'] = min(100, self.memory['volume_level'] + level)
        self.save_memory()

    def volume_down(self, level: int = 5) -> None:
        """Decrease system volume by specified level"""
        for _ in range(level):
            pyautogui.press('volumedown')
            time.sleep(0.1)
        # Update memory
        self.memory['volume_level'] = max(0, self.memory['volume_level'] - level)
        self.save_memory()

    def parse_volume_level(self, command: str) -> int:
        """Extract volume level from command"""
        try:
            # Look for numbers in the command
            import re
            numbers = re.findall(r'\d+', command)
            if numbers:
                level = int(numbers[0])
                # Limit level between 1 and 100
                return min(max(level, 1), 100)
            return 5  # Default level if no number found
        except:
            return 5  # Default level if parsing fails

    def mute_audio(self) -> None:
        """Mute system audio"""
        pyautogui.press('volumemute')
        # Update memory
        self.memory['muted'] = True
        self.save_memory()

    def unmute_audio(self) -> None:
        """Unmute system audio"""
        pyautogui.press('volumemute')
        # Update memory
        self.memory['muted'] = False
        self.save_memory()

    def pause_media(self) -> None:
        """Pause media playback"""
        pyautogui.press('playpause')

    def unpause_media(self) -> None:
        """Unpause media playback"""
        pyautogui.press('playpause')

    def system_control(self, command: str) -> str:
        """Execute system control commands"""
        try:
            command = command.lower().strip()
            
            # Handle volume commands with specific levels
            if "volume up" in command or ("increase" and "volume" in command):
                level = self.parse_volume_level(command)
                self.volume_up(level)
                return f"Increasing volume by {level} levels"
                
            if "volume down" in command or ("decrease" and "volume" in command):
                level = self.parse_volume_level(command)
                self.volume_down(level)
                return f"Decreasing volume by {level} levels"
            
            # Handle mute/unmute
            if "mute" in command:
                self.mute_audio()
                return "Muting audio"
                
            if "unmute" in command:
                self.unmute_audio()
                return "Unmuting audio"

            # Handle pause/unpause/resume/stop
            if "pause" in command or "stop" in command:
                self.pause_media()
                return "Pausing media playback"
                
            if "unpause" in command or "resume" in command:
                self.unpause_media()
                return "Resuming media playback"
            
            # Handle other system controls
            if command in ['sleep', 'shutdown', 'restart', 'cancel shutdown']:
                if 'sleep' in command:
                    os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
                elif 'shutdown' in command:
                    os.system('shutdown /s /t 60')
                elif 'restart' in command:
                    os.system('shutdown /r /t 60')
                elif 'cancel shutdown' in command:
                    os.system('shutdown /a')
                return f"Executing {command}"
            else:
                return f"Sorry, I don't know how to {command}"
        except Exception as e:
            return f"Sorry, I couldn't execute {command}: {str(e)}"
    def play_music(self, song_name: str) -> str:
        """Play music on YouTube"""
        try:
            # Search for the video using pytube
            s = Search(song_name)
            results = s.results
            
            if results:
                # Get the first video result
                video = results[0]
                video_url = f"https://www.youtube.com/watch?v={video.video_id}"
                
                # Open the video in the default browser
                webbrowser.open(video_url)
                
                # Update memory
                self.memory['last_played_song'] = {
                    'title': video.title,
                    'url': video_url,
                    'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                self.save_memory()
                
                return f"Playing {video.title} on YouTube"
            else:
                # Fallback to search results if no video found
                search_url = f"https://www.youtube.com/results?search_query={quote(song_name)}"
                webbrowser.open(search_url)
                return f"Couldn't find exact video. Opening YouTube search for {song_name}"
                
        except Exception as e:
            return f"Sorry, I couldn't play {song_name}: {str(e)}"
            
    def stop_music(self) -> str:
        """Stop currently playing music (placeholder)"""
        return "To stop the music, please close the YouTube tab in your browser."

    def get_identity(self) -> str:
        """Get assistant's identity information"""
        return f"I am {self.name}, your AI assistant."
    
    def process_command(self, command):
        # Check for deactivation
        if any(word in command for word in self.deactivate_words):
            self.is_active = False
            self.speak("Goodbye! Have a great day!")
            return

        # Check for wake words
        if any(word in command for word in self.wake_words):
            self.is_active = True
            greeting = self.get_time_greeting()
            self.speak(f"{greeting}! How can I help you?")
            return

        # Only process commands if active
        if not self.is_active:
            return

        # Capabilities command
        if "what can you do" in command or "capabilities" in command or "what are your capabilities" in command:
            capabilities = self.get_capabilities()
            self.speak("Here are my capabilities. I'll display them on the console for you to read.")
            print("\n" + capabilities)
            return

        # Basic commands
        if "your name" in command:
            self.speak(self.get_identity())
        elif "time" in command:
            self.speak(self.get_time())
        elif "date" in command:
            self.speak(self.get_date())
        elif "day" in command:
            self.speak(self.get_day())
        elif any(greet in command for greet in ["hello", "hi", "hey"]):
            self.speak("Hello! How can I assist you?")
        elif "how are you" in command:
            self.speak("I'm doing well, thank you for asking!")
        elif any(greet in command for greet in ["good morning", "good afternoon", "good evening"]):
            self.speak(f"{command.capitalize()} to you too!")
            
        # Application commands
        elif command.startswith("open "):
            app_name = command.replace("open", "").strip()
            response = self.open_application(app_name)
            self.speak(response)
            
        elif command.startswith("close "):
            app_name = command.replace("close", "").strip()
            response = self.close_application(app_name)
            self.speak(response)
            
        # Memory commands
        elif "remember" in command:
            parts = command.replace("remember", "").strip().split(" is ")
            if len(parts) == 2:
                key, value = parts
                response = self.remember("user_preferences", key, value)
                self.speak(response)
                
        elif "what is my" in command or "what's my" in command:
            key = command.replace("what is my", "").replace("what's my", "").strip()
            value = self.recall("user_preferences", key)
            if value:
                self.speak(value)
            else:
                self.speak(f"I don't know your {key}. Please tell me by saying 'remember my {key} is [value]'")
                
        # Notes and dates
        elif "add" in command and "notes" in command:
            response = self.add_note()
            if response:
                self.speak(response)
            
        elif "list" in command and "notes" in command:
            response = self.list_notes()
            self.speak(response)
            
        elif "edit" in command and "note" in command:
            note_name = command.replace("edit", "").replace("note", "").strip()
            response = self.edit_note_by_name(note_name)
            if response:
                self.speak(response)
            
        elif "delete" in command and "note" in command:
            if len(self.memory['notes']) == 1:
                response = self.delete_note_by_name(self.memory['notes'][0]['content'])
            else:
                self.speak("What is the note that you want to delete?")
                note_name = self.listen()
                response = self.delete_note_by_name(note_name)
            self.speak(response)
            
        # Reminders
        elif "add" in command and "reminder" in command:
            response = self.add_reminder()
            if response:
                self.speak(response)
            
        elif "list" in command and "reminders" in command:
            response = self.list_reminders()
            self.speak(response)
            
        elif ("edit" in command or "update" in command) and "reminder" in command:
            reminder_name = command.replace("edit", "").replace("update", "").replace("reminder", "").strip()
            response = self.edit_reminder_by_name(reminder_name)
            if response:
                self.speak(response)
            
        elif "delete" in command and "reminder" in command:
            if len(self.memory['reminders']) == 1:
                response = self.delete_reminder_by_name(self.memory['reminders'][0]['name'])
            else:
                self.speak("What is the reminder that you want to delete?")
                reminder_name = self.listen()
                response = self.delete_reminder_by_name(reminder_name)
            self.speak(response)
            
        elif "add" in command and "important" in command and "date" in command:
            parts = command.replace("add important date", "").strip().split(" on ")
            if len(parts) == 2:
                event, date = parts
                response = self.add_important_date(event, date)
                self.speak(response)
            
        elif "when is" in command:
            event = command.replace("when is", "").strip()
            response = self.get_important_date(event)
            self.speak(response)
            
        elif "list" in command and "important" in command and "dates" in command:
            response = self.list_important_dates()
            self.speak(response)
            
        # Favorite apps
        elif "add" in command and "favorite" in command and "app" in command:
            app = command.replace("add favorite app", "").strip()
            response = self.add_favorite_app(app)
            self.speak(response)
            
        elif "list" in command and "favorite" in command and "apps" in command:
            response = self.list_favorite_apps()
            self.speak(response)
            
        # Screenshot
        elif "take" in command and "screenshot" in command:
            response = self.take_screenshot()
            self.speak(response)
            
        # Weather
        elif "weather" in command:
            response = self.get_weather()
            self.speak(response)
            
        # Clear memory
        elif "clear" in command and "memory" in command:
            if "category" in command:
                category = command.replace("clear memory category", "").strip()
                response = self.clear_memory(category)
            else:
                response = self.clear_memory()
            self.speak(response)
            
                # System controls
        elif "volume up" in command or "increase volume" in command:
            level = self.parse_volume_level(command)
            self.volume_up(level)
            self.speak(f"Increasing volume by {level} levels")
            
        elif "volume down" in command or "decrease volume" in command:
            level = self.parse_volume_level(command)
            self.volume_down(level)
            self.speak(f"Decreasing volume by {level} levels")
            
        elif "mute" in command or "silence" in command:
            self.mute_audio()
            self.speak("Muting audio")
            
        elif "unmute" in command or "unsilence" in command:
            self.unmute_audio()
            self.speak("Unmuting audio")
            
        elif "pause" in command or "stop" in command:
             self.pause_media()
             self.speak("Pausing media")
                
        elif "unpause" in command or "resume" in command:
            self.unpause_media()
            self.speak("Resuming media")      
                 
        # Media controls
        elif "play" in command and ("music" in command or "song" in command):
            song_name = command.replace("play", "").replace("music", "").replace("song", "").strip()
            response = self.play_music(song_name)
            self.speak(response)
            
        elif "stop" in command or "stop song" in command:
            response = self.stop_music()
            self.speak(response)
            
            
        # Default response
        else:
            print("Listening...")  # Only print, do not speak

    def run(self):
        self.speak(f"Hello! I'm {self.name}.")
        while True:
            command = self.listen()
            self.process_command(command)
            time.sleep(0.1)

    def get_time_greeting(self):
        """Get a time-appropriate greeting"""
        hour = datetime.datetime.now().hour
        
        if 0 <= hour < 12:
            return "Good morning"
        elif 12 <= hour < 17:
            return "Good afternoon"
        else:
            return "Good evening"

if __name__ == "__main__":
    assistant = AIAssistant()
    assistant.run()
