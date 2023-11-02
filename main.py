import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog
import sv_ttk
import json
import time

easyFactor = 3.0
goodFactor = 1.5
hardFactor = 1.0
easyIncrement = 2
goodIncrement = 1
hardIncrement = -1

flashcardsLearnt = 0
easy = 0
good = 0
hard = 0

#setting base values for the algorithm to use
        
def close(window):
    window.destroy()

def startTime():
    global start
    start = time.time()

def stopTime():
    global elapsedTime
    elapsedTime = round((time.time() - start) / 60, 2)

def addDeck(inp):
    name = inp.get("1.0", "end-1c")
    if not name:
        tk.messagebox.showerror("Error", "Deck name is empty")
    else:
        decks.append(name.rstrip())
        #print(decks)

def add_edit(flashcard):
    global frontEdit, backEdit
    front_text = frontEdit.get("1.0", "end-1c")
    back_text = backEdit.get("1.0", "end-1c")
    flashcard["front"] = front_text
    flashcard["back"] = back_text

def add_flashcard():
    global flashcard_front_input, flashcard_back_input, deck_dropdown
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
    tk.Label(decks_window, text="All Decks", font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=3)
    decks_window.columnconfigure(0, weight=1)
    decks_window.columnconfigure(1, weight=1)
    decks_window.columnconfigure(2, weight=1)
    #basic settings for the viewDecks menu, weighting is implemented to make sure the window scales


    def delete_deck(deck_name): # If the user wants to delete the deck
        if deck_name in flashcards_dict:
            #print(decks)
            del flashcards_dict[deck_name]
            pointer = decks.index(deck_name)
            decks.pop(pointer)
            decks_window.destroy()
            viewDecks()     

    for i, deck_name in enumerate(flashcards_dict, start=1): #for loops lists all the decks
        tk.Label(decks_window, text=deck_name).grid(row=i, column=0, padx=5, pady=5, sticky='w')
        tk.Button(decks_window, text="View Flashcards", command=lambda name=deck_name: view_flashcards(name)).grid(row=i, column=2, padx=5, pady=5)
        tk.Button(decks_window, text="Delete Deck", command=lambda name=deck_name: delete_deck(name)).grid(row=i, column=1, padx=5, pady=5)

    for i in range(1, len(flashcards_dict) + 1): #for loops adds weightings to all the decks shown in the menu 
        decks_window.rowconfigure(i, weight=1)

def view_flashcards(deck_name):
    flashcards_window = tk.Toplevel(root)
    flashcards_window.title(deck_name)

    tk.Label(flashcards_window, text=deck_name, font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=3)

    flashcards_window.columnconfigure(0, weight=1)
    flashcards_window.rowconfigure(0, weight=1)

    def edit_flashcard(flashcard):
        f = flashcard
        menu = tk.Toplevel(root)
        menu.title("Edit flashcard")
        flashcard_front_heading = tk.Label(menu, text="Flashcard Front", font=('Arial', 30, 'bold'))
        flashcard_front_heading.grid(row=0, column=0, pady=10)
        global frontEdit
        frontEdit = tk.Text(menu, height=5)
        frontEdit.grid(row=1, column=0, pady=10)

        flashcard_back_heading = tk.Label(menu, text="Flashcard Back", font=('Arial', 30, 'bold'))
        flashcard_back_heading.grid(row=2, column=0, pady=10)
        global backEdit
        backEdit = tk.Text(menu, height=5)
        backEdit.grid(row=3, column=0, pady=10)

        editButton = tk.Button(menu, text="Edit", command=lambda card=f:[add_edit(card), close(menu)] )
        editButton.grid(row=4, column=0, pady=10)
        
    def delete_flashcard(flashcard, frame): #function that deletes a flashcard if clicked.
        flashcards_dict[deck_name].remove(flashcard)
        frame.destroy()

    def reset_flashcard(flashcard):
        flashcard['time'] = 0
        flashcard['cardFactor'] = 1

    for i, flashcard in enumerate(flashcards_dict[deck_name], start=1): #loops through all the cards
        front = flashcard['front']
        back = flashcard['back']
        flashcardFrame = tk.Frame(flashcards_window) #frame to organise the flashcard front and back
        flashcardFrame.grid(row=i, column=0, padx=10, pady=5, sticky='nsew')

        flashcardFrame.columnconfigure(0, weight=1)
        flashcardFrame.columnconfigure(1, weight=1)
        flashcardFrame.columnconfigure(2, weight=1)
        flashcardFrame.columnconfigure(3, weight=1)
        flashcardFrame.columnconfigure(4, weight=1)

        tk.Label(flashcardFrame, text=f'Front: {front}').grid(row=0, column=0, padx=5, pady=1, sticky='nsew')
        tk.Label(flashcardFrame, text=f'Back: {back}').grid(row=0, column=1, padx=5, pady=1, sticky='nsew')
        delete_button = tk.Button(flashcardFrame, text="Delete", command=lambda card=flashcard, frame=flashcardFrame: delete_flashcard(card, frame))
        delete_button.grid(row=0, column=2, padx=5, pady=1, sticky='nsew')
        reset_button = tk.Button(flashcardFrame, text="Reset", command=lambda card=flashcard: reset_flashcard(card))
        reset_button.grid(row=0, column=3, padx=5, pady=1, sticky='nsew')
        edit_button = tk.Button(flashcardFrame, text="Edit", command=lambda card=flashcard: edit_flashcard(card))
        edit_button.grid(row=0, column=4, padx=5, pady=1, sticky='nsew')

    flashcards_window.grid_rowconfigure(i+1, weight=1)




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
    startTime()
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
    try:
        deck_dropdown.set(decks[0])
    except:
        tk.messagebox.showerror("Error", "No decks to review")
    deck_menu = tk.OptionMenu(learn_flashcards_window, deck_dropdown, *decks)
    deck_menu.grid(row=1, column=0, columnspan=2, pady=5)

    select_deck_button = tk.Button(learn_flashcards_window, font=('Arial', 15), text="Select Deck",command=lambda: select_deck(deck_dropdown.get()))
    select_deck_button.grid(row=1, column=1, columnspan=4, pady=5)

    global easy_button, good_button, hard_button
    easy_button = tk.Button(learn_flashcards_window, text="Easy", font=('Arial', 15), command=lambda: rate_flashcard("Easy"), bg="green")
    good_button = tk.Button(learn_flashcards_window, text="Good", font=('Arial', 15), command=lambda: rate_flashcard("Good"), bg="orange")
    hard_button = tk.Button(learn_flashcards_window, text="Hard", font=('Arial', 15), command=lambda: rate_flashcard("Hard"), bg="red")
    flip_button = tk.Button(learn_flashcards_window, text="Flip", font=('Arial', 15), command=flip_flashcard)
    flip_button.grid(row=7, column=0, padx=10, pady=20)

    global flashcard_text
    flashcard_text = tk.StringVar()
    flashcard_label = tk.Label(learn_flashcards_window, textvariable=flashcard_text, font=('Arial', 16))
    flashcard_label.grid(row=3, column=0, columnspan=4, pady=20)

    
def flip_flashcard():
    global nextIndex, current_flashcard_side
    current_flashcard_side = "back" if current_flashcard_side == "front" else "front"
    display_flashcard()
    show_rating_buttons()

def rate_flashcard(rating): # rating is either "Good", "Easy" or "Hard" depending on what the user chose.
    global nextIndex, reviewFlashcards, flashcardsLearnt, good, easy, hard
    time = current_flashcard["time"]
    cardFactor = current_flashcard["cardFactor"]
    flashcardsLearnt += 1

    if rating == "Easy": # if they found it easy
        current_flashcard["time"] += cardFactor * easyFactor
        current_flashcard["cardFactor"] += easyIncrement
        easy += 1
    elif rating == "Good": # if they found it Good
        current_flashcard["time"] += cardFactor * goodFactor
        current_flashcard["cardFactor"] += goodIncrement
        good += 1
    elif rating == "Hard": # if they found it hard
        current_flashcard["time"] += cardFactor * hardFactor
        hard += 1
        if current_flashcard["cardFactor"] == 0: # This if statement makes sure the flashcard doesn't have a negative factor
            pass
        else:
            current_flashcard["cardFactor"] += hardIncrement
    try:
        nextIndex = reviewFlashcards[0]
        reviewFlashcards.pop(0)
        display_flashcard()
        flip_flashcard()
        hide_rating_buttons()
    except:
        tk.messagebox.showerror("Error", "All due flashcards have been reviewed.")
        learn_flashcards_window.destroy()
        stopTime()

def select_deck(deck_name):
    global current_deck_flashcards, nextIndex, current_flashcard_side, reviewFlashcards
    current_deck_flashcards = flashcards_dict.get(deck_name, [])
    current_flashcard_side = "front"
    reviewFlashcards = []
    for i, flashcard in enumerate(current_deck_flashcards):
        if flashcard.get("time", 0) == 0:
            reviewFlashcards.append(i)
    try:
        nextIndex = reviewFlashcards[0]
        reviewFlashcards.pop(0)
    except:
        tk.messagebox.showerror("Error", "Deck has been completed. No flashcards due")
    display_flashcard()
    hide_rating_buttons()

def display_flashcard():
    global current_flashcard
    try:
        current_flashcard = current_deck_flashcards[nextIndex]
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

def helpW():
    window = tk.Toplevel(root) # creates a new menu
    window.title("Information")
    window.geometry("300x300")
    infoHeading = ttk.Label(window, text="Information", font=("Arial", 14, "bold"))
    infoHeading.pack(pady=10)
    info = ttk.Label(window, text="This app is intended to help students revise effectively by creating and reviewing flashcards under a spaced repetition algorithm that helps manage when flashcards should be reviewed. ")
    info.config(wraplength=250)
    info.pack()
    helpHeading = ttk.Label(window, text="Help", font=("Arial", 14, "bold"))
    helpHeading.pack(pady=10)
    helpT = ttk.Label(window, text="Start by creating a deck by clicking New Deck in the main menu. You can then name your deck, add flashcards using the button in the menu and then review them using the review flashcards button also in the main menu.")
    helpT.config(wraplength=250)
    helpT.pack()

def statistics():
    global elapsedTime
    window = tk.Toplevel(root)
    window.title("Statistics")
    window.grid_rowconfigure(0, weight=1)  
    window.grid_columnconfigure(0, weight=1)  

    title = tk.Label(window, text="Statistics", font=('Arial', 16, 'bold'))
    title.grid(row=0, column=0, pady=10)

    stats = [
        ("Easy Flashcards Done:", easy),
        ("Good Flashcards Done:", good),
        ("Hard Flashcards Done:", hard),
        ("Total Flashcards Done:", flashcardsLearnt),
        ("Time Spent (minutes):", elapsedTime)
    ]

    for i, (label_text, value) in enumerate(stats, start=1):
        window.grid_rowconfigure(i, weight=1)
        label = tk.Label(window, text=label_text, font=('Helvetica', 12))
        value_label = tk.Label(window, text=value, font=('Helvetica', 12))
        label.grid(row=i, column=0, sticky='w')
        value_label.grid(row=i, column=1, sticky='e')

toolbar_frame = tk.Frame(root)
toolbar_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
settings_button = ttk.Button(toolbar_frame, text="Settings", command=open_settings)
settings_button.grid(row=0, column=2, padx=10, pady=5)
help_button = ttk.Button(toolbar_frame, text="Help and Info", command=helpW)
help_button.grid(row=0, column=3, padx=10, pady=5)
statistics = ttk.Button(toolbar_frame, text="Statistics", command=statistics)
statistics.grid(row=0, column=4, padx=10, pady=5)
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




