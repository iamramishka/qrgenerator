import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import qrcode
import os

def generate_qrs():
    # Clear previous images and their references to prevent memory leaks
    for label in qr_labels:
        label.destroy()
    qr_labels.clear()
    images.clear()

    # Get the input text from the entry widget and split by commas
    input_text = entry.get()
    if not input_text.strip():
        messagebox.showinfo("Input error", "Please enter some text, separated by commas, to generate QR codes.")
        return

    words = [word.strip() for word in input_text.split(',')]
    
    # Generate a QR code for each word or phrase
    row = 2  # Start from the second row (index starts at 0)
    for word in words:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(word)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white').convert('RGB')
        
        # Store image for later use (e.g., saving to files)
        images.append((img, word))

        # Convert PIL image to a Tkinter-compatible image and display it
        img_tk = ImageTk.PhotoImage(img)
        label = tk.Label(root, image=img_tk)
        label.image = img_tk  # keep a reference to avoid garbage collection
        label.grid(row=row, column=0, columnspan=2, pady=5)
        qr_labels.append(label)
        row += 1

def save_qrs():
    if not images:
        messagebox.showinfo("Save error", "No QR codes to save. Generate them first.")
        return
    
    # Ensure the directory for saving QR codes exists
    save_path = 'saved_qr_codes'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    # Save each image as a PNG file in the specified directory
    for img, name in images:
        file_path = os.path.join(save_path, f'{name}.png')
        img.save(file_path)
    messagebox.showinfo("Success", f"Saved all QR codes to the '{save_path}' directory.")

# Main application window setup
root = tk.Tk()
root.title("QR Code Generator")

qr_labels = []  # List to store label widgets for QR codes
images = []  # List to store image objects

entry = tk.Entry(root, width=40)
entry.grid(row=0, column=0, padx=10, pady=10)

generate_button = tk.Button(root, text="Generate QR Codes", command=generate_qrs)
generate_button.grid(row=0, column=1, padx=10, pady=10)

save_button = tk.Button(root, text="Save QR Codes", command=save_qrs)
save_button.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()  # Start the event loop
