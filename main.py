import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog


root = tk.Tk()
root.title("Revisio")
root.geometry("600x600")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
def on_resize(event):
    new_width = event.width
    new_height = event.height
    
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button):
            button_width = new_width // 6
            button_height = new_height // 20
            widget.config(width=button_width, height=button_height, font=("Helvetica", 10))
        elif isinstance(widget, tk.Label) and widget == heading_label:
            widget.config(font=("Helvetica", 20))
root.bind("<Configure>", on_resize)

decks = []
flashcards_dict = {}


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
   label = tk.Label(top, text="Enter the deck name:", font=("Arial", 15))
   label.pack(padx=20, pady=20)
   entry = tk.Entry(top, font=("Arial", 15))
   entry.pack(padx=20, pady=20)
   add = ttk.Button(top, text="Add", command = lambda:[addDeck(entry), close(top)]).pack(padx=20, pady=20)

def createCards():
    menu_window = tk.Toplevel()
    menu_window.geometry("400x400")
    menu_window.grid_columnconfigure(0, weight=1)

    flashcard_front_heading = tk.Label(menu_window, text="Flashcard Front", font=('Arial', 30, 'bold'))
    flashcard_front_heading.grid(row=0, column=0,)
    global flashcard_front_input
    flashcard_front_input = tk.Entry(menu_window)
    flashcard_front_input.grid(row=1, column=0)

    flashcard_back_heading = tk.Label(menu_window, text="Flashcard Back", font=('Arial', 30, 'bold'))
    flashcard_back_heading.grid(row=2, column=0, )
    global flashcard_back_input
    flashcard_back_input = tk.Entry(menu_window)
    flashcard_back_input.grid(row=3, column=0)

    deck_label = tk.Label(menu_window, text="Select Deck", font=('Arial', 12, 'bold'))
    deck_label.grid(row=5, column=0, )
    global deck_dropdown
    deck_dropdown = tk.StringVar(menu_window)
    try:
        deck_dropdown.set(decks[0][0])
        deck_menu = tk.OptionMenu(menu_window, deck_dropdown, *decks)
        deck_menu.grid(row=6, column=0)
        add_flashcard_button = tk.Button(menu_window, text="Add Flashcard", command=add_flashcard)
        add_flashcard_button.grid(row=4, column=0)
    except:
            tk.messagebox.showerror("Error", "There are no decks to add cards to.")




def add_flashcard():
    global flashcard_front_input
    global flashcard_back_input
    global deck_dropdown
    front_text = flashcard_front_input.get()
    back_text = flashcard_back_input.get()
    selected_deck = deck_dropdown.get()
    flashcard_front_input.delete(0, tk.END)
    flashcard_back_input.delete(0, tk.END)

    if selected_deck not in flashcards_dict:
        flashcards_dict[selected_deck] = []
    flashcards_dict[selected_deck].append({"front": front_text, "back": back_text})
    print(flashcards_dict)

deckTitle = ttk.Label(root,text = "Main Menu",foreground = "black",font=('Nexa', 40))
deckTitle.grid(row=0, column=0, columnspan=3, pady=20)

newDeck = ttk.Button(root,text="New deck",command = createNewDeck)
viewDeck = ttk.Button(root,text="View decks",command = viewDecks)
createCard = ttk.Button(root,text="Create cards",command = createCards)
viewDeck.grid(row=1, column=2, padx=5, pady=1, sticky='nsew')
newDeck.grid(row=1, column=0, padx=5, pady=1, sticky='nsew')
createCard.grid(row=1, column = 1, padx=5, pady=1, sticky='nsew')


root.mainloop()




