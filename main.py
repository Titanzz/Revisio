import tkinter as tk
import tkinter.ttk as ttk


root = tk.Tk()
root.title("Revisio")
root.geometry("500x500")


decks = []

def addDeck(inp):
    name = inp.get()
    decks.append([name])
    print(decks)
    
def viewDecks():
    new_window = tk.Toplevel()
    deck_name_heading = tk.Label(new_window, text="Deck Name", font=('Arial', 12, 'bold'))
    deck_name_heading.grid(row=0, column=0)
    num_cards_heading = tk.Label(new_window, text="Number of Cards", font=('Arial', 12, 'bold'))
    num_cards_heading.grid(row=0, column=1, padx=1)
    new_window.grid_rowconfigure(1, weight=1)
    new_window.grid_columnconfigure(0, weight=1)
    new_window.grid_columnconfigure(1, weight=1)


    for i, deck_info in enumerate(decks, start=1):
        deck_name = deck_info[0]
        deck_label = tk.Label(new_window, text=deck_name)
        deck_label.grid(row=i, column=0)


 
def close(window):
    window.destroy()

def createNewDeck():
    top = tk.Toplevel(root)
    top.geometry("250x250")
    top.title("New deck")
    ttk.Label(top, text="Deck name", font=("Nexa", 15)).grid(padx=20, pady=20)
    deckNameInput = tk.Entry(top)
    deckNameInput.grid(padx=20, pady=22)
    add = ttk.Button(top, text="Add", command = lambda:[addDeck(deckNameInput), close(top)]).grid(padx=20, pady=25)

def createCards():
    menu_window = tk.Toplevel()

    flashcard_front_heading = tk.Label(menu_window, text="Flashcard Front", font=('Arial', 12, 'bold'))
    flashcard_front_heading.grid(row=0, column=0, sticky="w")
    global flashcard_front_input
    flashcard_front_input = tk.Entry(menu_window)
    flashcard_front_input.grid(row=1, column=0, padx=10, pady=5)

    flashcard_back_heading = tk.Label(menu_window, text="Flashcard Back", font=('Arial', 12, 'bold'))
    flashcard_back_heading.grid(row=2, column=0, sticky="w")
    global flashcard_back_input
    flashcard_back_input = tk.Entry(menu_window)
    flashcard_back_input.grid(row=3, column=0, padx=10, pady=5)

    deck_label = tk.Label(menu_window, text="Select Deck", font=('Arial', 12, 'bold'))
    deck_label.grid(row=5, column=0, sticky="w")
    global deck_dropdown
    deck_dropdown = tk.StringVar(menu_window)
    try:
        deck_dropdown.set(decks[0][0])
        deck_menu = tk.OptionMenu(menu_window, deck_dropdown, *decks)
        deck_menu.grid(row=6, column=0, padx=10, pady=5)
        add_flashcard_button = tk.Button(menu_window, text="Add Flashcard", command=add_flashcard)
        add_flashcard_button.grid(row=4, column=0, padx=10, pady=10)
    except:
            error = tk.Toplevel()
            error.geometry("250x100")
            error.title("Error message")
            errormsg = tk.Label(error, text="Error, no decks to add flashcards into.").grid(padx=20, pady=20)
            menu_window.destroy()




def add_flashcard():
    global flashcard_front_input
    global flashcard_back_input
    global deck_dropdown
    front_text = flashcard_front_input.get()
    back_text = flashcard_back_input.get()
    selected_deck = deck_dropdown.get()

    flashcard_front_input.delete(0, tk.END)
    flashcard_back_input.delete(0, tk.END)

    print("Flashcard Front:", front_text)
    print("Flashcard Back:", back_text)
    print("Selected Deck:", selected_deck)

deckTitle = ttk.Label(root,text = "Main Menu",foreground = "black",font=('Nexa', 40))
deckTitle.grid(row=0, column=2,padx=5, pady=5)

newDeck = ttk.Button(root,text="New deck",command = createNewDeck)
viewDeck = ttk.Button(root,text="View decks",command = viewDecks)
createCard = ttk.Button(root,text="Create cards",command = createCards)
viewDeck.grid(row=1, column=3, padx=5, pady=1, sticky='nsew')
newDeck.grid(row=1, column=1, padx=5, pady=1, sticky='nsew')
createCard.grid(row=1, column = 2, padx=5, pady=1, sticky='nsew')

root.mainloop()




