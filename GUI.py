import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
from VGbot import detect_game_name, predict_class, detected_response

def send_message(): #handles user input from search button
    user_text = user_input.get().strip()
    user_input.delete(0, tk.END)
    chat_box.tag_config("user", foreground="blue")
    chat_box.insert(tk.END, "You: " + user_text + "\n", "user")

    Thread(target=process_message, args=(user_text,)).start()

def process_message(user_text): #processes users inputted message, calls upon functions
    game_names = detect_game_name(user_text)
    detected_game = game_names[0] if game_names else None
    if detected_game:
        game_queries(detected_game, send_button)
    else:
        predicted = predict_class(user_text)
        if predicted:
            chat_box.tag_config("bot", foreground="green")
            chat_box.insert(tk.END, "Game Bot: Seems like you might be interested in: " + str(predicted) + "\n", "bot")
            chat_box.insert(tk.END, "Type the name of the one you are interested in\n", "bot")

def game_queries(game, send_button):
    available_info = ['description', 'release date', 'developer']
    chat_box.tag_config("bot", foreground="green")  # Add color for bot response
    chat_box.insert(tk.END, "Game Bot: I see you're interested in {}\n".format(game), "bot")
    chat_box.insert(tk.END,
                    "Game Bot: What would you like to know about this game? ({} or click 'Restart Program')\n".format(
                        ', '.join(available_info)), "bot")

    def handle_response():
        user_response = user_input.get().strip().lower()
        chat_box.insert(tk.END, "You: " + user_response + "\n", "user")  #show user's input
        if user_response == 'done':
            chat_box.tag_config("bot", foreground="green")  # Add color for bot response
            chat_box.insert(tk.END, "Game Bot: Interested in any other game? Go ahead and tell me the name.\n", "bot")
            chat_box.insert(tk.END, "Game Bot: If not, just say goodbye to exit.\n", "bot")
            # Clear the user input
            user_input.delete(0, tk.END)
            process_message("")  # Call process_message with an empty string to continue with the next input
        elif user_response == 'goodbye':
            chat_box.tag_config("bot", foreground="green")  # Add color for bot response
            chat_box.insert(tk.END, "Game Bot: Thank you for using, goodbye!\n", "bot")
            root.destroy()  # Exit the program gracefully
        elif user_response in available_info:
            response = detected_response(game, user_response)
            chat_box.tag_config("bot", foreground="green")  # Add color for bot response
            chat_box.insert(tk.END, "Game Bot: {}\n".format(response), "bot")
            available_info.remove(user_response)
            # Clear the user input
            user_input.delete(0, tk.END)
            # Check if there are more info to ask about
            if available_info:
                chat_box.tag_config("bot", foreground="green")
                chat_box.insert(tk.END,
                                "Game Bot: What else would you like to know? ({} or click 'Restart Program')\n".format(
                                    ', '.join(available_info)), "bot")
            else:
                chat_box.tag_config("bot", foreground="green")
                chat_box.insert(tk.END, "Game Bot: That's all the information I have about this game, click 'Restart "
                                        "Program.\n", "bot")
        else:
            chat_box.tag_config("bot", foreground="green")
            chat_box.insert(tk.END,
                            "Game Bot: I'm sorry, I don't understand that. Please choose from the available options.\n",
                            "bot")

    #bind the callback function to the send button
    send_button.config(command=handle_response)

def restart_program(): #destroys current window and opens new one
    global root
    root.destroy()

    root = tk.Tk()
    root.title("Game Bot")
    root.geometry("500x400")

    global chat_box, user_input, send_button  # Add send_button to global variables
    chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
    chat_box.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
    chat_box.insert(tk.END, "Game Bot: Hi there! I'm a Video Game Bot. "
                                    "Name a video game you would like to learn about!\n")

    user_input = tk.Entry(root, width=40)
    user_input.grid(row=1, column=0, padx=10, pady=10)

    send_button = tk.Button(root, text="Send", command=send_message)
    send_button.grid(row=1, column=1, padx=10, pady=10)

    restart_button = tk.Button(root, text="Restart Program", command=restart_program)
    restart_button.grid(row=2, column=0, padx=10, pady=10)

    root.mainloop()


root = tk.Tk()
root.title("Game Bot")
root.geometry("500x400")

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
chat_box.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
chat_box.insert(tk.END, "Game Bot: Hi there! I'm a Video Game Bot. "
                            "Name a video game you would like to learn about!\n")

user_input = tk.Entry(root, width=40)
user_input.grid(row=1, column=0, padx=10, pady=10)

send_button = tk.Button(root, text="Search", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

restart_button = tk.Button(root, text="Restart Program", command=restart_program)
restart_button.grid(row=2, column=0, padx=10, pady=10)

root.mainloop()

#test game names: Streamer Life Simulator, Path of Exile, May 13, 2020