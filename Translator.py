from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.ttk import Combobox
from tkinter.scrolledtext import ScrolledText
import googletrans, pyttsx3, os, sys
from googletrans import Translator

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

try: 
	engine = pyttsx3.init()
except ImportError as e:
	messagebox.showerror("Error: The driver is not found")
except RuntimeError as e:
	messagebox.showerror("Error: The driver fails to initialize")

translator = Translator()
LANGUAGES = googletrans.LANGUAGES
NAMES = []
KEYS = []

for key in LANGUAGES:
        KEYS.append(key)
        NAMES.append(LANGUAGES[key])

root = Tk()
root.title("My Translator")
root.iconbitmap(os.path.join(resource_path(""), "icon.ico"))
root.attributes('-alpha', 0.8)

text_frame = Frame(root)
text_frame.pack(pady = 20)

inputfield = ScrolledText(text_frame, wrap=None, width = 16, height = 10, font=("Arial", 16))
inputfield.grid(row = 0, column = 0)
inputfield.focus()
outputfield = ScrolledText(text_frame, width = 16, height = 10, font=("Arial", 16))
outputfield.grid(row = 0, column = 1)
outputfield.configure(state = 'disabled')

button_frame = Frame(root)
button_frame.pack(pady = 20, padx = 0)

def trans():
	outputfield.configure(state = 'normal')
	outputfield.delete(1.0, END)
	words = str(inputfield.get(1.0, END))
	fr = option1.current()
	fr = KEYS[fr]
	to = option2.current()
	to = KEYS[to]
	words = translator.translate(words, src=fr, dest=to)
	words = words.text
	outputfield.insert(1.0, words)
	outputfield.configure(state = 'disabled')

def clear_input():
	inputfield.delete(1.0, END)

def clear_output():
	outputfield.configure(state = 'normal')
	outputfield.delete(1.0, END)
	outputfield.configure(state = 'disabled')

def speak_input():
	engine.say(inputfield.get(1.0, END))
	engine.runAndWait()

def speak_output():
	engine.say(outputfield.get(1.0, END))
	engine.runAndWait()

def setVoice(gender):
	voices = engine.getProperty('voices')  
	if gender == "male":
		engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
	else:
		engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

def save_input():
	try:
		input_text = inputfield.get(1.0, END)

		file_name = filedialog.asksaveasfilename(initialdir = "/", title = "Save File", filetypes = ())

		if file_name:
			engine.save_to_file(input_text, f"{file_name}.mp3")
			engine.runAndWait()
			messagebox.showinfo("Translator", "File saved")
	except:
		messagebox.showerror("Error", "Oh sh*t Translator just crashed")

def save_output():
	try:
		output_text = outputfield.get(1.0, END)

		file_name = filedialog.asksaveasfilename(initialdir = "/", title = "Save File", filetypes = ())

		if file_name:
			engine.save_to_file(output_text, f"{file_name}.mp3")
			engine.runAndWait()
			messagebox.showinfo("Translator", "File saved")
	except:
		messagebox.showerror("Error", "Oh sh*t Translator just crashed")

def about():
	about_win = Toplevel(root)
	about_win.title("About Translator")
	about_win.attributes('-alpha', 0.8)
	
	txt = ScrolledText(about_win, width = 60, font = ("Segoe UI", 10))
	words = """
MIT License

Copyright (c) 2022 Anh Duc Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
	txt.pack()
	txt.insert(1.0, words)
	txt.focus()

def close():
	exit()

speak_input_btn = Button(button_frame, font = ("Segoe UI", 10), text = "Speak", command=speak_input)
speak_input_btn.grid(row = 0, column = 0)

fr_lbl = Label(button_frame, font = ("Segoe UI", 10), text = "From:")
fr_lbl.grid(row = 0, column = 1)

option1 = Combobox(button_frame, values = NAMES, width = 15)
option1.grid(row = 0, column = 2)
option1.current(21)

btn = Button(button_frame, font = ("Segoe UI", 10), text = "Translate!", command = trans, width = 10)
btn.grid(row = 0, column = 3)

to_lbl = Label(button_frame, font = ("Segoe UI", 10), text = "To:")
to_lbl.grid(row = 0, column = 4)

option2 = Combobox(button_frame, values = NAMES, width = 15)
option2.grid(row = 0, column = 5)
option2.current(101)

speak_output_btn = Button(button_frame, font = ("Segoe UI", 10), text = "Speak", command = speak_output)
speak_output_btn.grid(row = 0, column = 6)

menuBar = Menu(root)

fileMenu = Menu(menuBar, tearoff=0)
fileMenu.add_command(label = "Clear input", command = clear_input)
fileMenu.add_command(label = "Clear output", command = clear_output)
fileMenu.add_separator()
fileMenu.add_command(label = "About Translator", command = about)
fileMenu.add_command(label = "Exit", command = close)
menuBar.add_cascade(label = "Text", menu = fileMenu)

optionMenu = Menu(menuBar, tearoff=0)
optionMenu.add_command(label = "Translate", command = trans)
optionMenu.add_separator()
# optionMenu.add_command(label = "Speak input", command = speak_input)
# optionMenu.add_command(label = "Speak input", command = speak_output)
# optionMenu.add_separator()
optionMenu.add_command(label = "Set voice to male", command = lambda : setVoice("male"))
optionMenu.add_command(label = "Set voice to female", command = lambda : setVoice("female"))
optionMenu.add_command(label = "Save input speech to a file", command = save_input)
optionMenu.add_command(label = "Save output speech to a file", command = save_output)
menuBar.add_cascade(label = "Options", menu = optionMenu)

root.config(menu = menuBar)

root.mainloop()
