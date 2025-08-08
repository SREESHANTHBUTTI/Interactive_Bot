import json
import random
import tkinter as tk
from tkinter import scrolledtext, filedialog
import networkx as nx
import cv2
from PIL import Image, ImageTk
import numpy as np

# Fetch intents from the intents.json file
def fetch_intents(file):
    with open(file, 'r') as intent_file:
        outsource = json.load(intent_file)

        
    return outsource["intents"]

# Match user input with intents in the intents file
def match_intentions(user_input, intents):
    for intent in intents:
        for pattern in intent["text"]:
            if pattern.lower() in user_input.lower():
                return intent["responses"]
    return ["Sorry! I did not catch that. Can you rephrase that? For reference kindly see the intents.json"]

# Graph-based Intent Tracking: This creates a graph structure to analyze relationships
def create_intent_graph(intents):
    G = nx.Graph()
    for intent in intents:
        G.add_node(intent['intent'], responses=intent['responses'], text=intent['text'])
        # Add edges based on intent relationships (this can be expanded further)
        for connected_intent in intents:
            if intent != connected_intent:
                G.add_edge(intent['intent'], connected_intent['intent'], weight=random.random())
    return G

# Image Processing: Detect simple objects (as an example, we'll just load and display the image)
def process_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)  # Apply binary thresholding
    return thresh  # Return processed image

# GUI setup for the chatbot
def chatbot_gui():
    intents = fetch_intents("intents.json")
    G = create_intent_graph(intents)  # Create a graph of intents

    def get_response(user_input):
        responses = match_intentions(user_input, intents)
        return random.choice(responses)

    def send():
        user_input = entry.get()
        if user_input.lower() == "bye":
            chatbox.config(state=tk.NORMAL)
            chatbox.insert(tk.END, f"You: {user_input}\nChatbot: Goodbye! Have a great day!\n")
            chatbox.config(state=tk.DISABLED)
            app.quit()
        else:
            response = get_response(user_input)
            chatbox.config(state=tk.NORMAL)
            chatbox.insert(tk.END, f"You: {user_input}\nChatbot: {response}\n")
            chatbox.config(state=tk.DISABLED)
            entry.delete(0, tk.END)

    def upload_image():
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if filepath:
            processed_image = process_image(filepath)
            # Convert the processed image to a format suitable for display in Tkinter
            processed_image = Image.fromarray(processed_image)
            processed_image = processed_image.resize((300, 300))  # Resize for display
            processed_image = ImageTk.PhotoImage(processed_image)
            
            img_label.config(image=processed_image)
            img_label.image = processed_image  # Keep a reference to avoid garbage collection

            chatbox.config(state=tk.NORMAL)
            chatbox.insert(tk.END, f"Chatbot: Image processed and ready for analysis.\n")
            chatbox.config(state=tk.DISABLED)

    # Setup GUI
    app = tk.Tk()
    app.title("Chatbot")

    chatbox = scrolledtext.ScrolledText(app, height=15, width=50, state=tk.DISABLED)
    chatbox.pack(padx=10, pady=10)

    entry = tk.Entry(app, width=50)
    entry.pack(padx=10, pady=5)

    send_button = tk.Button(app, text="Send", command=send)
    send_button.pack(pady=5)

    upload_button = tk.Button(app, text="Upload Image", command=upload_image)
    upload_button.pack(pady=5)

    img_label = tk.Label(app)
    img_label.pack(pady=10)

    app.mainloop()

if __name__ == "__main__":
    chatbot_gui()
  