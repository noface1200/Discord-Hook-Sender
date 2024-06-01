import tkinter as tk
from tkinter import messagebox, colorchooser
from PIL import Image, ImageTk
import requests
import json
import os

def send_message():
    webhook_url = entry_webhook.get()
    message_content = entry_message.get()
    embed_title = entry_embed_title.get()
    embed_description = entry_embed_description.get()
    embed_image_url = entry_embed_image.get()
    embed_color = selected_color.get()

    if not webhook_url:
        messagebox.showerror("Error", "Webhook URL is required")
        return

    data = {}

    if message_content:
        data["content"] = message_content

    if embed_title and embed_description:
        embed = {
            "title": embed_title,
            "description": embed_description,
            "color": int(embed_color.replace("#", "0x"), 16) if embed_color else 5814783
        }
        if embed_image_url:
            embed["image"] = {"url": embed_image_url}
        data["embeds"] = [embed]

    if not data:
        messagebox.showerror("Error", "Either a message or embed details must be provided")
        return

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))

    if response.status_code != 204:
        messagebox.showerror("Error", f"Failed to send message. Status code: {response.status_code}")

def choose_color():
    color_code = colorchooser.askcolor(title="Choose color")[1]
    if color_code:
        selected_color.set(color_code)
        color_display.config(bg=color_code)

root = tk.Tk()
root.title("K9 Hook sender")
root.configure(bg='#2e2e2e')
root.geometry("500x500")

# Set window icon
icon_path = os.path.join("assets", "icon.png")
icon_image = ImageTk.PhotoImage(Image.open(icon_path))
root.iconphoto(False, icon_image)

top_bar = tk.Frame(root, bg="#3c3f41", height=40)
top_bar.pack(fill="x")
top_bar.pack_propagate(False)

top_label = tk.Label(top_bar, text="K9 Hook Sender", bg="#3c3f41", fg="white", font=("Helvetica", 16))
top_label.pack(side="left", padx=10)

def close_app():
    root.destroy()

close_button = tk.Button(top_bar, text="X", command=close_app, bg="#3c3f41", fg="white", bd=0, font=("Helvetica", 12))
close_button.pack(side="right", padx=10)

def configure_style(widget):
    widget.configure(bg="#2e2e2e", fg="white", insertbackground="white", bd=0, highlightthickness=1, highlightbackground="#444444")
    widget.pack(padx=10, pady=5, fill=tk.X)

content_frame = tk.Frame(root, bg="#2e2e2e")
content_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

label_webhook = tk.Label(content_frame, text="Webhook URL:", bg="#2e2e2e", fg="white")
label_webhook.pack(anchor="w")
entry_webhook = tk.Entry(content_frame, width=50)
configure_style(entry_webhook)

label_message = tk.Label(content_frame, text="Message Content:", bg="#2e2e2e", fg="white")
label_message.pack(anchor="w")
entry_message = tk.Entry(content_frame, width=50)
configure_style(entry_message)

label_embed_title = tk.Label(content_frame, text="Embed Title:", bg="#2e2e2e", fg="white")
label_embed_title.pack(anchor="w")
entry_embed_title = tk.Entry(content_frame, width=50)
configure_style(entry_embed_title)

label_embed_description = tk.Label(content_frame, text="Embed Description:", bg="#2e2e2e", fg="white")
label_embed_description.pack(anchor="w")
entry_embed_description = tk.Entry(content_frame, width=50)
configure_style(entry_embed_description)

label_embed_image = tk.Label(content_frame, text="Embed Image URL:", bg="#2e2e2e", fg="white")
label_embed_image.pack(anchor="w")
entry_embed_image = tk.Entry(content_frame, width=50)
configure_style(entry_embed_image)

label_embed_color = tk.Label(content_frame, text="Embed Color:", bg="#2e2e2e", fg="white")
label_embed_color.pack(anchor="w")
color_display = tk.Label(content_frame, text="Color Display", bg="#444444", fg="white", width=50)
color_display.pack(anchor="w", padx=10, pady=5, fill=tk.X)
color_button = tk.Button(content_frame, text="Choose Color", command=choose_color, bg="#444444", fg="white", bd=0)
color_button.pack(anchor="w", padx=10, pady=5)

selected_color = tk.StringVar()
selected_color.set("#000000")

send_button = tk.Button(root, text="Send", command=send_message, bg="#444444", fg="white", bd=0, highlightthickness=1, highlightbackground="#444444")
send_button.pack(pady=20)

root.mainloop()
