import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog
import sv_ttk
import json

easyFactor = 3.0
goodFactor = 1.5
hardFactor = 1.0
easyIncrement = 2
goodIncrement = 1
hardIncrement = -1
        
def close(window):
    window.destroy()


def addDeck(inp):
    name = inp.get("1.0", "end-1c")
    if not name:
        tk.messagebox.showerror("Error", "Deck name is empty")
    else:
        decks.append(name.rstrip())
        #print(decks)

def add_flashcard():
    global flashcard_front_input
    global flashcard_back_input
    global deck_dropdown
    front_text = flashcard_front_input.get("1.0", "end-1c")
    back_text = flashcard_back_input.get("1.0", "end-1c")
    selected_deck = deck_dropdown.get()
    flashcard_front_input.delete("1.0", "end")
    flashcard_back_input.delete("1.0", "end")

    if not front_text or not back_text:
        tk.messagebox.showerror("Error", "Contents flashcard is empty")
    else:
        if selected_deck not in flashcards_dict:
            flashcards_dict[selected_deck] = []
        flashcards_dict[selected_deck].append({"front": front_text.rstrip(), "back": back_text.rstrip(), "time": 0, "cardFactor": 1})
        #print(flashcards_dict)    
        
def viewDecks():
    decks_window = tk.Toplevel()
    decks_window.title("Decks")

    tk.Label(decks_window, text="Deck Names", font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=3)

    decks_window.columnconfigure(0, weight=1)
    decks_window.columnconfigure(1, weight=1)
    decks_window.columnconfigure(2, weight=1)

    def delete_deck(deck_name):
        if deck_name in flashcards_dict:
            #print(decks)
            del flashcards_dict[deck_name]
            pointer = decks.index(deck_name)
            decks.pop(pointer)
            decks_window.destroy()
            viewDecks()

    for i, deck_name in enumerate(flashcards_dict, start=1):
        tk.Label(decks_window, text=deck_name).grid(row=i, column=0, padx=5, pady=5, sticky='w')
        tk.Button(decks_window, text="View Flashcards", command=lambda name=deck_name: view_flashcards(name)).grid(row=i, column=2, padx=5, pady=5)
        tk.Button(decks_window, text="Delete Deck", command=lambda name=deck_name: delete_deck(name)).grid(row=i, column=1, padx=5, pady=5)

    for i in range(1, len(flashcards_dict) + 1):
        decks_window.rowconfigure(i, weight=1)

def view_flashcards(deck_name):
    flashcards_window = tk.Toplevel(root)
    flashcards_window.title(deck_name)
    flashcards_window.grid_columnconfigure(1, weight=1)
    flashcards_window.grid_columnconfigure(2, weight=1)
    flashcards_window.grid_columnconfigure(3, weight=1)
    flashcards_window.grid_rowconfigure(0, weight=1)

    def delete_flashcard(flashcard, frame):
        flashcards_dict[deck_name].remove(flashcard)
        frame.destroy()
    
    for i, flashcard in enumerate(flashcards_dict[deck_name], start=1):
        flashcards_window.grid_rowconfigure(i, weight=1)
        front = flashcard['front']
        back = flashcard['back']
        flashcard_frame = tk.Frame(flashcards_window)
        tk.Label(flashcard_frame, text=f'Front: {front}').grid(row=0, column=1,padx=5, pady=1, sticky='nsew')
        tk.Label(flashcard_frame, text=f'Back: {back}').grid(row=0, column=2,padx=5, pady=1, sticky='nsew')
        delete_button = tk.Button(flashcard_frame, text="Delete", command=lambda card=flashcard, frame=flashcard_frame: delete_flashcard(card, frame))
        delete_button.grid(row=0, column=3,padx=5, pady=1, sticky='nsew' )
        flashcard_frame.grid(row=i, column=0, padx=10, pady=5,sticky='nsew')


def createNewDeck():
   top = tk.Toplevel(root)
   top.geometry("250x250")
   top.title("New deck")
   label = tk.Label(top, text="Enter the deck name:", font=("Arial", 15))
   label.pack(padx=20, pady=20)
   entry = tk.Text(top, font=("Arial", 15), height=1)
   entry.pack(padx=20, pady=20)
   add = ttk.Button(top, text="Add", command = lambda:[addDeck(entry), close(top)]).pack(padx=20, pady=20)

def createCards():
    menu_window = tk.Toplevel()
    menu_window.geometry("400x600")
    menu_window.grid_columnconfigure(0, weight=1)

    flashcard_front_heading = tk.Label(menu_window, text="Flashcard Front", font=('Arial', 30, 'bold'))
    flashcard_front_heading.grid(row=0, column=0, pady=10)
    global flashcard_front_input
    flashcard_front_input = tk.Text(menu_window, height=5)
    flashcard_front_input.grid(row=1, column=0, pady=10)

    flashcard_back_heading = tk.Label(menu_window, text="Flashcard Back", font=('Arial', 30, 'bold'))
    flashcard_back_heading.grid(row=2, column=0, pady=10)
    global flashcard_back_input
    flashcard_back_input = tk.Text(menu_window, height=5)
    flashcard_back_input.grid(row=3, column=0, pady=10)

    deck_label = tk.Label(menu_window, text="Select Deck", font=('Arial', 12, 'bold'))
    deck_label.grid(row=5, column=0, pady=10)
    global deck_dropdown
    deck_dropdown = tk.StringVar(menu_window)
    try:
        deck_dropdown.set(decks[0])
        deck_menu = tk.OptionMenu(menu_window, deck_dropdown, *decks)
        deck_menu.grid(row=6, column=0)
        add_flashcard_button = tk.Button(menu_window, text="Add Flashcard", command=add_flashcard)
        add_flashcard_button.grid(row=4, column=0, pady=10)
    except:
            tk.messagebox.showerror("Error", "There are no decks to add cards to.")
            close(menu_window)

def reviewCards():
    global learn_flashcards_window, easy_button, good_button, hard_button
    learn_flashcards_window = tk.Toplevel(root)
    learn_flashcards_window.title("Learn Flashcards")
    learn_flashcards_window.geometry("600x600")
    learn_flashcards_window.grid_rowconfigure(0, weight=1)
    learn_flashcards_window.grid_rowconfigure(1, weight=1)
    learn_flashcards_window.grid_rowconfigure(2, weight=1)
    learn_flashcards_window.grid_rowconfigure(3, weight=1)
    learn_flashcards_window.grid_columnconfigure(0, weight=1)
    learn_flashcards_window.grid_columnconfigure(1, weight=1)

    deck_label = tk.Label(learn_flashcards_window, text="Review Flashcards", font=('Arial', 20, 'bold'))
    deck_label.grid(row=0, column=0, columnspan=4, pady=5)

    deck_dropdown = tk.StringVar(learn_flashcards_window)
    deck_dropdown.set(decks[0])
    deck_menu = tk.OptionMenu(learn_flashcards_window, deck_dropdown, *decks)
    deck_menu.grid(row=1, column=0, columnspan=2, pady=5)

    select_deck_button = tk.Button(learn_flashcards_window, font=('Arial', 15), text="Select Deck",command=lambda: select_deck(deck_dropdown.get()))
    select_deck_button.grid(row=1, column=1, columnspan=4, pady=5)

    global easy_button, good_button, hard_button
    easy_button = tk.Button(learn_flashcards_window, text="Easy", font=('Arial', 15), command=lambda: rate_flashcard("Easy"), bg="green")
    #button for easy triggers the rate_flashcard function and "Easy" is given as the response
    good_button = tk.Button(learn_flashcards_window, text="Good", font=('Arial', 15), command=lambda: rate_flashcard("Good"), bg="orange")
    #button for good triggers the rate_flashcard function and "Good" is given as the response
    hard_button = tk.Button(learn_flashcards_window, text="Hard", font=('Arial', 15), command=lambda: rate_flashcard("Hard"), bg="red")
    #button for hard triggers the rate_flashcard function and "Hard" is given as the response
    flip_button = tk.Button(learn_flashcards_window, text="Flip", font=('Arial', 15), command=flip_flashcard)
    flip_button.grid(row=7, column=0, padx=10, pady=20)

    global flashcard_text
    flashcard_text = tk.StringVar()
    flashcard_label = tk.Label(learn_flashcards_window, textvariable=flashcard_text, font=('Arial', 16))
    flashcard_label.grid(row=3, column=0, columnspan=4, pady=20)

    
def flip_flashcard():
    global current_flashcard_index, current_flashcard_side
    current_flashcard_side = "back" if current_flashcard_side == "front" else "front"
    display_flashcard()
    show_rating_buttons()

def rate_flashcard(rating):
    global current_flashcard_index
    time = current_flashcard["time"]
    originalFactor = current_flashcard["cardFactor"]

    if rating == "Easy":
        current_flashcard["time"] += originalFactor * easyFactor
        current_flashcard["cardFactor"] += easyIncrement
        print(current_flashcard["cardFactor"])
        print(current_flashcard["time"])
    elif rating == "Good":
        current_flashcard["time"] += originalFactor * goodFactor
        current_flashcard["cardFactor"] += goodIncrement
        print(current_flashcard["cardFactor"])
        print(current_flashcard["time"])
    elif rating == "Hard":
        current_flashcard["time"] += originalFactor * hardFactor
        if current_flashcard["cardFactor"] == 0:
            pass
        else:
            current_flashcard["cardFactor"] += hardIncrement
        print(current_flashcard["cardFactor"])
        print(current_flashcard["time"])

    current_flashcard_index += 1
    if current_flashcard_index < len(current_deck_flashcards):
        display_flashcard()
        flip_flashcard()
        hide_rating_buttons()
    else:
        learn_flashcards_window.destroy()

def select_deck(deck_name):
    global current_deck_flashcards, current_flashcard_index, current_flashcard_side
    current_deck_flashcards = flashcards_dict.get(deck_name, [])
    current_flashcard_index = 0
    current_flashcard_side = "front"
    display_flashcard()
    hide_rating_buttons()

def display_flashcard():
    global current_flashcard
    try:
        current_flashcard = current_deck_flashcards[current_flashcard_index]
        flashcard_text.set(current_flashcard[current_flashcard_side])
    except:
        tk.messagebox.showerror("Error", "No flashcards to review in this deck")

def show_rating_buttons(): # These show the ratings button when the flashcard is flipped
    easy_button.grid(row=7, column=1, padx=10, pady=10, sticky="e")
    good_button.grid(row=7, column=2, padx=10, pady=10, sticky="e")
    hard_button.grid(row=7, column=3, padx=10, pady=10, sticky="e")

def hide_rating_buttons(): # These make the buttons dissapear when the flashcard is front sided
    easy_button.grid_forget()
    good_button.grid_forget()
    hard_button.grid_forget()


root = tk.Tk()
root.title("Revisio")
root.geometry("600x600")
#root.configure(bg="gray")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

def open_settings():
    settings_window = tk.Toplevel(root) # creates a new menu
    settings_window.title("Settings")
    settings_window.geometry("300x300")
    settings_window.columnconfigure(0, weight=1) 
    settings_window.rowconfigure(0, weight=1)
    settings_window.rowconfigure(1, weight=1)
    button = ttk.Button(settings_window, text="Toggle theme", command=sv_ttk.toggle_theme)
    # the line above: after pressing the toggle theme button this command is what changes the theme.
    button.grid(row=1, column=0)
    
toolbar_frame = tk.Frame(root)
toolbar_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
settings_button = ttk.Button(toolbar_frame, text="Settings", command=open_settings)
settings_button.grid(row=0, column=2, padx=10, pady=5)
sv_ttk.set_theme("dark")
#This is the code for the toolbar where the button is


decks = []
flashcards_dict = {}
try:
    file = open("flashcards", "r")
    flashcards_dict = json.load(file)
    file.close()
    file = open("decks", "r")
    decks = json.load(file)
    file.close()
except:
    pass
#json is used to handle saving and downloading the flashcards.

deckTitle = tk.Label(root,text = "Revisio",font=('Nexa', 40))
deckTitle.grid(row=1, column=0, columnspan=3, pady=20)

newDeck = ttk.Button(root,text="New deck",command = createNewDeck)
viewDeck = ttk.Button(root,text="View decks",command = viewDecks)
createCard = ttk.Button(root,text="Create cards",command = createCards)
revise = ttk.Button(root,text="Revise Cards",command = reviewCards)
viewDeck.grid(row=2, column=2, padx=5, pady=1, sticky='nsew')
newDeck.grid(row=2, column=0, padx=5, pady=1, sticky='nsew')
createCard.grid(row=2, column = 1, padx=5, pady=1, sticky='nsew')
revise.grid(row=3, column = 1, padx=5, pady=20, sticky='nsew')

def on_closing():
    file = open("flashcards", "w")
    json.dump(flashcards_dict, file)
    file.close()
    file = open("decks", "w")
    json.dump(decks, file)
    file.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing) #calls on_closing when window is closed

root.mainloop()




