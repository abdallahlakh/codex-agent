import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
from agent_action import run_agent
from agent_tool import run_command
import re

def execute_command():
    execute_button.config(text="waiting...")  # Update button text to "waiting..."
    root.update_idletasks()  # Force update the GUI

    while True:
        user_input = input_text.get("1.0", tk.END).strip()
        system_user_input = user_input + "\n write only one & between each command not two && and write only the command"
        output_text.config(state=tk.NORMAL)  # Enable the text widget to insert text
        output_text.insert(tk.END, f"User Input: {system_user_input}\n", "user_input")
        
        # Get AI response
        response = run_agent(user_input)
        command = response['output']
        
        # Extract the command written inside the bash block from the AI response
        real_command = ""
        match = re.search(r'```bash\n(.*?)\n```', command, re.DOTALL)
        if match:
            real_command = match.group(1).strip()
        else:
            match = re.search(r'```\n(.*?)\n```', command, re.DOTALL)
            if match:
                real_command = match.group(1).strip()
            else:
                match = re.search(r'``\n(.*?)\n``', command, re.DOTALL)
                if match:
                    real_command = match.group(1).strip()
                else:
                    match = re.search(r'`\n(.*?)\n`', command, re.DOTALL)
                    if match:
                        real_command = match.group(1).strip()
    
        output_text.insert(tk.END, f"AI Response: {real_command}\n", "ai_response")
       
        # Execute the command
        final_output = run_command(real_command)
        output_text.insert(tk.END, f"Command Output: {final_output}\n", "command_output")
        
        # Check if the command output is empty
        if not final_output:
            break
        
        # Check if the command was successful
        if "is not recognized as an internal or external command,operable program or batch file" not in final_output and "Exception" not in final_output:
            status_label.config(text="Command executed successfully!", fg="#27ae60")
            break
        else:
            output_text.insert(tk.END, "Command failed. Please try again.\n", "error")
            status_label.config(text="Command failed. Please try again.", fg="#e74c3c")
        
        output_text.config(state=tk.DISABLED)  # Disable the text widget to make it read-only

    execute_button.config(text="Execute")  # Reset button text to "Execute"

def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = original_image.resize((new_width, new_height), Image.LANCZOS)
    background_image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image=background_image, anchor="nw")
    canvas.image = background_image  # Keep a reference to avoid garbage collection

def type_text(label, text, index=0):
    if index < len(text):
        label.config(text=text[:index + 1])
        label.after(50, type_text, label, text, index + 1)  # Adjust the delay as needed

def on_focus_in(event):
    if input_text.get("1.0", tk.END).strip() == placeholder:
        input_text.delete("1.0", tk.END)
        input_text.config(fg="#ecf0f1")

def on_focus_out(event):
    if not input_text.get("1.0", tk.END).strip():
        input_text.insert("1.0", placeholder)
        input_text.config(fg="grey")

# Create the main window
root = tk.Tk()
root.title("AI Command Executor")
root.geometry("700x600")

# Create a canvas to hold the background image and other widgets
canvas = tk.Canvas(root, width=700, height=600)
canvas.pack(fill="both", expand=True)

# Load the original background image
original_image = Image.open(r"C:\Users\laab2\Downloads\ai-agent\codex-agent\img\logo.png")
background_image = ImageTk.PhotoImage(original_image)
canvas.create_image(0, 0, image=background_image, anchor="nw")

# Bind the resize event to the canvas
canvas.bind("<Configure>", resize_image)

# Create a frame to hold the widgets
frame = tk.Frame(root, bg="#2c3e50")
frame.place(relwidth=1, relheight=1)

# Resize the logo image to make it smaller
logo_image = original_image.resize((100, 100), Image.LANCZOS)
logo = ImageTk.PhotoImage(logo_image)

# Create a label for the logo and place it at the top of the window
logo_label = tk.Label(frame, image=logo, bg="#2c3e50")
logo_label.place(relx=0.5, rely=0.0, anchor="n")

# Create a frame for the input label
input_frame = tk.Frame(frame, bg="#2c3e50")
input_frame.pack(pady=(120, 5), fill="x")

# Create a label for the input prompt with typing effect
input_label = tk.Label(input_frame, font=("Helvetica", 12, "bold"), bg="#2c3e50", fg="#ecf0f1")
input_label.pack(side="left", padx=(0, 10))
type_text(input_label, "Hey, i'm your command executer agent give me the order to execute it in your windows OS :)")

# Create a frame for the input text and button
input_text_frame = tk.Frame(frame, bg="#2c3e50")
input_text_frame.pack(pady=(5, 20), fill="x")

# Create a text box for user input
input_text = scrolledtext.ScrolledText(input_text_frame, wrap=tk.WORD, width=60, height=5, font=("Helvetica", 10), bg="#34495e", fg="grey", insertbackground="#ecf0f1", borderwidth=0, relief="flat")
input_text.pack(side="left", padx=(0, 10), expand=True, fill="x")

# Placeholder text
placeholder = "Enter the location folder here..."

# Insert placeholder text
input_text.insert("1.0", placeholder)

# Bind focus in and focus out events
input_text.bind("<FocusIn>", on_focus_in)
input_text.bind("<FocusOut>", on_focus_out)

# Load the execute button icon
execute_icon = Image.open(r"C:\Users\laab2\Downloads\ai-agent\codex-agent\img\icon.png")  # Replace with the path to your icon
execute_icon = execute_icon.resize((30, 30), Image.LANCZOS)
execute_icon = ImageTk.PhotoImage(execute_icon)

# Create a button to execute the command with the icon
execute_button = tk.Button(input_text_frame, text="Execute", image=execute_icon, compound="left", command=execute_command, bg="#27ae60", borderwidth=0, relief="flat", highlightthickness=0)
execute_button.pack(side="left", padx=(10, 0))

# Center the input text frame
input_text_frame.pack(anchor="center")

# Create a text box to display the output
output_label = tk.Label(frame, text="Output:", font=("Helvetica", 12, "bold"), bg="#2c3e50", fg="#ecf0f1")
output_label.pack(pady=(10, 5))
output_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=70, height=15, font=("Helvetica", 10), bg="#34495e", fg="#ecf0f1", insertbackground="#ecf0f1", borderwidth=0, relief="flat")
output_text.pack(pady=(5, 20))
output_text.config(state=tk.DISABLED)  # Make the output text box read-only initially

# Add tags for different text styles in the output text box
output_text.tag_config("user_input", foreground="red")
output_text.tag_config("ai_response", foreground="#8e44ad")
output_text.tag_config("command_output", foreground="#27ae60")
output_text.tag_config("error", foreground="#e74c3c", font=("Helvetica", 12, "bold"))

# Create a status label to display the status of the command execution
status_label = tk.Label(frame, text="", font=("Helvetica", 12, "bold"), bg="#2c3e50", fg="#ecf0f1")
status_label.pack(pady=(10, 10))

# Run the main loop
root.mainloop()