from openai import OpenAI
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox

token = input("Paste your GitHub Models Token here to unlock the interface: ")

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=token,
)

chat_history = []
knowledge = "No extra manual loaded. Respond normally."

def reset_memory():
    global chat_history
    
    instructions = f"You are the Factory Engineering Assistant.\nRespond EXCLUSIVELY based on the manual below. If you do not know, say you do not know.\nTECHNICAL MANUAL:\n{knowledge}"
    
    chat_history = [{"role": "system", "content": instructions}]

reset_memory()

def load_file():
    global knowledge
    
    file_path = filedialog.askopenfilename(title="Select Factory Manual", filetypes=[("Text Files", "*.txt")])
    
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            knowledge = file.read()
            
        reset_memory()
        messagebox.showinfo("Success", "Manual loaded successfully! The AI now knows the factory rules.")

def clear_chat():
    chat_area.config(state=tk.NORMAL)
    chat_area.delete('1.0', tk.END) 
    chat_area.config(state=tk.DISABLED)
    reset_memory()
    messagebox.showinfo("System Reset", "The conversation has been cleared and the AI memory has been reset for the next operator.")

def exit_system():
    confirmation = messagebox.askyesno("Exit", "Are you sure you want to close the system?")
    if confirmation:
        window.destroy()

def send_message(event=None):
    question = input_field.get()
    
    if question.strip() == "":
        return

    input_field.delete(0, tk.END)

    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"OPERATOR: {question}\n\n")
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)

    window.update() 
    
    chat_history.append({"role": "user", "content": question})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_history
        )
        
        ai_response = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": ai_response})

        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, f"VIRTUAL ENGINEER:\n{ai_response}\n")
        chat_area.insert(tk.END, "-"*50 + "\n\n")
        chat_area.config(state=tk.DISABLED)
        chat_area.yview(tk.END)
        
    except Exception as error:
        messagebox.showerror("Communication Error", f"Failed to connect to the AI.\nError: {error}")

window = tk.Tk()
window.title("Industrial Totem - Local Interface")
window.geometry("650x700")

btn_load = tk.Button(window, text="📁 Load Manual (.txt)", command=load_file, bg="#4CAF50", fg="#FFFFFF", font=("Arial", 10, "bold"))
btn_load.pack(pady=10) 

chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 11), bg="#f4f4f4")
chat_area.pack(padx=15, pady=5, fill=tk.BOTH, expand=True) 

input_field = tk.Entry(window, font=("Arial", 12))
input_field.pack(padx=15, pady=10, fill=tk.X) 
input_field.bind("<Return>", send_message)

button_frame = tk.Frame(window)
button_frame.pack(pady=10)

btn_clear = tk.Button(button_frame, text="Clear Chat", command=clear_chat, bg="#FF9800", fg="white", font=("Arial", 10, "bold"))
btn_clear.pack(side=tk.LEFT, padx=10) 

btn_send = tk.Button(button_frame, text="Send Message", command=send_message, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
btn_send.pack(side=tk.LEFT, padx=10)

btn_exit = tk.Button(button_frame, text="Exit", command=exit_system, bg="#f44336", fg="white", font=("Arial", 10, "bold"))
btn_exit.pack(side=tk.LEFT, padx=10)

window.mainloop()
