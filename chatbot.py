import tkinter as tk
from tkinter import scrolledtext
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# FAQ Q&A
faq_pairs = {
    "hello": "Hello! How can I help you today?",
    "what is your return policy": "You can return any item within 30 days of delivery.",
    "how do i get a refund": "Refunds are processed within 5-7 business days.",
    "i want to cancel my order": "To cancel your order, please provide the order ID.",
    "how do i contact support": "You can contact us at support@example.com or call 1800-123-456.",
    "how can i track my order": "Please provide your order ID to check the status.",
    "bye": "Thank you for chatting with us. Have a great day!"
}

questions = list(faq_pairs.keys())
answers = list(faq_pairs.values())

def get_bot_response(user_input):
    user_input = user_input.lower().strip()
    if user_input == "":
        return "Please enter something."

    try:
        questions_copy = questions + [user_input]
        # No custom tokenizer here to avoid errors
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(questions_copy)

        similarity = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
        index = similarity.argsort()[0][-1]
        score = similarity[0][index]

        print(f"[DEBUG] User Input: {user_input}")
        print(f"[DEBUG] Best match index: {index}")
        print(f"[DEBUG] Similarity score: {score}")

        if score > 0.3:
            return answers[index]
        elif "bye" in user_input:
            return faq_pairs["bye"]
        else:
            return "I'm sorry, I didn't understand that. Could you please rephrase?"
    except Exception as e:
        print(f"[ERROR] {e}")
        return "Sorry, something went wrong on my side."

def log_chat(text):
    with open("chat_history.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")

def send_message(event=None):
    user_msg = user_input.get()
    if user_msg.strip() == "":
        return

    chat_window.insert(tk.END, "You: " + user_msg + "\n")
    log_chat("You: " + user_msg)

    bot_response = get_bot_response(user_msg)
    chat_window.insert(tk.END, "Bot: " + bot_response + "\n\n")
    log_chat("Bot: " + bot_response + "\n")

    user_input.delete(0, tk.END)
    chat_window.see(tk.END)  # Scroll to the end

# GUI setup
root = tk.Tk()
root.title("Customer Service Chatbot")

chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Arial", 12))
chat_window.pack(padx=10, pady=10)
chat_window.insert(tk.END, "Bot: Hello! How can I help you today?\n\n")
log_chat("Bot: Hello! How can I help you today?\n")

user_input = tk.Entry(root, width=50, font=("Arial", 12))
user_input.pack(padx=10, pady=(0, 10))
user_input.bind("<Return>", send_message)

send_button = tk.Button(root, text="Send", command=send_message, font=("Arial", 12))
send_button.pack()

root.mainloop()
